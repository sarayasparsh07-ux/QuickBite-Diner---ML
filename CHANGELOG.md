# Change log

## Final Documentation Corrections — Control-Case Counts (5 Nov 2026, final)

Documentation only. No code, data, model, bundle, notebook, report generator or validation logic changed.

Both figures were checked against the latest results before editing:
* **DQ-05 cases:** `negative_controls.py` (group `dq05_quantity`) defines 10 cases: 9 expected to FAIL (Q-4, Q-5, Q-7,
  Q-T1, Q-T2, Q-B, Q-U, Q-S, Q-E) and 1 expected to PASS (Q-0, the shipped "6 of 7 classifier input controls").
  `validation/negative_controls_results.json` records all 10 behaving as required.
* **Total:** the same file records 73 control cases, all behaving as required: framework 25, checksum 6, DQ issue log 8,
  DQ-05 quantity 10, CV display 11, CV stored values 2, prediction structure 11 (25 + 6 + 8 + 10 + 11 + 2 + 11 = 73).

| # | File | Previous wording | Corrected wording |
|---|---|---|---|
| C1 | `CHANGELOG.md` (DQ-05 section below), `reports/submission_readiness_assessment.md` (DQ-05 section) | "New negative controls (10 …)" / "10 new negative controls" | "10 new DQ-05 quantity control cases: nine negative cases and one positive control" |
| C2 | `reports/submission_readiness_assessment.md`, Validation evidence rating | "52 controls, each required to name its specific defect" | "73 control cases across the framework, checksum, data-quality, DQ-05 quantity, cross-validation and prediction-structure checks (25 + 6 + 8 + 10 + 11 + 2 + 11); all 73 behaved as expected …" |

Historical figures are kept where they were true at the time. These include "52/52 controls" in the dated 5 Nov
final-polish record, 43, 55 and 63 in the earlier entries, and the totals inside each earlier change-log section. The
rating stays at 9 / 10.

---

## Final Refinement — DQ-05 Input-Range Count Correction (5 Nov 2026, late night)

### What was wrong

DQ-05 recorded its Quantity as **"4 inputs"**. The earlier validator only required that field to stay equal to its
baseline, so the wrong count passed every run.

An independent comparison of the seven classifier input controls gives a different answer. Each control's permitted
dashboard range (`INPUT_SPEC` in `app.py`) was compared with its observed adult classifier range, the minimum–maximum
over the 460 classifier-eligible adults. A control counts once if `ui_min < observed_min or ui_max > observed_max`.

| Feature | Dashboard input range | Observed adult classifier range | Counted |
|---|---|---|---|
| orders_per_month | 1–20 | 1–20 | no (exact match) |
| avg_order_value | 15–250 | 29.5–218.66 | yes |
| avg_items_per_order | 1–10 | 1–9 | yes |
| days_since_last_order | 0–60 | 0–34 | yes |
| discount_rate | 0–1 | 0–0.86 | yes |
| age | 18–70 | 18–52 | yes |
| total_spend | 50–20,000 | 134.04–1,490.17 | yes |

Result: **6 of 7 classifier input controls**.

### Correction at the source (`build/notebook_source.py`)

* **Count derived, not typed.** The issue-log cell now builds the 7-row comparison from `APP_INPUT_RANGES` and the 460
  adults, and derives the quantity from it.
  * The notebook asserts that `APP_INPUT_RANGES` equals `INPUT_SPEC` parsed from `app.py`.
  * The 460 adults are `diners.loc[diners.include_in_classifier]`, the same population as `train_ranges`.
* **DQ-05 Quantity:** `4 inputs` → `6 of 7 classifier input controls`.
* **DQ-05 Treatment.** It now states explicitly that out-of-range values remain permitted by the input limits and are only
  flagged: "Values outside it remain permitted by the dashboard input limits (INPUT_SPEC); the dashboard shows an
  observed adult reference-range warning …".
* **DQ-05 Issue.** The text is unchanged; its quoted numbers are now formatted from the same values instead of being
  typed.
* **ID, dataset, classification and impact:** unchanged.
* **Data-quality report.** `reports/data_quality_report.md` gains a section, "DQ-05 — how the quantity is calculated". It
  gives:
  * the counting rule: once per control, either bound;
  * that a control is not counted when its range lies within or exactly matches the observed range;
  * that the range uses all 460 eligible adults;
  * that out-of-range values stay permitted;
  * the 7-row table, and that `orders_per_month` is the only exact match.
* **Notebook output.** The comparison table is also displayed in the notebook.

### Regenerated (in a scratch copy first, compared, then copied in)

* **Notebook:** of its 91 cells, only the issue-log cell's output changed; the issue-log and report cells' sources
  changed. It executed without errors.
* **Bundle:** of 17,657 values, exactly 2 differ: the DQ-05 row (Quantity and Treatment) and `meta.trained_at`
  (05 Nov 2026, 21:13 → 21:56).
* **Reports:** the issue-log CSV and the data-quality report were regenerated, the report with the new section.
  `model_evaluation_report.md` changed only in the timestamp line.
* **Byte-identical:** `food_models.joblib`, raw and cleaned data, all 17 figures.
* **`app.py`:** not modified. The Governance page displays the regenerated bundle, and `INPUT_SPEC` is untouched.
* **Screenshots:** all 15 regenerated, because the training timestamp changed; every image is the same size.

### Validation

* **Independent recalculation (`dq_consistency.py`).** The DQ-05 Quantity is no longer compared with an earlier value.
  * The validator parses `INPUT_SPEC` from `app.py` with `ast`, reads the limits shown on the Governance page, and
    requires the two to agree.
  * It recounts the observed adult classifier range from `data/clean/diners_clean.csv` (460 adults).
  * It applies the either-bound rule once per control, builds `"<counted> of <controls> classifier input controls"`, and
    requires every representation's Quantity to equal it.
  * It also confirms:
    * the controls are exactly the 7 classifier features, matching `food_models.joblib` features + age + total_spend;
    * the calculation equals the documented expectation (7 · 6 outside · 1 within, `orders_per_month`);
    * the report's explanation table matches row by row.
  * The DQ-05 baseline-equality check keeps ID, dataset, classification and impact; only Quantity left it. The issue
    numbers, terminology and cross-document checks are unchanged. 23/23 checks pass.
* **Approved differences.**
  * The DQ05 entries (bundle row and Governance row) are exact before/after rows.
  * When the whitelist is built, it asserts that the approved Quantity equals the independent calculation.
  * For the new comparison, it asserts that only Quantity and Treatment changed.
  * Nothing else is exempted.
* **New baseline v6** (`*_v6_dq_correction.*`). The strict comparison *dq correction → final* finds 88 differences:
  86 TS (timestamp), 2 DQ05 and 0 unexplained.
* **10 new DQ-05 quantity control cases: nine negative cases and one positive control (group `dq05_quantity`):**
  * Quantity "4 of 7", "5 of 7", "7 of 7" and "6 of 8" → FAIL, incorrect DQ-05 quantity.
  * One control missing from the limits → FAIL, classifier input controls incomplete.
  * Observed `orders_per_month` max 20 → 19: recalculation gives 7 of 7 → FAIL.
  * UI age max 70 → 52: recalculation gives 5 of 7, so the shipped "6 of 7" is rejected. This shows the check is a
    calculation, not a stored answer.
  * Governance limits ≠ `app.py` → FAIL.
  * Explanation table altered → FAIL.
  * Positive control, as shipped ("6 of 7 classifier input controls" with the real limits and ranges) → PASS.
