"""
Visualization module for manufacturing quality analysis.

Uses matplotlib only (no seaborn).
"""

import matplotlib.pyplot as plt
import pandas as pd
from pathlib import Path
from typing import Union, Optional

from .config import TARGET_COL, FAILURE_MODE_COLS


def set_style():
    """Set consistent matplotlib style."""
    plt.rcParams.update({
        "figure.figsize": (10, 6),
        "figure.dpi": 100,
        "axes.titlesize": 14,
        "axes.labelsize": 12,
        "xtick.labelsize": 10,
        "ytick.labelsize": 10,
        "axes.spines.top": False,
        "axes.spines.right": False,
    })


def plot_failure_rate_by_type(
    df: pd.DataFrame, output_path: Optional[Union[str, Path]] = None
) -> plt.Figure:
    """
    Create bar chart of failure rate by product type.

    Parameters
    ----------
    df : pd.DataFrame
        Data with 'Type' and 'Machine failure' columns.
    output_path : str or Path, optional
        If provided, save figure to this path.

    Returns
    -------
    plt.Figure
        The figure object.
    """
    set_style()

    # Compute failure rates
    grouped = df.groupby("Type").agg(
        count=(TARGET_COL, "size"),
        failures=(TARGET_COL, "sum"),
    ).reset_index()
    grouped["failure_rate"] = grouped["failures"] / grouped["count"] * 100

    # Sort by type order
    type_order = {"L": 0, "M": 1, "H": 2}
    grouped["sort_key"] = grouped["Type"].map(type_order)
    grouped = grouped.sort_values("sort_key")

    # Create figure
    fig, ax = plt.subplots()

    bars = ax.bar(
        grouped["Type"],
        grouped["failure_rate"],
        color=["#1f77b4", "#2ca02c", "#ff7f0e"],
        edgecolor="black",
        linewidth=0.5,
    )

    # Add value labels on bars
    for bar, rate, count in zip(bars, grouped["failure_rate"], grouped["count"]):
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            bar.get_height() + 0.2,
            f"{rate:.2f}%\n(n={count:,})",
            ha="center",
            va="bottom",
            fontsize=10,
        )

    ax.set_xlabel("Product Type (L=Low, M=Medium, H=High Quality)")
    ax.set_ylabel("Failure Rate (%)")
    ax.set_title("Machine Failure Rate by Product Type")
    ax.set_ylim(0, max(grouped["failure_rate"]) * 1.3)

    plt.tight_layout()

    if output_path:
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        fig.savefig(output_path, dpi=150, bbox_inches="tight")
        print(f"Saved: {output_path}")

    return fig


def plot_failure_mode_counts(
    df: pd.DataFrame, output_path: Optional[Union[str, Path]] = None
) -> plt.Figure:
    """
    Create bar chart of failure mode counts.

    Parameters
    ----------
    df : pd.DataFrame
        Data with failure mode columns.
    output_path : str or Path, optional
        If provided, save figure to this path.

    Returns
    -------
    plt.Figure
        The figure object.
    """
    set_style()

    # Compute counts
    mode_counts = {mode: int(df[mode].sum()) for mode in FAILURE_MODE_COLS}

    mode_labels = {
        "TWF": "Tool Wear\nFailure",
        "HDF": "Heat Dissipation\nFailure",
        "PWF": "Power\nFailure",
        "OSF": "Overstrain\nFailure",
        "RNF": "Random\nFailure",
    }

    labels = [mode_labels.get(m, m) for m in FAILURE_MODE_COLS]
    counts = [mode_counts[m] for m in FAILURE_MODE_COLS]

    # Create figure
    fig, ax = plt.subplots()

    colors = ["#d62728", "#9467bd", "#8c564b", "#e377c2", "#7f7f7f"]
    bars = ax.bar(labels, counts, color=colors, edgecolor="black", linewidth=0.5)

    # Add value labels
    for bar, count in zip(bars, counts):
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            bar.get_height() + 1,
            str(count),
            ha="center",
            va="bottom",
            fontsize=10,
            fontweight="bold",
        )

    ax.set_xlabel("Failure Mode")
    ax.set_ylabel("Count")
    ax.set_title("Failure Mode Distribution\n(Note: Records can have multiple modes)")
    ax.set_ylim(0, max(counts) * 1.15)

    plt.tight_layout()

    if output_path:
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        fig.savefig(output_path, dpi=150, bbox_inches="tight")
        print(f"Saved: {output_path}")

    return fig


