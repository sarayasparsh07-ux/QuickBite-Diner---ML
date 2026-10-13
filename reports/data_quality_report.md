# QuickBite — Data-Quality Report

Generated 06 Oct 2026. Overall status: **PASS WITH REVIEW NOTES**

## Scorecard

| Metric                                    | Value                              | Status   |
|:------------------------------------------|:-----------------------------------|:---------|
| Total records                             | 480 diners · 4,924 order-item rows | —        |
| Valid diner records (all fields)          | 479 / 480                          | PASS     |
| Adult diners in classifier scope (18+)    | 460 / 480                          | PASS     |
| Duplicate rate (all grains)               | 0.0%                               | PASS     |
| Missing-value rate                        | 0.0%                               | PASS     |
| Invalid values                            | 1 (age = 9)                        | REVIEW   |
| Under-18 diners (out of classifier scope) | 20 (ages 9–17)                     | REVIEW   |
| Referential-integrity failures            | 0                                  | PASS     |
| Statistical outliers (retained, genuine)  | 11                                 | PASS     |
| Data completeness                         | 100.0%                             | PASS     |
| Data validity (cell level)                | 99.99%                             | PASS     |

## Reconciliation

| Reconciliation check                               |   Count | Status   |
|:---------------------------------------------------|--------:|:---------|
| Diners in diners.csv                               |     480 | —        |
| Unique diners in orders.csv                        |     480 | —        |
| Matching diner IDs (valid relational overlap)      |     480 | PASS     |
| Orphan diner IDs in orders.csv (no profile)        |       0 | PASS     |
| Orphan order rows                                  |       0 | PASS     |
| Diners without any orders                          |       0 | PASS     |
| Duplicate diner IDs                                |       0 | PASS     |
| Duplicate exact order-item rows                    |       0 | PASS     |
| Duplicate items within an order                    |       0 | PASS     |
| Invalid order→diner mappings (order with >1 diner) |       0 | PASS     |

## Issue log & treatments

| ID    | Dataset   | Issue                                                                                                  | Quantity                         | Classification         | Treatment                                                                                                                                      | Impact                                                        |
|:------|:----------|:-------------------------------------------------------------------------------------------------------|:---------------------------------|:-----------------------|:-----------------------------------------------------------------------------------------------------------------------------------------------|:--------------------------------------------------------------|
| DQ-01 | diners    | Age below plausible account-holder age                                                                 | 1 diner (D1052, age 9)           | Invalid                | Excluded from the classifier and the app's age input (under-18 policy). Retained for clustering & baskets (age not used there). No imputation. | Classifier trained on 460 adult diners                        |
| DQ-02 | diners    | Age 14–17, below the app's 18–70 age input                                                             | 19 diners                        | Out of scope (minor)   | Excluded from the classifier and the app's age input under the 18+ policy. Not deleted: retained for segmentation & baskets. No age capping.   | Not scored; shown as 'not scored — under 18' in the dashboard |
| DQ-03 | diners    | total_spend ≈ orders/month × AOV (ratio 0.85–1.15)                                                     | All 480 diners                   | Valid (semantic note)  | Unchanged. Interpreted as ~1 month of spend; customer value reported as monthly run-rate, not lifetime value.                                  | Interpretation only                                           |
| DQ-04 | diners    | Statistical outliers (IQR rule)                                                                        | 11 values (recency, total spend) | Outlier — genuine      | Retained: within plausible business ranges and consistent with each diner's other fields.                                                      | None                                                          |
| DQ-05 | diners    | Dashboard input ranges exceed training ranges (e.g. recency ≤60 vs max 34; spend ≤20,000 vs max 1,490) | 4 inputs                         | Application constraint | Dashboard shows an extrapolation warning when inputs fall outside the training range.                                                          | Dashboard governance                                          |
| DQ-06 | orders    | orders.csv is a basket sample, not the full log                                                        | 2–6 baskets per diner            | Valid (scope note)     | Used for basket composition only; diner profile metrics not recomputed from it.                                                                | Interpretation only                                           |
| DQ-07 | orders    | Gaps in order_id sequence                                                                              | 8 IDs                            | Informational          | No action — gaps do not break any join (likely cancelled/voided orders).                                                                       | None                                                          |
| DQ-08 | orders    | Single-item baskets                                                                                    | 140 baskets                      | Valid                  | Retained — count towards item support; cannot form pair rules by construction.                                                                 | None                                                          |
| DQ-09 | both      | Duplicates at all three grains, orphans, multi-diner orders, missing values, ID formats                | 0 everywhere                     | Valid                  | Checks codified in pipeline; no rows removed.                                                                                                  | None                                                          |

## Outlier screening (not removed)

| feature               |   IQR low fence |   IQR high fence |   IQR outliers |   |z|>3 |    min |     max |
|:----------------------|----------------:|-----------------:|---------------:|--------:|-------:|--------:|
| orders_per_month      |           -5.5  |            22.5  |              0 |       0 |   1    |   20    |
| avg_order_value       |         -126.58 |           327.5  |              0 |       0 |  29.5  |  218.66 |
| avg_items_per_order   |           -2.5  |             9.5  |              0 |       0 |   1    |    9    |
| days_since_last_order |          -10    |            30    |              3 |       2 |   0    |   34    |
| discount_rate         |           -0.51 |             1.26 |              0 |       0 |   0    |    0.86 |
| age                   |            0.5  |            60.5  |              0 |       0 |   9    |   52    |
| total_spend           |           92.38 |          1207.47 |              8 |       2 | 134.04 | 1490.17 |

## Files

- Raw (untouched): `data/raw/diners.csv`, `data/raw/orders.csv`
- Clean: `data/clean/diners_clean.csv` (adds `age_flag`, `include_in_classifier`, `include_in_clustering`), `data/clean/orders_clean.csv` (adds `basket_size`)
