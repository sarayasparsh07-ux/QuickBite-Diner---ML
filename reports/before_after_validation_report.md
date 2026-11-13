# Before-and-after validation report

Generated 05 Nov 2026, 22:37 by `validation/validation_scripts/run_validation.py`. Machine-readable results: `validation/before_after_validation_report.json`. Approved differences: `validation/approved_differences.json`.

**Overall result: PASS** — 0 unexplained difference(s) across all comparisons.

**Comparisons.** *received → final*: the project exactly as received (its own app, artifacts and bundle) against this submission — strict. *previous refinement → final*: everything since the submission before the CV-interpretation refinement — strict. *micro refinement → final*: isolates this final polish (the submission immediately before it) — strict. *final polish → final*: isolates the observed-adult-range terminology correction — strict. *range correction → final* and *dq correction → final*: the DQ-01 / DQ-05 correction and the DQ-05 quantity correction — strict. *pre-redesign → final*: the dashboard before the visual redesign — every number compared; labels and styling out of scope.

**How a difference can pass.** Only if (1) it carries an approved code, (2) it occurs in that code's location, and (3) it passes that code's own content test. Everything else is UNEXPECTED = FAIL.

**Tolerance.** floats: relative 1e-12 (serialisation round-off only; nothing is rounded away); text, labels, table cells: exact string match (chart titles: <br> line breaks compare as spaces); predictions: exact equality (same artifact, same inputs).

## Result summary

| Validation | Result |
|---|---|
| CV validation | **PASS** |
| Prediction schema validation | **PASS** |
| Prediction value validation | **PASS** |
| Observed adult range terminology (tests A–F) | **PASS** |
| Data-quality issue log consistency (DQ-01 / DQ-05, 5 representations) | **PASS** |
| Checksum integrity (protected artifacts) | **PASS** |
| Negative controls | **PASS (73/73 executed controls behaved as required)** |
| Overall validation | **PASS** |

## Dedicated checks (CV precision · prediction schema · observed adult range · DQ log · checksums)

| Check | Result | Detail (component · model/profile · expected · actual) |
|---|---|---|
| DQ log — notebook: DQ-01 and DQ-05 present exactly once | PASS | PASS |
| DQ log — csv: DQ-01 and DQ-05 present exactly once | PASS | PASS |
| DQ log — markdown: DQ-01 and DQ-05 present exactly once | PASS | PASS |
| DQ log — bundle: DQ-01 and DQ-05 present exactly once | PASS | PASS |
| DQ log — dashboard: DQ-01 and DQ-05 present exactly once | PASS | PASS |
| DQ log — DQ-01: identical in notebook, CSV, Markdown report, analytics bundle and Governance dashboard | PASS | PASS |
| DQ log — DQ-05: identical in notebook, CSV, Markdown report, analytics bundle and Governance dashboard | PASS | PASS |
| DQ log — DQ-01: identifier, dataset, issue, quantity (D1052, age 9), classification and treatment unchanged | PASS | PASS |
| DQ log — DQ-01: names the 368 training observations (not 'trained on 460') | PASS | PASS |
| DQ log — DQ-01: names the 92 held-out test observations | PASS | PASS |
| DQ log — DQ-01: names the 460 classifier-eligible adults as eligibility, not fitting | PASS | PASS |
| DQ log — DQ-05: identifier, dataset, classification and impact unchanged | PASS | PASS |
| DQ log — DQ-05: dashboard input limits on the Governance page = app.py INPUT_SPEC | PASS | PASS |
| DQ log — DQ-05: the controls are exactly the 7 classifier input features | PASS | PASS |
| DQ log — DQ-05: Quantity equals the independent calculation in every representation (computed: 6 of 7 classifier input controls; 1 control(s) within / equal) | PASS | PASS |
| DQ log — DQ-05: calculation agrees with the documented expectation (7 controls · 6 outside · 1 within / equal: orders_per_month) | PASS | PASS |
| DQ log — DQ-05: explanation table in the data-quality report = the independent calculation (row by row and result) | PASS | PASS |
| DQ log — DQ-05: quoted range values unchanged and equal to the observed adult maxima / dashboard input limits | PASS | PASS |
| DQ log — DQ-05: observed adult classifier range terminology; reference population = the 460 eligible adults | PASS | PASS |
| DQ log — Observed adult classifier range = min–max of the 460 adult diners, identical to the baseline | PASS | PASS |
| DQ log — Validator's 7 classifier features = food_models.joblib features + age + total_spend | PASS | PASS |
| DQ log — Executed notebook cells == cells generated from build/notebook_source.py | PASS | PASS |
| DQ log — Batch CSV export schema identical to the reference (incl. outside_training_range) | PASS | PASS |
| CV accuracy mean — stored (raw, 1e-12) and displayed (exact 'mean% ± sd%' string), 4 models | PASS | all 4 candidates match the independent recomputation |
| CV accuracy standard deviation — stored (raw, 1e-12) and displayed (exact 'mean% ± sd%' string), 4 models | PASS | all 4 candidates match the independent recomputation |
| Other selection-table fields (precision, recall, F1, ROC-AUC, Brier, interpretable) — exact | PASS | all match |
| Model selection — one row per candidate, exactly one selected, no test metrics, rule = highest CV ROC-AUC (Brier, interpretable) | PASS | selected Logistic Regression (scaled); lowest CV Brier Logistic Regression (scaled) |
| Prediction schema — field definition, field count, field order and types, collection length | PASS | fields ['profile_id', 'segment', 'reorder', 'prob', 'items', 'tier']; 5,179 records per version; 0 structural defects |
| Prediction/profile correspondence — every record matched to its profile identifier, deterministic order, no duplicates | PASS | 5,179 identifiers matched in each version |
| Prediction value equality — segment, reorder, probability (exact), items, tier | PASS | 10,358 record comparisons (5,179 profiles × 2 earlier versions), 0 mismatches |
| Negative controls — CV display contract | PASS | 11/11 behaved as required |
| Negative controls — stored CV values | PASS | 2/2 behaved as required |
| Negative controls — prediction structure | PASS | 11/11 behaved as required |
| Negative controls — checksum assessment (temporary copies) | PASS | 6/6 behaved as required |
| Negative controls — DQ-01 / DQ-05 issue log | PASS | 8/8 behaved as required |
| Negative controls — DQ-05 quantity recalculation | PASS | 10/10 behaved as required |
| Range A — reference range derived from the 460 adult classifier-eligible diners | PASS | 1/1 smoke checks pass |
| Range B/F — no 368-row 'training range' wording; Governance and warnings use 'observed adult' terms | PASS | 1/1 smoke checks pass |
| Range C — every feature minimum / maximum identical to the previous submission | PASS | 1/1 smoke checks pass |
| Range F — scoring, What-If and batch-table wording | PASS | 3/3 smoke checks pass |
| Batch D/E — export byte-identical incl. outside_training_range; predictions, tiers, flags unchanged | PASS | 2/2 smoke checks pass |
| Checksum-monitored protected artifacts present and equal to their recorded reference (MD5 and SHA-256) | PASS | 9 declared files (validation/protected_checksums.json) all present; the 7 byte-identical files match their reference under both algorithms |
| Validation run left all checksum-monitored protected artifacts unchanged | PASS | 9 files: MD5 and SHA-256 at the start of the run = at the end. Other files the run reads or writes are outside this assertion (see the checksum inventory) |

## Component summary

| Component | Original | Updated | Result |
|---|---|---|---|
| KPI values | 154 KPI cards in 42 page/state snapshots | every value identical; 17 label/context/timestamp records, all approved: M2:kpi-overview-rename, M2:kpi-retention-rename, M2:kpi-rocauc-context, M2:kpi-test-context, T1:kpi-governance-population, TS:kpi | PASS |
| Segment counts | {"Premium Foodies": 130, "Family Feasters": 150, "Budget Students": 200, "All diners": 480} | {"Premium Foodies": 130, "Family Feasters": 150, "Budget Students": 200, "All diners": 480} | PASS |
| Association rules | 126 overall rules | support/confidence/lift identical; 5 bundle row records, all R1; Biryani → Raita first in 4/4 rule tables | PASS |
| Classification metrics | test accuracy 0.902174 · ROC-AUC 0.973197 · repeated-CV 0.857826 | identical (bundle paths /metrics, /validation, /roc, /calibration, /importance, /threshold_table, /tier_summary) | PASS |
| Confusion matrix | [[30, 8], [1, 53]] | [[30, 8], [1, 53]] | PASS |
| Customer predictions (segment, reorder, probability) | 5,179 profiles × 2 earlier app versions | 10,358 per-profile comparisons · 0 differences | PASS |
| Recommendations & risk tiers | items per segment and tier per profile | identical for every profile | PASS |
| What-If outputs | scenario library, tornado, 6 interactive templates | identical | PASS |
| Financial calculations | ROI defaults, ROI curve, segment economics | identical | PASS |
| Revenue concentration | Gini 0.180593 | Gini 0.180593 (chart renamed: M3) | PASS |
| Chart numbers, names, text, hover, titles, axes, annotations | 184 charts · 363 traces · 681 layout text fields | 306 differences, M1 × 1, M2 × 3, M3 × 2, P1 × 296, R1 × 4 | PASS |
| Tables | 58 tables · 8,993 cells | 38 row/schema differences, DQ01 × 1, DQ05 × 1, M1 × 5, M2 × 2, R1 × 9, T2 × 20 | PASS |
| Model-selection table (M1 whitelist content test) | test columns for every candidate (received) | recomputed training-fold CV matches the table: True; no test columns: True; rule picks Logistic Regression (scaled): True | PASS |
| Since the CV-interpretation refinement (v2 submission → final) | v2 submission | 138 differences, DQ01 × 2, DQ05 × 2, M1 × 1, M2 × 29, P1 × 4, T1 × 4, T2 × 26, TS × 70 | PASS |
| Since the final polish began (micro-refinement submission → final) | micro-refinement submission | 112 differences, DQ01 × 2, DQ05 × 2, T1 × 4, T2 × 26, TS × 78 | PASS |
| Since the range-terminology correction began (final-polish submission → final) | final-polish submission | 110 differences, DQ01 × 2, DQ05 × 2, T2 × 26, TS × 80 | PASS |
| Since the DQ-01 / DQ-05 correction began (range-correction submission → final) | range-correction submission | 90 differences, DQ01 × 2, DQ05 × 2, TS × 86 | PASS |
| This DQ-05 quantity correction only (DQ-01 / DQ-05 submission → final) | DQ-01 / DQ-05 submission | 88 differences, DQ05 × 2, TS × 86 | PASS |
| Pre-redesign dashboard (numeric scope) | every number shown before the visual redesign | 7 differences, DQ01+DQ05 × 1, M2 × 5, T1 × 1 | PASS |
| Dashboard smoke test | — | 96 passed · 0 failed | PASS |
| Negative controls | — | 73/73 behaved as required · artifacts unchanged: True | PASS |

## Codes

| Code | Meaning |
|---|---|
| TS | Training timestamp changed (notebook re-executed; model artifact byte-identical) |
| M1 | Approved methodological reporting correction — model-selection table/chart now training-fold CV only |
| M1T | Approved methodology explanation text (selection protocol) |
| M2 | Approved repeated-CV interpretation and matched-baseline wording correction (this final refinement) |
| M3 | Approved terminology correction — Revenue Concentration Curve (not a Lorenz curve) |
| T1 | Approved terminology correction — Governance population KPI ('Analysis population': 480 → 460 adult classifier → 368 training + 92 test) and the training-range definition (final submission polish) |
| DQ01 | Approved data-quality documentation correction — DQ-01 population text (460 classifier-eligible adults = 368 training + 92 held-out test; not 'trained on 460'); corrected at the notebook source, bundle and reports regenerated |
| DQ05 | Approved data-quality documentation correction — DQ-05 wording (observed adult classifier range / observed adult reference-range warning, 460 eligible adults; values stay permitted) and Quantity '6 of 7 classifier input controls' (independently recalculated); range values unchanged |
| T2 | Approved terminology correction — 'observed adult classifier range' (display headings and wording only; the ranges, their calculation and the exported field outside_training_range are unchanged) and the final model's training count |
| R1 | Deterministic association-rule ordering (Biryani ↔ Raita listed alphabetically; values identical) |
| P1 | Presentation-only change (palette colours, shapes, textures, glyphs, wrapped/shortened labels) |
| ADD | Additional information displayed without removing substantive content |
| UNEXPECTED | Any unexplained change — FAIL |

## Content tests behind each code

* **TS** — only `meta.trained_at` / the 'Last model training' KPI, and only the digits of the old timestamp may vanish / the new one appear.
* **M1** — only `model_comparison` (bundle), the Governance selection table and the `gv_models` chart. The bundle schema must be exactly the recorded before/after column lists; shared columns (Model, CV accuracy, CV accuracy (sd), CV ROC-AUC, Interpretable) must be identical; in the Governance table every cell of a changed row must equal the string formatted from an independent recomputation of training-fold CV (including the full 'mean% ± sd%' CV-accuracy cell), and Model, Interpretable, CV ROC-AUC and the CV-accuracy mean must be unchanged; exactly one row is marked selected, and it is the model the rule picks. The chart's baseline label is an exact before/after entry.
* **R1** — a row may differ only by Biryani and Raita trading places inside one rule (afterwards Biryani → Raita); every support, confidence, lift, tier and hover value must be equal.
* **M2 / M3 / M1T / P1 (labels)** — exact before/after strings per chart, field, trace or table row (`approved_differences.json`); KPI renames require the same value on the same page.
* **T1** — the Governance KPI rename is one exact entry: old label, value and context → new label, value and context (`kpi_renames`); the value may only lose its unit word ('480 diners' → '480': the number itself must be identical); the numbers newly shown on the Governance page are an exact reviewed list (368, 368, 460, 480, 92, 92 added; 1,980 baskets dropped from the card). The smoke test recounts 480 / 460 / 368 / 92 independently from the cleaned data and the split.
* **P1 (styling)** — only colour / symbol / pattern / opacity / width / dash values may change, and every colour used afterwards must be a palette token or an alpha variant of one. Marker size (which encodes data in the rule map and priority matrix) is not allowed to change.
* **T2** — a column heading change is accepted only as an approved relabel (`column_relabels`: exact old → new heading, same column count and order) with every cell value identical under the new heading; DQ-05's displayed wording is one exact before/after table-row entry; the looked-up diner's note may add exactly 368 and 460. The ranges themselves are checked by smoke tests A and C, and the export by D/E (byte-identical to the previous submission).
* **DQ01 / DQ05** — only the DQ-01 and DQ-05 rows of `dq.issue_log` (bundle) and of the Governance issue-log table, each an exact before/after entry whose 'after' must equal the row in `reports/data_quality_issue_log.csv` (asserted when the whitelist is built); in the numeric-scope comparison the issue-log table may gain exactly the numbers those rows add. Content and cross-document rules: `dq_consistency.py`.
* **Numbers in text** — per page, the exact multiset of numbers allowed to appear or disappear is listed; anything else fails. When two approved changes touch the same page, the builder asserts that their combined lists equal the observation exactly.

## received vs final

Scope: strict. Baseline: capture_v1_received.json, bundle_v1_received.json.gz (app MD5 `b941e52fe17e`).

Compared 42 page/state snapshots: 154 KPI cards, 184 charts with 363 traces and 681 layout-text fields, 58 tables (8,993 cells), 2,068 numbers in text, 17,651 bundle values, 10,358 predictions.

By class: DQ01 × 2, DQ05 × 2, M1 × 7, M2 × 29, M3 × 2, P1 × 299, R1 × 18, T1 × 3, T1+M1T × 1, T2 × 26, TS × 70.

