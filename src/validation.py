"""
Data validation framework for manufacturing dataset.

Implements schema checks, domain validation, and consistency checks.
"""

import pandas as pd
from typing import List, Dict, Any, Tuple
from dataclasses import dataclass, field

from .config import (
    REQUIRED_COLUMNS,
    VALID_TYPES,
    FAILURE_MODE_COLS,
    TARGET_COL,
    VALIDATION_RULES,
)


@dataclass
class ValidationResult:
    """Container for a single validation check result."""
    check_name: str
    status: str  # PASS, FAIL, WARN
    message: str
    details: Dict[str, Any] = field(default_factory=dict)


class DataValidator:
    """
    Validates the manufacturing dataset against defined rules.

    Attributes
    ----------
    df : pd.DataFrame
        Data to validate.
    results : List[ValidationResult]
        Accumulated validation results.
    """

    def __init__(self, df: pd.DataFrame):
        self.df = df
        self.results: List[ValidationResult] = []

    def check_required_columns(self) -> ValidationResult:
        """Check that all required columns are present."""
        actual_cols = set(self.df.columns)
        required = set(REQUIRED_COLUMNS)
        missing = required - actual_cols

        if missing:
            result = ValidationResult(
                check_name="Required Columns",
                status="FAIL",
                message=f"Missing {len(missing)} required column(s).",
                details={"missing_columns": list(missing)},
            )
        else:
            result = ValidationResult(
                check_name="Required Columns",
                status="PASS",
                message=f"All {len(REQUIRED_COLUMNS)} required columns present.",
                details={"column_count": len(REQUIRED_COLUMNS)},
            )
        self.results.append(result)
        return result

    def check_type_domain(self) -> ValidationResult:
        """Check that 'Type' column contains only valid values {L, M, H}."""
        if "Type" not in self.df.columns:
            result = ValidationResult(
                check_name="Type Domain",
                status="FAIL",
                message="'Type' column not found.",
                details={},
            )
        else:
            actual_types = set(self.df["Type"].unique())
            invalid = actual_types - VALID_TYPES

            if invalid:
                result = ValidationResult(
                    check_name="Type Domain",
                    status="FAIL",
                    message=f"Invalid Type values found: {invalid}",
                    details={"invalid_values": list(invalid), "valid_values": list(VALID_TYPES)},
                )
            else:
                result = ValidationResult(
                    check_name="Type Domain",
                    status="PASS",
                    message=f"All Type values are valid: {actual_types}",
                    details={"found_types": list(actual_types)},
                )
        self.results.append(result)
        return result

    def check_numeric_ranges(self) -> List[ValidationResult]:
        """Check numeric columns against physical constraints."""
        results = []

        for col, rules in VALIDATION_RULES.items():
            if col not in self.df.columns:
                result = ValidationResult(
                    check_name=f"Range Check: {col}",
                    status="WARN",
                    message=f"Column '{col}' not found, skipping range check.",
                    details={},
                )
            else:
                series = self.df[col]
                violations = []

                min_val = rules.get("min")
                max_val = rules.get("max")
                strict_positive = rules.get("strict_positive", False)

                if min_val is not None:
                    if strict_positive:
                        bad_count = (series <= min_val).sum()
                        if bad_count > 0:
                            violations.append(f"{bad_count} values <= {min_val}")
                    else:
                        bad_count = (series < min_val).sum()
                        if bad_count > 0:
                            violations.append(f"{bad_count} values < {min_val}")

                if max_val is not None:
                    bad_count = (series > max_val).sum()
                    if bad_count > 0:
                        violations.append(f"{bad_count} values > {max_val}")

                if violations:
                    result = ValidationResult(
                        check_name=f"Range Check: {col}",
                        status="FAIL",
                        message="; ".join(violations),
                        details={"min": series.min(), "max": series.max()},
                    )
                else:
                    result = ValidationResult(
                        check_name=f"Range Check: {col}",
                        status="PASS",
                        message=f"All values within valid range. Min={series.min():.2f}, Max={series.max():.2f}",
                        details={"min": series.min(), "max": series.max()},
                    )

            results.append(result)
            self.results.append(result)

        return results

    def check_binary_flags(self) -> ValidationResult:
        """Check that target and failure mode columns are binary (0/1)."""
        all_flag_cols = [TARGET_COL] + FAILURE_MODE_COLS
        non_binary = {}

        for col in all_flag_cols:
            if col in self.df.columns:
                unique_vals = set(self.df[col].unique())
                if not unique_vals.issubset({0, 1}):
                    non_binary[col] = list(unique_vals)

        if non_binary:
            result = ValidationResult(
                check_name="Binary Flags",
                status="FAIL",
                message=f"{len(non_binary)} column(s) have non-binary values.",
                details={"non_binary_columns": non_binary},
            )
        else:
            result = ValidationResult(
                check_name="Binary Flags",
                status="PASS",
                message=f"All {len(all_flag_cols)} flag columns are binary (0/1).",
                details={"columns_checked": all_flag_cols},
            )
        self.results.append(result)
        return result

    def check_failure_consistency(self) -> ValidationResult:
        """
        Check logical consistency: if Machine failure == 0, all failure modes should be 0.

        This flags records where Machine failure is 0 but a failure mode is 1.
        """
        if TARGET_COL not in self.df.columns:
            result = ValidationResult(
                check_name="Failure Consistency",
                status="WARN",
                message=f"'{TARGET_COL}' column not found.",
                details={},
            )
        else:
            # Find rows where Machine failure == 0
            no_failure_mask = self.df[TARGET_COL] == 0

            # Check if any failure mode is 1 for these rows
            inconsistent_rows = []
            for col in FAILURE_MODE_COLS:
                if col in self.df.columns:
                    violations = self.df[no_failure_mask & (self.df[col] == 1)]
                    if len(violations) > 0:
                        inconsistent_rows.extend(violations.index.tolist())

            inconsistent_rows = list(set(inconsistent_rows))
            n_violations = len(inconsistent_rows)

            if n_violations > 0:
                result = ValidationResult(
                    check_name="Failure Consistency",
                    status="WARN",
                    message=f"{n_violations} row(s) have Machine failure=0 but a failure mode=1.",
                    details={
                        "violation_count": n_violations,
                        "sample_indices": inconsistent_rows[:10],  # First 10
                    },
                )
            else:
                result = ValidationResult(
                    check_name="Failure Consistency",
                    status="PASS",
                    message="All records are consistent (failure=0 implies all modes=0).",
                    details={},
                )
        self.results.append(result)
        return result

    def check_null_values(self) -> ValidationResult:
        """Check for null/missing values in the dataset."""
        null_counts = self.df.isnull().sum()
        cols_with_nulls = null_counts[null_counts > 0]

        if len(cols_with_nulls) > 0:
            result = ValidationResult(
                check_name="Null Values",
                status="WARN",
                message=f"{len(cols_with_nulls)} column(s) have null values.",
                details={"null_counts": cols_with_nulls.to_dict()},
            )
        else:
            result = ValidationResult(
                check_name="Null Values",
                status="PASS",
                message="No null values found in any column.",
                details={"total_rows": len(self.df)},
            )
        self.results.append(result)
        return result

    def run_all_checks(self) -> List[ValidationResult]:
        """Execute all validation checks and return results."""
        self.results = []  # Reset
        self.check_required_columns()
        self.check_type_domain()
        self.check_numeric_ranges()
        self.check_binary_flags()
        self.check_failure_consistency()
        self.check_null_values()
        return self.results

    def generate_report(self) -> str:
        """Generate a markdown validation report."""
        lines = [
            "# Data Validation Report",
            "",
            f"**Dataset:** ai4i2020.csv",
            f"**Total Records:** {len(self.df):,}",
            f"**Total Columns:** {len(self.df.columns)}",
            "",
            "## Validation Results",
            "",
            "| Check | Status | Message |",
            "|-------|--------|---------|",
        ]

        pass_count = 0
        warn_count = 0
        fail_count = 0

        for r in self.results:
            status_icon = {"PASS": "✅", "WARN": "⚠️", "FAIL": "❌"}.get(r.status, "❓")
            lines.append(f"| {r.check_name} | {status_icon} {r.status} | {r.message} |")

            if r.status == "PASS":
                pass_count += 1
            elif r.status == "WARN":
                warn_count += 1
            else:
                fail_count += 1

        lines.extend([
            "",
            "## Summary",
            "",
            f"- **PASS:** {pass_count}",
            f"- **WARN:** {warn_count}",
            f"- **FAIL:** {fail_count}",
            "",
        ])

        # Add details for warnings/failures
        issues = [r for r in self.results if r.status in ("WARN", "FAIL")]
        if issues:
            lines.append("## Details")
            lines.append("")
            for r in issues:
                lines.append(f"### {r.check_name} ({r.status})")
                lines.append("")
                lines.append(r.message)
                if r.details:
                    lines.append("")
                    lines.append("```")
                    for k, v in r.details.items():
                        lines.append(f"{k}: {v}")
                    lines.append("```")
                lines.append("")

        return "\n".join(lines)
