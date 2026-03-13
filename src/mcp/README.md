# SafeCity MCP Server (Claude Code)

This folder contains the MCP server for crime-category prediction:

- Server entrypoint: `src/mcp/server.py`
- Tool name: `predict_crime_category`

## Quick Setup (Claude Code)

From the project root:

```bash
claude mcp add -s project safecity-crime-predictor -- python3 src/mcp/server.py
claude mcp get safecity-crime-predictor
```

If the second command shows `Status: Connected`, the server is ready.
