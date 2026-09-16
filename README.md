# Manufacturing Quality Analysis

Quality and failure analysis on a manufacturing dataset, with a full Python pipeline behind it. I used the public AI4I 2020 predictive maintenance dataset and treated it like a real engagement: validation, KPIs, failure analysis, and docs.

## The data
- **Source:** AI4I 2020 Predictive Maintenance Dataset (UCI Machine Learning Repository)
- **License:** CC BY 4.0
- Everything here is reproducible from the code. No company data, no stakeholders, just the public dataset.

## What the pipeline does
- Validates the data and reports quality issues
- Computes KPIs (failure rates, failure mode counts)
- Breaks down failure modes by product type
- Checks process parameter thresholds against failures

## Repo layout
```
manufacturing-quality-analysis/
├── README.md
├── requirements.txt
├── .gitignore
├── LICENSE
├── src/
│   ├── __init__.py
│   ├── config.py
│   ├── io.py
│   ├── preprocess.py
│   ├── validation.py
│   ├── kpi.py
│   ├── viz.py
│   └── run_pipeline.py
├── notebooks/
│   └── 01_eda_defects.ipynb
├── docs/
│   ├── business_requirements.md
│   ├── technical_spec.md
│   ├── data_dictionary.md
│   └── assumptions.md
├── data/
│   ├── raw/
│   │   ├── README.md
│   │   └── ai4i2020.csv
│   └── processed/
│       └── README.md
└── reports/
    ├── summary.md (auto-generated)
    ├── validation_report.md (auto-generated)
    ├── figures/ (auto-generated PNG charts)
    └── bpmn/
        ├── README.md
        ├── current_state.png
        └── future_state.png
```

## Run it
```bash
git clone https://github.com/HamedXa/manufacturing-quality-analysis.git
cd manufacturing-quality-analysis
pip install -r requirements.txt
python -m src.run_pipeline
```

After it runs, check `reports/summary.md` for the KPI summary and `reports/validation_report.md` for data quality results. Charts land in `reports/figures/`.

## Key findings
Populated in `reports/summary.md` after you run the pipeline.

## Limitations
1. **Public dataset** - Results are based on simulated/synthetic data from UCI ML Repository
2. **No deployment context** - Analysis is exploratory; no production system integration
3. **No validated savings** - Cost estimates, if provided, are scenario-based assumptions only
4. **No stakeholder input** - Thresholds and KPI definitions are analyst-defined, not business-validated
5. **Multi-label targets** - Some records have multiple failure modes; analysis treats each mode independently

## Docs
- [Business Requirements](docs/business_requirements.md)
- [Technical Specification](docs/technical_spec.md)
- [Data Dictionary](docs/data_dictionary.md)
- [Assumptions](docs/assumptions.md)

There's also a BPMN section: `reports/bpmn/README.md` has current-state and future-state diagrams of the quality/maintenance workflow.

## Author
Hamed Sharafeldin — Data Science & ML diploma, RRC Polytech
[LinkedIn](https://www.linkedin.com/in/hamed-sharafeldin-821273203/) | [GitHub](https://github.com/HamedXa)
