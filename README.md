# SafeCity Analytics: LA Crime Data Analysis

## Course + Assignment Header
- **Subject Code:** EAS 587  
- **Course:** Data-Intensive Computing (Spring 2026)  
- **Assignment No.:** Project Phase 1 & Phase 2  
- **Project Title:** SafeCity Analytics: LA Crime Data Analysis  
- **Instructor:** Dr. Justice Del Vacio  
- **Team Members:**  
  - Harsh Mahesh Tikone  
  - Dev Desai  
  - Shwetangi  

---

## Report & Deliverables

| Deliverable | Link / File |
|---|---|
| **Phase 1 Report (Google Doc)** | [View Report](https://docs.google.com/document/d/1oYahBmjBAiVArPI48sZtJC_sIqrrbvFXyusX9ByZsmY/edit?usp=sharing) |
| **Phase 1 Workshop Slides** | `LA_Crime_Data_Analysis.pptx` |
| **Phase 2 Report (Google Doc)** | *(Add your Phase 2 Google Doc link here)* |
| **Phase 2 Workshop Slides** | *(Add your Phase 2 slides link here)* |

---

## Repository Structure

```text
DIC_Assignment_safecity-analytics/
├── README.md
├── requirements.txt
├── data/
│   ├── raw/
│   │   └── crime_data_2024_to_present.csv
│   └── processed/
│       └── crime_data_cleaned.csv            ← Phase 1 output / Phase 2 input
├── src/
│   ├── data_cleaning.py                      ← Phase 1: data cleaning pipeline
│   ├── eda.py                                ← Phase 1: exploratory data analysis
│   └── models/                               ← Phase 2: ML algorithms
│       ├── preprocess.py                     ← shared feature engineering
│       ├── train_knn.py                      ← Algorithm 1: k-NN
│       ├── train_decision_tree.py            ← Algorithm 2: Decision Tree
│       ├── train_kmeans.py                   ← Algorithm 3: k-Means
│       ├── train_naive_bayes.py              ← Algorithm 4: Naive Bayes
│       ├── train_random_forest.py            ← Algorithm 5: Random Forest (outside class)
│       ├── train_logistic_regression.py      ← Algorithm 6: Logistic Regression (outside class)
│       └── compare_algorithms.py             ← head-to-head algorithm comparison
├── src/mcp/                                  ← Phase 2: MCP deployment
│   ├── server.py
│   └── README.md
├── models/                                   ← Phase 2: serialized trained models
│   ├── knn_model.pkl
│   ├── decision_tree_model.pkl
│   ├── kmeans_model.pkl
│   ├── naive_bayes_model.pkl
│   ├── random_forest_model.pkl
│   └── logistic_regression_model.pkl
├── outputs/                                  ← Phase 2: plots and metrics CSVs
│   ├── knn/
│   ├── decision_tree/
│   ├── kmeans/
│   ├── naive_bayes/
│   ├── random_forest/
│   ├── logistic_regression/
│   └── comparison/
└── figures/                                  ← Phase 1: EDA visualizations
    ├── temporal_patterns.png
    ├── geographic_distribution.png
    ├── victim_demographics.png
    ├── crime_type_analysis.png
    ├── reporting_patterns.png
    ├── cross_tabulation.png
    ├── correlation_matrix.png
    ├── outlier_detection.png
    └── weapon_analysis.png
```

---

---

# PHASE 1: Data Collection, Cleaning & EDA

---

## Phase 1 Overview

Phase 1 implements the data ingestion, cleaning, and exploratory analysis steps of the data science pipeline using Python. The goal was to prepare a clean, analysis-ready dataset and surface key patterns in LA crime data to inform modeling decisions in Phase 2.

Primary dataset:
- **Source:** [Crime Data from 2020 to Present (data.gov)](https://catalog.data.gov/dataset/crime-data-from-2020-to-present)
- **File in repo:** `data/raw/crime_data_2024_to_present.csv`
- **Scale:** ~62K rows (meets 50,000+ row requirement)

---

## Phase 1 Setup Instructions

### Prerequisites
- Python 3.8+
- pip package manager

### Installation
```bash
git clone <repository-url>
cd DIC_Assignment_safecity-analytics
pip install -r requirements.txt
```

### Running Phase 1

**1. Data Cleaning:**
```bash
cd src
python data_cleaning.py
```

**2. Exploratory Data Analysis:**
```bash
python eda.py
```

---

## Data Cleaning Operations (10)

1. **Date Column Conversion:** Converted `Date Rptd` and `DATE OCC` to datetime format; extracted Year, Month, Day, DayOfWeek, Hour
2. **Time Validation:** Fixed invalid time values (>2400)
3. **Missing Victim Info:** Replaced zero ages with NaN; filled missing sex/descent with 'Unknown'
4. **Categorical Standardization:** Standardized sex codes (M→Male, F→Female, X→Unknown); mapped descent codes to full descriptions
5. **Column Removal:** Removed `Crm Cd 2`, `Crm Cd 3`, `Crm Cd 4` (98–100% missing)
6. **Crime Categorization:** Grouped 140+ crime types into 12 categories (Vehicle Crime, Theft, Burglary, etc.)
7. **Premise Categorization:** Grouped premise types into 9 categories (Public Street, Parking Area, Commercial, etc.)
8. **Age Grouping:** Created 7 age groups (0–17, 18–24, 25–34, 35–44, 45–54, 55–64, 65+)
9. **Coordinate Validation:** Flagged coordinates outside LA bounds (none found)
10. **Reporting Delay:** Calculated days between crime occurrence and report

---

## EDA Operations (10) — Following John Tukey's Principles

1. **Summary Statistics:** Generated descriptive statistics for numeric variables
2. **Temporal Patterns:** Analyzed crime by hour, day of week, and month
3. **Geographic Distribution:** Mapped crimes by LAPD area and coordinates
4. **Victim Demographics:** Analyzed age, sex, and descent distributions
5. **Crime Type Analysis:** Examined crime categories and premise types
6. **Reporting Patterns:** Analyzed reporting delays and case statuses
7. **Cross-tabulation:** Crime categories by victim sex and area
8. **Correlation Analysis:** Correlation matrix of numeric variables
9. **Outlier Detection:** Box plots for age, reporting delay, and hour
10. **Weapon Analysis:** Weapon usage patterns and types

---

## Phase 1 Key Findings

### Temporal Patterns
- **Peak crime hour:** 6:00 PM (3,911 crimes)
- **Highest crime day:** Friday (9,550 crimes)
- **Highest crime month:** May (9,388 crimes)

### Geographic Distribution
- **Highest crime area:** Central LA (6,024 crimes)
- **Lowest crime area:** Foothill (1,774 crimes)

### Crime Types
- **Top category:** Vehicle Crime (28,700 crimes, 46.2%)
- **Top premise:** Public Street (23,518 crimes, 37.9%)

### Victim Demographics
- **Median age:** 35 years
- **Sex distribution:** 37.6% Male, 29.3% Female, 33.1% Unknown
- **Top descent:** Hispanic (10,399), Black (4,089), Other (3,666)

### Reporting
- **Median reporting delay:** 1 day
- **Case status:** 94.5% under investigation

---

## Phase 1 Surprise Findings

1. **High proportion of unknown victim data:** 48.5% of records have unknown victim demographics (age=0, sex=X), suggesting many crimes are reported without victim information (e.g., property crimes)
2. **Low weapon usage:** Only 5.9% of crimes involve weapons, with "strong-arm" (physical force) being the most common
3. **Quick reporting:** 75% of crimes are reported within 3 days, indicating relatively prompt reporting

---

## Phase 1 Dead Ends

1. **Attempted crime analysis:** Initially tried to analyze attempted vs. completed crimes using crime codes, but the distinction was inconsistent across crime types and difficult to categorize reliably.
2. **Seasonal trend analysis:** Attempted to analyze seasonal patterns, but the dataset only covers ~1 year (2024), making seasonal comparisons impossible.
3. **Victim-offender relationship analysis:** The dataset doesn't include offender information or relationship data, preventing analysis of crime dynamics.

---

## Phase 1 Design Decisions

1. **Age handling:** Replaced age=0 with NaN rather than imputing, as 0 likely represents "unknown" rather than actual age
2. **Crime categorization:** Created broad categories to simplify analysis of 140+ crime types while maintaining interpretability
3. **Coordinate outliers:** Flagged rather than removed outliers to preserve data integrity
4. **Visualization approach:** Used multiple chart types (bar, line, pie, scatter) to reveal different aspects of the data

---

---

# PHASE 2: Machine Learning & Statistical Analysis

---

## Phase 2 Overview

Phase 2 applies 6 ML and statistical algorithms to the cleaned dataset from Phase 1, produces visualizations and performance metrics for each, deploys one model as an MCP server, and compares algorithms head-to-head. All algorithm choices are tied directly to the use cases defined in Phase 1.

- **Input:** `data/processed/crime_data_cleaned.csv` (Phase 1 output)
- **Scale:** ~62K rows, 46 features

---

## Phase 2 Setup Instructions

Dependencies are the same as Phase 1, plus scikit-learn and mcp:

```bash
pip install -r requirements.txt
```

### Running Phase 2

Run all scripts from the project root in this order:

```bash
python src/models/train_knn.py
python src/models/train_decision_tree.py
python src/models/train_kmeans.py
python src/models/train_naive_bayes.py
python src/models/train_random_forest.py
python src/models/train_logistic_regression.py
python src/models/compare_algorithms.py
```

All plots are saved to `outputs/<algorithm>/` and all serialized models to `models/`.

### Running the MCP Server

```bash
# Step 1: Train Random Forest first (if not already done)
python src/models/train_random_forest.py

# Step 2: Start the MCP server
python src/mcp/server.py
```

See `src/mcp/README.md` for Claude Desktop integration instructions.

---

## ML Algorithms (6)

### In-Class Algorithms

1. **k-Nearest Neighbours (kNN)** — Predicts crime **severity** (High/Medium/Low) from time, location, and context features. k tuned via 5-fold cross-validation (k=3 to 15). Features scaled with StandardScaler (distance-based model requires scaling).

2. **Decision Tree** — Predicts **crime category** (13 classes) and produces human-readable decision rules. Hyperparameters tuned with GridSearchCV across `max_depth` and `min_samples_split`. Outputs tree structure visualization and feature importances.

3. **k-Means Clustering** — Unsupervised discovery of geographic **crime hotspots** across Los Angeles. Optimal k selected by combining elbow method (inertia) and silhouette score. Outputs a lat/lon cluster map with crime category breakdown per cluster.

4. **Naive Bayes** — Fast probabilistic prediction of **crime category** from categorical features. Compares GaussianNB vs. ComplementNB via cross-validation; ComplementNB selected for better handling of class imbalance across the 13 categories.

### Outside-Class Algorithms

5. **Random Forest** *(Breiman, 2001)* — Ensemble of Decision Trees predicting **crime category**. Reduces overfitting vs. a single DT; handles class imbalance via `class_weight='balanced'`. Tuned with RandomizedSearchCV. **Also deployed as the MCP server model.**

6. **Logistic Regression** *(Hosmer & Lemeshow, 2000)* — Binary classification predicting **weapon involvement** (True/False). Outputs calibrated probabilities for risk scoring. Regularisation strength C tuned via cross-validation. Evaluated with ROC-AUC and Precision-Recall curves.

---

## Algorithms Summary Table

| # | Algorithm | Type | Target Variable | Source |
|---|-----------|------|-----------------|--------|
| 1 | k-Nearest Neighbours | Classification | Severity (High/Med/Low) | In-class |
| 2 | Decision Tree | Classification | Crime Category (13 classes) | In-class |
| 3 | k-Means | Clustering | Geographic Hotspots | In-class |
| 4 | Naive Bayes | Classification | Crime Category (13 classes) | In-class |
| 5 | Random Forest | Classification | Crime Category (13 classes) | Outside class |
| 6 | Logistic Regression | Classification | Weapon Involvement (binary) | Outside class |

---

## Features Used

All supervised models share a common feature set built in `preprocess.py`:

| Feature | Type | Description |
|---------|------|-------------|
| `AREA` | Numeric | LAPD area code (1–21) |
| `Hour` | Numeric | Hour of day the crime occurred |
| `Month` | Numeric | Month of occurrence |
| `IsWeekend` | Binary | 1 if Saturday or Sunday |
| `Has Weapon` | Binary | 1 if a weapon was used |
| `Premise Category` | Encoded | Commercial / Residential / Public Street / etc. |
| `TimeBucket` | Encoded | Morning / Afternoon / Evening / Night |
| `Severity` | Encoded | High / Medium / Low (used when predicting category) |
| `Part 1-2` | Numeric | LAPD crime seriousness classification |
| `Reporting Delay (Days)` | Numeric | Days between crime and report |

---

## MCP Deployment

The trained **Random Forest** model is deployed as an MCP (Model Context Protocol) server, making it callable from Claude Desktop or any MCP-compatible AI assistant.

- **Exposed tool:** `predict_crime_category`
- **Input:** Area, hour, month, weekend flag, weapon flag, premise type, time bucket, severity, part classification, reporting delay
- **Output:** Predicted crime category + top-3 probability breakdown

Full setup instructions: [`src/mcp/README.md`](src/mcp/README.md)

---

## Phase 2 Key Results

*(Fill in after running the scripts)*

### Classification Performance

| Algorithm | Target | Test Accuracy | Weighted F1 |
|-----------|--------|--------------|-------------|
| kNN (best k) | Severity | *(run to populate)* | *(run to populate)* |
| Decision Tree | Crime Category | *(run to populate)* | *(run to populate)* |
| Naive Bayes | Crime Category | *(run to populate)* | *(run to populate)* |
| Random Forest | Crime Category | *(run to populate)* | *(run to populate)* |
| Logistic Regression | Weapon Involved | *(run to populate)* | *(run to populate)* |

### Clustering Performance

| Algorithm | Best k | Silhouette Score |
|-----------|--------|-----------------|
| k-Means | *(run to populate)* | *(run to populate)* |

---

## Phase 2 Dead Ends

1. **SVM on full dataset** — Attempted Support Vector Machine for crime category classification but training time exceeded 30 minutes on the full 62K-row dataset even with `LinearSVC`. Downsampling was considered but would sacrifice representativeness of rare crime types. Abandoned in favour of Random Forest which trains faster and achieves higher accuracy at scale.

2. **DBSCAN for geographic clustering** — Attempted density-based spatial clustering as an alternative to k-Means. DBSCAN labelled over 60% of points as noise (label = -1) due to the relatively uniform density of crime across LA. The resulting clusters were not geographically meaningful. Reverted to k-Means with silhouette-guided k selection.

---

## Phase 2 Design Decisions

1. **Shared preprocessing module** (`preprocess.py`): All models draw from the same feature encoding pipeline to ensure consistent label encoding and avoid data leakage between scripts.
2. **Random Forest for MCP deployment:** Chosen over Decision Tree because it generalises better and handles class imbalance, while still being fast enough for real-time inference.
3. **Logistic Regression on weapon involvement:** Applied to a binary target (`Has Weapon`) rather than the same crime category as the tree-based models, to add variety and produce an actionable risk score.
4. **ComplementNB over GaussianNB:** ComplementNB is designed for imbalanced multi-class problems, matching the skewed crime category distribution (Vehicle Crime = 35%, Homicide = 0.02%).
5. **Silhouette + elbow for k-Means:** Using both metrics together avoids selecting a k that minimises inertia but produces poor cluster separation.

---

## Reproducibility

- All random seeds are set to `42` across all Phase 2 scripts
- `preprocess.py` provides a single shared feature pipeline used by all models
- Run scripts in the order listed under **Running Phase 2** above
- Verified on a fresh environment: confirmed by *(team member name)* on *(date)*

---

## Dependencies

See `requirements.txt` for full list:
- pandas
- numpy
- matplotlib
- seaborn
- scikit-learn
- mcp

---

## References

1. Tukey, J. W. (1977). *Exploratory Data Analysis*. Addison-Wesley.
2. Los Angeles Police Department. Crime Data from 2020 to Present. https://data.lacity.org/
3. Breiman, L. (2001). Random Forests. *Machine Learning*, 45(1), 5–32. https://doi.org/10.1023/A:1010933404324
4. Hosmer, D.W. & Lemeshow, S. (2000). *Applied Logistic Regression* (2nd ed.). Wiley. https://doi.org/10.1002/0471722146
5. Pedregosa, F. et al. (2011). Scikit-learn: Machine Learning in Python. *JMLR*, 12, 2825–2830. https://scikit-learn.org
6. Model Context Protocol Documentation. https://modelcontextprotocol.io/
7. VanderPlas, J. (2016). *Python Data Science Handbook*. O'Reilly. https://jakevdp.github.io/PythonDataScienceHandbook/

---

## License

This project is for educational purposes (EAS 587).
