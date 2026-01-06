"""
KPI computation module for manufacturing quality analysis.
"""

import pandas as pd
from typing import Dict, Any, List
from .config import TARGET_COL, FAILURE_MODE_COLS


def compute_overall_failure_rate(df: pd.DataFrame) -> Dict[str, Any]:
    """
    Compute overall machine failure rate.

    Parameters
    ----------
    df : pd.DataFrame
        Data with 'Machine failure' column.

    Returns
    -------
    dict
        Dictionary with total_records, failure_count, failure_rate.
    """
    total = len(df)
    failures = df[TARGET_COL].sum()
    rate = failures / total if total > 0 else 0.0

    return {
        "total_records": total,
        "failure_count": int(failures),
        "failure_rate": rate,
        "failure_rate_pct": rate * 100,
    }


def compute_failure_rate_by_type(df: pd.DataFrame) -> pd.DataFrame:
    """
    Compute failure rate segmented by product Type (L/M/H).

    Parameters
    ----------
    df : pd.DataFrame
        Data with 'Type' and 'Machine failure' columns.

    Returns
    -------
    pd.DataFrame
        Summary with Type, count, failure_count, failure_rate.
    """
    grouped = df.groupby("Type").agg(
        count=(TARGET_COL, "size"),
        failure_count=(TARGET_COL, "sum"),
    ).reset_index()

    grouped["failure_rate"] = grouped["failure_count"] / grouped["count"]
    grouped["failure_rate_pct"] = grouped["failure_rate"] * 100

    # Sort by Type in order L, M, H
    type_order = {"L": 0, "M": 1, "H": 2}
    grouped["sort_key"] = grouped["Type"].map(type_order)
    grouped = grouped.sort_values("sort_key").drop(columns=["sort_key"])

    return grouped


def compute_failure_mode_counts(df: pd.DataFrame) -> pd.DataFrame:
    """
    Compute counts for each failure mode.

    Note: Records can have multiple failure modes (multi-label).

    Parameters
    ----------
    df : pd.DataFrame
        Data with failure mode columns.

    Returns
    -------
    pd.DataFrame
        DataFrame with mode, count, percentage columns.
    """
    total_failures = df[TARGET_COL].sum()
    total_records = len(df)

    records = []
    for mode in FAILURE_MODE_COLS:
        count = int(df[mode].sum())
        pct_of_failures = (count / total_failures * 100) if total_failures > 0 else 0.0
        pct_of_total = count / total_records * 100

        records.append({
            "failure_mode": mode,
            "count": count,
            "pct_of_failures": pct_of_failures,
            "pct_of_total": pct_of_total,
        })

    return pd.DataFrame(records)


def compute_quantile_failure_rates(
    df: pd.DataFrame, column: str, q_low: float = 0.10, q_high: float = 0.90
) -> Dict[str, Any]:
    """
    Compute failure rates for values at quantile extremes.

    Parameters
    ----------
    df : pd.DataFrame
        Data.
    column : str
        Numeric column to analyze.
    q_low : float
        Lower quantile threshold.
    q_high : float
        Upper quantile threshold.

    Returns
    -------
    dict
        Stats for low/medium/high segments.
    """
    low_threshold = df[column].quantile(q_low)
    high_threshold = df[column].quantile(q_high)

    low_mask = df[column] <= low_threshold
    high_mask = df[column] >= high_threshold
    mid_mask = ~low_mask & ~high_mask

    def segment_stats(mask, label):
        subset = df[mask]
        n = len(subset)
        failures = subset[TARGET_COL].sum()
        rate = failures / n if n > 0 else 0.0
        return {
            "segment": label,
            "count": n,
            "failure_count": int(failures),
            "failure_rate": rate,
            "failure_rate_pct": rate * 100,
        }

    return {
        "column": column,
        "q_low": q_low,
        "q_low_value": low_threshold,
        "q_high": q_high,
        "q_high_value": high_threshold,
        "segments": [
            segment_stats(low_mask, f"Low (≤{low_threshold:.2f})"),
            segment_stats(mid_mask, "Medium"),
            segment_stats(high_mask, f"High (≥{high_threshold:.2f})"),
        ],
    }


