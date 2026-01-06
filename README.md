# Manufacturing Quality & Process Analysis

A portfolio project demonstrating manufacturing quality analysis and predictive maintenance concepts using the AI4I 2020 Predictive Maintenance Dataset.

## Dataset

**Source:** [UCI Machine Learning Repository - AI4I 2020 Predictive Maintenance Dataset](https://archive.ics.uci.edu/ml/datasets/AI4I+2020+Predictive+Maintenance+Dataset)

**License:** CC BY 4.0 (Creative Commons Attribution 4.0 International)

**Last Updated:** January 2026

**Note:** This project uses a public dataset for demonstration purposes. No proprietary data or stakeholder collaboration is implied. All findings are reproducible from the code in this repository.

## Project Overview

This project analyzes machine failure patterns in a simulated manufacturing environment. It demonstrates:

- Data validation and quality assurance frameworks
- KPI computation and reporting
- Failure mode analysis across product quality types
- Process parameter threshold analysis
- Documentation practices (BRD, technical spec, data dictionary)

## Repository Structure

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

## Quick Start

### Prerequisites

- Python 3.9+
- pip

### Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/manufacturing-quality-analysis.git
cd manufacturing-quality-analysis

# Create virtual environment (optional but recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Running the Pipeline

```bash
python -m src.run_pipeline
```

### Expected Outputs

After running the pipeline, the following files are generated:

- `reports/summary.md` - KPI summary with failure rates and mode counts
- `reports/validation_report.md` - Data quality validation results
- `reports/figures/failure_rate_by_type.png` - Bar chart of failure rates by product type
- `reports/figures/failure_mode_counts.png` - Bar chart of failure mode distribution
- `reports/figures/temp_delta_vs_failure.png` - Box plot of temperature delta by failure status

## Key Findings

*(Auto-populated after running pipeline - see `reports/summary.md`)*

## Limitations

1. **Public dataset** - Results are based on simulated/synthetic data from UCI ML Repository
2. **No deployment context** - Analysis is exploratory; no production system integration
3. **No validated savings** - Cost estimates, if provided, are scenario-based assumptions only
4. **No stakeholder input** - Thresholds and KPI definitions are analyst-defined, not business-validated
5. **Multi-label targets** - Some records have multiple failure modes; analysis treats each mode independently

## Documentation

- [Business Requirements Document](docs/business_requirements.md)
- [Technical Specification](docs/technical_spec.md)
- [Data Dictionary](docs/data_dictionary.md)
- [Assumptions](docs/assumptions.md)

## Process Workflow (BPMN)

See `reports/bpmn/README.md` for current-state and future-state process diagrams illustrating the quality/maintenance workflow concept.

## Author

**Hamed Sharafeldin**  
Data Science & Machine Learning Graduate  
[LinkedIn](https://linkedin.com/in/hamed-sharafeldin-821273203) | [GitHub](https://github.com/HamedXa)