def plot_temp_delta_by_failure(
    df: pd.DataFrame, output_path: Optional[Union[str, Path]] = None
) -> plt.Figure:
    """
    Create box plot comparing temperature delta for failed vs non-failed records.

    Parameters
    ----------
    df : pd.DataFrame
        Data with 'Temp_Delta [K]' and 'Machine failure' columns.
    output_path : str or Path, optional
        If provided, save figure to this path.

    Returns
    -------
    plt.Figure
        The figure object.
    """
    set_style()

    delta_col = "Temp_Delta [K]"

    if delta_col not in df.columns:
        raise ValueError(f"Column '{delta_col}' not found. Run preprocessing first.")

    not_failed = df[df[TARGET_COL] == 0][delta_col]
    failed = df[df[TARGET_COL] == 1][delta_col]

    fig, ax = plt.subplots()

    bp = ax.boxplot(
        [not_failed, failed],
        labels=["No Failure\n(n={:,})".format(len(not_failed)), 
                "Failure\n(n={:,})".format(len(failed))],
        patch_artist=True,
    )

    colors = ["#2ca02c", "#d62728"]
    for patch, color in zip(bp["boxes"], colors):
        patch.set_facecolor(color)
        patch.set_alpha(0.6)

    ax.set_xlabel("Machine Status")
    ax.set_ylabel("Temperature Delta (Process - Air) [K]")
    ax.set_title("Temperature Delta Distribution by Failure Status")

    # Add mean markers
    means = [not_failed.mean(), failed.mean()]
    ax.scatter([1, 2], means, marker="D", color="black", s=50, zorder=3, label="Mean")
    ax.legend(loc="upper right")

    plt.tight_layout()

    if output_path:
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        fig.savefig(output_path, dpi=150, bbox_inches="tight")
        print(f"Saved: {output_path}")

    return fig


def plot_quantile_analysis(
    df: pd.DataFrame,
    column: str,
    output_path: Optional[Union[str, Path]] = None,
    q_low: float = 0.10,
    q_high: float = 0.90,
) -> plt.Figure:
    """
    Create bar chart showing failure rates at quantile extremes.

    Parameters
    ----------
    df : pd.DataFrame
        Data.
    column : str
        Numeric column to analyze.
    output_path : str or Path, optional
        If provided, save figure to this path.
    q_low : float
        Lower quantile.
    q_high : float
        Upper quantile.

    Returns
    -------
    plt.Figure
        The figure object.
    """
    set_style()

    low_threshold = df[column].quantile(q_low)
    high_threshold = df[column].quantile(q_high)

    low_mask = df[column] <= low_threshold
    high_mask = df[column] >= high_threshold
    mid_mask = ~low_mask & ~high_mask

    def get_rate(mask):
        subset = df[mask]
        if len(subset) == 0:
            return 0, 0
        return len(subset), subset[TARGET_COL].sum() / len(subset) * 100

    low_n, low_rate = get_rate(low_mask)
    mid_n, mid_rate = get_rate(mid_mask)
    high_n, high_rate = get_rate(high_mask)

    labels = [
        f"Low\n(≤{low_threshold:.1f})\nn={low_n:,}",
        f"Medium\nn={mid_n:,}",
        f"High\n(≥{high_threshold:.1f})\nn={high_n:,}",
    ]
    rates = [low_rate, mid_rate, high_rate]

    fig, ax = plt.subplots()

    colors = ["#1f77b4", "#7f7f7f", "#d62728"]
    bars = ax.bar(labels, rates, color=colors, edgecolor="black", linewidth=0.5)

    for bar, rate in zip(bars, rates):
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            bar.get_height() + 0.2,
            f"{rate:.2f}%",
            ha="center",
            va="bottom",
            fontsize=10,
            fontweight="bold",
        )

    ax.set_xlabel(f"{column} Segment (Q{int(q_low*100)}/Q{int(q_high*100)} thresholds)")
    ax.set_ylabel("Failure Rate (%)")
    ax.set_title(f"Failure Rate by {column} Quantile Segments")
    ax.set_ylim(0, max(rates) * 1.3 if max(rates) > 0 else 1)

    plt.tight_layout()

    if output_path:
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        fig.savefig(output_path, dpi=150, bbox_inches="tight")
        print(f"Saved: {output_path}")

    return fig


def generate_all_figures(df: pd.DataFrame, output_dir: Union[str, Path]) -> None:
    """
    Generate and save all figures.

    Parameters
    ----------
    df : pd.DataFrame
        Preprocessed data.
    output_dir : str or Path
        Directory to save figures.
    """
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    plot_failure_rate_by_type(df, output_dir / "failure_rate_by_type.png")
    plot_failure_mode_counts(df, output_dir / "failure_mode_counts.png")
    plot_temp_delta_by_failure(df, output_dir / "temp_delta_vs_failure.png")

    plt.close("all")
    print(f"\nAll figures saved to {output_dir}")