def compute_temp_delta_stats(df: pd.DataFrame) -> Dict[str, Any]:
    """
    Compute statistics for temperature delta by failure status.

    Parameters
    ----------
    df : pd.DataFrame
        Data with 'Temp_Delta [K]' and 'Machine failure' columns.

    Returns
    -------
    dict
        Stats for failed vs non-failed records.
    """
    delta_col = "Temp_Delta [K]"

    if delta_col not in df.columns:
        return {"error": f"Column '{delta_col}' not found. Run preprocessing first."}

    failed = df[df[TARGET_COL] == 1][delta_col]
    not_failed = df[df[TARGET_COL] == 0][delta_col]

    return {
        "overall": {
            "mean": df[delta_col].mean(),
            "median": df[delta_col].median(),
            "std": df[delta_col].std(),
            "min": df[delta_col].min(),
            "max": df[delta_col].max(),
        },
        "failed": {
            "count": len(failed),
            "mean": failed.mean(),
            "median": failed.median(),
            "std": failed.std(),
        },
        "not_failed": {
            "count": len(not_failed),
            "mean": not_failed.mean(),
            "median": not_failed.median(),
            "std": not_failed.std(),
        },
    }


def generate_kpi_summary(df: pd.DataFrame) -> str:
    """
    Generate a markdown summary of all KPIs.

    Parameters
    ----------
    df : pd.DataFrame
        Preprocessed data.

    Returns
    -------
    str
        Markdown formatted summary.
    """
    overall = compute_overall_failure_rate(df)
    by_type = compute_failure_rate_by_type(df)
    modes = compute_failure_mode_counts(df)
    temp_stats = compute_temp_delta_stats(df)

    lines = [
        "# Manufacturing Quality Analysis Summary",
        "",
        "## Dataset Overview",
        "",
        f"- **Total Records:** {overall['total_records']:,}",
        f"- **Total Failures:** {overall['failure_count']:,}",
        f"- **Overall Failure Rate:** {overall['failure_rate_pct']:.2f}%",
        "",
        "## Failure Rate by Product Type",
        "",
        "Product types represent quality tiers (L=Low, M=Medium, H=High quality).",
        "",
        "| Type | Count | Failures | Failure Rate |",
        "|------|-------|----------|--------------|",
    ]

    for _, row in by_type.iterrows():
        lines.append(
            f"| {row['Type']} | {int(row['count']):,} | {int(row['failure_count']):,} | {row['failure_rate_pct']:.2f}% |"
        )

    lines.extend([
        "",
        "## Failure Mode Distribution",
        "",
        "Note: Records can have multiple failure modes (multi-label). Percentages may exceed 100% when summed.",
        "",
        "| Mode | Full Name | Count | % of Failures |",
        "|------|-----------|-------|---------------|",
    ])

    mode_names = {
        "TWF": "Tool Wear Failure",
        "HDF": "Heat Dissipation Failure",
        "PWF": "Power Failure",
        "OSF": "Overstrain Failure",
        "RNF": "Random Failure",
    }

    for _, row in modes.iterrows():
        mode = row["failure_mode"]
        full_name = mode_names.get(mode, mode)
        lines.append(
            f"| {mode} | {full_name} | {int(row['count']):,} | {row['pct_of_failures']:.1f}% |"
        )

    lines.extend([
        "",
        "## Temperature Delta Analysis",
        "",
        "Temperature delta = Process temperature - Air temperature (in Kelvin).",
        "",
    ])

    if "error" in temp_stats:
        lines.append(f"*{temp_stats['error']}*")
    else:
        lines.extend([
            "| Metric | Failed Records | Non-Failed Records |",
            "|--------|----------------|---------------------|",
            f"| Count | {temp_stats['failed']['count']:,} | {temp_stats['not_failed']['count']:,} |",
            f"| Mean | {temp_stats['failed']['mean']:.2f} K | {temp_stats['not_failed']['mean']:.2f} K |",
            f"| Median | {temp_stats['failed']['median']:.2f} K | {temp_stats['not_failed']['median']:.2f} K |",
            f"| Std Dev | {temp_stats['failed']['std']:.2f} K | {temp_stats['not_failed']['std']:.2f} K |",
        ])

    lines.extend([
        "",
        "## Quantile Threshold Analysis",
        "",
        "Failure rates at parameter extremes (10th and 90th percentiles):",
        "",
    ])

    for col in ["Torque [Nm]", "Tool wear [min]", "Rotational speed [rpm]"]:
        q_stats = compute_quantile_failure_rates(df, col)
        lines.append(f"### {col}")
        lines.append("")
        lines.append(f"- Q10 threshold: {q_stats['q_low_value']:.2f}")
        lines.append(f"- Q90 threshold: {q_stats['q_high_value']:.2f}")
        lines.append("")
        lines.append("| Segment | Count | Failures | Rate |")
        lines.append("|---------|-------|----------|------|")
        for seg in q_stats["segments"]:
            lines.append(
                f"| {seg['segment']} | {seg['count']:,} | {seg['failure_count']:,} | {seg['failure_rate_pct']:.2f}% |"
            )
        lines.append("")

    lines.extend([
        "---",
        "",
        "*Report auto-generated by the manufacturing quality analysis pipeline.*",
    ])

    return "\n".join(lines)
