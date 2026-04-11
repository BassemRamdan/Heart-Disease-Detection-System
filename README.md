# Heart Disease Detection Project

This project implements a complete heart disease detection workflow using:

- A rule-based expert system built using the **Experta** Rule Engine
- A machine-learning model (Decision Tree Classifier)
- Data preprocessing and visualization pipelines (Jupyter format)
- A modern Streamlit UI for interactive predictions

## Project Deliverables

- Cleaned and preprocessed dataset: `data/cleaned_data.csv`
- Data analysis notebook: `notebooks/data_analysis.ipynb`
- Model training notebook: `notebooks/model_training.ipynb`
- Rule-based expert system utilizing 12 custom clauses: `rule_based_system/rules.py`
- Tuned ML model: `ml_model/decision_tree_model.pkl`
- Finalized Official Project HTML Report: `reports/project_report.html`

## Folder Structure

```text
Heart_Disease_Detection/
├── data/                    # Contains raw dataset, cleaned datasets, and scalers
├── notebooks/               # Jupyter Notebooks for visual data exploration & training breakdown
│   ├── data_analysis.ipynb
│   └── model_training.ipynb
├── rule_based_system/       # Medical logic rule-engine (Experta)
│   ├── rules.py             # Defined medical rules
│   └── expert_system.py     # Evaluation on entire test-set
├── ml_model/                # Statistical ML operations
│   ├── train_model.py       # Trains Decision Tree, saves scalers/artifacts
│   └── predict.py           # Used by the UI to evaluate new patient data
├── utils/                   # Helper functions
│   └── data_processing.py   # Dataset loading, cleaning, and normalization functions
├── reports/                 # JSON evaluation metrics & generated project reports
│   ├── ml_metrics.json
│   ├── expert_metrics.json
│   └── project_report.html
├── ui/                      # Interactive user interface
│   └── app.py
├── requirements.txt         # Dependencies list
└── README.md                # Project documentation
```

## Setup

```bash
python -m venv .venv
# Windows
.\.venv\Scripts\activate
# Linux/macOS
# source .venv/bin/activate

pip install -r requirements.txt
```

## How To Run It Correctly

There are no disconnected visualization or temporary scripts. Use the following robust core modules to regenerate files or test the system:

1. **Automatically preprocess dataset and train the ML Decision Tree:**
   *(This step normalizes the raw data, creates `cleaned_data.csv`, and trains the tree, saving it for the UI)*
```bash
python ml_model/train_model.py
```

2. **Evaluate the Preventative Experta Rule-Based System:**
   *(Runs the Experta engine over the test cases and writes performance inside `expert_metrics.json`)*
```bash
python -m rule_based_system.expert_system
```

3. **Interact with the Visual Interface (Streamlit Dashboard):**
   *(Spin up the UI to test patients dynamically)*
```bash
streamlit run ui/app.py
```

4. **Test an individual patient programmatically (Developer Mode):**
```bash
python ml_model/predict.py
```

5. **Interact with Jupyter Dashboards:**
If you want to view the plots locally, launch `jupyter notebook` in your browser and check out `notebooks/data_analysis.ipynb` and `notebooks/model_training.ipynb`.

## Notes
- The Decision Tree predicts existing blockages based on data statistics representing the current situation.
- The `experta` engine is strictly engineered to flag *risks* preventatively using established human logic strings.
- Please refer to `reports/project_report.html` (open it in your web browser) for a full comparative overview of both performance profiles.
