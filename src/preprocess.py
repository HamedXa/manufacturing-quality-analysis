"""
Preprocessing utilities for the manufacturing dataset.
"""

import pandas as pd
from typing import Tuple


def add_temp_delta(df: pd.DataFrame) -> pd.DataFrame:
    """
    Add temperature delta feature (Process - Air temperature).

    Parameters
    ----------
    df : pd.DataFrame
        Input data with temperature columns.

    Returns
    -------
    pd.DataFrame
        Data with added 'Temp_Delta [K]' column.
    """
    df = df.copy()
    df["Temp_Delta [K]"] = df["Process temperature [K]"] - df["Air temperature [K]"]
    return df


def categorize_by_quantiles(
    series: pd.Series, q_low: float = 0.10, q_high: float = 0.90
) -> pd.Series:
    """
    Categorize a numeric series into Low/Medium/High based on quantile thresholds.

    Parameters
    ----------
    series : pd.Series
        Numeric values to categorize.
    q_low : float, default 0.10
        Lower quantile threshold.
    q_high : float, default 0.90
        Upper quantile threshold.

    Returns
    -------
    pd.Series
        Categorical series with values 'Low', 'Medium', 'High'.
    """
    low_val = series.quantile(q_low)
    high_val = series.quantile(q_high)

    def assign_category(x):
        if x <= low_val:
            return "Low"
        elif x >= high_val:
            return "High"
        else:
            return "Medium"

    return series.apply(assign_category)


def compute_quantile_stats(
    df: pd.DataFrame, column: str, q_low: float = 0.10, q_high: float = 0.90
) -> dict:
    """
    Compute quantile thresholds and summary statistics for a column.

    Parameters
    ----------
    df : pd.DataFrame
        Input data.
    column : str
        Column name.
    q_low : float
        Lower quantile.
    q_high : float
        Upper quantile.

    Returns
    -------
    dict
        Dictionary with q_low_value, q_high_value, min, max, mean, median.
    """
    series = df[column]
    return {
        "column": column,
        "q_low": q_low,
        "q_low_value": series.quantile(q_low),
        "q_high": q_high,
        "q_high_value": series.quantile(q_high),
        "min": series.min(),
        "max": series.max(),
        "mean": series.mean(),
        "median": series.median(),
    }


def preprocess_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Apply all preprocessing steps to the raw data.

    Steps:
    1. Add temperature delta feature.

    Parameters
    ----------
    df : pd.DataFrame
        Raw data.

    Returns
    -------
    pd.DataFrame
        Preprocessed data.
    """
    df = add_temp_delta(df)
    return df
