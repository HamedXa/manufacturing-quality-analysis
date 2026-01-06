# Data Validation Report

**Dataset:** ai4i2020.csv
**Total Records:** 10,000
**Total Columns:** 14

## Validation Results

| Check | Status | Message |
|-------|--------|---------|
| Required Columns | ✅ PASS | All 14 required columns present. |
| Type Domain | ✅ PASS | All Type values are valid: {'M', 'L', 'H'} |
| Range Check: Torque [Nm] | ✅ PASS | All values within valid range. Min=3.80, Max=76.60 |
| Range Check: Tool wear [min] | ✅ PASS | All values within valid range. Min=0.00, Max=253.00 |
| Range Check: Rotational speed [rpm] | ✅ PASS | All values within valid range. Min=1168.00, Max=2886.00 |
| Range Check: Air temperature [K] | ✅ PASS | All values within valid range. Min=295.30, Max=304.50 |
| Range Check: Process temperature [K] | ✅ PASS | All values within valid range. Min=305.70, Max=313.80 |
| Binary Flags | ✅ PASS | All 6 flag columns are binary (0/1). |
| Failure Consistency | ⚠️ WARN | 18 row(s) have Machine failure=0 but a failure mode=1. |
| Null Values | ✅ PASS | No null values found in any column. |

## Summary

- **PASS:** 9
- **WARN:** 1
- **FAIL:** 0

## Details

### Failure Consistency (WARN)

18 row(s) have Machine failure=0 but a failure mode=1.

```
violation_count: 18
sample_indices: [7488, 6913, 7868, 1221, 5471, 5509, 5639, 6091, 6960, 5489]
```