| Where | What differs | Class | Rule | Before | After |
|---|---|---|---|---|---|
| /dq/issue_log | /dq/issue_log: row 0 (0) | DQ01 | dq01-bundle-row | {"ID": "DQ-01", "Dataset": "diners", "Issue": "Age below plausible account-holder age", "Quantity": "1 diner ( | {"ID": "DQ-01", "Dataset": "diners", "Issue": "Age below plausible account-holder age", "Quantity": "1 diner ( |
| /dq/issue_log | /dq/issue_log: row 4 (4) | DQ05 | dq05-bundle-row | {"ID": "DQ-05", "Dataset": "diners", "Issue": "Dashboard input ranges exceed training ranges (e.g. recency ≤60 | {"ID": "DQ-05", "Dataset": "diners", "Issue": "Dashboard inputs may fall outside the observed adult classifier |
| /meta/train_majority_share | /meta/train_majority_share | M2 | training-set majority baseline | null | 0.5842391304347826 |
| /meta/trained_at | /meta/trained_at | TS | trained_at | 06 Oct 2026, 18:48 | 05 Nov 2026, 21:56 |
| /model_comparison | /model_comparison: columns changed | M1 | bundle schema | ["Model", "CV accuracy", "CV accuracy (sd)", "CV ROC-AUC", "Test accuracy", "Test ROC-AUC", "Test Brier (lower | ["Model", "CV accuracy", "CV accuracy (sd)", "CV precision (reorder)", "CV recall (reorder)", "CV F1 (reorder) |
| /risk_tiers[1][3] | /risk_tiers[1][3] | P1 | nb-tier-colour | #6FAF9F | #5B6B82 |
| /rules_all | /rules_all: row 16 (16) | R1 | bundle rule row | {"antecedent": "Raita", "consequent": "Biryani", "support": 0.06161616161616162, "confidence": 0.8970588235294 | {"antecedent": "Biryani", "consequent": "Raita", "support": 0.06161616161616162, "confidence": 0.8970588235294 |
| /rules_all | /rules_all: row 17 (17) | R1 | bundle rule row | {"antecedent": "Biryani", "consequent": "Raita", "support": 0.06161616161616162, "confidence": 0.8970588235294 | {"antecedent": "Raita", "consequent": "Biryani", "support": 0.06161616161616162, "confidence": 0.8970588235294 |
| /seg_colors/Budget Students | /seg_colors/Budget Students | P1 | nb-seg-colour-bs | #3E7CB1 | #4DA8DA |
| /seg_colors/Family Feasters | /seg_colors/Family Feasters | P1 | nb-seg-colour-ff | #7E6BB8 | #3A66E8 |
| /seg_rules/Family Feasters | /seg_rules/Family Feasters: row 9 (32) | R1 | bundle rule row | {"antecedent": "Raita", "consequent": "Biryani", "support": 0.40131578947368424, "confidence": 0.8970588235294 | {"antecedent": "Biryani", "consequent": "Raita", "support": 0.40131578947368424, "confidence": 0.8970588235294 |
| /strategic_overall | /strategic_overall: row 1 (16) | R1 | bundle rule row | {"antecedent": "Raita", "consequent": "Biryani", "support": 0.06161616161616162, "confidence": 0.8970588235294 | {"antecedent": "Biryani", "consequent": "Raita", "support": 0.06161616161616162, "confidence": 0.8970588235294 |
| /takeaway | /takeaway | M2 | takeaway | **1. Prioritise Premium Foodies.** They are 27% of diners but 36% of estimated monthly revenue (AED 872 per di | **1. Prioritise Premium Foodies.** They are 27% of diners but 36% of estimated monthly revenue (AED 872 per di |
| /top_overall | /top_overall: row 7 (16) | R1 | bundle rule row | {"antecedent": "Raita", "consequent": "Biryani", "support": 0.06161616161616162, "confidence": 0.8970588235294 | {"antecedent": "Biryani", "consequent": "Raita", "support": 0.06161616161616162, "confidence": 0.8970588235294 |
| Governance & Data Quality | KPI 'Analysis population' newly shown | T1 | kpi-governance-population | null | ["Analysis population", "480", "480 diners · 460 adult classifier population · 368 training observations · 92  |
| Retention & Churn (+2 states) | KPI 'Expected accuracy' no longer shown | M2 | kpi-retention-rename | ["Expected accuracy", "85.8%", "Repeated 5-fold CV (50 fits) ± 3.0% · baseline 58.5%"] | null |
| Governance & Data Quality | KPI 'Last model training' value changed | TS | kpi | 06 Oct 2026, 18:48 | 05 Nov 2026, 21:56 |
| Executive Overview | KPI 'Model accuracy' no longer shown | M2 | kpi-overview-rename | ["Model accuracy", "85.8%", "Repeated CV ± 3.0% · baseline 58.5% · AUC 0.94"] | null |
| Retention & Churn (+2 states) | KPI 'ROC-AUC' context changed | M2 | kpi-rocauc-context | CV mean · test 0.973 (0.5 = random) | Repeated-CV mean · held-out test 0.973 (0.5 = random) |
| Executive Overview | KPI 'Repeated-CV accuracy' newly shown | M2 | kpi-overview-rename | null | ["Repeated-CV accuracy", "85.8%", "Post-selection stability check ± 3.0% · its baseline 58.5% · AUC 0.94"] |
| Retention & Churn (+2 states) | KPI 'Repeated-CV accuracy' newly shown | M2 | kpi-retention-rename | null | ["Repeated-CV accuracy", "85.8%", "Stability check, 50 fits ± 3.0% · its baseline 58.5%"] |
| Retention & Churn (+2 states) | KPI 'Test-split accuracy' context changed | M2 | kpi-test-context | 95% CI 83.7%–95.7% · +31.5 pp vs baseline | Held-out · 95% CI 83.7%–95.7% · +31.5 pp vs its 58.7% baseline |
| Governance & Data Quality | KPI 'Training data' no longer shown | T1 | kpi-governance-population | ["Training data", "480 diners", "460 in classifier · 1,980 baskets"] | null |
| batch:example file | chart 'batch_fig' · bar:'At-risk' · marker | P1 | styling | {"color": "#FFC76B"} | {"color": "#FFC76B", "pattern": {"fgcolor": "#0B1020", "fillmode": "overlay", "shape": "/", "size": 7, "solidi |
| batch:example file | chart 'batch_fig' · bar:'At-risk' · name | P1 | batch-tier-names-3 | At-risk | ▽ At-risk |
| batch:example file | chart 'batch_fig' · bar:'High churn risk' · marker | P1 | styling | {"color": "#FF7D91"} | {"color": "#FF7D91", "pattern": {"fgcolor": "#0B1020", "fillmode": "overlay", "shape": "x", "size": 7, "solidi |
| batch:example file | chart 'batch_fig' · bar:'High churn risk' · name | P1 | batch-tier-names-4 | High churn risk | ▼ High churn risk |
| batch:example file | chart 'batch_fig' · bar:'High retention likelihood' · marker | P1 | styling | {"color": "#45E3C1"} | {"color": "#45E3C1", "pattern": {"fgcolor": "#0B1020", "fillmode": "overlay", "shape": "", "size": 7, "solidit |
| batch:example file | chart 'batch_fig' · bar:'High retention likelihood' · name | P1 | batch-tier-names-1 | High retention likelihood | ▲ High retention likelihood |
| batch:example file | chart 'batch_fig' · bar:'Moderate retention likelihood' · marker | P1 | styling | {"color": "#4AA6C9"} | {"color": "#8A99B0", "pattern": {"fgcolor": "#0B1020", "fillmode": "overlay", "shape": "", "size": 7, "solidit |
| batch:example file | chart 'batch_fig' · bar:'Moderate retention likelihood' · name | P1 | batch-tier-names-2 | Moderate retention likelihood | △ Moderate retention likelihood |
| Basket Intelligence (+3 states) | chart 'bk_map' · scatter:'Low confidence' · marker | P1 | styling | {"color": "#8A99B0", "line": {"color": "#0B1020", "width": 0.5}, "opacity": 0.75, "size": {"dtype": "f8", "bda | {"color": "#8A99B0", "line": {"color": "#0B1020", "width": 0.5}, "opacity": 0.75, "size": {"dtype": "f8", "bda |
| Basket Intelligence (+3 states) | chart 'bk_map' · scatter:'Low support — test only' · marker | P1 | styling | {"color": "#FFC76B", "line": {"color": "#0B1020", "width": 0.5}, "opacity": 0.75, "size": {"dtype": "f8", "bda | {"color": "#FFC76B", "line": {"color": "#0B1020", "width": 0.5}, "opacity": 0.75, "size": {"dtype": "f8", "bda |
| Basket Intelligence (+3 states) | chart 'bk_map' · scatter:'No real association (lift ≈ 1)' · marker | P1 | styling | {"color": "#FF7D91", "line": {"color": "#0B1020", "width": 0.5}, "opacity": 0.75, "size": {"dtype": "f8", "bda | {"color": "#FF7D91", "line": {"color": "#0B1020", "width": 0.5}, "opacity": 0.75, "size": {"dtype": "f8", "bda |
| Basket Intelligence (+3 states) | chart 'bk_map' · scatter:'Strategic' · customdata | R1 | rule-map hover | [["Green Tea", "Miso Soup + Sushi", 13.83361366282831, "Lift 13.83 means the pair occurs together about 13.83× | [["Green Tea", "Miso Soup + Sushi", 13.83361366282831, "Lift 13.83 means the pair occurs together about 13.83× |
| Basket Intelligence (+3 states) | chart 'bk_map' · scatter:'Strategic' · marker | P1 | styling | {"color": "#45E3C1", "line": {"color": "#0B1020", "width": 0.5}, "opacity": 0.75, "size": {"dtype": "f8", "bda | {"color": "#45E3C1", "line": {"color": "#0B1020", "width": 0.5}, "opacity": 0.75, "size": {"dtype": "f8", "bda |
| Basket Intelligence (+3 states) | chart 'bk_opp_bar' · bar:None · marker | P1 | styling | {"color": ["#A5E4FF", "#5B84FF", "#D98CF2", "#D98CF2", "#5B84FF"]} | {"color": ["#A5E4FF", "#5B84FF", "#FFC76B", "#FFC76B", "#5B84FF"]} |
| Basket Intelligence (+1 states) | chart 'bk_pen' · bar:None · marker | P1 | styling | {"color": "#D98CF2"} | {"color": "#FFC76B"} |
| Retention Economics (+3 states) | chart 'ec_curve' · scatter:'Campaign cost' · line | P1 | styling | {"color": "#FF7D91"} | {"color": "#FF7D91", "dash": "dash"} |
| Retention Economics (+3 states) | chart 'ec_curve' · scatter:'Campaign cost' · marker | P1 | styling | null | {"symbol": "square"} |
| Retention Economics (+3 states) | chart 'ec_curve' · scatter:'Expected margin recovered' · marker | P1 | styling | null | {"symbol": "circle"} |
| Retention Economics (+3 states) | chart 'ec_curve' · scatter:'Net value (margin − cost)' · line | P1 | styling | {"color": "#8EA6FF", "width": 3} | {"color": "#5B84FF", "width": 3} |
| Retention Economics (+3 states) | chart 'ec_curve' · scatter:'Net value (margin − cost)' · marker | P1 | styling | null | {"symbol": "diamond"} |
| Retention Economics (+1 states) | chart 'ec_seg' · bar:None · marker | P1 | styling | {"color": ["#D98CF2", "#5B84FF"]} | {"color": ["#FFC76B", "#5B84FF"]} |
| Retention Economics (+3 states) | chart 'ec_sens' · scatter:'Expected-value ranking' · line | P1 | styling | {"color": "#8EA6FF", "width": 3} | {"color": "#5B84FF", "width": 3} |
| Retention Economics (+3 states) | chart 'ec_sens' · scatter:'Expected-value ranking' · marker | P1 | styling | null | {"symbol": "diamond"} |
| Retention Economics (+3 states) | chart 'ec_sens' · scatter:'Offer to every diner with P < 50%' · line | P1 | styling | {"color": "#7A8CB0"} | {"color": "#8A99B0", "dash": "dash"} |
| Retention Economics (+3 states) | chart 'ec_sens' · scatter:'Offer to every diner with P < 50%' · marker | P1 | styling | null | {"symbol": "circle"} |
| Governance & Data Quality | chart 'gv_models' · annotations | M1 | gv-baseline-line | ["majority baseline 58.7%"] | ["majority-class share (training set) 58.4%"] |
| Governance & Data Quality | chart 'gv_models' · bar:'CV ROC-AUC' · marker | P1 | styling | {"color": "#D98CF2"} | {"color": "#D98CF2", "pattern": {"fgcolor": "#0B1020", "fillmode": "overlay", "shape": "", "size": 7, "solidit |
| Governance & Data Quality | chart 'gv_models' · bar:'CV accuracy' · marker | P1 | styling | {"color": "#7A8CB0"} | {"color": "#8A99B0", "pattern": {"fgcolor": "#0B1020", "fillmode": "overlay", "shape": "/", "size": 7, "solidi |
| Governance & Data Quality | chart 'gv_models' · bar:'CV accuracy' · name | P1 | gv-hatched-name | CV accuracy | CV accuracy (hatched) |
| Governance & Data Quality | chart 'gv_u18_seg' · bar:None · marker | P1 | styling | {"color": ["#D98CF2", "#5B84FF", "#A5E4FF"]} | {"color": ["#FFC76B", "#5B84FF", "#A5E4FF"]} |
| Customer Segmentation (+7 states) | chart 'k_Inertia' · scatter:'Inertia' · line | P1 | styling | {"color": "#7A8CB0", "width": 2} | {"color": "#8A99B0", "width": 2} |
| Customer Segmentation (+7 states) | chart 'k_Inertia' · scatter:'Inertia' · marker | P1 | styling | {"color": ["#7A8CB0", "#D98CF2", "#7A8CB0", "#7A8CB0", "#7A8CB0", "#7A8CB0", "#7A8CB0"], "size": 9} | {"color": ["#8A99B0", "#D98CF2", "#8A99B0", "#8A99B0", "#8A99B0", "#8A99B0", "#8A99B0"], "size": 9} |
| Customer Segmentation (+7 states) | chart 'k_Silhouette' · scatter:'Silhouette' · line | P1 | styling | {"color": "#7A8CB0", "width": 2} | {"color": "#8A99B0", "width": 2} |
| Customer Segmentation (+7 states) | chart 'k_Silhouette' · scatter:'Silhouette' · marker | P1 | styling | {"color": ["#7A8CB0", "#D98CF2", "#7A8CB0", "#7A8CB0", "#7A8CB0", "#7A8CB0", "#7A8CB0"], "size": 9} | {"color": ["#8A99B0", "#D98CF2", "#8A99B0", "#8A99B0", "#8A99B0", "#8A99B0", "#8A99B0"], "size": 9} |
| Executive Overview | chart 'ov_conc' · bar:'Share of est. monthly revenue' · marker | P1 | styling | {"color": ["#D98CF2", "#5B84FF", "#A5E4FF"]} | {"color": ["#FFC76B", "#5B84FF", "#A5E4FF"]} |
| Executive Overview | chart 'ov_items' · bar:None · marker | P1 | styling | {"color": "#7A8CB0"} | {"color": "#8A99B0"} |
| Executive Overview | chart 'ov_lorenz' · subtitle | M3 | fix2-subtitle | null | Illustrates the cumulative share of observed diner revenue contributed by customers ranked from highest to low |
| Executive Overview | chart 'ov_lorenz' · title | M3 | fix2-title | Lorenz curve — cumulative revenue by share of diners | Revenue Concentration Curve — Highest-Spending Diners First |
| Executive Overview | chart 'ov_ret' · bar:None · marker | P1 | styling | {"color": ["#D98CF2", "#5B84FF", "#A5E4FF"]} | {"color": ["#FFC76B", "#5B84FF", "#A5E4FF"]} |
| Executive Overview | chart 'ov_tiers' · bar:'Budget Students' · marker | P1 | styling | {"color": "#A5E4FF"} | {"color": "#A5E4FF", "pattern": {"fgcolor": "#0B1020", "fillmode": "overlay", "shape": ".", "size": 6, "solidi |
| Executive Overview | chart 'ov_tiers' · bar:'Family Feasters' · marker | P1 | styling | {"color": "#5B84FF"} | {"color": "#5B84FF", "pattern": {"fgcolor": "#0B1020", "fillmode": "overlay", "shape": "", "size": 6, "solidit |
| Executive Overview | chart 'ov_tiers' · bar:'Premium Foodies' · marker | P1 | styling | {"color": "#D98CF2"} | {"color": "#FFC76B", "pattern": {"fgcolor": "#0B1020", "fillmode": "overlay", "shape": "", "size": 6, "solidit |
| Executive Overview | chart 'ov_tiers' · legend_title | P1 | tiers-legend-title | <b>Segment</b> | null |
| Executive Overview | chart 'ov_tiers' · yaxis.ticktext | P1 | tier-glyphs-overview | null | ["▼ High churn risk", "▽ At-risk", "△ Moderate retention likelihood", "▲ High retention likelihood"] |
| Executive Overview | chart 'ov_top20' · bar:None · marker | P1 | styling | {"color": ["#D98CF2", "#5B84FF", "#A5E4FF"]} | {"color": ["#FFC76B", "#5B84FF", "#A5E4FF"]} |
| Recommendations | chart 'rec_pm' · scatter:'Budget Students' · marker | P1 | styling | {"color": "#A5E4FF", "line": {"color": "#0B1020", "width": 1}, "opacity": 0.85, "size": 14} | {"color": "#A5E4FF", "line": {"color": "#0B1020", "width": 1}, "opacity": 0.85, "size": 14, "symbol": "triangl |
| Recommendations | chart 'rec_pm' · scatter:'Family Feasters' · marker | P1 | styling | {"color": "#5B84FF", "line": {"color": "#0B1020", "width": 1}, "opacity": 0.85, "size": 29.415365095536444} | {"color": "#5B84FF", "line": {"color": "#0B1020", "width": 1}, "opacity": 0.85, "size": 29.415365095536444, "s |
| Recommendations | chart 'rec_pm' · scatter:'Premium Foodies' · marker | P1 | styling | {"color": "#D98CF2", "line": {"color": "#0B1020", "width": 1}, "opacity": 0.85, "size": 66.06587060850148} | {"color": "#FFC76B", "line": {"color": "#0B1020", "width": 1}, "opacity": 0.85, "size": 66.06587060850148, "sy |
| Retention & Churn (+2 states) | chart 'rt_ci' · scatter:'Point estimate ± 95% CI' · marker | P1 | styling | {"color": "#8EA6FF", "size": 11} | {"color": "#5B84FF", "size": 11} |
| Retention & Churn (+2 states) | chart 'rt_cv' · box:'Accuracy' · marker | P1 | styling | {"color": "#7A8CB0"} | {"color": "#8A99B0"} |
| Retention & Churn (+2 states) | chart 'rt_cv' · title | M2 | rcv-chart-title | Repeated 5-fold CV — 50 out-of-sample fits | Repeated 5-fold CV — post-selection stability check (50 fits, all adults) |
| Retention & Churn (+2 states) | chart 'rt_hist' · histogram:'Actually churned' · marker | P1 | styling | {"color": "#FF7D91"} | {"color": "#FF7D91", "pattern": {"fgcolor": "#0B1020", "fillmode": "overlay", "shape": "/", "size": 7, "solidi |
| Retention & Churn (+2 states) | chart 'rt_hist' · histogram:'Actually churned' · name | P1 | hist-hatched-name | Actually churned | Actually churned (hatched) |
| Retention & Churn (+2 states) | chart 'rt_hist' · histogram:'Actually reordered' · marker | P1 | styling | {"color": "#45E3C1"} | {"color": "#45E3C1", "pattern": {"fgcolor": "#0B1020", "fillmode": "overlay", "shape": "", "size": 7, "solidit |
| Retention & Churn (+2 states) | chart 'rt_tierbar' · xaxis.ticktext | P1 | tier-glyphs-retention | null | ["▲ High retention likelihood", "△ Moderate retention likelihood", "▽ At-risk", "▼ High churn risk"] |
| Customer Segmentation (+7 states) | chart 'seg_bar_Diners' · bar:None · marker | P1 | styling | {"color": ["#D98CF2", "#5B84FF", "#A5E4FF"]} | {"color": ["#FFC76B", "#5B84FF", "#A5E4FF"]} |
| Customer Segmentation (+7 states) | chart 'seg_bar_Est. monthly spend (AED)' · bar:None · marker | P1 | styling | {"color": ["#D98CF2", "#5B84FF", "#A5E4FF"]} | {"color": ["#FFC76B", "#5B84FF", "#A5E4FF"]} |
| Customer Segmentation (+7 states) | chart 'seg_bar_Reorder rate' · bar:None · marker | P1 | styling | {"color": ["#D98CF2", "#5B84FF", "#A5E4FF"]} | {"color": ["#FFC76B", "#5B84FF", "#A5E4FF"]} |
| Customer Segmentation (+7 states) | chart 'seg_box_fig' · box:'Premium Foodies' · marker | P1 | styling | {"color": "#D98CF2"} | {"color": "#FFC76B"} |
| Customer Segmentation (+7 states) | chart 'seg_freq' · scatter:'Budget Students' · marker | P1 | styling | {"color": "#A5E4FF", "opacity": 0.58, "size": 6.5, "symbol": "circle"} | {"color": "#A5E4FF", "opacity": 0.66, "size": 7, "symbol": "triangle-up"} |
| Customer Segmentation (+7 states) | chart 'seg_freq' · scatter:'Family Feasters' · marker | P1 | styling | {"color": "#5B84FF", "opacity": 0.58, "size": 6.5, "symbol": "square"} | {"color": "#5B84FF", "opacity": 0.66, "size": 7, "symbol": "diamond"} |
| Customer Segmentation (+7 states) | chart 'seg_freq' · scatter:'Premium Foodies' · marker | P1 | styling | {"color": "#D98CF2", "opacity": 0.58, "size": 6.5, "symbol": "diamond"} | {"color": "#FFC76B", "opacity": 0.66, "size": 7, "symbol": "circle"} |
| Customer Segmentation (+7 states) | chart 'seg_freq' · scatter:None · marker | P1 | styling | {"color": "#D98CF2", "line": {"color": "#F4F7FC", "width": 1}, "size": 14, "symbol": "x"} | {"color": "#FFC76B", "line": {"color": "#F4F7FC", "width": 1}, "size": 14, "symbol": "x"} |
| Customer Segmentation (+7 states) | chart 'seg_kw' · bar:None · marker | P1 | styling | {"color": ["#7A8CB0", "#D98CF2", "#7A8CB0", "#D98CF2", "#D98CF2", "#D98CF2", "#D98CF2"]} | {"color": ["#8A99B0", "#D98CF2", "#8A99B0", "#D98CF2", "#D98CF2", "#D98CF2", "#D98CF2"]} |
| Customer Segmentation (+7 states) | chart 'seg_kw' · title | P1 | kw-title | Effect size of segment on each feature (violet = clustering feature, grey = not used) | Effect size by feature (violet = used in clustering) |
| Customer Segmentation (+7 states) | chart 'seg_pca' · scatter:'Budget Students (200)' · marker | P1 | styling | {"color": "#A5E4FF", "opacity": 0.62, "size": 6.5, "symbol": "circle"} | {"color": "#A5E4FF", "opacity": 0.7, "size": 7, "symbol": "triangle-up"} |
| Customer Segmentation (+7 states) | chart 'seg_pca' · scatter:'Family Feasters (150)' · marker | P1 | styling | {"color": "#5B84FF", "opacity": 0.62, "size": 6.5, "symbol": "square"} | {"color": "#5B84FF", "opacity": 0.7, "size": 7, "symbol": "diamond"} |
| Customer Segmentation (+7 states) | chart 'seg_pca' · scatter:'Premium Foodies (130)' · marker | P1 | styling | {"color": "#D98CF2", "opacity": 0.62, "size": 6.5, "symbol": "diamond"} | {"color": "#FFC76B", "opacity": 0.7, "size": 7, "symbol": "circle"} |
| Customer Segmentation (+7 states) | chart 'seg_pca' · scatter:None · marker | P1 | styling | {"color": "#D98CF2", "line": {"color": "#F4F7FC", "width": 1}, "size": 14, "symbol": "x"} | {"color": "#FFC76B", "line": {"color": "#F4F7FC", "width": 1}, "size": 14, "symbol": "x"} |
| Customer Segmentation (+7 states) | chart 'seg_stab' · bar:None · marker | P1 | styling | {"color": ["#D98CF2", "#D98CF2", "#7A8CB0", "#7A8CB0"]} | {"color": ["#D98CF2", "#D98CF2", "#8A99B0", "#8A99B0"]} |
| What-If Simulator (+6 states) | chart 'wi_sens_fig' · scatter:'After' · marker | P1 | styling | {"color": "#D98CF2", "line": {"color": "#F4F7FC", "width": 1}, "size": 12} | {"color": "#D98CF2", "line": {"color": "#F4F7FC", "width": 1}, "size": 12, "symbol": "diamond"} |
| What-If Simulator (+6 states) | chart 'wi_sens_fig' · scatter:'Before' · marker | P1 | styling | {"color": "#A8B6CB", "line": {"color": "#F4F7FC", "width": 1}, "size": 11} | {"color": "#8A99B0", "line": {"color": "#F4F7FC", "width": 1}, "size": 11, "symbol": "circle"} |
| What-If Simulator (+6 states) | chart 'wi_sens_fig' · scatter:'P(reorder) as input varies' · line | P1 | styling | {"color": "#8EA6FF", "width": 2.5} | {"color": "#5B84FF", "width": 2.5} |
| What-If Simulator (+6 states) | chart 'wi_tornado' · bar:'Input lowered by 1 SD' · marker | P1 | styling | {"color": "#8FA6C8"} | {"color": "#8A99B0", "pattern": {"fgcolor": "#0B1020", "fillmode": "overlay", "shape": "/", "size": 7, "solidi |
| What-If Simulator (+6 states) | chart 'wi_tornado' · bar:'Input lowered by 1 SD' · name | P1 | tornado-hatched-name | Input lowered by 1 SD | Input lowered by 1 SD (hatched) |
| What-If Simulator (+6 states) | chart 'wi_tornado' · bar:'Input raised by 1 SD' · marker | P1 | styling | {"color": "#2E5C9A"} | {"color": "#5B84FF"} |
| Executive Overview | numbers newly displayed in text | TS | timestamp digits | null | ["05", "05", "21", "21", "56", "56"] |
| Customer Segmentation (+29 states) | numbers newly displayed in text | TS | timestamp digits | null | ["05", "21", "56"] |
| Retention & Churn (+2 states) | numbers newly displayed in text | M2 | retention-note | null | ["05", "21", "3.0", "368", "460", "5", "56", "58.7", "58.7", "92"] |
| Recommendations | numbers newly displayed in text | M2 | takeaway-text | null | ["0.97", "05", "21", "3.0", "56", "58.5", "58.7", "83.7", "85.8", "90.2", "92", "95", "95.7"] |
| Governance & Data Quality | numbers newly displayed in text | T1+M1T | governance-population-terms+governance-protocol-text | null | ["05", "05", "21", "21", "368", "368", "368", "460", "480", "5", "56", "56", "92", "92", "92"] |
| diner:Look up an existing diner… (+5 states) | numbers newly displayed in text | T2 | final-model-training-count | null | ["05", "21", "368", "460", "56"] |
| Executive Overview | numbers no longer displayed in text | TS | timestamp digits | ["06", "06", "18", "18", "48", "48"] | null |
| Customer Segmentation (+35 states) | numbers no longer displayed in text | TS | timestamp digits | ["06", "18", "48"] | null |
| Retention & Churn (+2 states) | numbers no longer displayed in text | M2 | retention-note | ["06", "18", "27.3", "48"] | null |
| Recommendations | numbers no longer displayed in text | M2 | takeaway-text | ["0.94", "06", "18", "48", "59", "86", "90"] | null |
| Governance & Data Quality | numbers no longer displayed in text | T1 | governance-population-terms | ["06", "06", "18", "18", "1980", "48", "48"] | null |
| batch:example file | table 1, row 1 | T2 | batch-display-range-heading (values identical) | {"diner_id": "NEW001", "status": "Scored", "segment": "Premium Foodies", "p_reorder": "71.9", "will_reorder":  | {"diner_id": "NEW001", "status": "Scored", "segment": "Premium Foodies", "p_reorder": "71.9", "will_reorder":  |
| batch:example file | table 1, row 10 | T2 | batch-display-range-heading (values identical) | {"diner_id": "D1110", "status": "Not scored — under 18 (18+ policy)", "segment": NaN, "p_reorder": NaN, "will_ | {"diner_id": "D1110", "status": "Not scored — under 18 (18+ policy)", "segment": NaN, "p_reorder": NaN, "will_ |
| batch:example file | table 1, row 11 | T2 | batch-display-range-heading (values identical) | {"diner_id": "D1102", "status": "Not scored — under 18 (18+ policy)", "segment": NaN, "p_reorder": NaN, "will_ | {"diner_id": "D1102", "status": "Not scored — under 18 (18+ policy)", "segment": NaN, "p_reorder": NaN, "will_ |
| batch:example file | table 1, row 2 | T2 | batch-display-range-heading (values identical) | {"diner_id": "D1113", "status": "Scored", "segment": "Budget Students", "p_reorder": "99.4", "will_reorder": " | {"diner_id": "D1113", "status": "Scored", "segment": "Budget Students", "p_reorder": "99.4", "will_reorder": " |
| batch:example file | table 1, row 3 | T2 | batch-display-range-heading (values identical) | {"diner_id": "D1396", "status": "Scored", "segment": "Premium Foodies", "p_reorder": "54.3", "will_reorder": " | {"diner_id": "D1396", "status": "Scored", "segment": "Premium Foodies", "p_reorder": "54.3", "will_reorder": " |
| batch:example file | table 1, row 4 | T2 | batch-display-range-heading (values identical) | {"diner_id": "D1109", "status": "Scored", "segment": "Budget Students", "p_reorder": "99.4", "will_reorder": " | {"diner_id": "D1109", "status": "Scored", "segment": "Budget Students", "p_reorder": "99.4", "will_reorder": " |
| batch:example file | table 1, row 5 | T2 | batch-display-range-heading (values identical) | {"diner_id": "D1197", "status": "Scored", "segment": "Budget Students", "p_reorder": "96.7", "will_reorder": " | {"diner_id": "D1197", "status": "Scored", "segment": "Budget Students", "p_reorder": "96.7", "will_reorder": " |
| batch:example file | table 1, row 6 | T2 | batch-display-range-heading (values identical) | {"diner_id": "D1471", "status": "Scored", "segment": "Premium Foodies", "p_reorder": "54.8", "will_reorder": " | {"diner_id": "D1471", "status": "Scored", "segment": "Premium Foodies", "p_reorder": "54.8", "will_reorder": " |
| batch:example file | table 1, row 7 | T2 | batch-display-range-heading (values identical) | {"diner_id": "D1136", "status": "Scored", "segment": "Budget Students", "p_reorder": "99.0", "will_reorder": " | {"diner_id": "D1136", "status": "Scored", "segment": "Budget Students", "p_reorder": "99.0", "will_reorder": " |
| batch:example file | table 1, row 8 | T2 | batch-display-range-heading (values identical) | {"diner_id": "D1238", "status": "Scored", "segment": "Family Feasters", "p_reorder": "25.8", "will_reorder": " | {"diner_id": "D1238", "status": "Scored", "segment": "Family Feasters", "p_reorder": "25.8", "will_reorder": " |
| batch:example file | table 1, row 9 | T2 | batch-display-range-heading (values identical) | {"diner_id": "D1057", "status": "Scored", "segment": "Budget Students", "p_reorder": "98.1", "will_reorder": " | {"diner_id": "D1057", "status": "Scored", "segment": "Budget Students", "p_reorder": "98.1", "will_reorder": " |
| batch:example file | table 1: columns changed | T2 | batch-display-range-heading (values identical) | ["diner_id", "status", "segment", "p_reorder", "will_reorder", "risk_tier", "action", "recommended_items", "ou | ["diner_id", "status", "segment", "p_reorder", "will_reorder", "risk_tier", "action", "recommended_items", "Ou |
| basket_segment:Family Feasters | table 2, row 10 | R1 | rule-table row | {"If basket has": "Raita", "→ also contains": "Biryani", "Support": "40%", "Confidence": "90%", "Lift": "2.01× | {"If basket has": "Biryani", "→ also contains": "Raita", "Support": "40%", "Confidence": "90%", "Lift": "2.01× |
| Governance & Data Quality | table 3, row 10 | M2 | model-card-stability-row | {"Item": "Robustness", "Detail": "Repeated 5-fold CV (50 fits): accuracy 85.8% ± 3.0%, AUC 0.944; cluster stab | {"Item": "Post-selection stability", "Detail": "Repeated 5-fold CV (50 fits, all adults incl. test diners; not |
| Basket Intelligence (+3 states) | table 3, row 17 | R1 | rule-table row | {"If basket has": "Raita", "→ also contains": "Biryani", "Support": "6.2%", "Confidence": "90%", "Lift": "13.0 | {"If basket has": "Biryani", "→ also contains": "Raita", "Support": "6.2%", "Confidence": "90%", "Lift": "13.0 |
| Basket Intelligence (+3 states) | table 3, row 18 | R1 | rule-table row | {"If basket has": "Biryani", "→ also contains": "Raita", "Support": "6.2%", "Confidence": "90%", "Lift": "13.0 | {"If basket has": "Raita", "→ also contains": "Biryani", "Support": "6.2%", "Confidence": "90%", "Lift": "13.0 |
| Governance & Data Quality | table 3, row 7 | M2 | model-card-test-row | {"Item": "Test performance", "Detail": "Accuracy 90.2% · ROC-AUC 0.973 · F1 0.922 · Brier 0.073"} | {"Item": "Held-out test performance (independent)", "Detail": "Accuracy 90.2% · ROC-AUC 0.973 · F1 0.922 · Bri |
| Governance & Data Quality | table 4, row 1 | T2 | feature-contract-range-heading (values identical) | {"Feature": "orders_per_month", "Business meaning": "Orders per month", "Clustering (5)": "✓", "Classifier (7) | {"Feature": "orders_per_month", "Business meaning": "Orders per month", "Clustering (5)": "✓", "Classifier (7) |
| Governance & Data Quality | table 4, row 2 | T2 | feature-contract-range-heading (values identical) | {"Feature": "avg_order_value", "Business meaning": "Avg order value (AED)", "Clustering (5)": "✓", "Classifier | {"Feature": "avg_order_value", "Business meaning": "Avg order value (AED)", "Clustering (5)": "✓", "Classifier |
| Governance & Data Quality | table 4, row 3 | T2 | feature-contract-range-heading (values identical) | {"Feature": "avg_items_per_order", "Business meaning": "Avg items per order", "Clustering (5)": "✓", "Classifi | {"Feature": "avg_items_per_order", "Business meaning": "Avg items per order", "Clustering (5)": "✓", "Classifi |
| Governance & Data Quality | table 4, row 4 | T2 | feature-contract-range-heading (values identical) | {"Feature": "days_since_last_order", "Business meaning": "Days since last order", "Clustering (5)": "✓", "Clas | {"Feature": "days_since_last_order", "Business meaning": "Days since last order", "Clustering (5)": "✓", "Clas |
| Governance & Data Quality | table 4, row 5 | T2 | feature-contract-range-heading (values identical) | {"Feature": "discount_rate", "Business meaning": "Discount usage rate", "Clustering (5)": "✓", "Classifier (7) | {"Feature": "discount_rate", "Business meaning": "Discount usage rate", "Clustering (5)": "✓", "Classifier (7) |
| Governance & Data Quality | table 4, row 6 | T2 | feature-contract-range-heading (values identical) | {"Feature": "age", "Business meaning": "Age (years)", "Clustering (5)": "", "Classifier (7)": "✓", "Training r | {"Feature": "age", "Business meaning": "Age (years)", "Clustering (5)": "", "Classifier (7)": "✓", "Observed a |
| Governance & Data Quality | table 4, row 7 | T2 | feature-contract-range-heading (values identical) | {"Feature": "total_spend", "Business meaning": "Total spend (AED)", "Clustering (5)": "", "Classifier (7)": "✓ | {"Feature": "total_spend", "Business meaning": "Total spend (AED)", "Clustering (5)": "", "Classifier (7)": "✓ |
| Governance & Data Quality | table 4: columns changed | T2 | feature-contract-range-heading (values identical) | ["Feature", "Business meaning", "Clustering (5)", "Classifier (7)", "Training range", "Dashboard input range"] | ["Feature", "Business meaning", "Clustering (5)", "Classifier (7)", "Observed adult classifier range", "Dashbo |
| Governance & Data Quality | table 5, row 1 | M1 | governance table row (every cell = independent recomputation; shared values unchanged) | {"Model": "Logistic Regression (scaled)", "CV accuracy": "84.8%", "CV ROC-AUC": "0.934", "Test accuracy": "90. | {"Model": "Logistic Regression (scaled)", "Selected": "✓ selected", "CV accuracy": "84.8% ± 2.9%", "CV precisi |
| Governance & Data Quality | table 5, row 2 | M1 | governance table row (every cell = independent recomputation; shared values unchanged) | {"Model": "Random Forest (300 trees)", "CV accuracy": "82.9%", "CV ROC-AUC": "0.929", "Test accuracy": "87.0%" | {"Model": "Random Forest (300 trees)", "Selected": "", "CV accuracy": "82.9% ± 2.6%", "CV precision": "0.871", |
| Governance & Data Quality | table 5, row 3 | M1 | governance table row (every cell = independent recomputation; shared values unchanged) | {"Model": "Gradient Boosting", "CV accuracy": "82.1%", "CV ROC-AUC": "0.913", "Test accuracy": "79.3%", "Test  | {"Model": "Gradient Boosting", "Selected": "", "CV accuracy": "82.1% ± 2.0%", "CV precision": "0.845", "CV rec |
| Governance & Data Quality | table 5, row 4 | M1 | governance table row (every cell = independent recomputation; shared values unchanged) | {"Model": "Decision Tree (depth 4)", "CV accuracy": "81.5%", "CV ROC-AUC": "0.862", "Test accuracy": "79.3%",  | {"Model": "Decision Tree (depth 4)", "Selected": "", "CV accuracy": "81.5% ± 3.5%", "CV precision": "0.850", " |
| Governance & Data Quality | table 5: columns changed | M1 | governance table schema | ["Model", "CV accuracy", "CV ROC-AUC", "Test accuracy", "Test ROC-AUC", "Test Brier ↓", "Interpretable"] | ["Model", "Selected", "CV accuracy", "CV precision", "CV recall", "CV F1", "CV ROC-AUC ↑", "CV Brier ↓", "Inte |
| Governance & Data Quality | table 9, row 1 | DQ01 | dq01-governance-row | {"ID": "DQ-01", "Dataset": "diners", "Issue": "Age below plausible account-holder age", "Quantity": "1 diner ( | {"ID": "DQ-01", "Dataset": "diners", "Issue": "Age below plausible account-holder age", "Quantity": "1 diner ( |
| Governance & Data Quality | table 9, row 5 | DQ05 | dq05-governance-row | {"ID": "DQ-05", "Dataset": "diners", "Issue": "Dashboard input ranges exceed training ranges (e.g. recency ≤60 | {"ID": "DQ-05", "Dataset": "diners", "Issue": "Dashboard inputs may fall outside the observed adult classifier |

## previous refinement vs final

Scope: strict. Baseline: capture_v2_previous_refinement.json, bundle_v2_previous_refinement.json.gz (app MD5 `40910923259b`).

Compared 42 page/state snapshots: 154 KPI cards, 184 charts with 363 traces and 685 layout-text fields, 58 tables (9,001 cells), 2,071 numbers in text, 17,656 bundle values, 0 predictions.

By class: DQ01 × 2, DQ05 × 2, M1 × 1, M2 × 29, P1 × 4, T1 × 4, T2 × 26, TS × 70.

| Where | What differs | Class | Rule | Before | After |
|---|---|---|---|---|---|
| /dq/issue_log | /dq/issue_log: row 0 (0) | DQ01 | dq01-bundle-row | {"ID": "DQ-01", "Dataset": "diners", "Issue": "Age below plausible account-holder age", "Quantity": "1 diner ( | {"ID": "DQ-01", "Dataset": "diners", "Issue": "Age below plausible account-holder age", "Quantity": "1 diner ( |
| /dq/issue_log | /dq/issue_log: row 4 (4) | DQ05 | dq05-bundle-row | {"ID": "DQ-05", "Dataset": "diners", "Issue": "Dashboard input ranges exceed training ranges (e.g. recency ≤60 | {"ID": "DQ-05", "Dataset": "diners", "Issue": "Dashboard inputs may fall outside the observed adult classifier |
| /meta/train_majority_share | /meta/train_majority_share | M2 | training-set majority baseline | null | 0.5842391304347826 |
| /meta/trained_at | /meta/trained_at | TS | trained_at | 31 Oct 2026, 18:51 | 05 Nov 2026, 21:56 |
| /takeaway | /takeaway | M2 | takeaway | **1. Prioritise Premium Foodies.** They are 27% of diners but 36% of estimated monthly revenue (AED 872 per di | **1. Prioritise Premium Foodies.** They are 27% of diners but 36% of estimated monthly revenue (AED 872 per di |
| Governance & Data Quality | KPI 'Analysis population' newly shown | T1 | kpi-governance-population | null | ["Analysis population", "480", "480 diners · 460 adult classifier population · 368 training observations · 92  |
| Retention & Churn (+2 states) | KPI 'Expected accuracy' no longer shown | M2 | kpi-retention-rename | ["Expected accuracy", "85.8%", "Repeated 5-fold CV (50 fits) ± 3.0% · baseline 58.5%"] | null |
| Governance & Data Quality | KPI 'Last model training' value changed | TS | kpi | 31 Oct 2026, 18:51 | 05 Nov 2026, 21:56 |
| Executive Overview | KPI 'Model accuracy' no longer shown | M2 | kpi-overview-rename | ["Model accuracy", "85.8%", "Repeated CV ± 3.0% · baseline 58.5% · AUC 0.94"] | null |
| Retention & Churn (+2 states) | KPI 'ROC-AUC' context changed | M2 | kpi-rocauc-context | CV mean · test 0.973 (0.5 = random) | Repeated-CV mean · held-out test 0.973 (0.5 = random) |
| Executive Overview | KPI 'Repeated-CV accuracy' newly shown | M2 | kpi-overview-rename | null | ["Repeated-CV accuracy", "85.8%", "Post-selection stability check ± 3.0% · its baseline 58.5% · AUC 0.94"] |
| Retention & Churn (+2 states) | KPI 'Repeated-CV accuracy' newly shown | M2 | kpi-retention-rename | null | ["Repeated-CV accuracy", "85.8%", "Stability check, 50 fits ± 3.0% · its baseline 58.5%"] |
| Retention & Churn (+2 states) | KPI 'Test-split accuracy' context changed | M2 | kpi-test-context | 95% CI 83.7%–95.7% · +31.5 pp vs baseline | Held-out · 95% CI 83.7%–95.7% · +31.5 pp vs its 58.7% baseline |
| Governance & Data Quality | KPI 'Training data' no longer shown | T1 | kpi-governance-population | ["Training data", "480 diners", "460 in classifier · 1,980 baskets"] | null |
| Governance & Data Quality | chart 'gv_models' · annotations | M1 | gv-baseline-line | ["majority-class share (adult diners) 58.5%"] | ["majority-class share (training set) 58.4%"] |
| Executive Overview | chart 'ov_tiers' · title | P1 | wrap-hyphen-fix-tiers | Risk-tier composition by segment (460 adult diners, out- of-fold) | Risk-tier composition by segment (460 adult diners, out-of-fold) |
| Retention & Churn (+2 states) | chart 'rt_cv' · title | M2 | rcv-chart-title | Repeated 5-fold CV — 50 out-of-sample fits | Repeated 5-fold CV — post-selection stability check (50 fits, all adults) |
| Retention & Churn (+2 states) | chart 'rt_hist' · title | P1 | wrap-hyphen-fix-hist | Predicted P(reorder) by actual outcome (dotted = tier cut- offs 25/50/75%) | Predicted P(reorder) by actual outcome (dotted = tier cut-offs 25/50/75%) |
| Executive Overview | numbers newly displayed in text | TS | timestamp digits | null | ["05", "05", "21", "21", "56", "56"] |
| Customer Segmentation (+29 states) | numbers newly displayed in text | TS | timestamp digits | null | ["05", "21", "56"] |
| Retention & Churn (+2 states) | numbers newly displayed in text | M2 | retention-note | null | ["05", "21", "3.0", "368", "460", "5", "56", "58.7", "58.7", "92"] |
| Recommendations | numbers newly displayed in text | M2 | takeaway-text | null | ["0.97", "05", "21", "3.0", "56", "58.5", "58.7", "83.7", "85.8", "90.2", "92", "95", "95.7"] |
| Governance & Data Quality | numbers newly displayed in text | T1 | governance-population-terms | null | ["05", "05", "21", "21", "368", "368", "460", "480", "56", "56", "92", "92"] |
| diner:Look up an existing diner… (+5 states) | numbers newly displayed in text | T2 | final-model-training-count | null | ["05", "21", "368", "460", "56"] |
| Executive Overview | numbers no longer displayed in text | TS | timestamp digits | ["18", "18", "31", "31", "51", "51"] | null |
| Customer Segmentation (+35 states) | numbers no longer displayed in text | TS | timestamp digits | ["18", "31", "51"] | null |
| Retention & Churn (+2 states) | numbers no longer displayed in text | M2 | retention-note | ["18", "27.3", "31", "51"] | null |
| Recommendations | numbers no longer displayed in text | M2 | takeaway-text | ["0.94", "18", "31", "51", "59", "86", "90"] | null |
| Governance & Data Quality | numbers no longer displayed in text | T1 | governance-population-terms | ["18", "18", "1980", "31", "31", "51", "51"] | null |
| batch:example file | table 1, row 1 | T2 | batch-display-range-heading (values identical) | {"diner_id": "NEW001", "status": "Scored", "segment": "Premium Foodies", "p_reorder": "71.9", "will_reorder":  | {"diner_id": "NEW001", "status": "Scored", "segment": "Premium Foodies", "p_reorder": "71.9", "will_reorder":  |
| batch:example file | table 1, row 10 | T2 | batch-display-range-heading (values identical) | {"diner_id": "D1110", "status": "Not scored — under 18 (18+ policy)", "segment": NaN, "p_reorder": NaN, "will_ | {"diner_id": "D1110", "status": "Not scored — under 18 (18+ policy)", "segment": NaN, "p_reorder": NaN, "will_ |
| batch:example file | table 1, row 11 | T2 | batch-display-range-heading (values identical) | {"diner_id": "D1102", "status": "Not scored — under 18 (18+ policy)", "segment": NaN, "p_reorder": NaN, "will_ | {"diner_id": "D1102", "status": "Not scored — under 18 (18+ policy)", "segment": NaN, "p_reorder": NaN, "will_ |
| batch:example file | table 1, row 2 | T2 | batch-display-range-heading (values identical) | {"diner_id": "D1113", "status": "Scored", "segment": "Budget Students", "p_reorder": "99.4", "will_reorder": " | {"diner_id": "D1113", "status": "Scored", "segment": "Budget Students", "p_reorder": "99.4", "will_reorder": " |
| batch:example file | table 1, row 3 | T2 | batch-display-range-heading (values identical) | {"diner_id": "D1396", "status": "Scored", "segment": "Premium Foodies", "p_reorder": "54.3", "will_reorder": " | {"diner_id": "D1396", "status": "Scored", "segment": "Premium Foodies", "p_reorder": "54.3", "will_reorder": " |
| batch:example file | table 1, row 4 | T2 | batch-display-range-heading (values identical) | {"diner_id": "D1109", "status": "Scored", "segment": "Budget Students", "p_reorder": "99.4", "will_reorder": " | {"diner_id": "D1109", "status": "Scored", "segment": "Budget Students", "p_reorder": "99.4", "will_reorder": " |
| batch:example file | table 1, row 5 | T2 | batch-display-range-heading (values identical) | {"diner_id": "D1197", "status": "Scored", "segment": "Budget Students", "p_reorder": "96.7", "will_reorder": " | {"diner_id": "D1197", "status": "Scored", "segment": "Budget Students", "p_reorder": "96.7", "will_reorder": " |
| batch:example file | table 1, row 6 | T2 | batch-display-range-heading (values identical) | {"diner_id": "D1471", "status": "Scored", "segment": "Premium Foodies", "p_reorder": "54.8", "will_reorder": " | {"diner_id": "D1471", "status": "Scored", "segment": "Premium Foodies", "p_reorder": "54.8", "will_reorder": " |
| batch:example file | table 1, row 7 | T2 | batch-display-range-heading (values identical) | {"diner_id": "D1136", "status": "Scored", "segment": "Budget Students", "p_reorder": "99.0", "will_reorder": " | {"diner_id": "D1136", "status": "Scored", "segment": "Budget Students", "p_reorder": "99.0", "will_reorder": " |
| batch:example file | table 1, row 8 | T2 | batch-display-range-heading (values identical) | {"diner_id": "D1238", "status": "Scored", "segment": "Family Feasters", "p_reorder": "25.8", "will_reorder": " | {"diner_id": "D1238", "status": "Scored", "segment": "Family Feasters", "p_reorder": "25.8", "will_reorder": " |
| batch:example file | table 1, row 9 | T2 | batch-display-range-heading (values identical) | {"diner_id": "D1057", "status": "Scored", "segment": "Budget Students", "p_reorder": "98.1", "will_reorder": " | {"diner_id": "D1057", "status": "Scored", "segment": "Budget Students", "p_reorder": "98.1", "will_reorder": " |
| batch:example file | table 1: columns changed | T2 | batch-display-range-heading (values identical) | ["diner_id", "status", "segment", "p_reorder", "will_reorder", "risk_tier", "action", "recommended_items", "ou | ["diner_id", "status", "segment", "p_reorder", "will_reorder", "risk_tier", "action", "recommended_items", "Ou |
| Governance & Data Quality | table 3, row 10 | M2 | model-card-stability-row | {"Item": "Robustness", "Detail": "Repeated 5-fold CV (50 fits): accuracy 85.8% ± 3.0%, AUC 0.944; cluster stab | {"Item": "Post-selection stability", "Detail": "Repeated 5-fold CV (50 fits, all adults incl. test diners; not |
| Governance & Data Quality | table 3, row 7 | M2 | model-card-test-row | {"Item": "Test performance", "Detail": "Accuracy 90.2% · ROC-AUC 0.973 · F1 0.922 · Brier 0.073"} | {"Item": "Held-out test performance (independent)", "Detail": "Accuracy 90.2% · ROC-AUC 0.973 · F1 0.922 · Bri |
| Governance & Data Quality | table 4, row 1 | T2 | feature-contract-range-heading (values identical) | {"Feature": "orders_per_month", "Business meaning": "Orders per month", "Clustering (5)": "✓", "Classifier (7) | {"Feature": "orders_per_month", "Business meaning": "Orders per month", "Clustering (5)": "✓", "Classifier (7) |
| Governance & Data Quality | table 4, row 2 | T2 | feature-contract-range-heading (values identical) | {"Feature": "avg_order_value", "Business meaning": "Avg order value (AED)", "Clustering (5)": "✓", "Classifier | {"Feature": "avg_order_value", "Business meaning": "Avg order value (AED)", "Clustering (5)": "✓", "Classifier |
| Governance & Data Quality | table 4, row 3 | T2 | feature-contract-range-heading (values identical) | {"Feature": "avg_items_per_order", "Business meaning": "Avg items per order", "Clustering (5)": "✓", "Classifi | {"Feature": "avg_items_per_order", "Business meaning": "Avg items per order", "Clustering (5)": "✓", "Classifi |
| Governance & Data Quality | table 4, row 4 | T2 | feature-contract-range-heading (values identical) | {"Feature": "days_since_last_order", "Business meaning": "Days since last order", "Clustering (5)": "✓", "Clas | {"Feature": "days_since_last_order", "Business meaning": "Days since last order", "Clustering (5)": "✓", "Clas |
| Governance & Data Quality | table 4, row 5 | T2 | feature-contract-range-heading (values identical) | {"Feature": "discount_rate", "Business meaning": "Discount usage rate", "Clustering (5)": "✓", "Classifier (7) | {"Feature": "discount_rate", "Business meaning": "Discount usage rate", "Clustering (5)": "✓", "Classifier (7) |
| Governance & Data Quality | table 4, row 6 | T2 | feature-contract-range-heading (values identical) | {"Feature": "age", "Business meaning": "Age (years)", "Clustering (5)": "", "Classifier (7)": "✓", "Training r | {"Feature": "age", "Business meaning": "Age (years)", "Clustering (5)": "", "Classifier (7)": "✓", "Observed a |
| Governance & Data Quality | table 4, row 7 | T2 | feature-contract-range-heading (values identical) | {"Feature": "total_spend", "Business meaning": "Total spend (AED)", "Clustering (5)": "", "Classifier (7)": "✓ | {"Feature": "total_spend", "Business meaning": "Total spend (AED)", "Clustering (5)": "", "Classifier (7)": "✓ |
| Governance & Data Quality | table 4: columns changed | T2 | feature-contract-range-heading (values identical) | ["Feature", "Business meaning", "Clustering (5)", "Classifier (7)", "Training range", "Dashboard input range"] | ["Feature", "Business meaning", "Clustering (5)", "Classifier (7)", "Observed adult classifier range", "Dashbo |
| Governance & Data Quality | table 9, row 1 | DQ01 | dq01-governance-row | {"ID": "DQ-01", "Dataset": "diners", "Issue": "Age below plausible account-holder age", "Quantity": "1 diner ( | {"ID": "DQ-01", "Dataset": "diners", "Issue": "Age below plausible account-holder age", "Quantity": "1 diner ( |
| Governance & Data Quality | table 9, row 5 | DQ05 | dq05-governance-row | {"ID": "DQ-05", "Dataset": "diners", "Issue": "Dashboard input ranges exceed training ranges (e.g. recency ≤60 | {"ID": "DQ-05", "Dataset": "diners", "Issue": "Dashboard inputs may fall outside the observed adult classifier |

## micro refinement vs final

Scope: strict. Baseline: capture_v3_micro_refinement.json, bundle_v3_micro_refinement.json.gz (app MD5 `cb5fb20f7ff0`).

Compared 42 page/state snapshots: 154 KPI cards, 184 charts with 363 traces and 685 layout-text fields, 58 tables (9,001 cells), 2,095 numbers in text, 17,657 bundle values, 0 predictions.

By class: DQ01 × 2, DQ05 × 2, T1 × 4, T2 × 26, TS × 78.

| Where | What differs | Class | Rule | Before | After |
|---|---|---|---|---|---|
| /dq/issue_log | /dq/issue_log: row 0 (0) | DQ01 | dq01-bundle-row | {"ID": "DQ-01", "Dataset": "diners", "Issue": "Age below plausible account-holder age", "Quantity": "1 diner ( | {"ID": "DQ-01", "Dataset": "diners", "Issue": "Age below plausible account-holder age", "Quantity": "1 diner ( |
| /dq/issue_log | /dq/issue_log: row 4 (4) | DQ05 | dq05-bundle-row | {"ID": "DQ-05", "Dataset": "diners", "Issue": "Dashboard input ranges exceed training ranges (e.g. recency ≤60 | {"ID": "DQ-05", "Dataset": "diners", "Issue": "Dashboard inputs may fall outside the observed adult classifier |
| /meta/trained_at | /meta/trained_at | TS | trained_at | 31 Oct 2026, 20:06 | 05 Nov 2026, 21:56 |
| Governance & Data Quality | KPI 'Analysis population' newly shown | T1 | kpi-governance-population | null | ["Analysis population", "480", "480 diners · 460 adult classifier population · 368 training observations · 92  |
| Governance & Data Quality | KPI 'Last model training' value changed | TS | kpi | 31 Oct 2026, 20:06 | 05 Nov 2026, 21:56 |
| Governance & Data Quality | KPI 'Training data' no longer shown | T1 | kpi-governance-population | ["Training data", "480 diners", "460 in classifier · 1,980 baskets"] | null |
| Executive Overview | numbers newly displayed in text | TS | timestamp digits | null | ["05", "05", "21", "21", "56", "56"] |
| Customer Segmentation (+33 states) | numbers newly displayed in text | TS | timestamp digits | null | ["05", "21", "56"] |
| Governance & Data Quality | numbers newly displayed in text | T1 | governance-population-terms | null | ["05", "05", "21", "21", "368", "368", "460", "480", "56", "56", "92", "92"] |
| diner:Look up an existing diner… (+5 states) | numbers newly displayed in text | T2 | final-model-training-count | null | ["05", "21", "368", "460", "56"] |
| Executive Overview | numbers no longer displayed in text | TS | timestamp digits | ["06", "06", "20", "20", "31", "31"] | null |
| Customer Segmentation (+39 states) | numbers no longer displayed in text | TS | timestamp digits | ["06", "20", "31"] | null |
| Governance & Data Quality | numbers no longer displayed in text | T1 | governance-population-terms | ["06", "06", "1980", "20", "20", "31", "31"] | null |
| batch:example file | table 1, row 1 | T2 | batch-display-range-heading (values identical) | {"diner_id": "NEW001", "status": "Scored", "segment": "Premium Foodies", "p_reorder": "71.9", "will_reorder":  | {"diner_id": "NEW001", "status": "Scored", "segment": "Premium Foodies", "p_reorder": "71.9", "will_reorder":  |
| batch:example file | table 1, row 10 | T2 | batch-display-range-heading (values identical) | {"diner_id": "D1110", "status": "Not scored — under 18 (18+ policy)", "segment": NaN, "p_reorder": NaN, "will_ | {"diner_id": "D1110", "status": "Not scored — under 18 (18+ policy)", "segment": NaN, "p_reorder": NaN, "will_ |
| batch:example file | table 1, row 11 | T2 | batch-display-range-heading (values identical) | {"diner_id": "D1102", "status": "Not scored — under 18 (18+ policy)", "segment": NaN, "p_reorder": NaN, "will_ | {"diner_id": "D1102", "status": "Not scored — under 18 (18+ policy)", "segment": NaN, "p_reorder": NaN, "will_ |
| batch:example file | table 1, row 2 | T2 | batch-display-range-heading (values identical) | {"diner_id": "D1113", "status": "Scored", "segment": "Budget Students", "p_reorder": "99.4", "will_reorder": " | {"diner_id": "D1113", "status": "Scored", "segment": "Budget Students", "p_reorder": "99.4", "will_reorder": " |
| batch:example file | table 1, row 3 | T2 | batch-display-range-heading (values identical) | {"diner_id": "D1396", "status": "Scored", "segment": "Premium Foodies", "p_reorder": "54.3", "will_reorder": " | {"diner_id": "D1396", "status": "Scored", "segment": "Premium Foodies", "p_reorder": "54.3", "will_reorder": " |
| batch:example file | table 1, row 4 | T2 | batch-display-range-heading (values identical) | {"diner_id": "D1109", "status": "Scored", "segment": "Budget Students", "p_reorder": "99.4", "will_reorder": " | {"diner_id": "D1109", "status": "Scored", "segment": "Budget Students", "p_reorder": "99.4", "will_reorder": " |
| batch:example file | table 1, row 5 | T2 | batch-display-range-heading (values identical) | {"diner_id": "D1197", "status": "Scored", "segment": "Budget Students", "p_reorder": "96.7", "will_reorder": " | {"diner_id": "D1197", "status": "Scored", "segment": "Budget Students", "p_reorder": "96.7", "will_reorder": " |
| batch:example file | table 1, row 6 | T2 | batch-display-range-heading (values identical) | {"diner_id": "D1471", "status": "Scored", "segment": "Premium Foodies", "p_reorder": "54.8", "will_reorder": " | {"diner_id": "D1471", "status": "Scored", "segment": "Premium Foodies", "p_reorder": "54.8", "will_reorder": " |
| batch:example file | table 1, row 7 | T2 | batch-display-range-heading (values identical) | {"diner_id": "D1136", "status": "Scored", "segment": "Budget Students", "p_reorder": "99.0", "will_reorder": " | {"diner_id": "D1136", "status": "Scored", "segment": "Budget Students", "p_reorder": "99.0", "will_reorder": " |
| batch:example file | table 1, row 8 | T2 | batch-display-range-heading (values identical) | {"diner_id": "D1238", "status": "Scored", "segment": "Family Feasters", "p_reorder": "25.8", "will_reorder": " | {"diner_id": "D1238", "status": "Scored", "segment": "Family Feasters", "p_reorder": "25.8", "will_reorder": " |
| batch:example file | table 1, row 9 | T2 | batch-display-range-heading (values identical) | {"diner_id": "D1057", "status": "Scored", "segment": "Budget Students", "p_reorder": "98.1", "will_reorder": " | {"diner_id": "D1057", "status": "Scored", "segment": "Budget Students", "p_reorder": "98.1", "will_reorder": " |
| batch:example file | table 1: columns changed | T2 | batch-display-range-heading (values identical) | ["diner_id", "status", "segment", "p_reorder", "will_reorder", "risk_tier", "action", "recommended_items", "ou | ["diner_id", "status", "segment", "p_reorder", "will_reorder", "risk_tier", "action", "recommended_items", "Ou |
| Governance & Data Quality | table 4, row 1 | T2 | feature-contract-range-heading (values identical) | {"Feature": "orders_per_month", "Business meaning": "Orders per month", "Clustering (5)": "✓", "Classifier (7) | {"Feature": "orders_per_month", "Business meaning": "Orders per month", "Clustering (5)": "✓", "Classifier (7) |
| Governance & Data Quality | table 4, row 2 | T2 | feature-contract-range-heading (values identical) | {"Feature": "avg_order_value", "Business meaning": "Avg order value (AED)", "Clustering (5)": "✓", "Classifier | {"Feature": "avg_order_value", "Business meaning": "Avg order value (AED)", "Clustering (5)": "✓", "Classifier |
| Governance & Data Quality | table 4, row 3 | T2 | feature-contract-range-heading (values identical) | {"Feature": "avg_items_per_order", "Business meaning": "Avg items per order", "Clustering (5)": "✓", "Classifi | {"Feature": "avg_items_per_order", "Business meaning": "Avg items per order", "Clustering (5)": "✓", "Classifi |
| Governance & Data Quality | table 4, row 4 | T2 | feature-contract-range-heading (values identical) | {"Feature": "days_since_last_order", "Business meaning": "Days since last order", "Clustering (5)": "✓", "Clas | {"Feature": "days_since_last_order", "Business meaning": "Days since last order", "Clustering (5)": "✓", "Clas |
| Governance & Data Quality | table 4, row 5 | T2 | feature-contract-range-heading (values identical) | {"Feature": "discount_rate", "Business meaning": "Discount usage rate", "Clustering (5)": "✓", "Classifier (7) | {"Feature": "discount_rate", "Business meaning": "Discount usage rate", "Clustering (5)": "✓", "Classifier (7) |
| Governance & Data Quality | table 4, row 6 | T2 | feature-contract-range-heading (values identical) | {"Feature": "age", "Business meaning": "Age (years)", "Clustering (5)": "", "Classifier (7)": "✓", "Training r | {"Feature": "age", "Business meaning": "Age (years)", "Clustering (5)": "", "Classifier (7)": "✓", "Observed a |
| Governance & Data Quality | table 4, row 7 | T2 | feature-contract-range-heading (values identical) | {"Feature": "total_spend", "Business meaning": "Total spend (AED)", "Clustering (5)": "", "Classifier (7)": "✓ | {"Feature": "total_spend", "Business meaning": "Total spend (AED)", "Clustering (5)": "", "Classifier (7)": "✓ |
| Governance & Data Quality | table 4: columns changed | T2 | feature-contract-range-heading (values identical) | ["Feature", "Business meaning", "Clustering (5)", "Classifier (7)", "Training range", "Dashboard input range"] | ["Feature", "Business meaning", "Clustering (5)", "Classifier (7)", "Observed adult classifier range", "Dashbo |
| Governance & Data Quality | table 9, row 1 | DQ01 | dq01-governance-row | {"ID": "DQ-01", "Dataset": "diners", "Issue": "Age below plausible account-holder age", "Quantity": "1 diner ( | {"ID": "DQ-01", "Dataset": "diners", "Issue": "Age below plausible account-holder age", "Quantity": "1 diner ( |
| Governance & Data Quality | table 9, row 5 | DQ05 | dq05-governance-row | {"ID": "DQ-05", "Dataset": "diners", "Issue": "Dashboard input ranges exceed training ranges (e.g. recency ≤60 | {"ID": "DQ-05", "Dataset": "diners", "Issue": "Dashboard inputs may fall outside the observed adult classifier |

## final polish vs final

Scope: strict. Baseline: capture_v4_final_polish.json, bundle_v4_final_polish.json.gz (app MD5 `75a40a85ca98`).

Compared 42 page/state snapshots: 154 KPI cards, 184 charts with 363 traces and 685 layout-text fields, 58 tables (9,001 cells), 2,100 numbers in text, 17,657 bundle values, 0 predictions.

By class: DQ01 × 2, DQ05 × 2, T2 × 26, TS × 80.

| Where | What differs | Class | Rule | Before | After |
|---|---|---|---|---|---|
| /dq/issue_log | /dq/issue_log: row 0 (0) | DQ01 | dq01-bundle-row | {"ID": "DQ-01", "Dataset": "diners", "Issue": "Age below plausible account-holder age", "Quantity": "1 diner ( | {"ID": "DQ-01", "Dataset": "diners", "Issue": "Age below plausible account-holder age", "Quantity": "1 diner ( |
| /dq/issue_log | /dq/issue_log: row 4 (4) | DQ05 | dq05-bundle-row | {"ID": "DQ-05", "Dataset": "diners", "Issue": "Dashboard input ranges exceed training ranges (e.g. recency ≤60 | {"ID": "DQ-05", "Dataset": "diners", "Issue": "Dashboard inputs may fall outside the observed adult classifier |
| /meta/trained_at | /meta/trained_at | TS | trained_at | 31 Oct 2026, 20:06 | 05 Nov 2026, 21:56 |
| Governance & Data Quality | KPI 'Last model training' value changed | TS | kpi | 31 Oct 2026, 20:06 | 05 Nov 2026, 21:56 |
| Executive Overview (+1 states) | numbers newly displayed in text | TS | timestamp digits | null | ["05", "05", "21", "21", "56", "56"] |
| Customer Segmentation (+33 states) | numbers newly displayed in text | TS | timestamp digits | null | ["05", "21", "56"] |
| diner:Look up an existing diner… (+5 states) | numbers newly displayed in text | T2 | final-model-training-count | null | ["05", "21", "368", "460", "56"] |
| Executive Overview (+1 states) | numbers no longer displayed in text | TS | timestamp digits | ["06", "06", "20", "20", "31", "31"] | null |
| Customer Segmentation (+39 states) | numbers no longer displayed in text | TS | timestamp digits | ["06", "20", "31"] | null |
| batch:example file | table 1, row 1 | T2 | batch-display-range-heading (values identical) | {"diner_id": "NEW001", "status": "Scored", "segment": "Premium Foodies", "p_reorder": "71.9", "will_reorder":  | {"diner_id": "NEW001", "status": "Scored", "segment": "Premium Foodies", "p_reorder": "71.9", "will_reorder":  |
| batch:example file | table 1, row 10 | T2 | batch-display-range-heading (values identical) | {"diner_id": "D1110", "status": "Not scored — under 18 (18+ policy)", "segment": NaN, "p_reorder": NaN, "will_ | {"diner_id": "D1110", "status": "Not scored — under 18 (18+ policy)", "segment": NaN, "p_reorder": NaN, "will_ |
| batch:example file | table 1, row 11 | T2 | batch-display-range-heading (values identical) | {"diner_id": "D1102", "status": "Not scored — under 18 (18+ policy)", "segment": NaN, "p_reorder": NaN, "will_ | {"diner_id": "D1102", "status": "Not scored — under 18 (18+ policy)", "segment": NaN, "p_reorder": NaN, "will_ |
| batch:example file | table 1, row 2 | T2 | batch-display-range-heading (values identical) | {"diner_id": "D1113", "status": "Scored", "segment": "Budget Students", "p_reorder": "99.4", "will_reorder": " | {"diner_id": "D1113", "status": "Scored", "segment": "Budget Students", "p_reorder": "99.4", "will_reorder": " |
| batch:example file | table 1, row 3 | T2 | batch-display-range-heading (values identical) | {"diner_id": "D1396", "status": "Scored", "segment": "Premium Foodies", "p_reorder": "54.3", "will_reorder": " | {"diner_id": "D1396", "status": "Scored", "segment": "Premium Foodies", "p_reorder": "54.3", "will_reorder": " |
| batch:example file | table 1, row 4 | T2 | batch-display-range-heading (values identical) | {"diner_id": "D1109", "status": "Scored", "segment": "Budget Students", "p_reorder": "99.4", "will_reorder": " | {"diner_id": "D1109", "status": "Scored", "segment": "Budget Students", "p_reorder": "99.4", "will_reorder": " |
| batch:example file | table 1, row 5 | T2 | batch-display-range-heading (values identical) | {"diner_id": "D1197", "status": "Scored", "segment": "Budget Students", "p_reorder": "96.7", "will_reorder": " | {"diner_id": "D1197", "status": "Scored", "segment": "Budget Students", "p_reorder": "96.7", "will_reorder": " |
| batch:example file | table 1, row 6 | T2 | batch-display-range-heading (values identical) | {"diner_id": "D1471", "status": "Scored", "segment": "Premium Foodies", "p_reorder": "54.8", "will_reorder": " | {"diner_id": "D1471", "status": "Scored", "segment": "Premium Foodies", "p_reorder": "54.8", "will_reorder": " |
| batch:example file | table 1, row 7 | T2 | batch-display-range-heading (values identical) | {"diner_id": "D1136", "status": "Scored", "segment": "Budget Students", "p_reorder": "99.0", "will_reorder": " | {"diner_id": "D1136", "status": "Scored", "segment": "Budget Students", "p_reorder": "99.0", "will_reorder": " |
| batch:example file | table 1, row 8 | T2 | batch-display-range-heading (values identical) | {"diner_id": "D1238", "status": "Scored", "segment": "Family Feasters", "p_reorder": "25.8", "will_reorder": " | {"diner_id": "D1238", "status": "Scored", "segment": "Family Feasters", "p_reorder": "25.8", "will_reorder": " |
| batch:example file | table 1, row 9 | T2 | batch-display-range-heading (values identical) | {"diner_id": "D1057", "status": "Scored", "segment": "Budget Students", "p_reorder": "98.1", "will_reorder": " | {"diner_id": "D1057", "status": "Scored", "segment": "Budget Students", "p_reorder": "98.1", "will_reorder": " |
| batch:example file | table 1: columns changed | T2 | batch-display-range-heading (values identical) | ["diner_id", "status", "segment", "p_reorder", "will_reorder", "risk_tier", "action", "recommended_items", "ou | ["diner_id", "status", "segment", "p_reorder", "will_reorder", "risk_tier", "action", "recommended_items", "Ou |
| Governance & Data Quality | table 4, row 1 | T2 | feature-contract-range-heading (values identical) | {"Feature": "orders_per_month", "Business meaning": "Orders per month", "Clustering (5)": "✓", "Classifier (7) | {"Feature": "orders_per_month", "Business meaning": "Orders per month", "Clustering (5)": "✓", "Classifier (7) |
| Governance & Data Quality | table 4, row 2 | T2 | feature-contract-range-heading (values identical) | {"Feature": "avg_order_value", "Business meaning": "Avg order value (AED)", "Clustering (5)": "✓", "Classifier | {"Feature": "avg_order_value", "Business meaning": "Avg order value (AED)", "Clustering (5)": "✓", "Classifier |
| Governance & Data Quality | table 4, row 3 | T2 | feature-contract-range-heading (values identical) | {"Feature": "avg_items_per_order", "Business meaning": "Avg items per order", "Clustering (5)": "✓", "Classifi | {"Feature": "avg_items_per_order", "Business meaning": "Avg items per order", "Clustering (5)": "✓", "Classifi |
| Governance & Data Quality | table 4, row 4 | T2 | feature-contract-range-heading (values identical) | {"Feature": "days_since_last_order", "Business meaning": "Days since last order", "Clustering (5)": "✓", "Clas | {"Feature": "days_since_last_order", "Business meaning": "Days since last order", "Clustering (5)": "✓", "Clas |
| Governance & Data Quality | table 4, row 5 | T2 | feature-contract-range-heading (values identical) | {"Feature": "discount_rate", "Business meaning": "Discount usage rate", "Clustering (5)": "✓", "Classifier (7) | {"Feature": "discount_rate", "Business meaning": "Discount usage rate", "Clustering (5)": "✓", "Classifier (7) |
| Governance & Data Quality | table 4, row 6 | T2 | feature-contract-range-heading (values identical) | {"Feature": "age", "Business meaning": "Age (years)", "Clustering (5)": "", "Classifier (7)": "✓", "Training r | {"Feature": "age", "Business meaning": "Age (years)", "Clustering (5)": "", "Classifier (7)": "✓", "Observed a |
| Governance & Data Quality | table 4, row 7 | T2 | feature-contract-range-heading (values identical) | {"Feature": "total_spend", "Business meaning": "Total spend (AED)", "Clustering (5)": "", "Classifier (7)": "✓ | {"Feature": "total_spend", "Business meaning": "Total spend (AED)", "Clustering (5)": "", "Classifier (7)": "✓ |
| Governance & Data Quality | table 4: columns changed | T2 | feature-contract-range-heading (values identical) | ["Feature", "Business meaning", "Clustering (5)", "Classifier (7)", "Training range", "Dashboard input range"] | ["Feature", "Business meaning", "Clustering (5)", "Classifier (7)", "Observed adult classifier range", "Dashbo |
| Governance & Data Quality | table 9, row 1 | DQ01 | dq01-governance-row | {"ID": "DQ-01", "Dataset": "diners", "Issue": "Age below plausible account-holder age", "Quantity": "1 diner ( | {"ID": "DQ-01", "Dataset": "diners", "Issue": "Age below plausible account-holder age", "Quantity": "1 diner ( |
| Governance & Data Quality | table 9, row 5 | DQ05 | dq05-governance-row | {"ID": "DQ-05", "Dataset": "diners", "Issue": "Dashboard input ranges exceed training ranges (e.g. recency ≤60 | {"ID": "DQ-05", "Dataset": "diners", "Issue": "Dashboard inputs may fall outside the observed adult classifier |

## range correction vs final

Scope: strict. Baseline: capture_v5_range_correction.json, bundle_v5_range_correction.json.gz (app MD5 `dec5e977ff55`).

Compared 42 page/state snapshots: 154 KPI cards, 184 charts with 363 traces and 685 layout-text fields, 58 tables (9,001 cells), 2,112 numbers in text, 17,657 bundle values, 0 predictions.

By class: DQ01 × 2, DQ05 × 2, TS × 86.

| Where | What differs | Class | Rule | Before | After |
|---|---|---|---|---|---|
| /dq/issue_log | /dq/issue_log: row 0 (0) | DQ01 | dq01-bundle-row | {"ID": "DQ-01", "Dataset": "diners", "Issue": "Age below plausible account-holder age", "Quantity": "1 diner ( | {"ID": "DQ-01", "Dataset": "diners", "Issue": "Age below plausible account-holder age", "Quantity": "1 diner ( |
| /dq/issue_log | /dq/issue_log: row 4 (4) | DQ05 | dq05-bundle-row | {"ID": "DQ-05", "Dataset": "diners", "Issue": "Dashboard input ranges exceed training ranges (e.g. recency ≤60 | {"ID": "DQ-05", "Dataset": "diners", "Issue": "Dashboard inputs may fall outside the observed adult classifier |
| /meta/trained_at | /meta/trained_at | TS | trained_at | 31 Oct 2026, 20:06 | 05 Nov 2026, 21:56 |
| Governance & Data Quality | KPI 'Last model training' value changed | TS | kpi | 31 Oct 2026, 20:06 | 05 Nov 2026, 21:56 |
| Executive Overview (+1 states) | numbers newly displayed in text | TS | timestamp digits | null | ["05", "05", "21", "21", "56", "56"] |
| Customer Segmentation (+39 states) | numbers newly displayed in text | TS | timestamp digits | null | ["05", "21", "56"] |
| Executive Overview (+1 states) | numbers no longer displayed in text | TS | timestamp digits | ["06", "06", "20", "20", "31", "31"] | null |
| Customer Segmentation (+39 states) | numbers no longer displayed in text | TS | timestamp digits | ["06", "20", "31"] | null |
| Governance & Data Quality | table 9, row 1 | DQ01 | dq01-governance-row | {"ID": "DQ-01", "Dataset": "diners", "Issue": "Age below plausible account-holder age", "Quantity": "1 diner ( | {"ID": "DQ-01", "Dataset": "diners", "Issue": "Age below plausible account-holder age", "Quantity": "1 diner ( |
| Governance & Data Quality | table 9, row 5 | DQ05 | dq05-governance-row | {"ID": "DQ-05", "Dataset": "diners", "Issue": "Dashboard input ranges exceed the observed adult classifier ran | {"ID": "DQ-05", "Dataset": "diners", "Issue": "Dashboard inputs may fall outside the observed adult classifier |

## dq correction vs final

Scope: strict. Baseline: capture_v6_dq_correction.json, bundle_v6_dq_correction.json.gz (app MD5 `e01606439b07`).

Compared 42 page/state snapshots: 154 KPI cards, 184 charts with 363 traces and 685 layout-text fields, 58 tables (9,001 cells), 2,112 numbers in text, 17,657 bundle values, 0 predictions.

By class: DQ05 × 2, TS × 86.

| Where | What differs | Class | Rule | Before | After |
|---|---|---|---|---|---|
| /dq/issue_log | /dq/issue_log: row 4 (4) | DQ05 | dq05-bundle-row | {"ID": "DQ-05", "Dataset": "diners", "Issue": "Dashboard inputs may fall outside the observed adult classifier | {"ID": "DQ-05", "Dataset": "diners", "Issue": "Dashboard inputs may fall outside the observed adult classifier |
| /meta/trained_at | /meta/trained_at | TS | trained_at | 05 Nov 2026, 21:13 | 05 Nov 2026, 21:56 |
| Governance & Data Quality | KPI 'Last model training' value changed | TS | kpi | 05 Nov 2026, 21:13 | 05 Nov 2026, 21:56 |
| Executive Overview (+1 states) | numbers newly displayed in text | TS | timestamp digits | null | ["56", "56"] |
| Customer Segmentation (+39 states) | numbers newly displayed in text | TS | timestamp digits | null | ["56"] |
| Executive Overview (+1 states) | numbers no longer displayed in text | TS | timestamp digits | ["13", "13"] | null |
| Customer Segmentation (+39 states) | numbers no longer displayed in text | TS | timestamp digits | ["13"] | null |
| Governance & Data Quality | table 9, row 5 | DQ05 | dq05-governance-row | {"ID": "DQ-05", "Dataset": "diners", "Issue": "Dashboard inputs may fall outside the observed adult classifier | {"ID": "DQ-05", "Dataset": "diners", "Issue": "Dashboard inputs may fall outside the observed adult classifier |

## pre redesign vs final

Scope: numeric (KPI values, every number in charts/tables/text; labels and styling out of scope — they were redesigned on purpose). Baseline: capture_pre_redesign.json (app MD5 `1fd983f4b0fb`).


By class: DQ01+DQ05 × 1, M2 × 5, T1 × 1.

| Where | What differs | Class | Rule | Before | After |
|---|---|---|---|---|---|
| Governance & Data Quality | KPI values differ | T1 | kpi-governance-population (value re-formatted, number unchanged) | ["480 diners"] | ["480"] |
| Retention & Churn (+2 states) | numbers no longer displayed in text | M2 | retention-note | ["27.3"] | null |
| Recommendations | numbers no longer displayed in text | M2 | takeaway-text | ["0.94", "59", "86", "90"] | null |
| Governance & Data Quality | table 3: numbers differ | M2 | model-card-stability-row (adds the matched 58.5% baseline) | [] | ["58.5"] |
| Governance & Data Quality | table 9: numbers differ | DQ01+DQ05 | issue-log numbers exactly as in the approved DQ-01 / DQ-05 rows | ["4"] | ["368", "460", "6", "7", "92"] |

## Model-selection verification (independent recomputation)

Training-fold 5-fold CV re-run on the 368 training diners. Table matches recomputation: **True**; no held-out test column for any candidate: **True**; highest CV ROC-AUC: Logistic Regression (scaled); lowest CV Brier: Logistic Regression (scaled); selected: Logistic Regression (scaled); rule satisfied: **True**; training-set majority share 0.5842 (stored: True).

| Model | CV acc | sd | precision | recall | F1 | ROC-AUC | Brier |
|---|---|---|---|---|---|---|---|
| Logistic Regression (scaled) | 0.8478 | 0.0292 | 0.8862 | 0.8512 | 0.8676 | 0.9343 | 0.1014 |
| Decision Tree (depth 4) | 0.8153 | 0.0348 | 0.8499 | 0.8372 | 0.8411 | 0.8624 | 0.1444 |
| Random Forest (300 trees) | 0.8287 | 0.0258 | 0.8707 | 0.8326 | 0.8507 | 0.9286 | 0.1025 |
| Gradient Boosting | 0.8207 | 0.0196 | 0.8453 | 0.8512 | 0.8472 | 0.9129 | 0.1290 |

## CV accuracy — mean and standard deviation (exact formatted string)

Expected strings are formatted from the independent recomputation only (`f"{x*100:.1f}%"`, mirroring app.py `pct()`), never read from the dashboard. Values are normalised to shares before formatting; strings are compared exactly. The stored raw values are compared separately with a relative tolerance of 1e-12, which also catches changes too small to show at one decimal.

| Model | Recomputed mean | Recomputed SD | Expected display | Displayed | Mean | SD |
|---|---|---|---|---|---|---|
| Logistic Regression (scaled) | 0.847760 | 0.029243 | 84.8% ± 2.9% | 84.8% ± 2.9% | PASS | PASS |
| Random Forest (300 trees) | 0.828730 | 0.025819 | 82.9% ± 2.6% | 82.9% ± 2.6% | PASS | PASS |
| Gradient Boosting | 0.820696 | 0.019564 | 82.1% ± 2.0% | 82.1% ± 2.0% | PASS | PASS |
| Decision Tree (depth 4) | 0.815291 | 0.034800 | 81.5% ± 3.5% | 81.5% ± 3.5% | PASS | PASS |

## Model selection — every displayed field

| Model | Selected | CV accuracy | precision | recall | F1 | ROC-AUC | Brier | Interpretable | Row matches |
|---|---|---|---|---|---|---|---|---|---|
| Logistic Regression (scaled) | ✓ selected | 84.8% ± 2.9% | 0.886 | 0.851 | 0.868 | 0.934 | 0.101 | Yes | PASS (exact) |
| Random Forest (300 trees) | — | 82.9% ± 2.6% | 0.871 | 0.833 | 0.851 | 0.929 | 0.103 | No | PASS (exact) |
| Gradient Boosting | — | 82.1% ± 2.0% | 0.845 | 0.851 | 0.847 | 0.913 | 0.129 | No | PASS (exact) |
| Decision Tree (depth 4) | — | 81.5% ± 3.5% | 0.850 | 0.837 | 0.841 | 0.862 | 0.144 | Yes | PASS (exact) |

Rule: highest CV ROC-AUC = **Logistic Regression (scaled)**, confirmed by lowest CV Brier (Logistic Regression (scaled)) and interpretable; exactly one row marked selected; no held-out test metric in the table: **True**. Stored-table defects: 0; displayed-table defects: 0.

## Prediction schema, correspondence and values

Authoritative record definition (`vcore.RECORD_FIELDS`): `profile_id, segment, reorder, prob, items, tier`. Structure is validated for every record of every version BEFORE any value is compared: field definition, field count (fewer / extra), field order and types, collection length (missing / extra records, with the identifiers), duplicate identifiers, and record ↔ profile correspondence in deterministic order. Only then are values compared, matched by profile identifier, with exact equality.

| Check | Result | Detail |
|---|---|---|
| Prediction schema — field definition, field count, field order and types, collection length | PASS | fields ['profile_id', 'segment', 'reorder', 'prob', 'items', 'tier']; 5,179 records per version; 0 structural defects |
| Prediction/profile correspondence — every record matched to its profile identifier, deterministic order, no duplicates | PASS | 5,179 identifiers matched in each version |
| Prediction value equality — segment, reorder, probability (exact), items, tier | PASS | 10,358 record comparisons (5,179 profiles × 2 earlier versions), 0 mismatches |
| Negative controls — prediction structure | PASS | 11/11 behaved as required |

## Data-quality issue log — DQ-01 and DQ-05 before and after

Corrected at the source (`build/notebook_source.py`); the notebook was re-executed, which regenerated `reports/data_quality_issue_log.csv`, `reports/data_quality_report.md` and `dashboard_bundle.joblib`. Before = `validation/baselines/bundle_v6_dq_correction.json.gz` (the previous submission's bundle). Populations recounted independently from the cleaned data: {'total': 480, 'eligible': 460, 'train': 368, 'test': 92, 'under18': 20}.

| Entry | Field | Before | After |
|---|---|---|---|
| DQ-01 | Issue | Age below plausible account-holder age | (unchanged) |
| DQ-01 | Quantity | 1 diner (D1052, age 9) | (unchanged) |
| DQ-01 | Treatment | Excluded from the classifier and the app's age input (under-18 policy). Retained for clustering & baskets (age not used there). No imputation. | (unchanged) |
| DQ-01 | Impact | Classifier-eligible population: 460 adult diners (368 training observations and 92 held-out test observations) | (unchanged) |
| DQ-05 | Issue | Dashboard inputs may fall outside the observed adult classifier range (input limits exceed it, e.g. recency ≤60 vs max 34; spend ≤20,000 vs max 1,490) | (unchanged) |
| DQ-05 | Quantity | 4 inputs | 6 of 7 classifier input controls |
| DQ-05 | Treatment | Dashboard shows an observed adult reference-range warning when an input falls outside the feature range calculated from the 460 adult classifier-eligible diners. | Values outside it remain permitted by the dashboard input limits (INPUT_SPEC); the dashboard shows an observed adult reference-range warning when an input falls outside the feature range calculated from the 460 adult classifier-eligible diners. |
| DQ-05 | Impact | Dashboard governance | (unchanged) |

**DQ-05 Quantity — independent calculation** (`dq_consistency.dq05_calculation`): permitted limits from app.py `INPUT_SPEC` (parsed) and the Governance page (must agree); observed adult classifier range recounted from `data/clean/diners_clean.csv` (460 eligible adults); a control counts once if `ui_min < observed_min or ui_max > observed_max`.

| Feature | Dashboard input range | Observed adult classifier range | Lower bound outside | Upper bound outside | Counted |
|---|---|---|---|---|---|
| age | 18–70 | 18–52 | no | yes | **yes** |
| orders_per_month | 1–20 | 1–20 | no | no | no |
| avg_order_value | 15–250 | 29.5–218.66 | yes | yes | **yes** |
| avg_items_per_order | 1–10 | 1–9 | no | yes | **yes** |
| days_since_last_order | 0–60 | 0–34 | no | yes | **yes** |
| discount_rate | 0–1 | 0–0.86 | no | yes | **yes** |
| total_spend | 50–20000 | 134.04–1490.17 | yes | yes | **yes** |

Result: **6 of 7 classifier input controls** (1 within / equal). Shipped DQ-05 Quantity: `6 of 7 classifier input controls`.

| Representation check | Result | Detail |
|---|---|---|
| notebook: DQ-01 and DQ-05 present exactly once | PASS | — |
| csv: DQ-01 and DQ-05 present exactly once | PASS | — |
| markdown: DQ-01 and DQ-05 present exactly once | PASS | — |
| bundle: DQ-01 and DQ-05 present exactly once | PASS | — |
| dashboard: DQ-01 and DQ-05 present exactly once | PASS | — |
| DQ-01: identical in notebook, CSV, Markdown report, analytics bundle and Governance dashboard | PASS | — |
| DQ-05: identical in notebook, CSV, Markdown report, analytics bundle and Governance dashboard | PASS | — |
| DQ-01: identifier, dataset, issue, quantity (D1052, age 9), classification and treatment unchanged | PASS | — |
| DQ-01: names the 368 training observations (not 'trained on 460') | PASS | — |
| DQ-01: names the 92 held-out test observations | PASS | — |
| DQ-01: names the 460 classifier-eligible adults as eligibility, not fitting | PASS | — |
| DQ-05: identifier, dataset, classification and impact unchanged | PASS | — |
| DQ-05: dashboard input limits on the Governance page = app.py INPUT_SPEC | PASS | — |
| DQ-05: the controls are exactly the 7 classifier input features | PASS | — |
| DQ-05: Quantity equals the independent calculation in every representation (computed: 6 of 7 classifier input controls; 1 control(s) within / equal) | PASS | — |
| DQ-05: calculation agrees with the documented expectation (7 controls · 6 outside · 1 within / equal: orders_per_month) | PASS | — |
| DQ-05: explanation table in the data-quality report = the independent calculation (row by row and result) | PASS | — |
| DQ-05: quoted range values unchanged and equal to the observed adult maxima / dashboard input limits | PASS | — |
| DQ-05: observed adult classifier range terminology; reference population = the 460 eligible adults | PASS | — |
| Observed adult classifier range = min–max of the 460 adult diners, identical to the baseline | PASS | — |
| Validator's 7 classifier features = food_models.joblib features + age + total_spend | PASS | — |
| Executed notebook cells == cells generated from build/notebook_source.py | PASS | — |
| Batch CSV export schema identical to the reference (incl. outside_training_range) | PASS | — |

## Differences by kind

Metadata-only = the training timestamp (TS) and the timestamp digits shown in text; analytics-bundle descriptive = approved text changes inside `dashboard_bundle.joblib` (DQ-01 / DQ-05 issue-log rows); analytics-bundle reporting = earlier approved bundle changes (model-selection table schema, rule order, matched baseline); presentation / documentation = approved dashboard wording, labels and styling; unexplained = anything else (FAIL).

| Comparison | Metadata-only | Analytics-bundle descriptive | Analytics-bundle reporting | Presentation / documentation | Unexplained |
|---|---|---|---|---|---|
| received vs final | 70 | 2 | 11 | 376 | 0 |
| previous refinement vs final | 70 | 2 | 2 | 64 | 0 |
| micro refinement vs final | 78 | 2 | 0 | 32 | 0 |
| final polish vs final | 80 | 2 | 0 | 28 | 0 |
| range correction vs final | 86 | 2 | 0 | 2 | 0 |
| dq correction vs final | 86 | 1 | 0 | 1 | 0 |
| pre redesign vs final | 0 | 0 | 0 | 7 | 0 |

## Checksum inventory and protected-artifact checksums

Two checksum mechanisms exist. They cover only the files listed here. Files that the validation reads but are not listed (validation scripts, captures, prediction results, generated reports, README, CHANGELOG, requirements, figures) are not covered by either checksum assertion; their content is checked in other ways where relevant (e.g. the dashboard capture is compared value by value) or not at all.

| Mechanism | Files | Algorithm | When hashed | Compared with | Failure rule |
|---|---|---|---|---|---|
| A. Protected artifacts (`validation/protected_checksums.json`, read by `run_validation.py`) | 9 (listed below) | MD5 and SHA-256 | start and end of every validation run | the recorded reference, and start vs end | missing file, any byte-identical file ≠ reference, or any monitored file changed during the run → FAIL |
| B. Negative-control watch list (`negative_controls.py`) | 28: `app.py`, `dashboard_bundle.joblib`, `food_models.joblib`, `validation/approved_differences.json`, `validation/baselines/README.md`, `validation/baselines/app_original_supplied.py`, `validation/baselines/app_pre_redesign.py`, `validation/baselines/app_v1_received.py`, `validation/baselines/app_v2_previous_refinement.py`, `validation/baselines/app_v3_micro_refinement.py`, `validation/baselines/app_v4_final_polish.py`, `validation/baselines/app_v5_range_correction.py`, `validation/baselines/bundle_v1_received.json.gz`, `validation/baselines/bundle_v2_previous_refinement.json.gz`, `validation/baselines/bundle_v3_micro_refinement.json.gz`, `validation/baselines/bundle_v4_final_polish.json.gz`, `validation/baselines/bundle_v5_range_correction.json.gz`, `validation/baselines/bundle_v6_dq_correction.json.gz`, `validation/baselines/capture_pre_redesign.json`, `validation/baselines/capture_v1_received.json`, `validation/baselines/capture_v2_previous_refinement.json`, `validation/baselines/capture_v3_micro_refinement.json`, `validation/baselines/capture_v4_final_polish.json`, `validation/baselines/capture_v5_range_correction.json`, `validation/baselines/capture_v6_dq_correction.json`, `validation/captures/capture_final.json`, `validation/inference_check_results.per_profile.json.gz`, `validation/protected_checksums.json` | MD5 | before and after the negative controls | each other | any change → FAIL (controls mutate in-memory copies; checksum controls use a temporary directory that is deleted afterwards) |

Mechanism A reference: 5 Nov 2026, after the DQ-05 quantity correction (notebook source corrected and re-executed; bundle and notebook references updated; app.py, data and model artifact unchanged).

| Protected artifact | Rule | Algorithm | Reference | Before (start of run) | After (end of run) | Result |
|---|---|---|---|---|---|---|
| `data/raw/diners.csv` | byte-identical to reference | MD5 | `11ba8cfa2b2ab1499c5422cabbe80d1c` | `11ba8cfa2b2ab1499c5422cabbe80d1c` | `11ba8cfa2b2ab1499c5422cabbe80d1c` | PASS |
| `data/raw/diners.csv` | byte-identical to reference | SHA-256 | `0a05f70cc6de63ab6501b8a119a74ee6dde6ffdba8dae5ad84179e62b56acc26` | `0a05f70cc6de63ab6501b8a119a74ee6dde6ffdba8dae5ad84179e62b56acc26` | `0a05f70cc6de63ab6501b8a119a74ee6dde6ffdba8dae5ad84179e62b56acc26` | PASS |
| `data/raw/orders.csv` | byte-identical to reference | MD5 | `776f66420a6669d62764daab11863c03` | `776f66420a6669d62764daab11863c03` | `776f66420a6669d62764daab11863c03` | PASS |
| `data/raw/orders.csv` | byte-identical to reference | SHA-256 | `aff2b91297d575a387159b0906fce6fb06b401a46ee2c9c575d1fa9f3bffc7d7` | `aff2b91297d575a387159b0906fce6fb06b401a46ee2c9c575d1fa9f3bffc7d7` | `aff2b91297d575a387159b0906fce6fb06b401a46ee2c9c575d1fa9f3bffc7d7` | PASS |
| `data/clean/diners_clean.csv` | byte-identical to reference | MD5 | `01ee01ca7fe20d31c91a82ea0788c698` | `01ee01ca7fe20d31c91a82ea0788c698` | `01ee01ca7fe20d31c91a82ea0788c698` | PASS |
| `data/clean/diners_clean.csv` | byte-identical to reference | SHA-256 | `b28dc806504f00b0cb6532f9db4745a6d8dcba1d6d7261e39a96d776107d81a0` | `b28dc806504f00b0cb6532f9db4745a6d8dcba1d6d7261e39a96d776107d81a0` | `b28dc806504f00b0cb6532f9db4745a6d8dcba1d6d7261e39a96d776107d81a0` | PASS |
| `data/clean/orders_clean.csv` | byte-identical to reference | MD5 | `2188c9e4977acd5765e5d8ced0c8966d` | `2188c9e4977acd5765e5d8ced0c8966d` | `2188c9e4977acd5765e5d8ced0c8966d` | PASS |
| `data/clean/orders_clean.csv` | byte-identical to reference | SHA-256 | `d9b1b74f3abce70c800b8acea40b6d232583c25789e34123f1a6ace59059dadd` | `d9b1b74f3abce70c800b8acea40b6d232583c25789e34123f1a6ace59059dadd` | `d9b1b74f3abce70c800b8acea40b6d232583c25789e34123f1a6ace59059dadd` | PASS |
| `food_models.joblib` | byte-identical to reference | MD5 | `7b1f8a39310cc735d15cbc3f89754045` | `7b1f8a39310cc735d15cbc3f89754045` | `7b1f8a39310cc735d15cbc3f89754045` | PASS |
| `food_models.joblib` | byte-identical to reference | SHA-256 | `d47477932350b79023589b4622261b1809d0ee6bc0bc3da86e3ed34dbef598c1` | `d47477932350b79023589b4622261b1809d0ee6bc0bc3da86e3ed34dbef598c1` | `d47477932350b79023589b4622261b1809d0ee6bc0bc3da86e3ed34dbef598c1` | PASS |
| `app.py` | byte-identical to reference | MD5 | `e01606439b07fc2c89ef8d838701caf1` | `e01606439b07fc2c89ef8d838701caf1` | `e01606439b07fc2c89ef8d838701caf1` | PASS |
| `app.py` | byte-identical to reference | SHA-256 | `182243a536224095b7417f4bf3089ca771ba47d77949a4474c97de3d42838212` | `182243a536224095b7417f4bf3089ca771ba47d77949a4474c97de3d42838212` | `182243a536224095b7417f4bf3089ca771ba47d77949a4474c97de3d42838212` | PASS |
| `build/notebook_source.py` | byte-identical to reference | MD5 | `d0a5937da73fc6e2de67d0b99c4ba200` | `d0a5937da73fc6e2de67d0b99c4ba200` | `d0a5937da73fc6e2de67d0b99c4ba200` | PASS |
| `build/notebook_source.py` | byte-identical to reference | SHA-256 | `646f60df3c22c66fc161dc15a6cad623825f57290cc7668b0257edfcd86277a1` | `646f60df3c22c66fc161dc15a6cad623825f57290cc7668b0257edfcd86277a1` | `646f60df3c22c66fc161dc15a6cad623825f57290cc7668b0257edfcd86277a1` | PASS |
| `dashboard_bundle.joblib` | unchanged during run; reported if ≠ reference (rewritten by a notebook re-execution) | MD5 | `202bb66471fea96a3e6fde3aef08e47a` | `202bb66471fea96a3e6fde3aef08e47a` | `202bb66471fea96a3e6fde3aef08e47a` | PASS |
| `dashboard_bundle.joblib` | unchanged during run; reported if ≠ reference (rewritten by a notebook re-execution) | SHA-256 | `e090772ad1b4a8626216fda126068d1ae1fa14184460cdecfcadd6242d28ce0d` | `e090772ad1b4a8626216fda126068d1ae1fa14184460cdecfcadd6242d28ce0d` | `e090772ad1b4a8626216fda126068d1ae1fa14184460cdecfcadd6242d28ce0d` | PASS |
| `QuickBite_Analysis.ipynb` | unchanged during run; reported if ≠ reference (rewritten by a notebook re-execution) | MD5 | `67e51531c3628c6e51da7eb8e12b6dfa` | `67e51531c3628c6e51da7eb8e12b6dfa` | `67e51531c3628c6e51da7eb8e12b6dfa` | PASS |
| `QuickBite_Analysis.ipynb` | unchanged during run; reported if ≠ reference (rewritten by a notebook re-execution) | SHA-256 | `b2353a08215e604c2e4fc58e8e28aa930e4dc5cb5f1bf17faf7ae25c397b28ed` | `b2353a08215e604c2e4fc58e8e28aa930e4dc5cb5f1bf17faf7ae25c397b28ed` | `b2353a08215e604c2e4fc58e8e28aa930e4dc5cb5f1bf17faf7ae25c397b28ed` | PASS |

**Validation run left all checksum-monitored protected artifacts unchanged** — all 9 files above kept their MD5 and SHA-256 values from the start to the end of the run, and the 7 byte-identical files equal their recorded reference.

Timestamp / metadata: No timestamp or metadata change in this run: the dashboard bundle and the notebook equal their recorded reference.

## Validation steps

| Step | Exit status | Result |
|---|---|---|
| dashboard capture | 0 | PASS |
| smoke test | 0 | PASS |
| prediction test (inference) | 0 | PASS |
| independent CV recomputation + model-selection validation | 0 | PASS |
| palette check | 0 | PASS |
| data-quality issue log consistency | 0 | PASS |
| negative controls | 0 | PASS |

## Identical-profile prediction test

Profiles: real adult diners 460, boundary grid 2,187, random in range 1,000, threshold edge 1,532. Every profile's segment, reorder flag, probability (exact), recommended items and risk tier are compared one by one (per-profile file: `validation/inference_check_results.per_profile.json.gz`).

| Comparison | Structural defects | Segment | Reorder | Probability | Items | Tier | analyse() logic identical |
|---|---|---|---|---|---|---|---|
| supplied_original vs v1_received | 0 | 0 | 0 | 0 | 0 | 0 | True |
| supplied_original vs final | 0 | 0 | 0 | 0 | 0 | 0 | True |

## Negative controls

**73 controls executed, 73 behaved as required** (framework: 25/25, checksum: 6/6, dq log: 8/8, dq05 quantity: 10/10, cv display: 11/11, cv stored: 2/2, prediction structure: 11/11). Run on in-memory copies; MD5 of 28 project/baseline files identical before and after: **True**. A FAIL control passes only if the framework reports the *specific* defect named in the brief and the strict comparison also fails.

### Framework controls (strict comparison; H9–H11 added in the final polish, H12–H14 in the range-terminology correction)

| Control | Expected | Framework verdict | As required | Detected / accepted as |
|---|---|---|---|---|
| 0  Unmodified final version (reference run) | PASS | PASS | yes | DQ01:dq01-bundle-row; DQ01:dq01-governance-row; DQ05:dq05-bundle-row; DQ05:dq05-governance-row |
| A  Association-rule lift + 1e-6 | FAIL | FAIL | yes | /rules_all · /rules_all: row 3 (3) |
| B  Chart text label changed (ov_ret bar label, numbers unchanged) | FAIL | FAIL | yes | Executive Overview · chart 'ov_ret' · bar:None · text |
| C  Trace renamed (ov_conc 'Share of diners'), data unchanged | FAIL | FAIL | yes | Executive Overview · chart 'ov_conc' · bar:'Share of diners' · name |
| D  One profile's segment changed | FAIL | FAIL | yes | final vs supplied_original · real_adult_diners:0 · prediction value mismatch (real_adult_diners:0 · segment) |
| E1 Shared CV-accuracy value changed in model_comparison (bundle) | FAIL | FAIL | yes | /model_comparison · /model_comparison: row 1 (1) |
| E2 CV-accuracy cell changed in the Governance selection table | FAIL | FAIL | yes | Governance & Data Quality · table 5, row 2 |
| F  Documented R1 tie-break applied to the received bundle | PASS | PASS | yes | R1:bundle rule row |
| F2 Direction of a different rule swapped (R1 must not cover it) | FAIL | FAIL | yes | /rules_all · /rules_all: row 0 (0) |
| G  Documented M1 correction applied to the received bundle | PASS | PASS | yes | M1:bundle schema |
| G2 M1 correction plus one unrelated change in a shared column (must not hide behind M1) | FAIL | FAIL | yes | /model_comparison · /model_comparison: row 2 (2) |
| H1 Cluster count changed (meta.K 3 → 4) | FAIL | FAIL | yes | /meta/K · /meta/K |
| H2 Segment renamed in the segment profile | FAIL | FAIL | yes | /seg_profile · /seg_profile: index changed |
| H3 Confusion matrix changed | FAIL | FAIL | yes | /cm[0][0] · /cm[0][0]; /cm[0][1] · /cm[0][1] |
| H4 What-If scenario result changed | FAIL | FAIL | yes | /scenarios · /scenarios: row 0 (0) |
| H5 Financial value changed (ROI curve net value + AED 1) | FAIL | FAIL | yes | /roi_curve · /roi_curve: row 5 (5) |
| H6 Chart category renamed (x label), values unchanged | FAIL | FAIL | yes | Executive Overview · chart 'ov_ret' · bar:None · x |
| H7 Chart title changed back to an unapproved wording | FAIL | FAIL | yes | Retention & Churn · chart 'rt_cv' · title |
| H8 KPI value changed | FAIL | FAIL | yes | Executive Overview · KPI 'Retention rate' value changed |
| H9 Governance 'Analysis population' value changed (480 → 479) behind the approved rename | FAIL | FAIL | yes | Governance & Data Quality · KPI 'Training data' no longer shown; Governance & Data Quality · KPI 'Analysis population' newly shown |
| H10 Governance population context changed (368 → 369 training observations) | FAIL | FAIL | yes | Governance & Data Quality · KPI 'Training data' no longer shown; Governance & Data Quality · KPI 'Analysis population' newly shown |
| H11 New population context shown under the old 'Training data' label | FAIL | FAIL | yes | Governance & Data Quality · KPI 'Training data' value changed; Governance & Data Quality · KPI 'Training data' context changed |
| H12 Relabelled range column with one value changed to the training-split range | FAIL | FAIL | yes | Governance & Data Quality · table 4, row 2 |
| H13 Range column shown under an unapproved heading | FAIL | FAIL | yes | Governance & Data Quality · table 4: columns changed; Governance & Data Quality · table 4, row 1 |
| H14 DQ-05 display wording reverted in one cell | FAIL | FAIL | yes | Governance & Data Quality · table 9, row 5 |

### CV display contract (micro-refinement)

| Control | Expected | Required defect | Reported | As required |
|---|---|---|---|---|
| CV0  Unchanged selection table (positive control) | PASS | None | PASS — all CV accuracy means and standard deviations match independent recomputation | yes |
| CV1  Displayed CV-accuracy SD + 0.05 (Random Forest) | FAIL | CV accuracy standard deviation mismatch | cv_accuracy_sd_mismatch: CV accuracy standard deviation mismatch · Random Forest (300 trees) · CV accuracy · expected '82.9% ± 2.6%' · actual '82.9% ± 7.6%' | yes |
| CV2  Displayed CV-accuracy mean wrong (+1 pp, Random Forest) | FAIL | CV accuracy mean mismatch | cv_accuracy_mean_mismatch: CV accuracy mean mismatch · Random Forest (300 trees) · CV accuracy · expected '82.9% ± 2.6%' · actual '83.9% ± 2.6%' | yes |
| CV3  '±' separator removed | FAIL | separator missing | cv_accuracy_separator_missing: CV accuracy '±' separator missing · Random Forest (300 trees) · CV accuracy · expected '82.9% ± 2.6%' · actual '82.9% 2.6%' | yes |
| CV4  Display precision wrong (two decimals) | FAIL | display precision | cv_accuracy_precision: CV accuracy not shown with the display precision (one decimal, 'x.x% ± y.y%') · Random Forest (300 trees) · CV accuracy · expected '82.9% ± 2.6%' · actual '82.87% ± 2.58%' | yes |
| CV5  Standard deviation removed | FAIL | standard deviation missing | cv_accuracy_sd_missing: CV accuracy standard deviation missing · Random Forest (300 trees) · CV accuracy · expected '82.9% ± 2.6%' · actual '82.9%' | yes |
| CV6  CV precision value wrong (+0.010) | FAIL | CV precision differs | CV precision_mismatch: CV precision differs from the independent recomputation · Random Forest (300 trees) · CV precision · expected '0.871' · actual '0.881' | yes |
| CV7  One model row removed (Random Forest) | FAIL | candidate model row missing | row_missing: candidate model row missing · Random Forest (300 trees) · None · expected 1 · actual 0 | yes |
| CV8  One model row duplicated (Random Forest) | FAIL | duplicate model row | row_duplicate: duplicate model row · Random Forest (300 trees) · None · expected 1 · actual 2 | yes |
| CV9  Selected indicator moved to Random Forest | FAIL | exactly one row must be marked selected | selected_indicator: exactly one row must be marked selected — the model chosen by the documented rule · None · None · expected ['Logistic Regression (scaled)'] · actual ['Random Forest (300 trees)'] | yes |
| CV10 Held-out test column added | FAIL | test column | test_column_present: a held-out test column appears in the model-selection table · None · None · expected None · actual ['Test accuracy'] | yes |

### Stored CV values (micro-refinement)

| Control | Expected | Required defect | Reported | As required |
|---|---|---|---|---|
| CV11 Stored CV-accuracy SD + 0.05 (model_comparison row 2) | FAIL | CV accuracy standard deviation mismatch | cv_accuracy_sd_mismatch: CV accuracy standard deviation mismatch · Random Forest (300 trees) · CV accuracy (sd) · expected 0.025818666151887243 · actual 0.07581866615188725 | yes |
| CV12 Stored CV-accuracy SD + 0.0005 (below display precision) | FAIL | CV accuracy standard deviation mismatch | cv_accuracy_sd_mismatch: CV accuracy standard deviation mismatch · Random Forest (300 trees) · CV accuracy (sd) · expected 0.025818666151887243 · actual 0.026318666151887243 | yes |

### Prediction structure (micro-refinement)

| Control | Expected | Required defect | Reported | As required |
|---|---|---|---|---|
| PA Trailing field removed (tier) | FAIL | prediction record has fewer fields than expected | prediction record has fewer fields than expected (record 17) · version=final, record_index=17, expected_fields=6, actual_fields=5, missing_fields=['tier'] | yes |
| PB Extra field appended | FAIL | prediction record contains an unexpected field | prediction record contains an unexpected field (record 17) · version=final, record_index=17, expected_fields=6, actual_fields=7, extra_values=['extra'] | yes |
| PC Intermediate field removed (prob) | FAIL | prediction schema mismatch | prediction schema mismatch (a field is missing inside the record) (record 17) · version=final, record_index=17, expected_fields=6, actual_fields=5, missing_fields=['prob'] | yes |
| PD One record removed | FAIL | prediction collection length mismatch | prediction collection length mismatch · version=final, missing_profile_ids=['real_adult_diners:17'], extra_profile_ids=[] | yes |
| PE One record added | FAIL | prediction collection length mismatch | prediction collection length mismatch · version=final, missing_profile_ids=[], extra_profile_ids=['random_in_range:999999'] | yes |
| PF Identical copy (positive control) | PASS | prediction records match exactly | PASS — prediction records match exactly | yes |
| PG One probability + 1e-12 | FAIL | prediction value mismatch | prediction value mismatch (real_adult_diners:17 · prob) · profile_id=real_adult_diners:17, field=prob | yes |
| PH One profile identifier relabelled | FAIL | prediction/profile correspondence mismatch | prediction/profile correspondence mismatch (record 17) · version=final, record_index=17 | yes |
| PI Two fields swapped (reorder ↔ prob) | FAIL | prediction schema mismatch (field order or type) | prediction schema mismatch (field order or type) (record 17) · version=final, record_index=17, fields_failing_contract=['reorder', 'prob'] | yes |
| PJ Two records swapped (order) | FAIL | prediction/profile correspondence mismatch | prediction/profile correspondence mismatch (record 17) · version=final, record_index=17 | yes |
| PK Field definition changed (header 'prob' → 'probability') | FAIL | prediction field definition differs from the authoritative schema | prediction field definition differs from the authoritative schema · version=supplied_original | yes |

### Checksum assessment on temporary copies (final polish)

| Control | Expected | Required defect | Reported | As required |
|---|---|---|---|---|
| CK0 Unmodified copies of the protected artifacts (positive control) | PASS | all checksum-monitored protected artifacts unchanged | PASS — 9 files, MD5 and SHA-256 equal to reference | yes |
| CK1 One byte appended to a copy of data/raw/diners.csv | FAIL | data/raw/diners.csv · MD5 · FAIL (differs from reference) | data/raw/diners.csv · MD5 · FAIL (differs from reference) | yes |
| CK2 One bit flipped in a copy of food_models.joblib (same size) | FAIL | food_models.joblib · SHA-256 · FAIL (differs from reference) | food_models.joblib · SHA-256 · FAIL (differs from reference) | yes |
| CK3 Copy of app.py deleted | FAIL | app.py · MD5 · FAIL (file missing) | app.py · MD5 · FAIL (file missing) | yes |
| CK4 Copy of dashboard_bundle.joblib changed between the start and end of a run | FAIL | dashboard_bundle.joblib · MD5 · FAIL (changed during the run) | dashboard_bundle.joblib · MD5 · FAIL (changed during the run) | yes |
| CK5 Copy of data/clean/orders_clean.csv changed between the start and end of a run | FAIL | data/clean/orders_clean.csv · SHA-256 · FAIL (changed during the run) | data/clean/orders_clean.csv · SHA-256 · FAIL (changed during the run) | yes |

### Data-quality issue log DQ-01 / DQ-05 (final documentation consistency)

| Control | Expected | Required defect | Reported | As required |
|---|---|---|---|---|
| DQ-A DQ-01 claims the classifier was trained on 460 diners (all five representations) | FAIL | incorrect classifier training population description | FAIL — incorrect classifier training population description | yes |
| DQ-B DQ-01 states 93 held-out test observations instead of 92 | FAIL | incorrect held-out test population description | FAIL — incorrect held-out test population description | yes |
| DQ-C DQ-05 reverted to 'training range' wording | FAIL | obsolete reference-range terminology | FAIL — obsolete reference-range terminology | yes |
| DQ-D One observed adult range maximum changed in a bundle copy (age 52 → 53) | FAIL | observed adult reference range changed | FAIL — observed adult reference range changed | yes |
| DQ-E Export schema with outside_training_range renamed (temporary header copy) | FAIL | batch CSV schema compatibility broken | FAIL — batch CSV schema compatibility broken | yes |
| DQ-F Corrected DQ-01 and DQ-05 entries as shipped (positive control) | PASS | data-quality descriptions are consistent | PASS — data-quality descriptions are consistent | yes |
| DQ-G Unrelated analytical value changed in a bundle copy (accuracy + 0.001) next to the approved DQ changes | FAIL | unexplained analytical difference | FAIL — unexplained analytical difference (/metrics/Accuracy) | yes |
| DQ-H DQ-05 changed in the CSV only (other four representations correct) | FAIL | cross-document mismatch for DQ-05 | FAIL — cross-document mismatch for DQ-05 | yes |

### DQ-05 quantity — independent recalculation (final correction)

| Control | Expected | Required defect | Reported | As required |
|---|---|---|---|---|
| Q-4 DQ-05 Quantity '4 of 7 classifier input controls' (all five representations) | FAIL | incorrect DQ-05 quantity | FAIL — incorrect DQ-05 quantity | yes |
| Q-5 DQ-05 Quantity '5 of 7 classifier input controls' (all five representations) | FAIL | incorrect DQ-05 quantity | FAIL — incorrect DQ-05 quantity | yes |
| Q-7 DQ-05 Quantity '7 of 7 classifier input controls' (all five representations) | FAIL | incorrect DQ-05 quantity | FAIL — incorrect DQ-05 quantity | yes |
| Q-T1 DQ-05 Quantity with a wrong total ('6 of 8 classifier input controls') | FAIL | incorrect DQ-05 quantity | FAIL — incorrect DQ-05 quantity | yes |
| Q-T2 One classifier control missing from the input-limit specification (6 controls) | FAIL | classifier input controls incomplete | FAIL — classifier input controls incomplete | yes |
| Q-B Observed adult range boundary changed (orders_per_month max 20 → 19): recalculation gives 7 of 7, shipped text says 6 of 7 | FAIL | incorrect DQ-05 quantity | FAIL — incorrect DQ-05 quantity | yes |
| Q-U Dashboard input limit changed in both app.py and Governance copies (age max 70 → 52): recalculation gives 5 of 7, shipped '6 of 7' must now be rejected | FAIL | incorrect DQ-05 quantity | FAIL — incorrect DQ-05 quantity | yes |
| Q-S Governance input limits differ from app.py INPUT_SPEC (age max 70 vs 75) | FAIL | dashboard input limits differ between app.py and the Governance page | FAIL — dashboard input limits differ between app.py and the Governance page | yes |
| Q-E DQ-05 explanation table in the report marks orders_per_month as outside | FAIL | DQ-05 explanation table disagrees with the calculation | FAIL — DQ-05 explanation table disagrees with the calculation | yes |
| Q-0 Shipped DQ-05 (6 of 7 classifier input controls) with the real limits and observed ranges (positive control) | PASS | data-quality descriptions are consistent | PASS — data-quality descriptions are consistent | yes |

## Dashboard smoke test

96 PASS · 0 FAIL

| Check | Result | Detail |
|---|---|---|
| App starts without exceptions | PASS | [] |
| Navigation lists the 9 pages in order | PASS | ['Executive Overview', 'Customer Segmentation', 'Basket Intelligence', 'Retention & Churn', 'Retention Economics', 'Diner Intelligence', 'Wh |
| Sidebar status card rendered | PASS |  |
| Page renders with expected content: Executive Overview | PASS | exceptions=[] charts=6 (≥6) tables=0 (≥0) marker='Revenue Concentration Curve' found=True |
| Page renders with expected content: Customer Segmentation | PASS | exceptions=[] charts=11 (≥10) tables=2 (≥2) marker='Who are QuickBite' found=True |
| Page renders with expected content: Basket Intelligence | PASS | exceptions=[] charts=4 (≥4) tables=3 (≥3) marker='Basket opportunity matrix' found=True |
| Page renders with expected content: Retention & Churn | PASS | exceptions=[] charts=10 (≥10) tables=2 (≥2) marker='At-risk watch-list' found=True |
| Page renders with expected content: Retention Economics | PASS | exceptions=[] charts=3 (≥3) tables=1 (≥1) marker='Target list' found=True |
| Page renders with expected content: Diner Intelligence | PASS | exceptions=[] charts=1 (≥1) tables=0 (≥0) marker='Recommended items' found=True |
| Page renders with expected content: What-If Simulator | PASS | exceptions=[] charts=2 (≥2) tables=1 (≥1) marker='Standard scenario library' found=True |
| Page renders with expected content: Recommendations | PASS | exceptions=[] charts=1 (≥1) tables=3 (≥3) marker='30-day operating plan' found=True |
| Page renders with expected content: Governance & Data Quality | PASS | exceptions=[] charts=3 (≥3) tables=9 (≥8) marker='Live artifact checks' found=True |
| Every chart uses the registered QuantFin template with transparent backgrounds (no default/white plots) | PASS | 41 charts |
| Segment colours and marker symbols identical on every chart | PASS | 80 traces checked |
| Risk-tier colours follow teal / slate / amber / coral | PASS | [] |
| Segmentation distribution selector — all 7 features | PASS | [] |
| Basket segment selector — all 3 segments | PASS | [] |
| Watch-list with no segment selected → empty table, no crash | PASS | rows=[0] |
| Economics with no segment in scope → guidance message, no crash | PASS |  |
| Economics with a single low-value segment (few/no profitable targets) | PASS | [] |
| Retention Economics: ec_cost = 0.0 | PASS | [] |
| Retention Economics: ec_cost = 200.0 | PASS | [] |
| Retention Economics: ec_margin = 0.05 | PASS | [] |
| Retention Economics: ec_margin = 0.6 | PASS | [] |
| Retention Economics: ec_su = 0.0 | PASS | [] |
| Retention Economics: ec_su = 0.5 | PASS | [] |
| Retention Economics: ec_sl = 0.0 | PASS | [] |
| Retention Economics: ec_sl = 0.5 | PASS | [] |
| Retention Economics: ec_h = 1 | PASS | [] |
| Retention Economics: ec_h = 12 | PASS | [] |
| Retention Economics: probability cut-off slider = 0.05 | PASS | [] |
| Retention Economics: probability cut-off slider = 1.0 | PASS | [] |
| Diner input orders_per_month = 1: segment, probability and recommendations match the model | PASS | model Premium Foodies 0.3560; shown 36 |
| Diner input orders_per_month = 20: segment, probability and recommendations match the model | PASS | model Budget Students 0.9727; shown 97 |
| Diner input avg_order_value = 15.0: segment, probability and recommendations match the model | PASS | model Premium Foodies 0.8632; shown 86 |
| Diner input avg_order_value = 250.0: segment, probability and recommendations match the model | PASS | model Family Feasters 0.2731; shown 27 |
| Diner input avg_items_per_order = 1: segment, probability and recommendations match the model | PASS | model Premium Foodies 0.6502; shown 65 |
| Diner input avg_items_per_order = 10: segment, probability and recommendations match the model | PASS | model Family Feasters 0.8878; shown 89 |
| Diner input days_since_last_order = 0: segment, probability and recommendations match the model | PASS | model Premium Foodies 0.9616; shown 96 |
| Diner input days_since_last_order = 60: segment, probability and recommendations match the model | PASS | model Family Feasters 0.0000; shown 0 |
| Diner input discount_rate = 0.0: segment, probability and recommendations match the model | PASS | model Premium Foodies 0.5219; shown 52 |
| Diner input discount_rate = 1.0: segment, probability and recommendations match the model | PASS | model Budget Students 0.9495; shown 95 |
| Diner input age = 18: segment, probability and recommendations match the model | PASS | model Premium Foodies 0.7126; shown 71 |
| Diner input age = 70: segment, probability and recommendations match the model | PASS | model Premium Foodies 0.7471; shown 75 |
| Diner input total_spend = 50.0 | PASS | [] |
| Diner input total_spend = 20000.0 | PASS | [] |
| Diner preset 'App default (typical diner)' | PASS | [] |
| Diner preset 'Typical Premium Foodie' | PASS | [] |
| Diner preset 'Typical Family Feaster' | PASS | [] |
| Diner preset 'Typical Budget Student' | PASS | [] |
| Diner preset 'Lapsed Family Feaster' | PASS | [] |
| Diner preset 'Uncertain Premium Foodie (coin-flip)' | PASS | [] |
| Diner preset 'Look up an existing diner…' | PASS | [] |
| Batch scoring: example file (11 rows, 2 under-18 flagged, 9 scored) | PASS | {'Scored': 9, 'Not scored — under 18 (18+ policy)': 2} |
| Download buttons present (template + scored file) | PASS | 2 |
| Batch scoring: missing columns → clear error message | PASS | Missing required columns: orders_per_month, avg_order_value, avg_items_per_order, days_since_last_order, discount_rate, total_spend |
| Batch scoring: non-numeric value → row flagged, not scored | PASS | Not scored — missing / non-numeric value |
| Batch scoring: empty file → no crash, zero rows | PASS |  |
| What-If template 'Custom': before / after / change cards | PASS | cards=3 |
| What-If template 'A · Retention intervention': before / after / change cards | PASS | cards=3 |
| What-If template 'B · Discount strategy': before / after / change cards | PASS | cards=3 |
| What-If template 'C · Higher engagement': before / after / change cards | PASS | cards=3 |
| What-If template 'D · Premium behaviour': before / after / change cards | PASS | cards=3 |
| What-If template 'E · Recovery': before / after / change cards | PASS | cards=3 |
| What-If sensitivity: every input can be varied | PASS | [] |
| What-If: total spend unlinked (free input) | PASS |  |
| What-If input wi_orders_per_month = 1.0 | PASS | [] |
| What-If input wi_orders_per_month = 20.0 | PASS | [] |
| What-If input wi_days_since_last_order = 0.0 | PASS | [] |
| What-If input wi_days_since_last_order = 60.0 | PASS | [] |
| What-If input wi_avg_order_value = 15.0 | PASS | [] |
| What-If input wi_avg_order_value = 250.0 | PASS | [] |
| What-If 'Reset to base diner' button | PASS |  |
| Risk tiers at exact boundaries (25 / 50 / 75 %) follow the documented bands | PASS | {} |
| Five-feature clustering contract | PASS |  |
| Seven-feature classifier contract (order unchanged) | PASS |  |
| Independent preprocessing (cluster scaler ≠ classifier scaler) | PASS |  |
| predict() and predict_proba() both work and agree at the 0.5 cut-off | PASS |  |
| Every segment returns recommended items | PASS |  |
| Governance live artifact checks all PASS | PASS | {'Check': ['Artifact keys', 'Clustering features = 5, contract order', 'Cluster scaler expects 5 features', 'Classifier expects 7 features ( |
| Overview: repeated-CV KPI labelled as such and paired with its own 58.5% baseline | PASS | ('85.8%', 'Post-selection stability check ± 3.0% · its baseline 58.5% · AUC 0.94') |
| Retention: no 'expected real-world accuracy' claim for repeated CV | PASS |  |
| Retention: note separates selection, independent test evaluation and post-selection stability check (no nested CV) | PASS |  |
| Retention: repeated-CV KPI uses the 58.5% baseline, test KPI uses the 58.7% baseline | PASS | {'Repeated-CV accuracy': ('85.8%', 'Stability check, 50 fits ± 3.0% · its baseline 58.5%'), 'Test-split accuracy': ('90.2%', 'Held-out · 95% |
| Governance: selection-CV chart compares with the training-set baseline (58.4%) | PASS | ['majority-class share (training set) 58.4%'] |
| Governance model card: held-out test row marked independent; repeated CV marked post-selection, not nested | PASS |  |
| Governance: 'Analysis population' KPI shows 480 → 460 adult classifier → 368 training + 92 test (independent recount); no 'Training data' KPI | PASS | {'shown': ('480', '480 diners · 460 adult classifier population · 368 training observations · 92 test observations'), 'expected': ('480', '4 |
| Range A: reference range = min–max over the adult classifier-eligible diners (independent recount), not the training split | PASS | {'n_reference': 460, 'differs_from_368_split': ['avg_order_value', 'age']} |
| Range C: every feature minimum and maximum identical to the previous submission (exact) | PASS | {'now': {'orders_per_month': (1.0, 20.0), 'avg_order_value': (29.5, 218.66), 'avg_items_per_order': (1.0, 9.0), 'days_since_last_order': (0. |
| Range B/F: Governance shows 'Observed adult classifier range' (same values), the 460 = 368 + 92 note, and no 'training range' wording (feature table, note, DQ-05) | PASS | {'feature_table': True, 'note': True, 'dq05': {'ID': 'DQ-05', 'Dataset': 'diners', 'Issue': 'Dashboard inputs may fall outside the observed  |
| Range F: scoring-page warning reads 'Observed adult reference-range warning … observed adult range' | PASS | ['Days since last order = 60 (observed adult range 0–34)'] |
| Range F: What-If warning reads 'Outside the observed adult range' | PASS |  |
| Batch D/E (mixed_valid_and_invalid): export byte-identical to the previous submission (schema incl. 'outside_training_range' where rows are scored, field values, segments, probabilities, tiers, flagged rows) | PASS | {'bytes_now': 2884, 'bytes_before': 2884, 'field_present': True} |
| Batch D/E (under18_only): export byte-identical to the previous submission (schema incl. 'outside_training_range' where rows are scored, field values, segments, probabilities, tiers, flagged rows) | PASS | {'bytes_now': 340, 'bytes_before': 340, 'field_present': False} |
| Range F: batch table on screen shows 'Outside observed adult range' (technical name only in the export) | PASS | ['diner_id', 'status', 'segment', 'p_reorder', 'will_reorder', 'risk_tier', 'action', 'recommended_items', 'Outside observed adult range'] |
| Governance issue log: DQ-01 / DQ-05 identical to the regenerated issue-log CSV; DQ-01 names 460 eligible = 368 training + 92 held-out test; no runtime text substitution in app.py | PASS | {'DQ-01 impact': 'Classifier-eligible population: 460 adult diners (368 training observations and 92 held-out test observations)'} |

## Not tested

- Every check listed in the tables above ran in this run; a check that cannot run is labelled NOT TESTED and makes the overall result FAIL. Outside the automated checks:
- The batch CSV upload in a browser is not part of this run (AppTest cannot drive the uploader; `score_frame`, which the upload calls, is tested directly here). It is covered by the separate browser-level test `browser_upload_test.py` (needs a running app; last run 05 Nov 2026, 22:02, Chromium 153.0.8010.12 (headless, Playwright): PASS, 24 PASS / 0 FAIL, evidence in `validation/browser_upload_test/`). A person repeating the upload by hand (README, Validation) is a manual test and is not recorded here.
- Pixel-level appearance; see `submission_assets/dashboard_screenshots/`.
- Predictions of the previous submission's app are not re-run: its model artifact is byte-identical and its `analyse()` logic is identical to the final one (both checked).
