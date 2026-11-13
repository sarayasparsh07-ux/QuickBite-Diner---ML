# QuickBite Diner Intelligence — QuantFin AI Studio

Customer segmentation, market-basket analysis and reorder prediction for QuickBite, a food-delivery business, delivered as
an analysis notebook, a model artifact that plugs into the supplied dashboard contract, and a 9-page decision-support
dashboard built in Streamlit.

## A. Project overview

QuickBite's management asked three questions: *Who are our diners? What do they order together? Who is about to stop
ordering?* The project answers them from two files — a diner table (480 diners) and an order-item table (1,980 baskets,
4,924 rows) — and turns the answers into decisions: which segment to protect, which bundles to promote, which diners to
target with a retention offer and what that offer is worth in AED.

## B. Main analytical components

| Component | What it does | Where |
|---|---|---|
| Customer segmentation | K-Means (K = 3) on five standardised behavioural features → Premium Foodies, Family Feasters, Budget Students; validated with elbow, silhouette, Davies–Bouldin, Calinski–Harabasz, bootstrap and seed stability (ARI) and Kruskal–Wallis tests | Notebook §8 · dashboard page 2 |
| Market-basket analysis | Apriori association rules overall and within each segment (support, confidence, lift); within-segment lift is the decision-grade measure | Notebook §9 · page 3 |
| Reorder classification | Logistic regression (selected on training-set cross-validation, evaluated once on a held-out test set) on seven features; out-of-fold probabilities feed four risk tiers | Notebook §10 · pages 4 and 6 |
| Retention economics | Expected value of a retention offer = P(churn) × success rate × monthly spend × months × margin − cost; value ranking vs probability cut-offs | Notebook §11 · page 5 |
| What-If analysis | Model-based scenario simulation (not causal) with sensitivity curves and a tornado chart | Notebook §12 · page 7 |
| Executive dashboard | 9 pages: Executive Overview, Customer Segmentation, Basket Intelligence, Retention & Churn, Retention Economics, Diner Intelligence (single + batch scoring), What-If Simulator, Recommendations, Governance & Data Quality | `app.py` |

## C. Project architecture

```text
data/raw/diners.csv, orders.csv            (original files — never modified)
        │
        ▼
QuickBite_Analysis.ipynb  ──────────────►  data/clean/*.csv · reports/data_quality_report.md · reports/figures/*.png
   (generated from build/notebook_source.py by build/make_notebook.py)
        │
        ├──►  food_models.joblib        six-key contract: scaler, kmeans, segment_names, clf, features, reco
        └──►  dashboard_bundle.joblib   pre-computed analytics for the management pages
                     │
                     ▼
app.py  +  .streamlit/config.toml (native theme)  +  assets/theme.css (stylesheet)   →   streamlit run app.py
                     │
                     ▼
validation/validation_scripts/run_validation.py  →  validation/before_after_validation_report.json
                                                  →  reports/before_after_validation_report.md
```

## D. Installation

Validated using Python 3.13 on Linux in a clean virtual environment. Compatibility with Python 3.11 and 3.12 has not been
independently tested.

```bash
python -m venv .venv
source .venv/bin/activate            # Windows (not tested): .venv\Scripts\activate
pip install -r requirements.txt
```

In the validated environment (Python 3.13.18, Linux), these three commands install every pinned version, after which both
model artifacts load and `streamlit run app.py` serves the dashboard. Other operating systems and Python versions may work
with the same pins, but that has not been tested.

`requirements.txt` pins every direct dependency to the tested version. **scikit-learn must stay at 1.9.1**: that is the
version that pickled `food_models.joblib`; another version may warn or refuse to load it. If you must use another
version, re-run the notebook first (below) so the artifact is rebuilt in your environment.

## E. Launch instructions

```bash
streamlit run app.py
```

Run it from this folder. The dashboard opens at http://localhost:8501. Theme settings in `.streamlit/config.toml` are read
at start-up only, so restart after editing them.

To rebuild every artifact from the raw data (optional — the shipped artifacts are already built):

