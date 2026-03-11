import pickle
import os
import sys
from pathlib import Path

# ── MCP import ────────────────────────────────────────────────────────────────
try:
    from mcp.server import Server
    from mcp.server.stdio import stdio_server
    import mcp.types as types
except ImportError:
    print("ERROR: mcp package not installed. Run: pip install mcp", file=sys.stderr)
    sys.exit(1)

# ── Load model ────────────────────────────────────────────────────────────────
MODEL_PATH = Path(__file__).parent.parent.parent / "models" / "random_forest_model.pkl"

if not MODEL_PATH.exists():
    print(f"ERROR: Model not found at {MODEL_PATH}. Run train_random_forest.py first.",
          file=sys.stderr)
    sys.exit(1)

with open(MODEL_PATH, "rb") as f:
    bundle = pickle.load(f)

model        = bundle["model"]
encoders     = bundle["encoders"]
feature_names = bundle["feature_names"]

# Pre-extract encoder maps for validation
premise_classes  = list(encoders["Premise Category"].classes_)
timebucket_classes = list(encoders["TimeBucket"].classes_)
severity_classes = list(encoders["Severity"].classes_)
crime_classes    = list(encoders["Crime Category"].classes_)

# ── MCP Server ────────────────────────────────────────────────────────────────
server = Server("safecity-crime-predictor")


@server.list_tools()
async def list_tools():
    return [
        types.Tool(
            name="predict_crime_category",
            description=(
                "Predict the most likely crime category for a given incident context "
                "using a trained Random Forest model (SafeCity Phase 2)."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "area": {
                        "type": "integer",
                        "description": "LAPD area code (1–21)",
                        "minimum": 1, "maximum": 21
                    },
                    "hour": {
                        "type": "integer",
                        "description": "Hour of day (0–23)",
                        "minimum": 0, "maximum": 23
                    },
                    "month": {
                        "type": "integer",
                        "description": "Month (1–12)",
                        "minimum": 1, "maximum": 12
                    },
                    "is_weekend": {
                        "type": "boolean",
                        "description": "True if the incident occurred on a weekend"
                    },
                    "has_weapon": {
                        "type": "boolean",
                        "description": "True if a weapon was involved"
                    },
                    "premise_category": {
                        "type": "string",
                        "description": f"One of: {premise_classes}",
                        "enum": premise_classes
                    },
                    "time_bucket": {
                        "type": "string",
                        "description": f"One of: {timebucket_classes}",
                        "enum": timebucket_classes
                    },
                    "severity": {
                        "type": "string",
                        "description": f"One of: {severity_classes}",
                        "enum": severity_classes
                    },
                    "part_1_2": {
                        "type": "integer",
                        "description": "Part 1 or Part 2 crime (1 or 2)",
                        "enum": [1, 2]
                    },
                    "reporting_delay_days": {
                        "type": "integer",
                        "description": "Number of days between crime occurrence and report",
                        "minimum": 0
                    },
                },
                "required": [
                    "area", "hour", "month", "is_weekend", "has_weapon",
                    "premise_category", "time_bucket", "severity",
                    "part_1_2", "reporting_delay_days"
                ]
            }
        ),
        types.Tool(
            name="list_crime_categories",
            description="List all crime categories the model can predict.",
            inputSchema={"type": "object", "properties": {}}
        ),
    ]


@server.call_tool()
async def call_tool(name: str, arguments: dict):
    if name == "list_crime_categories":
        return [types.TextContent(
            type="text",
            text="Predictable crime categories:\n" + "\n".join(f"  • {c}" for c in crime_classes)
        )]

    if name == "predict_crime_category":
        # ── input validation ──────────────────────────────────────────────────
        try:
            area      = int(arguments["area"])
            hour      = int(arguments["hour"])
            month     = int(arguments["month"])
            is_weekend = int(bool(arguments["is_weekend"]))
            has_weapon = int(bool(arguments["has_weapon"]))
            premise   = arguments["premise_category"]
            timebucket = arguments["time_bucket"]
            severity   = arguments["severity"]
            part       = int(arguments["part_1_2"])
            delay      = int(arguments["reporting_delay_days"])
        except (KeyError, ValueError) as e:
            return [types.TextContent(type="text", text=f"Input error: {e}")]

        # Validate categorical values
        for val, valid_list, label in [
            (premise, premise_classes, "premise_category"),
            (timebucket, timebucket_classes, "time_bucket"),
            (severity, severity_classes, "severity"),
        ]:
            if val not in valid_list:
                return [types.TextContent(
                    type="text",
                    text=f"Invalid {label}: '{val}'. Must be one of {valid_list}"
                )]

        # ── encode categoricals ───────────────────────────────────────────────
        premise_enc  = encoders["Premise Category"].transform([premise])[0]
        time_enc     = encoders["TimeBucket"].transform([timebucket])[0]
        severity_enc = encoders["Severity"].transform([severity])[0]

        features = [[
            area, hour, month, is_weekend, has_weapon,
            premise_enc, time_enc, severity_enc, part, delay
        ]]

        # ── predict ───────────────────────────────────────────────────────────
        pred_idx   = model.predict(features)[0]
        pred_label = encoders["Crime Category"].inverse_transform([pred_idx])[0]
        probas     = model.predict_proba(features)[0]
        top3_idx   = probas.argsort()[-3:][::-1]
        top3 = [
            f"{encoders['Crime Category'].inverse_transform([i])[0]}: {probas[i]*100:.1f}%"
            for i in top3_idx
        ]

        result = (
            f"**Predicted Crime Category:** {pred_label}\n\n"
            f"**Top 3 Predictions:**\n" + "\n".join(f"  {i+1}. {t}" for i, t in enumerate(top3))
        )
        return [types.TextContent(type="text", text=result)]

    return [types.TextContent(type="text", text=f"Unknown tool: {name}")]


# ── Entry point ───────────────────────────────────────────────────────────────
if __name__ == "__main__":
    import asyncio

    async def main():
        async with stdio_server() as (read_stream, write_stream):
            await server.run(read_stream, write_stream,
                             server.create_initialization_options())

    asyncio.run(main())