* **Totals:** all 63 earlier control cases still pass, so 73/73.

**Final run (5 Nov 2026, late night):** overall **PASS**, exit status 0.
* All 7 comparisons have 0 unexplained differences.
* Smoke test 96/96.
* Controls 73/73.
* DQ consistency 23/23.
* Predictions: 10,358 comparisons identical.
* Browser CSV test 24/24, with the export byte-identical to the earlier reference.
* All 15 Python files compile (13 validation scripts, `app.py`, `build/notebook_source.py`).

**Unchanged:** raw and cleaned data; the model (`food_models.joblib` MD5 `7b1f8a39…`, interface
`{scaler, kmeans, segment_names, clf, features, reco}`); the split; predictions and probabilities; all metrics; rules,
financial and What-If results; `INPUT_SPEC`; the observed ranges; `train_ranges`; `outside_training_range`; and the
on-screen wording "Outside observed adult range".

| File | MD5 before | MD5 after |
|---|---|---|
| `build/notebook_source.py` | `bdf63fab9798f23347059e17c72902f7` | `d0a5937da73fc6e2de67d0b99c4ba200` |
| `QuickBite_Analysis.ipynb` | `d85c23e5d875b686bf505175263f3b51` | `67e51531c3628c6e51da7eb8e12b6dfa` |
| `dashboard_bundle.joblib` | `95f6e6f9a5e39dade4f50c74950f34cb` | `202bb66471fea96a3e6fde3aef08e47a` |
| `reports/data_quality_issue_log.csv` | `d0233c1d63303c55baff41e5d6585765` | `0feba62f473188a671a1cb65267957db` |
| `reports/data_quality_report.md` | `fab0547be0bf1cf6ea9eb3a621ed9d5c` | `61a65d829075aae7296940f8f613c702` |
| `reports/model_evaluation_report.md` | `89f028701033b8a04784541cfcc67ddc` | `e5188e2dd7e96b953db0a013749f7bfa` (timestamp only) |
| `app.py`, `food_models.joblib`, `data/**` | — | identical |

The three protected references that changed (notebook source, bundle, notebook) were updated in
`validation/protected_checksums.json`, and the previous values are kept in its `history`. "4 inputs" now appears only as
a recorded *before* value in the whitelist, the before/after reports and the frozen baselines.

---

## Final Documentation Consistency — DQ-01 and DQ-05 (5 Nov 2026, night)

The data-quality issue log has one source: the `issue_log` table in `build/notebook_source.py`. Executing the notebook
writes it to `reports/data_quality_issue_log.csv`, to the "Issue log & treatments" table of
`reports/data_quality_report.md` and to `dashboard_bundle.joblib` (`dq.issue_log`). The Governance page displays the
bundle's table. Both entries were corrected at that source and the dependent artifacts regenerated. No generated file was
edited by hand.

### DQ-01: classifier population

| | Text (Impact column) |
|---|---|
| Incorrect original | "Classifier trained on 460 adult diners" |
| Corrected | "Classifier-eligible population: 460 adult diners (368 training observations and 92 held-out test observations)" |

The 460 adults are the classifier-eligible population. The classifier was fitted, and selected, on the 368 training
observations; the other 92 are the held-out test set. The three numbers are computed in the notebook, not typed:
* `n_eligible` comes from `include_in_classifier`.
* The test count is ceil(0.20 · n), the rule `train_test_split(test_size=0.20)` uses.
* §10 asserts that the actual split has exactly these sizes.

Unchanged: ID, dataset, issue, quantity ("1 diner (D1052, age 9)"), classification, treatment, the eligibility flag and
the split.

### DQ-05: observed adult classifier range

| Field | Obsolete | Corrected |
|---|---|---|
| Issue | "Dashboard input ranges exceed training ranges (e.g. recency ≤60 vs max 34; spend ≤20,000 vs max 1,490)" | "Dashboard inputs may fall outside the observed adult classifier range (input limits exceed it, e.g. recency ≤60 vs max 34; spend ≤20,000 vs max 1,490)" |
| Treatment | "Dashboard shows an extrapolation warning when inputs fall outside the training range." | "Dashboard shows an observed adult reference-range warning when an input falls outside the feature range calculated from the 460 adult classifier-eligible diners." |

The quoted values (≤60 / 34, ≤20,000 / 1,490) and the ranges themselves are unchanged. They are still computed from
`diners.loc[diners.include_in_classifier]` (460 adults) and are identical to the previous bundle. Quantity,
classification and impact are unchanged.

### Artifact regeneration and code paths

* **Source edited:** `build/notebook_source.py`.
  * The DQ-01 and DQ-05 text.
  * Three population variables for the issue log.
  * One `assert` after the train/test split. This adds no logic and changes no result.
* **Regenerated** with the project's own process: `build/make_notebook.py`, then
  `jupyter nbconvert --execute --inplace` (run first in a scratch copy, compared, then copied in).
  * **Notebook.** Of its 91 cells, only the issue-log cell's output changed, plus the source of that cell and of the split
    cell. Every other output is identical; only execution timestamps in cell metadata differ.
  * **Bundle.** Of 17,657 values, exactly 3 differ: the DQ-01 row, the DQ-05 row and `meta.trained_at`
    (31 Oct 2026, 20:06 → 05 Nov 2026, 21:13).
  * **Reports.** The issue-log CSV changed in those 2 rows only. The data-quality report changed in those 2 rows, its
    table padding and its "Generated" date.
  * **`model_evaluation_report.md`** was regenerated with `build/make_model_evaluation_report.py`; only the training
    timestamp in line 3 changed.
* **Byte-identical after re-execution:** `food_models.joblib`, `data/clean/*.csv`, `data/raw/*.csv` and all 17 figures in
  `reports/figures/`.
* **`app.py`:** the runtime DQ-05 text substitution (`DQ_DISPLAY_WORDING`) added in the previous correction is removed.
  The bundle now carries the final wording, so the issue log is displayed from the bundle as it was originally
  (`table(dq["issue_log"], height=380)`). There is one authoritative text, and the layout and styling are unchanged.
* **Screenshots:** all 15 regenerated, because the sidebar and Governance show the new training timestamp. Every image
  has the same size as before.

### What did not change

The original data, the cleaned data and the trained model (`food_models.joblib` byte-identical, MD5 `7b1f8a39…`) are
all unchanged. So are:
* the predictions and probabilities (10,358 comparisons identical);
* the performance metrics, financial calculations, What-If scenarios and recommendations;
* the feature ranges;
* the batch export: the browser download is byte-identical to the previous submission's, including
  `outside_training_range`.

The bundle's only non-text change is the documented regeneration timestamp (TS).

### Validation added

