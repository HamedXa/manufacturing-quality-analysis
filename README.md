# Manufacturing Quality & Process Analysis (Public Dataset Case Study)

Portfolio case study analyzing manufacturing equipment/production records to identify failure drivers and propose process + data-quality improvements. No proprietary or internal company data is used. Any “impact” figures (if included) are scenario-based and documented with assumptions.

## Overview
This project combines:
- defect/failure pattern analysis (KPIs, Pareto-style breakdowns, driver analysis),
- process documentation (BPMN current vs. future state),
- an automated data validation framework to prevent bad records from affecting analytics.

## Dataset
Source: AI4I 2020 Predictive Maintenance dataset (CSV)
File used: `ai4i2020.csv`
Records: 10,000
Columns: 14
Missing values: 0

Key fields:
- Identifiers: `UDI`, `Product ID`, `Type` (L/M/H)
- Process parameters: `Air temperature [K]`, `Process temperature [K]`, `Rotational speed [rpm]`, `Torque [Nm]`, `Tool wear [min]`
- Targets: `Machine failure` (binary) + failure mode flags (`TWF`, `HDF`, `PWF`, `OSF`, `RNF`)
Note: failure modes are multi-label in some rows.

## Objectives
- Compute quality/reliability KPIs (failure rate overall and by segment).
- Identify top drivers (station/shift equivalents are modeled here as product/type segments + parameter thresholds).
- Produce BPMN diagrams for a maintenance/quality workflow:
  - current-state: monitor → detect → manual checks → action
  - future-state: validate → score → alert → triage → maintenance → verification
- Build a reusable Python validation suite and output a validation report.

## Method
1. Data preparation: type casting, derived features (e.g., temperature delta), sanity checks.
2. Analysis:
   - failure rate by product type
   - parameter threshold analysis (quantiles)
   - failure modes distribution (multi-label)
3. Validation framework:
   - required columns + dtypes
   - range/logic rules (e.g., non-negative wear/torque, valid timestamps if present)
   - uniqueness rules (where applicable)
   - anomaly flags (e.g., sudden failure-rate spikes)
4. Recommendations:
   - prioritized actions tied to observed drivers
   - scenario estimates (optional) with assumptions and limitations

## Key findings (reproducible)
- Overall failure rate: 3.39% (339/10,000)
- High torque (> 52.6 Nm, top 10%) shows higher failure rate: 18.46% vs 1.72%
- High tool wear (> 195 min, top 10%) shows higher failure rate: 12.92% vs 2.34%
- Low rotational speed (< 1364 rpm, bottom 10%) shows higher failure rate: 16.70%

## Deliverables
- Notebooks: EDA + driver analysis
- Exported figures and written summary in `reports/`
- BPMN diagrams (current vs. future state) in `reports/bpmn/`
- Data validation module in `src/validation.py` + validation report in `reports/validation_report.md`
- Docs: requirements, technical spec, data dictionary, assumptions in `docs/`

## Tech
Python (pandas, numpy, matplotlib), BPMN (draw.io/Lucidchart), Markdown

## Status
Completed case study — last updated: 2026-01-06
