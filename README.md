# Manufacturing Quality Analysis

Quality and failure analysis on a manufacturing dataset, with a full Python pipeline behind it. I used the public AI4I 2020 predictive maintenance dataset and treated it like a real engagement: validation, KPIs, and failure analysis.

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
├── manufacturing_quality_analysis .ipynb   (exploration notebook)
├── src/
│   ├── __init__.py
│   ├── config.py
│   ├── io.py
│   ├── preprocess.py
│   ├── validation.py
│   ├── kpi.py
│   ├── viz.py
│   └── run_pipeline.py
├── data/
│   ├── raw/
│   │   └── README.md   (download ai4i2020.csv here, see below)
│   └── processed/
└── reports/
    ├── summary.md (auto-generated)
    ├── validation_report.md (auto-generated)
    └── figures/ (auto-generated PNG charts)
```

## Run it
The dataset isn't committed. Download `ai4i2020.csv` from the [UCI repository](https://archive.ics.uci.edu/dataset/601/ai4i+2020+predictive+maintenance+dataset) and put it in `data/raw/`. Then:
```bash
git clone https://github.com/HamedXa/manufacturing-quality-analysis.git
cd manufacturing-quality-analysis
pip install -r requirements.txt
python -m src.run_pipeline
```

After it runs, check `reports/summary.md` for the KPI summary and `reports/validation_report.md` for data quality results. Charts land in `reports/figures/`.

## Key findings
From [`reports/summary.md`](reports/summary.md):
- **3.39% overall failure rate** (339 of 10,000 records).
- **Product tier matters.** Low-quality (L) parts fail at 3.92%, nearly 2x High-quality (H) at 2.09%.
- **Heat dissipation is the top failure mode** (115 failures, 33.9%), followed by overstrain (28.9%) and power (28.0%).
- **Extremes drive failures.** Top-decile torque (≥52.6 Nm) fails at 18.24% vs 1.45% in the normal range; bottom-decile rotational speed (≤1364 rpm) at 16.54%; top-decile tool wear (≥195 min) at 12.63%.

## Limitations
1. **Public dataset** - Results are based on simulated/synthetic data from UCI ML Repository
2. **No deployment context** - Analysis is exploratory; no production system integration
3. **No validated savings** - Cost estimates, if provided, are scenario-based assumptions only
4. **No stakeholder input** - Thresholds and KPI definitions are analyst-defined, not business-validated
5. **Multi-label targets** - Some records have multiple failure modes; analysis treats each mode independently

## Author
Hamed Sharafeldin — Data Science & ML diploma, RRC Polytech
[LinkedIn](https://www.linkedin.com/in/hamed-sharafeldin-821273203/) | [GitHub](https://github.com/HamedXa)
