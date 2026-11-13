# Validation baselines (reference only — not part of the running dashboard)

| File | What it is |
|---|---|
| `app_original_supplied.py` | The app supplied with the assignment (byte-identical). Its `analyse()` is used in the identical-profile prediction test. |
| `app_pre_redesign.py` | The dashboard before the QuantFin visual redesign. |
| `app_v1_received.py` | The dashboard exactly as received (before both refinements). |
| `app_v2_previous_refinement.py` | The dashboard as submitted after the first refinement (before the CV-interpretation refinement). |
| `capture_v1_received.json` | Every value the received dashboard rendered (42 page/state snapshots), captured with its own artifacts. MD5s of the app and artifacts are inside. |
| `capture_pre_redesign.json` | The same for the pre-redesign dashboard. |
| `bundle_v1_received.json.gz` | The received `dashboard_bundle.joblib` exported as plain JSON (17,651 values). |
| `capture_v2_previous_refinement.json`, `bundle_v2_previous_refinement.json.gz` | The same two snapshots for the previous submission — used to isolate exactly what the final refinement changed. |
| `app_v3_micro_refinement.py`, `capture_v3_micro_refinement.json`, `bundle_v3_micro_refinement.json.gz` | The submission after the CV-precision / prediction-schema micro-refinement, frozen immediately before the final submission polish — used to isolate exactly what the polish changed (the Governance population KPI and the training-range note). |
| `app_v4_final_polish.py`, `capture_v4_final_polish.json`, `bundle_v4_final_polish.json.gz` | The final-polish submission, frozen immediately before the observed-adult-range terminology correction — used to isolate exactly what that correction changed. |
| `batch_export_v4_final_polish/` | The browser test's inputs and the files the final-polish app served for download (`template.csv`, `scored_*.csv`). The smoke test and `browser_upload_test.py` require today's export to be byte-identical to these. |
| `app_v5_range_correction.py`, `capture_v5_range_correction.json`, `bundle_v5_range_correction.json.gz` | The range-correction submission, frozen immediately before the DQ-01 / DQ-05 documentation correction — isolates that correction; its bundle is also the "before" for `dq_consistency.py`. |
| `capture_v6_dq_correction.json`, `bundle_v6_dq_correction.json.gz` | The DQ-01 / DQ-05 submission, frozen immediately before the DQ-05 quantity correction — isolates that correction and is the "before" for `dq_consistency.py`. Its app is byte-identical to the final `app.py` (MD5 `e01606439b07fc2c89ef8d838701caf1`), so no separate copy is kept. |

These are frozen evidence for `../validation_scripts/run_validation.py`. Captures record every KPI, chart text and trace property, table cell and number in text (format of `capture_outputs.py`). The app files here are not meant to be run from
this folder (they look for the model artifacts next to themselves).
