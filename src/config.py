"""
Configuration settings for the manufacturing quality analysis pipeline.

Contains paths, column definitions, and validation parameters.
"""

from pathlib import Path

# -----------------------------------------------------------------------------
# Paths
# -----------------------------------------------------------------------------
PROJECT_ROOT = Path(__file__).parent.parent
DATA_RAW = PROJECT_ROOT / "data" / "raw"
DATA_PROCESSED = PROJECT_ROOT / "data" / "processed"
REPORTS_DIR = PROJECT_ROOT / "reports"
FIGURES_DIR = REPORTS_DIR / "figures"

RAW_CSV_PATH = DATA_RAW / "ai4i2020.csv"

# -----------------------------------------------------------------------------
# Column Definitions
# -----------------------------------------------------------------------------
# Required columns in the dataset
REQUIRED_COLUMNS = [
    "UDI",
    "Product ID",
    "Type",
    "Air temperature [K]",
    "Process temperature [K]",
    "Rotational speed [rpm]",
    "Torque [Nm]",
    "Tool wear [min]",
    "Machine failure",
    "TWF",  # Tool Wear Failure
    "HDF",  # Heat Dissipation Failure
    "PWF",  # Power Failure
    "OSF",  # Overstrain Failure
    "RNF",  # Random Failure
]

# Failure mode columns (binary flags)
FAILURE_MODE_COLS = ["TWF", "HDF", "PWF", "OSF", "RNF"]

# Target column
TARGET_COL = "Machine failure"

# Product type categories
VALID_TYPES = {"L", "M", "H"}

# Continuous feature columns for analysis
CONTINUOUS_FEATURES = [
    "Air temperature [K]",
    "Process temperature [K]",
    "Rotational speed [rpm]",
    "Torque [Nm]",
    "Tool wear [min]",
]

# -----------------------------------------------------------------------------
# Validation Parameters
# -----------------------------------------------------------------------------
# Physical constraints for domain validation
VALIDATION_RULES = {
    "Torque [Nm]": {"min": 0, "max": None},
    "Tool wear [min]": {"min": 0, "max": None},
    "Rotational speed [rpm]": {"min": 0, "max": None, "strict_positive": True},
    "Air temperature [K]": {"min": 0, "max": None, "strict_positive": True},
    "Process temperature [K]": {"min": 0, "max": None, "strict_positive": True},
}

# -----------------------------------------------------------------------------
# Quantile Thresholds for Analysis
# -----------------------------------------------------------------------------
QUANTILE_THRESHOLDS = {
    "low": 0.10,   # 10th percentile
    "high": 0.90,  # 90th percentile
}