* **`dq_consistency.py`.** It checks DQ-01 and DQ-05 in five representations: the notebook's rendered table (pandas
  truncates long cells there, so a truncated prefix is accepted), the CSV, the Markdown report, the bundle and the
  Governance dashboard.
  * Each entry exists exactly once, all five agree, and the notebook cells equal those generated from the source.
  * DQ-01: unchanged fields, plus 460 / 368 / 92 equal to an independent recount.
  * DQ-05: unchanged fields and values, corrected terminology and the 460 reference population.
  * The ranges equal the 460-adult recount and the previous bundle; the export schema equals the reference.
* **Approval codes DQ01 / DQ05.**
  * Each covers only the two issue-log rows in the bundle and in the Governance table.
  * Each is an exact before → after entry whose "after" must equal the CSV row, asserted when the whitelist is built.
  * The pre-redesign numeric comparison accepts exactly the numbers those rows add (368, 92, 460).
* **Negative controls DQ-A … DQ-H (8, in memory):**
  * A — "trained on 460": FAIL, incorrect classifier training population description.
  * B — 93 test observations: FAIL, incorrect held-out test population description.
  * C — old DQ-05 wording: FAIL, obsolete reference-range terminology.
  * D — one range maximum changed: FAIL, observed adult reference range changed, and the strict comparison also fails.
  * E — `outside_training_range` renamed: FAIL, batch CSV schema compatibility broken.
  * F — as shipped: PASS, data-quality descriptions are consistent.
  * G — accuracy + 0.001 next to the approved DQ changes: FAIL, unexplained analytical difference.
  * H — the CSV alone changed: FAIL, cross-document mismatch.
* Control H14 was updated to the new DQ-05 wording, because the old mutation no longer applied.
* **New smoke check:** the Governance DQ-01 / DQ-05 rows equal the CSV, and there is no runtime substitution.
* **New baseline v5** (`*_v5_range_correction.*`). The strict comparison *range correction → final* finds 90
  differences:
  * 86 metadata-only (TS: the timestamp KPI and timestamp digits);
  * 2 analytics-bundle descriptive (DQ01, DQ05);
  * 2 presentation (the two Governance rows);
  * 0 unexplained.

**Final validation (5 Nov 2026, night):**
* CV validation PASS; prediction schema PASS; prediction values PASS.
* Observed adult range (A–F) PASS.
* **Data-quality issue log consistency PASS.**
* Checksum integrity PASS.
* Negative controls **63/63**: the 55 earlier ones plus 8 new.
* Smoke test **96/96**: the 95 earlier checks, which include the original 86, plus 1 new.
* Browser CSV test **24/24**.
* 0 unexplained differences in all six comparisons; **Overall PASS**, exit status 0.

**Checksums (MD5)**

| File | Before | After | Note |
|---|---|---|---|
| `data/raw/*.csv`, `data/clean/*.csv` | `11ba8cfa…`, `776f6642…`, `01ee01ca…`, `2188c9e4…` | identical | |
| `food_models.joblib` | `7b1f8a39310cc735d15cbc3f89754045` | identical | |
| `build/notebook_source.py` | `2e0900fece1ac20a6f2f38b6a03a7c05` | `bdf63fab9798f23347059e17c72902f7` | source correction |
| `QuickBite_Analysis.ipynb` | `499654cb2693956c2c670db3d8e3dd63` | `d85c23e5d875b686bf505175263f3b51` | regenerated |
| `dashboard_bundle.joblib` | `abf4ea91f1ec59142a92b43f5ce1f5ad` | `95f6e6f9a5e39dade4f50c74950f34cb` | 2 DQ rows + timestamp |
| `reports/data_quality_issue_log.csv` | `288d0e212cd110ca5611a42cb97e859e` | `d0233c1d63303c55baff41e5d6585765` | regenerated |
| `reports/data_quality_report.md` | `55006a0c43623c53058bead07a8dfa69` | `fab0547be0bf1cf6ea9eb3a621ed9d5c` | regenerated |
| `reports/model_evaluation_report.md` | `e895e2b6e533eb2f175b707f6491b18e` | `89f028701033b8a04784541cfcc67ddc` | timestamp only |
| `app.py` | `dec5e977ff55da2ebd73a20941fada34` | `e01606439b07fc2c89ef8d838701caf1` | substitution removed |

`validation/protected_checksums.json` was updated for the four protected files that changed on purpose (MD5 + SHA-256).
The previous values are kept in its `history`.

---

## Final Micro-Correction — Observed Adult Classifier Range Terminology (5 Nov 2026, evening)

**Why it was needed.** The feature reference ranges are computed as
`diners.loc[diners.include_in_classifier, c].min() / .max()`. That covers all **460 adult classifier-eligible diners**:
the 368 training and 92 held-out test observations together. The dashboard called them "training ranges", which
suggests a 368-row training-only range. The two genuinely differ (average order value minimum 29.50 vs 29.84; age
maximum 52 vs 50). So the label, not the number, was wrong.

**What changed.** Wording on screen only. `app.py` is the only analytical-project file edited.