```bash
jupyter nbconvert --to notebook --execute --inplace QuickBite_Analysis.ipynb      # or "Run All" in Jupyter
python build/make_model_evaluation_report.py
```

Re-running the notebook reproduces `food_models.joblib` byte-for-byte (verified: identical MD5 across runs and across
Python hash seeds); `dashboard_bundle.joblib` differs only in its training timestamp.

## F. Model artifact requirements

`food_models.joblib` and `dashboard_bundle.joblib` must sit in the same folder as `app.py` (the app finds them, and
`assets/theme.css`, relative to its own location). Launch from this folder anyway: Streamlit reads `.streamlit/config.toml`
from the working directory, so launching from elsewhere loses the native theme.

* `food_models.joblib` is required. It holds the fitted clustering scaler, the K-Means model, the segment names, the
  classifier pipeline, the five clustering feature names and the per-segment recommendations. Without it the app stops with
  a clear message.
* `dashboard_bundle.joblib` holds pre-computed analytics (profiles, rules, metrics, scenarios). Without it only the Diner
  Intelligence page works; every other page explains how to create the file.

Inference contract (unchanged from the supplied app): `segment = kmeans.predict(scaler.transform(profile[5 features]))`,
`reorder = clf.predict / predict_proba(profile[5 features + age + total_spend])`, `items = reco[segment]`.

## G. Dataset descriptions

| File | Grain | Role |
|---|---|---|
| `data/raw/diners.csv` | one row per diner (480) | age, orders per month, average order value, items per order, days since last order, discount usage rate, total spend, and the target `reordered` |
| `data/raw/orders.csv` | one row per item in an order (4,924 rows, 1,980 orders) | `order_id`, `diner_id`, `item` — the baskets used for Apriori |
| `data/clean/diners_clean.csv` | as raw + audit flags | adds `age_flag`, `include_in_classifier`, `include_in_clustering`; no value changed or imputed |
| `data/clean/orders_clean.csv` | as raw | validated against the diner table (referential integrity, duplicate grains) |

Data quality is documented in `reports/data_quality_report.md` and `reports/data_quality_issue_log.csv`. The issue log
has one source, `build/notebook_source.py`. Executing the notebook writes it to the CSV, the Markdown report and
`dashboard_bundle.joblib`, and the Governance page displays it from the bundle unchanged. DQ-01 states the
classifier-eligible population: 460 adult diners (368 training observations and 92 held-out test observations). DQ-05
refers to the observed adult classifier range. Its quantity, **6 of 7 classifier input controls**, is calculated in the
notebook:
* Each permitted dashboard input range (`INPUT_SPEC`) is compared with the observed adult classifier range of the 460
  eligible adults.
* A control counts once if either permitted bound lies outside that range.
* `orders_per_month` (1–20) is the only control whose range matches exactly.
* Values outside the observed range remain permitted and are flagged with a warning.

The data-quality report shows the per-feature table. `validation/validation_scripts/dq_consistency.py` recalculates the
count independently. It also checks that all five representations agree: notebook, CSV, Markdown report, bundle and
dashboard.

**Batch-scoring export (data dictionary for the added columns).**

| Column | Meaning |
|---|---|
| `status` | `Scored`, `Not scored — under 18 (18+ policy)` or `Not scored — missing / non-numeric value` |
| `segment` | segment name from the K-Means model (scored rows only) |
| `p_reorder` | probability of reordering, 0–1 (scored rows only) |
| `will_reorder` | `Yes` when the classifier predicts a reorder (p > 0.5), otherwise `At risk` |
| `risk_tier` / `action` | tier from the fixed cut-offs 75 / 50 / 25 % and its recommended action |
| `recommended_items` | the segment's recommended items |
| `outside_training_range` | the inputs (business names, comma-separated) whose value lies outside the observed adult classifier range; empty when every input is inside it |

The exported field `outside_training_range` is retained for backward compatibility. It indicates whether a record falls
outside the observed adult classifier reference range calculated from all 460 adult diners, and lists which inputs do. It
does not indicate that the range was calculated exclusively from the 368 training observations. The field is added when at
least one row is scored. The dashboard table shows it under the heading *Outside observed adult range*.

