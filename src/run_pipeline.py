"""
Main pipeline runner for manufacturing quality analysis.

Usage:
    python -m src.run_pipeline
"""

import sys
from pathlib import Path

# Add project root to path for imports
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from src.config import RAW_CSV_PATH, REPORTS_DIR, FIGURES_DIR
from src.io import load_csv, save_markdown
from src.preprocess import preprocess_data
from src.validation import DataValidator
from src.kpi import generate_kpi_summary
from src.viz import generate_all_figures


def main():
    """Execute the full analysis pipeline."""
    print("=" * 60)
    print("Manufacturing Quality & Process Analysis Pipeline")
    print("=" * 60)
    print()

    # -------------------------------------------------------------------------
    # Step 1: Load data
    # -------------------------------------------------------------------------
    print("[1/5] Loading data...")
    try:
        df_raw = load_csv(RAW_CSV_PATH)
        print(f"      Loaded {len(df_raw):,} records from {RAW_CSV_PATH.name}")
    except FileNotFoundError as e:
        print(f"      ERROR: {e}")
        print("      Please place ai4i2020.csv in data/raw/ directory.")
        print("      Download from: https://archive.ics.uci.edu/ml/datasets/AI4I+2020+Predictive+Maintenance+Dataset")
        sys.exit(1)

    # -------------------------------------------------------------------------
    # Step 2: Validate data
    # -------------------------------------------------------------------------
    print("\n[2/5] Validating data...")
    validator = DataValidator(df_raw)
    results = validator.run_all_checks()

    pass_count = sum(1 for r in results if r.status == "PASS")
    warn_count = sum(1 for r in results if r.status == "WARN")
    fail_count = sum(1 for r in results if r.status == "FAIL")

    print(f"      Checks: {pass_count} PASS, {warn_count} WARN, {fail_count} FAIL")

    validation_report = validator.generate_report()
    validation_path = REPORTS_DIR / "validation_report.md"
    save_markdown(validation_report, validation_path)
    print(f"      Saved: {validation_path}")

    # -------------------------------------------------------------------------
    # Step 3: Preprocess data
    # -------------------------------------------------------------------------
    print("\n[3/5] Preprocessing data...")
    df = preprocess_data(df_raw)
    print(f"      Added derived features. Columns: {len(df.columns)}")

    # -------------------------------------------------------------------------
    # Step 4: Compute KPIs and generate summary
    # -------------------------------------------------------------------------
    print("\n[4/5] Computing KPIs...")
    summary = generate_kpi_summary(df)
    summary_path = REPORTS_DIR / "summary.md"
    save_markdown(summary, summary_path)
    print(f"      Saved: {summary_path}")

    # Print key stats to console
    total = len(df)
    failures = df["Machine failure"].sum()
    rate = failures / total * 100
    print(f"      Total records: {total:,}")
    print(f"      Total failures: {int(failures):,}")
    print(f"      Overall failure rate: {rate:.2f}%")

    # -------------------------------------------------------------------------
    # Step 5: Generate visualizations
    # -------------------------------------------------------------------------
    print("\n[5/5] Generating visualizations...")
    generate_all_figures(df, FIGURES_DIR)

    # -------------------------------------------------------------------------
    # Done
    # -------------------------------------------------------------------------
    print()
    print("=" * 60)
    print("Pipeline complete!")
    print("=" * 60)
    print()
    print("Generated outputs:")
    print(f"  - {REPORTS_DIR / 'summary.md'}")
    print(f"  - {REPORTS_DIR / 'validation_report.md'}")
    print(f"  - {FIGURES_DIR / 'failure_rate_by_type.png'}")
    print(f"  - {FIGURES_DIR / 'failure_mode_counts.png'}")
    print(f"  - {FIGURES_DIR / 'temp_delta_vs_failure.png'}")


if __name__ == "__main__":
    main()