| Where (app.py) | Previous wording | Corrected wording |
|---|---|---|
| Governance → Feature contract, column | Training range | **Observed adult classifier range** |
| Governance → note under that table | "Inputs outside the training range trigger an extrapolation warning … The training range is the observed minimum–maximum across all 460 adult classifier diners …" | "The observed adult classifier range is calculated using all 460 adult classifier-eligible diners, including both the 368 training observations and the 92 held-out test observations. It represents an observed population reference range, not a training-only range. Inputs outside it trigger an observed adult reference-range warning …" (counts read from the bundle's `meta`) |
| Diner Intelligence → scoring warning | "Extrapolation warning: outside the range the models were trained on — … (training range lo–hi)" | "Observed adult reference-range warning: outside the observed adult classifier range — … (observed adult range lo–hi)" |
| What-If Simulator → warning | "Outside the training data:" | "Outside the observed adult range:" |
| Diner Intelligence → batch table heading (screen only) | outside_training_range | Outside observed adult range |
| Governance → issue log, DQ-05 (display) | "… exceed training ranges …" / "… outside the training range." | "… exceed the observed adult classifier ranges …" / "… an observed adult reference-range warning … outside the observed adult classifier range." |
| Diner Intelligence → looked-up diner note (found during the inspection) | "the final model, which was trained on 80% of diners" | "trained on the 368 training observations (80% of the 460 adult diners)". The old phrase implied 80% of all 480 diners. |

**What did not change:**
* The ranges and their calculation. All 7 minimums and maximums are identical (test C), still from the 460 adult
  diners (test A).
* Scaling, preprocessing, input limits, the 5- and 7-feature contracts, the classifier, every prediction and
  probability, the risk thresholds and every metric.
* The exported CSV. Its schema, position and logic are unchanged, including the technical field
  `outside_training_range`. Despite the brief's wording, that field is not Boolean: it lists the inputs outside the range
  by business name, comma-separated, and is empty when all inputs are inside it. As before, it is added only when at least
  one row is scored.
* The browser download of the batch file is byte-identical to the previous submission's (tests D/E).
* Technical names `train_ranges` (notebook and bundle) and `outside_training_range` (export) are kept for backward
  compatibility.
* The notebook, its source and the notebook-generated data-quality report and log are unchanged. They still say
  "training ranges" in DQ-05. Correcting them would require re-executing the notebook, which rewrites the frozen
  `dashboard_bundle.joblib`. The README explains the term, and the dashboard's issue log shows the corrected wording.

| Effect on | Raw data | Cleaned data | Models | Predictions / probabilities | Feature ranges | Metrics | Exported CSV schema | Dashboard | Documentation / validation |
|---|---|---|---|---|---|---|---|---|---|
| This correction | No | No | No | No | No (identical) | No | No (byte-identical export) | Wording on 3 pages: Governance, Diner Intelligence, What-If | README (range definition, export data dictionary, DQ-05 note), validation (below) |

**Regression tests added (all PASS in the final run):**
* **A — reference population:** smoke check. The stored ranges equal min–max of the 460 adult diners, recounted from the
  cleaned data, and differ from the 368-row split.
* **B / F — wording:** smoke checks. The Governance column, the note and DQ-05 use the new terms, with no "training range"
  anywhere on the page. The scoring and What-If warnings and the batch table heading use the corrected wording.
* **C — values:** smoke check. Every minimum and maximum is identical to the previous submission's bundle. The strict
  bundle comparison also finds 0 changed values.
* **D / E — export and predictions:** smoke check. `score_frame` on the previous submission's browser-test inputs
  produces CSV bytes identical to what that submission served for download. This covers schema, the
  `outside_training_range` values, segments, probabilities, tiers, invalid and under-18 rows.
* **Browser test:** `browser_upload_test.py` now takes a reference folder. It passes 24/24, including all three downloads
  byte-identical to `validation/baselines/batch_export_v4_final_polish/`.
* **Approval rule T2:** a heading change passes only as an exact approved relabel, with the same columns and order and
  every cell identical. The DQ-05 wording is one exact before/after entry. The looked-up note may add exactly 368 and 460.
* **New controls:**
  * H12: relabel plus one changed value → FAIL.
  * H13: unapproved heading → FAIL.
  * H14: DQ-05 wording reverted in one cell → FAIL.
* **New baseline v4** (`*_v4_final_polish.*`). The strict comparison *final polish → final* finds 27 differences, all T2:
  * 8 Governance feature-table records;
  * 12 batch-table records;
  * 1 DQ-05 row;
  * 6 note-number records.

**Final validation (5 Nov 2026):**
* CV validation PASS; prediction schema PASS; prediction values PASS (10,358 comparisons identical).
* Observed adult range terminology (A–F) PASS.
* Checksum integrity PASS.
* Negative controls 55/55, including all 52 earlier ones.
* Smoke test 95/95, including all 87 earlier checks.
* 0 unexplained differences in all five comparisons; **Overall PASS**, exit status 0.

**Checksums:** the data files, `food_models.joblib`, `dashboard_bundle.joblib`, the notebook and its source are
unchanged; see the table in the next section. `app.py`: MD5 `75a40a85ca985a3b84d2f08156839217` → `dec5e977ff55da2ebd73a20941fada34`
(SHA-256 `9dd7f8792c01e5b4727538042059d96f329dc435a8ac8fb68be8394cd764d476`). The reference in
`validation/protected_checksums.json` was updated, and the previous value is kept in its `history`. No timestamp or
metadata changed.

---

## Final Submission Polish — Population Terminology, Environment Scope and Checksum Reporting (5 Nov 2026)

Scope: three housekeeping corrections. Nothing analytical was edited and the model was not retrained. The data files,
`food_models.joblib`, `dashboard_bundle.joblib`, the notebook and its source have the same checksums before and after.
`app.py` changed only in the Governance population card and one note on the same page. The previous submission is
frozen as `validation/baselines/*_v3_micro_refinement.*`. The strict comparison against it finds exactly 4 differences,
all classified T1 and nothing unexplained. Full results: `reports/before_after_validation_report.md`.

| # | Change | Raw data | Cleaned data | Models | Predictions / probabilities | Metrics, KPI calculations | Dashboard | Documentation / validation |
|---|---|---|---|---|---|---|---|---|
| F1 | **Governance population KPI.** <br>Previous: card *Training data*, value `480 diners`, context `460 in classifier · 1,980 baskets`. This was misleading because 480 is the whole analysis population; the classifier was trained on 368 diners. <br>New: card *Analysis population*, value `480`, context `480 diners · 460 adult classifier population · 368 training observations · 92 test observations`. <br>Breakdown: 480 total → 460 adult classifier population (20 under-18 diners excluded by the 18+ policy) → 368 training + 92 test (stratified 80/20 split). <br>The four numbers are read from `dashboard_bundle.joblib` → `meta` (`n_diners`, `n_model_rows`, `n_train`, `n_test`), which the notebook writes. Nothing is hard-coded and no calculation changed. The card keeps its styling, size and typography. Its icon is set to the population icon already used for *Total diners* (the old icon was chosen by the word "training"). The basket count is still shown in the page header chip and on the Executive Overview. <br>**Terminology sweep:** the app, README, notebook source and reports were searched for *training data / population / set*, *total diners*, *classifier population* and *test population*. Every use was checked and found correct except one: the Governance *Feature contract* table's "Training range" is the observed range across all 460 adult classifier diners, not only the 368 training rows. The note under that table now says so, using the same `meta` counts. The column names `Training range` and `outside_training_range` are unchanged, because renaming them would change the batch export schema. | No | No | No | No | No (same counts, same sources) | Governance page: one KPI card's label / value format / context, one note | New code **T1** in the approved-difference whitelist (one exact KPI-rename entry; the value may only lose its unit word, and the number is asserted identical; exact lists of the numbers that appear or disappear on the page). New baseline v3 and strict comparison *micro refinement → final*. Smoke check 87: recounts 480 / 460 / 368 / 92 independently from the cleaned data and the split. Controls H9–H11. New Governance screenshot. |
| F2 | **Python compatibility statement.** <br>Previous README: "Tested on Python 3.13 with a clean virtual environment (Python 3.11–3.13 supported by the pinned packages)." <br>New: "Validated using Python 3.13 on Linux in a clean virtual environment. Compatibility with Python 3.11 and 3.12 has not been independently tested." <br>The Windows activation hint is now marked *not tested*, and the README no longer implies other operating systems were checked. <br>Python 3.11 and 3.12 were never run; the old claim only reflected that the pinned packages publish wheels for them. <br>The same claim appeared as a comment in `requirements.txt` and is corrected there. Two other comment-only fixes in that file: "19 interactive states" became "every captured interactive state", and `build/shots.py` became the real path. <br>**No dependency version changed:** every non-comment line of `requirements.txt` is identical. The README commands were re-run on 5 Nov 2026 in a fresh Python 3.13.18 virtual environment: `python -m venv .venv`, activate, `pip install -r requirements.txt` (exit 0), both artifacts load, and `streamlit run app.py` serves the app (HTTP 200, health "ok"). | No | No | No | No | No | No | README §D, `requirements.txt` comments |
| F3 | **Checksum reporting.** <br>Previous wording: "Validation run left every file it reads unchanged". That was broader than the evidence, because only the files in `validation/protected_checksums.json` were hashed. <br>New wording: "Validation run left all checksum-monitored protected artifacts unchanged". The report states this only when the check passed. <br>The report now has a **checksum inventory** with two mechanisms: <br>(A) the 9 protected artifacts (raw and cleaned CSVs, both `.joblib` files, `app.py`, notebook source, notebook), hashed with **MD5 and SHA-256** at the start and end of every run and compared with the recorded reference; <br>(B) the negative-control watch list (20 files), hashed with MD5 before and after the controls. <br>Files outside these lists (scripts, captures, results, reports, docs) are explicitly not covered. The report table gives, for every protected file and algorithm: the reference, the value before and after the run, and the result. <br>One implementation (`vcore.file_digests`, `assess_checksums`) is shared by the runner and the controls. It fails on a missing file, on a byte-identical file that differs from its reference, and on any monitored file that changes during a run. <br>New controls CK0–CK5 work on copies in a temporary folder (one byte appended, one bit flipped, file deleted, file changed mid-run); the project files are never touched. <br>The `app.py` reference was updated because F1 intentionally changed it (MD5 `cb5fb20f…` → `75a40a85…`). The old value is kept in the file's `history`. | No | No | No | No | No | No | `vcore.py`, `run_validation.py`, `negative_controls.py`, `validation/protected_checksums.json` (now MD5 + SHA-256) |

**Validation framework adjustments needed for F1 (no rule weakened):**
* `micro_refinement_vs_final` is a new strict comparison.
* The text-number check accepts several reviewed lists on one page. Their union must **equal** the observation, and the
  builder asserts this.
* The numeric-scope (pre-redesign) comparison accepts only the exact `'480 diners' → '480'` re-format.
* All 43 earlier controls still run and pass. The 9 new ones are H9–H11 and CK0–CK5, for 52 in total. All 86 earlier
  smoke checks still pass, plus check 87.

**Batch CSV upload test:**

| Test | Result | Date | What was checked |
|---|---|---|---|
| Automated browser-level test (`browser_upload_test.py`, headless Chromium 153 via Playwright, app served by `streamlit run app.py`) | **PASS** (21/21 checks) | 5 Nov 2026 | Example CSV downloaded through the browser. Files uploaded with the real *Browse files* button. Mixed file: 16 rows, 12 scored, 2 under-18, 2 missing / non-numeric, plus an extra user column. The scored CSV downloaded through the browser has every row in order, IDs and the user column preserved, and the documented output columns appended. Segment, P(reorder) (exact), predicted class, tier and items equal an independent recomputation from `food_models.joblib`. Unscored rows are flagged, not guessed, and the KPI cards match the file. Missing column → clear error, no download. 0-byte file → "Could not read the file". Header-only → 0 rows, no error. Under-18-only → all flagged. No exception anywhere. Evidence: `validation/browser_upload_test/`. |
| Human, on-screen test with the operating system's file dialog | **NOT TESTED** | — | A headless browser draws no OS file dialog; Playwright answers the browser's file-chooser request instead. The step-by-step manual procedure is in README → Validation. |

Errors found: none. One observation (existing behaviour, not changed): in the scored file, a cell that could not be read
as a number is written back empty, so the original text (e.g. `abc`) is not echoed; the row is kept and flagged.

**Checksums before and after this polish** (the MD5 values are unchanged from the micro-refinement table below):

| File | MD5 before | MD5 after | SHA-256 after |
|---|---|---|---|
| `data/raw/diners.csv` | `11ba8cfa2b2ab1499c5422cabbe80d1c` | identical | `0a05f70cc6de63ab6501b8a119a74ee6dde6ffdba8dae5ad84179e62b56acc26` |
| `data/raw/orders.csv` | `776f66420a6669d62764daab11863c03` | identical | `aff2b91297d575a387159b0906fce6fb06b401a46ee2c9c575d1fa9f3bffc7d7` |
| `data/clean/diners_clean.csv` | `01ee01ca7fe20d31c91a82ea0788c698` | identical | `b28dc806504f00b0cb6532f9db4745a6d8dcba1d6d7261e39a96d776107d81a0` |
| `data/clean/orders_clean.csv` | `2188c9e4977acd5765e5d8ced0c8966d` | identical | `d9b1b74f3abce70c800b8acea40b6d232583c25789e34123f1a6ace59059dadd` |
| `food_models.joblib` | `7b1f8a39310cc735d15cbc3f89754045` | identical | `d47477932350b79023589b4622261b1809d0ee6bc0bc3da86e3ed34dbef598c1` |
| `dashboard_bundle.joblib` | `abf4ea91f1ec59142a92b43f5ce1f5ad` | identical | `5e6bad70be600cdadbe18c0533f369405d4cd145851b2f1f6084522cd230964c` |
| `build/notebook_source.py` | `2e0900fece1ac20a6f2f38b6a03a7c05` | identical | `05c6e69263a5bea1ef3b4bed66ff15eda3176ddb94fa61f5c0efdf282f088464` |
| `QuickBite_Analysis.ipynb` | `499654cb2693956c2c670db3d8e3dd63` | identical | `44bbfe07fbe1d0324a57de265426604d2404b5c5d7ecc1c50c0110d26005e663` |
| `app.py` | `cb5fb20f7ff05ff6385236281ac8df93` | `75a40a85ca985a3b84d2f08156839217` (F1, intended) | `33bd8e945487ba063aa48399ec3e8df7017540d0db4294312e819a7e5c43c1b5` |

**Timestamp / metadata:** none changed. The notebook was not re-executed, so `meta.trained_at` is still
31 Oct 2026, 20:06. Regenerated files: validation outputs, both reports, and the Governance desktop screenshot.

---

## Final Micro-Refinement — CV Accuracy Precision and Prediction Schema Integrity (1 Nov 2026)

Scope: the validation framework only. No analytical file was edited. The data, model artifact, dashboard bundle, app and
notebook have the same MD5 checksums before and after this refinement (table F3). This section was checked by
`python validation/validation_scripts/run_validation.py`; the results are in `reports/before_after_validation_report.md`.

| # | Change | Raw data | Cleaned data | Models | Predictions / probabilities | Metrics | Dashboard | Documentation / validation |
|---|---|---|---|---|---|---|---|---|
| F1 | **Exact CV-accuracy validation.** <br>Before: the M1 content test accepted a Governance CV-accuracy cell if it *started with* the old mean, so the "± SD" part was never checked. <br>Now: `verify_model_selection.py` re-runs 5-fold stratified CV on the 368 training diners. It builds every expected Governance cell from that recomputation alone (never from the dashboard). Values are normalised to shares and formatted as `app.py` does (`f"{x*100:.1f}%"`). The validator then requires the full displayed `mean% ± sd%` string to match **exactly**, for all 4 candidates. All other fields must also match exactly: model, selected, precision, recall, F1, ROC-AUC, Brier, interpretable. <br>The stored `model_comparison` values (mean, SD and all other fields) are checked against the recomputation with a relative tolerance of 1e-12. This also catches changes too small to show at one decimal. <br>Regression checks: one row per candidate (no missing, duplicate or unexpected row); ranked by CV ROC-AUC; exactly one row marked selected, the model chosen by the rule (highest CV ROC-AUC, confirmed by lowest CV Brier, interpretable); no held-out test metric. <br>Each defect is named: `cv_accuracy_sd_mismatch`, `_mean_mismatch`, `_sd_missing`, `_separator_missing`, `_precision`, `_format_invalid`, `row_missing`, `row_duplicate`, `selected_indicator`, `test_column_present` and `<column>_mismatch`. Each comes with its model, column, expected and actual value. The M1 classifier now requires every cell of a changed Governance row to equal the expected row. | No | No | No | No | No | No | `vcore.py` (`SEL_COLUMNS`, `expected_selection_row`, `validate_selection_table`, exact M1 row test), `verify_model_selection.py` (rewritten; takes the dashboard capture) |
| F2 | **Prediction schema validation before comparison.** <br>Before: `compare_predictions()` used `zip(PRED_FIELDS, x, y)`. A record with a missing or extra field would have been silently truncated, and records were matched only by position. <br>Now: each stored record carries its profile identifier (`profile_id, segment, reorder, prob, items, tier`, defined once as `vcore.RECORD_FIELDS`). <br>For every record of every version, `compare_pred_lists` first validates: the field definition; the field count, reporting fewer fields, a missing intermediate field or an extra field, with record index, version, expected and actual count and the missing fields; field order and types; collection length, with the missing and extra identifiers; duplicate identifiers; and record ↔ profile correspondence in deterministic order. <br>Only a structurally valid collection is compared. Values are matched by profile identifier and compared exactly. Exact equality and the 5,179-profile / 10,358-comparison design are unchanged. `inference_check.py` now writes the identifiers, self-validates before writing and exits 1 on a structural defect. | No | No | No | No (same values; the stored records gained an identifier field) | No | No | `vcore.py`, `inference_check.py`, `validation/inference_check_results*.json` regenerated |
| F3 | **Final regression validation and checksums.** <br>`run_validation.py` now runs, in one command: independent CV recomputation; exact formatted-CV check; model-selection validation; prediction schema, correspondence and values; strict before/after comparisons; smoke test; approved-difference classification; negative controls; and protected-artifact checksums (new reference file `validation/protected_checksums.json`, taken at the start and the end of the run). <br>A failing validator no longer aborts the run silently: its exit status is recorded and the component is reported as FAIL. A component that cannot run is NOT TESTED. Overall PASS requires every component to pass. The runner exits 1 otherwise. <br>`negative_controls.py` gains 24 controls: CV0–CV10 on a copy of the displayed table, CV11–CV12 on a copy of the stored table, and PA–PK on copies of the prediction records. Each is required to report its *specific* defect. Total: **43 controls executed, 43 behaved as required**; MD5 of the 16 watched files unchanged. Control D was updated for the new record layout. <br>End-to-end failure check (run once, on a scratch copy of the project): the displayed SD was changed by +0.05 in the copy's `app.py`. The runner reported `cv_accuracy_sd_mismatch` for each model, with expected `84.8% ± 2.9%` and actual `84.8% ± 7.9%` for logistic regression. It also reported the changed `app.py` checksum, printed *CV validation: FAIL · Overall validation: FAIL* and exited with status 1. | No | No | No | No | No | No | `run_validation.py`, `negative_controls.py`, both validation reports, this change log, the readiness assessment, README |

**F3 — checksums (MD5) before and after this refinement**

| File | Before | After |
|---|---|---|
| `data/raw/diners.csv` | `11ba8cfa2b2ab1499c5422cabbe80d1c` | identical |
| `data/raw/orders.csv` | `776f66420a6669d62764daab11863c03` | identical |
| `data/clean/diners_clean.csv` | `01ee01ca7fe20d31c91a82ea0788c698` | identical |
| `data/clean/orders_clean.csv` | `2188c9e4977acd5765e5d8ced0c8966d` | identical |
| `food_models.joblib` | `7b1f8a39310cc735d15cbc3f89754045` | identical |
| `dashboard_bundle.joblib` | `abf4ea91f1ec59142a92b43f5ce1f5ad` | identical |
| `app.py` | `cb5fb20f7ff05ff6385236281ac8df93` | identical |
| `build/notebook_source.py` | `2e0900fece1ac20a6f2f38b6a03a7c05` | identical |
| `QuickBite_Analysis.ipynb` | `499654cb2693956c2c670db3d8e3dd63` | identical |

**Timestamp / metadata changes:** none. The notebook was not re-executed, so `meta.trained_at` in the bundle is unchanged.
The only regenerated files are validation outputs: the captures, `inference_check_results*.json`,
`model_selection_verification.json`, `negative_controls_results.json`, `smoke_test_results.json`, the palette check and
both before/after reports. They contain new generation times and, for the prediction file, the new identifier field. No
analytical value changed.

---

## Final Refinement — Cross-Validation Interpretation and Validation Integrity (31 Oct 2026, evening)

Baseline for this section: the previous submission (frozen in `validation/baselines/*_v2_previous_refinement.*`).
Verified effect: `food_models.joblib` is byte-identical (MD5 `7b1f8a39…`). Every prediction is identical on 5,179 profiles.
All 17,656 stored analytical values are identical except for the reviewed wording and metadata items listed in
`reports/before_after_validation_report.md` (section *previous refinement vs final*: 112 differences: TS × 78, M2 × 29,
P1 × 4, M1 × 1, unexplained × 0).

| # | Change | Original data | Cleaned data | Trained model | Predictions | Metrics | Dashboard presentation | Docs / validation |
|---|---|---|---|---|---|---|---|---|
| F1 | **Repeated-CV interpretation corrected.** Repeated 5-fold CV over all 460 adults was described as "expected real-world accuracy … the figure to quote". It re-uses the 92 test diners and does not repeat the model selection. It is now labelled a **post-selection stability check** and is explicitly *not* an independent, selection-adjusted estimate. The docs now state that nested CV was not performed. The held-out test result (90.2%, 95% CI 83.7–95.7%) is presented as the independent evaluation. Updated in: the notebook (protocol section, uncertainty section, reading, and a new computed *evaluation hierarchy* cell with a guard that checks the quoted numbers against the code); `build/notebook_source.py`; the model evaluation report; the README; the readiness assessment; and the dashboard (Overview KPI "Model accuracy" → "Repeated-CV accuracy", Retention KPI "Expected accuracy" → "Repeated-CV accuracy", the Retention explanation, the repeated-CV chart title, the Governance model-card rows, and the hero chip). One sentence wrongly claimed the test interval "comfortably contains" the repeated-CV range (83.7–95.7% vs 80.4–90.2%). It has been corrected. | No | No | No | No | No (values identical, wording only) | Wording on 4 pages | Yes |
| F2 | **Matched baselines.** The business takeaway compared repeated-CV accuracy (86%) with the *test* baseline (59%). Every accuracy is now shown with its own baseline: training-fold CV 84.8% vs 58.4% (training set; now stored as `meta.train_majority_share` and recomputed independently), held-out test 90.2% vs 58.7%, repeated CV 85.8% vs 58.5%. The baseline line on the Governance selection-CV chart now uses the training-set share (58.4%) instead of the all-adults share. | No | No | No | No | No (one new stored value: the 58.4% training baseline) | Governance chart label, takeaway text | Yes |
| F3 | **Chart text is now compared.** The comparator previously keyed traces only on x / y / z / customdata / values. It now compares every chart, matched by Streamlit widget key, and every trace within it, matched by type + name (duplicates in order of appearance, leftovers by position). Per trace it compares: type, name, x, y, z, text, hovertext, customdata, labels, values, ids, legendgroup, showlegend, visible, orientation, hovertemplate, texttemplate, and styling (marker, line, mode). Per chart it also compares the title, subtitle, every axis title and category tick text, the legend title, every annotation (including reference-line labels) and every shape label. | No | No | No | No | No | No | Validation |
| F4 | **Trace names are now compared** (part of F3). A renamed trace or legend entry is a difference even when its data are identical. | No | No | No | No | No | No | Validation |
| F5 | **Exact M1 whitelist.** Previously, every difference in "table 5 on the Governance page" was accepted as a block. M1 now accepts only three things. (a) The bundle `model_comparison` schema change between two exact column lists. (b) The Governance selection table between two exact column lists, checked row by row: Model, Interpretable and CV ROC-AUC must be equal; CV accuracy must keep its value (with the sd appended); every new CV precision / recall / F1 / Brier cell must equal an independent recomputation of training-fold CV (`verify_model_selection.py`); and exactly one row is marked as selected, the model the rule picks. (c) One exact chart-label change on `gv_models`. Any change to a shared column fails. Every other approval is an exact before/after pair in `validation/approved_differences.json`. That file is generated from reviewed selectors, and each selector must match exactly one observed pair. | No | No | No | No | No | No | Validation |
| F6 | **Negative controls** (`negative_controls.py`): 19 controls run on in-memory copies. A: lift + 1e-6. B: chart text. C: trace name. D: one segment prediction. E1/E2: shared CV accuracy (bundle and dashboard). F/F2: R1 applied vs a different rule swapped. G/G2: M1 applied vs M1 plus an unrelated change. H1–H8: cluster count, segment name, confusion matrix, What-If result, ROI value, chart category, chart title, KPI value. All 19 behave as required, and the MD5 of the 16 artifact and baseline files is identical before and after. | No | No | No | No | No | No | Validation |
| F7 | **Regenerated validation:** strict *received → final* and *previous → final* comparisons; a numeric-scope *pre-redesign → final* comparison; 10,358 per-profile prediction comparisons; an independent recomputation of the model-selection table; and an 86-check smoke test (the previous 80 plus 6 for the CV wording and baselines). Overall PASS, with 0 unexplained differences. | No | No | No | No | No | No | Validation |
| F8 | **Defect from the previous submission, caught by the stricter comparison.** Automatic title wrapping split hyphenated words ("out- of-fold", "cut- offs"). Wrapping no longer breaks on hyphens (approved as P1 `wrap-hyphen-fix-*`). | No | No | No | No | No | Two chart titles | — |

**Still not done (stated, not hidden):** nested cross-validation was not performed. The 92-diner test set remains the only independent performance estimate.

---

## Earlier refinement (31 Oct 2026, afternoon)

Baseline: the project as received (`QuickBite_Diner_Intelligence_1.zip`). Authoritative versions used: `app.py` (the
QuantFin redesign — newest and working), `build/notebook_source.py` (the notebook's source; the received `.ipynb` was
confirmed cell-for-cell identical to it), `food_models.joblib` and `dashboard_bundle.joblib` from the received package.
`app_original.py` (the supplied app) and `build/app_pre_redesign.py` were older versions; they are kept only as
validation baselines in `validation/baselines/`.

**Effect on results in one line:** no dataset changed, `food_models.joblib` is byte-identical (MD5 `7b1f8a39…`), every
prediction is identical on 5,179 test profiles, and every metric, KPI, segment count, rule value, What-If output and AED
figure is unchanged. The only analytical-content differences are the documented ones in section 3 (verified
automatically in `reports/before_after_validation_report.md`).

### 1. Presentation-only changes

| # | What was wrong or inconsistent | What changed | Why | Data | Model | Metrics |
|---|---|---|---|---|---|---|
| P1 | `primaryColor` was teal, so teal meant both "favourable outcome" and "clickable" | `.streamlit/config.toml`: `primaryColor = "#3A66E8"`; link/focus `#789BFF`; sidebar on the sunken surface; status colours, dataframe header and font keys aligned with the approved tokens | Teal is kept for positive outcomes only; white text on `#3A66E8` is 4.95:1 | No | No | No |
| P2 | Token set in `app.py` included colours outside the approved palette (`#C9D3E3`, `#8EA6FF`, `#7A8CB0`, `#4AA6C9`, `#22344F`, `#1E2D47`, tornado `#8FA6C8`/`#2E5C9A`, heat-map stops) | One token dictionary with exactly the 16 approved colours; every chart, scale and CSS rule now uses them (alpha variants only) | Single source of truth; no stray accents | No | No | No |
| P3 | Segment colours were orchid / blue / ice with diamond / square / circle | `SEGMENT_COLORS` amber / blue / ice and `SEGMENT_SYMBOLS` circle / diamond / triangle-up exactly as specified, used by every chart, card, chip and the What-If and Diner panels (text glyphs ● ◆ ▲ match) | Consistent identity; amber/blue/ice differ in lightness as well as hue | No | No | No |
| P4 | Moderate retention tier was steel-cyan | Tiers teal / slate `#8A99B0` / amber / coral, each with ▲ △ ▽ ▼ | Specified mapping; thresholds untouched | No | No | No |
| P5 | Segment colour and status colour met in the same chart (priority-matrix quadrants coloured coral/teal/amber next to an amber Premium bubble; What-If observed-range band in segment colour) | Quadrants and the range band are neutral slate and named in text; bubbles keep segment colour + shape; tier axes show glyph + label; hatching added where colour alone carried meaning (churned histogram, −1 SD tornado bars, CV accuracy bars) and textures on stacked bars (Budget Students; At-risk / High churn risk) | "One chart, one colour system"; meaning survives greyscale and projectors | No | No | No |
| P6 | Rainbow KPI cards (each card tinted by its icon) and value text recoloured by tone | KPI cards neutral by default; teal / amber / coral edge only for a favourable / caution / risk status; orchid edge marks model-derived KPIs; values always primary text | Accent colours keep meaning | No | No | No |
| P7 | Background had four blooms incl. bottom corners, a grid over most of the viewport and a fixed network motif that sat behind charts while scrolling | Two restrained top blooms (≤ 0.10 alpha), grid confined to the top 20 rem, network motif only inside the hero; hero compacted (one fewer line, smaller mark) | Decoration never behind analytical content; first KPI row at ≈ 260 px on desktop | No | No | No |
| P8 | Inline 290-line stylesheet in `app.py` | Moved to `assets/theme.css`, loaded with `st.html`; selectors use `data-testid` / `st-key-*` / state attributes only | Maintainability; matches the documented structure | No | No | No |
| P9 | Plotly template not set as default; some chart titles and legends clipped in half-width cards and on tablets | `pio.templates.default = "quantfin"`; long titles wrap automatically; legend titles sit on their own row so items wrap instead of clipping; threshold labels get headroom/background | No chart can fall back to default styling; no clipped legends at ≥ 1024 px | No | No | No |
| P10 | Slider read-out text was painted in `primaryColor` (3.8:1 on the page) | Read-out uses link/focus blue (7.2:1) | WCAG AA for small text | No | No | No |
| P11 | Notebook figures used different segment colours (gold / purple / blue) from the dashboard | Notebook figures use darker equivalents of amber / blue / ice (visible on white) and the same marker shapes | Same identity in notebook and dashboard | No | No | No |
| P12 | Big probability read-outs were coloured by tier (the slate "Moderate" tier made the number look disabled) | Read-out in primary text; tier carried by glyph + label + panel edge | Numbers prominent; colour not the only cue | No | No | No |

### 2. Technical fixes

| # | What was wrong | What changed | Why | Data | Model | Metrics |
|---|---|---|---|---|---|---|
| T1 | **Association-rule order depended on Python's random hash seed.** Re-running the received notebook could list the symmetric rule as Raita → Biryani or Biryani → Raita (identical support 6.2%, confidence 89.7%, lift 13.06 both ways), and tied rows could swap places | `mine_rules()` and `best_per_bundle()` break exact ties alphabetically by item names | Reproducibility: verified identical output under four different `PYTHONHASHSEED` values | No | No | No — the rule is now always shown as Biryani → Raita; every value unchanged |
| T2 | `requirements.txt` used open ranges (`streamlit>=1.50`, `plotly>=6.0`, `scikit-learn>=1.3`) although the artifact was pickled with scikit-learn 1.9.1 | Every direct dependency pinned to the tested version (Streamlit 1.65.0, Plotly 7.1.0, scikit-learn 1.9.1, pandas 3.0.5, NumPy 2.5.3, joblib 1.6.0, mlxtend 0.25.0, …); clean-venv install tested | Reproducible environment; avoids unpickling failures | No | No | No |
| T3 | Before/after comparison captured KPI metrics but never compared them; it only read `st.metric` (the app uses custom KPI cards, so nothing was captured); table diffs said only "differ"; no prediction test; no bundle comparison; no expected-difference rules | New `validation/` framework: KPI cards parsed from markup and compared card by card; chart data per trace; tables per column/cell; 17,651 bundle values; 5,179 identical profiles through every app version; smoke test; strict classification of every difference; JSON + Markdown report | Objective evidence that only documented things changed (negative controls confirm a 1e-6 change in one lift is caught) | No | No | No |
| T4 | Smoke testing covered startup only | `smoke_test.py`: 80 checks — all 9 pages with expected content, all filters incl. empty selections, every diner input at min/max with probability checked against the model, What-If templates/inputs/reset, Economics controls at extremes, batch scoring (valid, missing columns, non-numeric, under-18, empty), download buttons, tier boundaries, template and colour contract on every chart | Fix 6 | No | No | No |
| T5 | Folder held obsolete and duplicate files at the top level | `app_original.py` and `app_pre_redesign.py` moved to `validation/baselines/`; old capture/compare scripts replaced; screenshot tool moved to `validation/validation_scripts/` | No obsolete artifacts in the submission root | No | No | No |

### 3. Methodological corrections

| # | Finding | What changed | Data | Model | Metrics |
|---|---|---|---|---|---|
| M1 | **Model selection vs evaluation.** The received notebook fitted all four candidates on the training set and scored *each of them on the test set* inside the selection cell, put those test columns in the comparison table, and cited "the best test calibration (lowest Brier score)" in the rationale. Investigation (Situation 1 of the brief): the choice was in fact determined by cross-validation — Logistic Regression is best on every training-fold CV metric (accuracy 84.8%, ROC-AUC 0.934, F1 0.868, precision 0.886, Brier 0.101; recall tied with Gradient Boosting) — so no test result changed the decision. It was a protocol/reporting defect, not leakage that altered the model. | Selection cell now uses training-fold CV only (accuracy, precision, recall, F1, ROC-AUC, Brier), states the selection rule in code and asserts it; the selected configuration is refitted on the training set and scored **once** on the test set; new section "Model Selection vs. Final Model Evaluation"; Governance page table and chart now show CV metrics only (+ "Selected" column) and the chart's baseline line uses the adult-population majority share instead of the test baseline. | No | No — identical coefficients, artifact byte-identical | No — all reported metrics identical; test scores of non-selected candidates are no longer reported |
| M2 | **Revenue concentration terminology.** The chart ranks diners highest-first but was called a Lorenz curve (Lorenz = lowest-first). | Renamed "Revenue Concentration Curve — Highest-Spending Diners First" with the specified subtitle (dashboard + notebook figure); notebook note explains the two sorting conventions and checks numerically that 2 × the area between the highest-first curve and the equality line equals the Gini (0.181 = 0.181). | No | No | No — Gini, sorting and curve data unchanged |
| M3 | Notebook text said "a single 96-diner test set"; the test set has 92 diners. | Corrected to 92. | No | No | No |

### 4. Numerical differences (all documented, all verified)

| Where | Difference | Code |
|---|---|---|
| Hero, sidebar, Governance "Last model training"; `meta.trained_at` | `06 Oct 2026, 18:48` → `31 Oct 2026, 20:06` (notebook re-executed) | TS |
| Governance model-comparison table; `model_comparison` in the bundle | test columns removed; CV precision / recall / F1 / Brier added; shared columns identical | M1 |
| Rule tables & rule-map hover (Basket Intelligence); `rules_all`, `seg_rules`, `top_overall`, `strategic_overall` | Raita → Biryani shown as Biryani → Raita; values identical | R1 |
| `seg_colors`, stored moderate-tier colour (notebook only; not read by the dashboard) | presentation colours | P1 |

### 5. Visual and accessibility audit — what was checked, and what remains

* Rendered in Chromium at 1440 px, 1024 px and 390 px (screenshots in `submission_assets/dashboard_screenshots/`).
  Desktop and medium widths: no clipped titles or legends, no overlap, no white plot backgrounds, charts stack below
  900 px of content width.
* Contrast (WCAG 2.2): primary / secondary / tertiary text on cards 14.8 / 7.8 / 5.5 : 1; every accent ≥ 4.7 : 1 on cards;
  white on the primary button 4.95 : 1; focus ring 6.0 : 1.
* Colour-vision simulation (Machado 2009, CIEDE2000; `validation/palette_accessibility_check.json`,
  `submission_assets/cvd_simulations/`): segment colours stay clearly distinct under protanopia (ΔE00 ≥ 26.0),
  deuteranopia (≥ 26.9) and tritanopia (≥ 21.2). **In greyscale amber and ice are nearly identical (ΔE00 2.5), and teal vs
  amber tiers likewise (1.1)** — so the dashboard does not rely on colour there: segments are named on axes or carry
  shapes, stacked bars carry textures, tiers carry ▲ △ ▽ ▼ and labels. The palette is therefore *not* claimed to be fully
  colour-blind accessible on colour alone.
* Remaining limitations: on phones (≈ 390 px) a few long chart titles and the Plotly subtitle are still truncated
  (Plotly titles cannot wrap to the device width) and wide tables scroll horizontally; the light Streamlit theme
  (Settings menu) is not styled — the app is designed for its default dark theme.