## H. Model methodology

* **Clustering feature set (5):** orders_per_month, avg_order_value, avg_items_per_order, days_since_last_order, discount_rate.
* **Classification feature set (7):** the five above + age + total_spend, in that order.
* **Preprocessing separation:** the clustering scaler and the classifier's scaler are independent objects; the classifier's
  scaler lives inside a scikit-learn `Pipeline`, so in every cross-validation fold it is fitted on that fold's training rows only.
* **Population:** all 480 diners for segmentation and baskets; the 460 adult diners (18+) for the classifier. The 20
  under-18 diners are documented and excluded from the classifier and the age input, not deleted.
* **Observed adult classifier range (feature reference range).** For each of the seven classifier inputs, the dashboard
  stores the observed minimum and maximum across **all 460 adult classifier-eligible diners**. That is the 368 training
  observations and the 92 held-out test observations together, so it is an observed population reference range, not a
  training-only range.
  * It is used only to warn when an input lies outside what was observed: the *observed adult reference-range warning* on
    the scoring and What-If pages.
  * It does not affect any prediction.
  * The Governance page lists it in the *Feature contract* table.
  * The internal name `train_ranges` in the notebook and the bundle is kept, because renaming it would change the frozen
    artifacts.
* **Train/test:** stratified 80/20 split of the adult diners → 368 train / 92 test.
* **Evaluation protocol — three exercises, three roles.** Each accuracy is compared only with the majority-class baseline of its own data.

  | Exercise | Data | Role | Accuracy | Matched baseline |
  |---|---|---|---|---|
  | A. Model selection | 5-fold stratified CV inside the 368 training diners | compare four candidates and select one | 84.8% ± 2.9% (logistic regression) | 58.4% (training set) |
  | B. Final independent evaluation | the untouched 92-diner test set, scored once | performance of the selected model on unseen diners | **90.2%** (bootstrap 95% CI 83.7–95.7%) | 58.7% (test set) |
  | C. Post-selection stability check | repeated stratified 5-fold CV, 50 fits, all 460 adults | stability of the fixed configuration across splits | 85.8% ± 3.0% | 58.5% (all adults) |

* **A — Model selection (training data only).** Logistic regression, a depth-4 decision tree, a random forest and gradient
  boosting are compared with 5-fold stratified CV on the 368 training diners (accuracy, precision, recall, F1, ROC-AUC, Brier).
  Rule, fixed before any test result: highest CV ROC-AUC, confirmed by the lowest CV Brier score, interpretable model preferred
  → logistic regression. The decision threshold (0.5) and the risk-tier cut-offs (25 / 50 / 75%) are fixed, not tuned. No
  candidate was ever scored on the test set.
* **B — Final independent evaluation.** The selected model is scored once on the 92 test diners, which played no part in
  fitting, selection or tuning: accuracy 90.2% (95% CI 83.7–95.7%), ROC-AUC 0.973, churn recall 78.9%, Brier 0.073, against
  the same diners' 58.7% majority baseline. This is the project's independent performance estimate.
* **C — Post-selection stability check.** Repeated CV re-fits the *already selected* configuration on all 460 adults,
  including the 92 test diners, and does not repeat the selection. It shows that performance is stable across splits
  (85.8% ± 3.0%, ROC-AUC 0.944, vs 58.5%), but it is **not** an independent, selection-adjusted estimate of generalisation
  performance. **Nested cross-validation was not performed.**
* **Why 85.8% and 90.2% are not contradictory.** They answer different questions on different data: the repeated-CV mean lies
  inside the test result's 95% interval, and 90.2% sits at the upper end of the individual repeated-CV folds (80.4–90.2%) —
  what one small 92-diner draw can produce. Both clear their own baselines by a wide margin.

Full details: `reports/model_evaluation_report.md`; the model-selection table is independently recomputed by
`validation/validation_scripts/verify_model_selection.py`.

## I. Known limitations

* The dataset is course-supplied and its provenance (real vs synthetic) is not documented; treat results as illustrative of
  this dataset, not as measurements of QuickBite's real operations.
* Observational data: logistic coefficients, what-if changes and retention economics describe associations, not causal
  effects. What-If results are **scenario simulations**; real effects need an A/B test.
* `total_spend` is described as "total spent to date", but in the data it tracks about one month of spend (≈ orders per
  month × average order value). Its interpretation as cumulative spend is unconfirmed.
* The classifier covers adult diners only; 20 under-18 diners are outside its population.
* Frequency, order value and basket size are collinear (VIF > 5): read coefficients as a joint profile.
* Overall Apriori lifts (13–30×) are inflated because each segment orders from an almost separate menu; use within-segment lift.
* The 92-diner test set is small, so test metrics carry wide intervals; campaign economics rest on management assumptions
  (offer cost, margin, success rate). Results should not be generalised to real QuickBite operations without new data.

## Visual design — QuantFin AI Studio

Presentation only — no data, model, threshold or calculation depends on it.

| Token | Colour | Use |
|---|---|---|
| Background / Sunken / Primary / Elevated surface | `#0B1020` / `#101A2D` / `#152238` / `#1B2B43` | page, sidebar, cards, hover & tooltips |
| Border | `#2B405C` | card outlines, separators |
| Primary / Secondary / Tertiary text | `#F4F7FC` / `#A8B6CB` / `#8A99B0` | headings & KPI values / body & chart labels / captions |
| Positive · Activity · Analytical blue · AI/ML | `#45E3C1` · `#A5E4FF` · `#5B84FF` · `#D98CF2` | favourable outcomes · volume · chart marks · model output |
| Caution · High risk | `#FFC76B` · `#FF7D91` | warnings / at-risk · churn exposure |
| Primary action · Link/focus | `#3A66E8` · `#789BFF` | buttons, sliders, selected navigation · links, keyboard focus |

* **Segments:** Premium Foodies amber ● circle, Family Feasters blue ◆ diamond, Budget Students ice ▲ triangle — one mapping on every chart, card and chip.
* **Risk tiers:** ▲ High retention (teal), △ Moderate (slate), ▽ At-risk (amber), ▼ High churn risk (coral).
* **Rule:** a chart encodes either segment identity or risk status in colour, never both; every status also has a glyph,
  label or sign. Amber vs ice (segments) and teal vs amber (tiers) are hard to tell apart in greyscale, so stacked bars add
  a texture and all other charts name the category on the axis or with a marker shape. The palette is not claimed to be
  fully colour-blind safe on colour alone — see `validation/palette_accessibility_check.json` and `submission_assets/cvd_simulations/`.
* **Charts:** one registered Plotly template (`quantfin`, set as the default), rendered with `theme=None`.
* **Fonts:** system font stack only (Inter if installed); no external fonts or CDNs.

## Folder guide

| Path | Contents |
|---|---|
| `app.py`, `assets/theme.css`, `.streamlit/config.toml` | dashboard, stylesheet, native theme |
| `QuickBite_Analysis.ipynb` | full analysis, executed, with outputs |
| `build/` | notebook source (`notebook_source.py`), notebook builder, model-report generator |
| `data/raw/`, `data/clean/` | original and validated datasets |
| `reports/` | data-quality report & issue log, model evaluation report, before/after validation report, notebook figures |
| `validation/` | validation scripts, approved-difference whitelist, protected-file checksum reference, frozen baselines of earlier versions, JSON results, browser upload-test evidence |
| `submission_assets/` | dashboard screenshots (desktop, medium, mobile) and colour-vision simulations |
| `CHANGELOG.md` | every change in this refinement, with its effect on data, models and metrics |
| `QuickBite_Problem_Statement.md` | the original brief |

## Validation

`python validation/validation_scripts/run_validation.py` (≈ 7 minutes; add `--skip-inference` to reuse the stored
5,179-profile prediction run) re-captures the dashboard and compares it, strictly, with the project as received and with the
previous submission: every KPI card, every chart's numbers, trace names, text labels, hover templates, titles, axis
labels, legend titles and annotations, every table cell, every number in text, all 17,000+ stored analytical values, and
every prediction. It also compares each later submission in turn (frozen in `validation/baselines/`), the last being
the one immediately before the observed-adult-range terminology correction, so every change is isolated on its own. A difference passes only if it is explicitly listed in `validation/approved_differences.json` (or meets a
coded content test, e.g. "only the timestamp digits changed") **and** sits in its approved location.

Two further checks guard the details most easily overlooked:

* **The model-selection table.** It is checked against an independent re-run of training-fold CV, both as stored
  (tolerance 1e-12) and as displayed. The full `mean% ± sd%` cell and every other cell must match exactly.
* **The predictions.** Every prediction record (`profile_id, segment, reorder, prob, items, tier`) is validated
  structurally before any value is compared: field count, order and types, collection length, and matching to its
  profile.

The control suite (`negative_controls.py`, 73 cases) includes 65 negative cases and eight positive controls:
* The 65 negative cases inject deliberate defects into in-memory copies, or into temporary copies of protected files. Each
  must be rejected with its specific defect.
* The eight positive controls confirm that valid inputs and unchanged artifacts pass.

The checksum assertion covers exactly the nine files listed in `validation/protected_checksums.json`: the raw and cleaned
data, both `.joblib` artifacts, `app.py`, the notebook source and the notebook. Each is hashed with MD5 and SHA-256 at the
start and end of every run and compared with the recorded reference. Other files the validation reads or writes are not
covered by that assertion; the report lists the inventory.

The runner exits with a non-zero status unless every component passes. Results:
`reports/before_after_validation_report.md`.

### Batch CSV upload — browser test and manual procedure

`validation/validation_scripts/browser_upload_test.py` runs the batch workflow in a real (headless) Chromium browser while
the app is running. It downloads the example CSV, uploads test files through the uploader's *Browse files* button,
downloads the scored file and checks it against an independent recomputation from `food_models.joblib`. Given a reference
folder, it also requires every download to be byte-identical to an earlier version's
(`validation/baselines/batch_export_v4_final_polish/`). Its last run is in
`validation/browser_upload_test/`. A headless browser draws no operating-system file dialog: Playwright answers the
browser's file-chooser request instead.

To repeat the test by hand on your own computer:

1. Start the dashboard with `streamlit run app.py` and open http://localhost:8501.
2. Open **Diner Intelligence**, then the **Batch scoring (CSV upload)** tab.
3. Click **Download example CSV** (11 rows, including 2 under-18 diners), open it, and add a few rows of your own. Use a
   new `diner_id` and values in the dashboard's input ranges.
4. Click **Browse files** in *Upload diners CSV* and choose the edited file.
5. Check that the *Rows uploaded* card equals the number of rows in your file. Check that *Scored* plus the not-scored
   rows add up to it, and that *Not scored — under 18* is 2.
6. In the table, check that every scored row has a segment, P(reorder), will_reorder, risk tier, action and recommended
   items.
7. Check that the under-18 rows show *Not scored — under 18 (18+ policy)* and nothing else.
8. Click **Download scored file (CSV)** and open it.
9. Check the downloaded file:
   * It has the same number of rows, in the same order, with every `diner_id` and any extra column of yours unchanged.
   * The columns `status`, `segment`, `p_reorder`, `will_reorder`, `risk_tier`, `action`, `recommended_items` and
     `outside_training_range` are added at the end. `outside_training_range` is added only when at least one row is
     scored; on screen the same column is headed *Outside observed adult range*.
   * `p_reorder` is a number between 0 and 1.
   * The tier follows the cut-offs: 75% or more → High retention likelihood, 50–75% → Moderate, 25–50% → At-risk,
     below 25% → High churn risk.
10. Test the error handling, one file at a time:
    * Delete the `discount_rate` column. Expect *Missing required columns: discount_rate*, and no download.
    * Type `abc` into one number. Expect that row to be flagged *Not scored — missing / non-numeric value*; the cell is
      written back empty in the scored file.
    * Upload an empty (0-byte) file. Expect *Could not read the file*.
    * Upload a file that has only the header row. Expect 0 rows uploaded and no error.
    * Upload a file with only under-18 rows. Expect every row to be flagged and nothing to be scored.
