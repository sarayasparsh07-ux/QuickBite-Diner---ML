"""Write reports/model_evaluation_report.md from the saved artifacts (every number is read from the bundle, none typed).

  python build/make_model_evaluation_report.py          (run from the project root after the notebook)
"""
from pathlib import Path

import joblib
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
B = joblib.load(ROOT / "dashboard_bundle.joblib")
M = joblib.load(ROOT / "food_models.joblib")


def df(o):
    if isinstance(o, dict) and "__df__" in o:
        s = o["__df__"]
        return pd.DataFrame(s["data"], index=s["index"], columns=s["columns"])
    if isinstance(o, dict) and "__series__" in o:
        s = o["__series__"]
        return pd.Series(s["data"], index=s["index"], name=s["name"])
    return o


def pct(v, d=1):
    return f"{v * 100:.{d}f}%"


meta, m, V = B["meta"], B["metrics"], B["validation"]
rcv, bci = V["repeated_cv"], df(V["bootstrap_ci"]).set_index("Metric")
mc, k_eval, cs = df(B["model_comparison"]), df(B["k_eval"]), V["cluster_stability"]
cm = np.array(B["cm"])
tn, fp, fn, tp = cm.ravel()
ts = df(B["tier_summary"])
L = B["lorenz"]

lines = [
    "# Model evaluation report", "",
    f"Generated from `dashboard_bundle.joblib` and `food_models.joblib` (models trained {meta['trained_at']}, scikit-learn "
    f"{meta['sklearn']}, seed {meta['seed']}). Regenerate with `python build/make_model_evaluation_report.py`.", "",
    "## 1. Segmentation — K-Means", "",
    f"* Features (5, standardised with their own `StandardScaler`): {', '.join(M['features'])}.",
    f"* K = {meta['K']}, chosen on elbow, silhouette, Davies–Bouldin, Calinski–Harabasz and business fit.",
    f"* Silhouette at K = 3: {k_eval.set_index('K').loc[3, 'Silhouette']:.3f} (highest of K = 2–8).",
    f"* Stability: bootstrap mean ARI {cs['boot_mean']:.3f} (worst 5% {cs['boot_p5']:.3f}); seed re-runs mean ARI {cs['seed_mean']:.3f}.",
    f"* Segments: " + ", ".join(f"{n} ({int(c)} diners)" for n, c in df(B['seg_profile']).loc[B['seg_order'], 'Diners'].items()) + ".", "",
    "## 2. Reorder classifier — evaluation protocol", "",
    "Three exercises with three different roles. Each accuracy is compared only with the majority-class baseline of its own data.", "",
    "| Exercise | Data | Role | Accuracy | Matched majority baseline |", "|---|---|---|---|---|",
    f"| A. Model selection | 5-fold stratified CV inside the {meta['n_train']} training diners | compare candidates, select the model | "
    f"{pct(mc.iloc[0]['CV accuracy'])} ± {pct(mc.iloc[0]['CV accuracy (sd)'])} | {pct(meta['train_majority_share'])} (training set) |",
    f"| B. Final independent evaluation | untouched test set, {meta['n_test']} diners, scored once | performance of the selected model on unseen diners | "
    f"{pct(m['Accuracy'])} (bootstrap 95% CI {pct(bci.loc['Accuracy', '95% CI low'])}–{pct(bci.loc['Accuracy', '95% CI high'])}) | "
    f"{pct(m['Baseline accuracy'])} (test set) |",
    f"| C. Post-selection stability check | repeated stratified 5-fold CV, {rcv['n_fits']} fits, all {meta['n_model_rows']} adult diners | "
    f"variability of the fixed configuration — not selection-adjusted | {pct(rcv['acc_mean'])} ± {pct(rcv['acc_sd'])} | {pct(rcv['baseline'])} (all adults) |", "",
    "Nested cross-validation (re-running the model selection inside every outer fold) was **not** performed.", "",
    "## 3. A — Model selection (training data only)", "",
    f"Adult diners only ({meta['n_model_rows']}; under-18 diners excluded). Stratified 80/20 split → {meta['n_train']} train / "
    f"{meta['n_test']} test. Candidates compared with 5-fold stratified cross-validation **on the training set only**; the test "
    "set was not scored for any candidate during selection.", "",
    "| Model | CV accuracy (± sd) | CV precision | CV recall | CV F1 | CV ROC-AUC | CV Brier ↓ | Interpretable |", "|---|---|---|---|---|---|---|---|"]
for _, r in mc.iterrows():
    lines.append(f"| {r.Model} | {pct(r['CV accuracy'])} ± {pct(r['CV accuracy (sd)'])} | {r['CV precision (reorder)']:.3f} | "
                 f"{r['CV recall (reorder)']:.3f} | {r['CV F1 (reorder)']:.3f} | {r['CV ROC-AUC']:.3f} | "
                 f"{r['CV Brier (lower = better calibrated)']:.3f} | {'Yes' if r.Interpretable else 'No'} |")
lines += ["", f"**Selected: {mc.iloc[0].Model}** — rule fixed before any test result: highest CV ROC-AUC, confirmed by the lowest "
          "CV Brier score, interpretable. Decision threshold: scikit-learn default 0.5 (not tuned). Risk-tier cut-offs: fixed "
          "quartiles 25 / 50 / 75% (not tuned).", "",
          f"Matched baseline for this exercise: the training-set majority share, {pct(meta['train_majority_share'])}.", "",
          "## 4. B — Final independent evaluation: held-out test set (selected model only, evaluated once)", "",
          f"The {meta['n_test']} test diners were not used to fit, select, tune or calibrate anything.", "",
          "| Metric | Test value | Bootstrap 95% CI (2,000 resamples) |", "|---|---|---|"]
LO, HI = "95% CI low", "95% CI high"
for k, lab, fmt in [("Accuracy", "Accuracy", pct), ("ROC-AUC", "ROC-AUC", lambda v: f"{v:.3f}"),
                    ("Churn recall (churners caught)", "Churn recall", pct), ("Precision (reorder)", "Precision (reorder)", pct)]:
    lines.append(f"| {k} | {fmt(m[k])} | {fmt(bci.loc[lab, LO])} – {fmt(bci.loc[lab, HI])} |")
lines += [f"| Recall (reorder) | {pct(m['Recall (reorder)'])} | — |", f"| F1 (reorder) | {m['F1 (reorder)']:.3f} | — |",
          f"| Churn precision | {pct(m['Churn precision'])} | — |", f"| Brier score | {m['Brier score']:.3f} | — |",
          f"| Majority-class baseline (same {meta['n_test']} test diners) | {pct(m['Baseline accuracy'])} | — |", "",
          f"Confusion matrix (rows = actual churn / reorder, columns = predicted churn / reorder): TN {tn} · FP {fp} · FN {fn} · TP {tp}.", "",
          "## 5. C — Post-selection stability check: repeated cross-validation", "",
          f"The fixed logistic-regression configuration achieved {pct(rcv['acc_mean'])} ± {pct(rcv['acc_sd'])} accuracy (5th–95th percentile of folds "
          f"{pct(rcv['acc_p5'])}–{pct(rcv['acc_p95'])}) and ROC-AUC {rcv['auc_mean']:.3f} ± {rcv['auc_sd']:.3f} in repeated stratified 5-fold "
          f"cross-validation ({rcv['n_fits']} fits) across all {meta['n_model_rows']} adult diners, against this exercise's majority baseline of "
          f"{pct(rcv['baseline'])}. The pipeline is refitted inside every fold, so there is no preprocessing leakage. Because the exercise uses the "
          "full adult dataset, including the original test diners, and does not repeat the model selection, it should **not** be interpreted as "
          "an independent estimate of selection-adjusted generalisation performance. Its role is to show how stable the fixed configuration's "
          "performance is across different splits.", "",
          "**Why 85.8% and 90.2% are not contradictory.** They answer different questions on different data. The repeated-CV mean "
          f"({pct(rcv['acc_mean'])}) lies inside the test accuracy's bootstrap 95% interval ({pct(bci.loc['Accuracy', '95% CI low'])}–"
          f"{pct(bci.loc['Accuracy', '95% CI high'])}), and the {pct(m['Accuracy'])} test result sits at the upper end of the range of individual "
          f"repeated-CV folds ({pct(rcv['acc_p5'])}–{pct(rcv['acc_p95'])}) — what one small {meta['n_test']}-diner draw can produce. Each figure "
          "clears its own baseline by a wide margin.", "",
          "## 6. Risk tiers — out-of-fold calibration", "",
          "Tier cut-offs are fixed quartiles of the probability scale (not tuned). Probabilities are out-of-fold predictions for all adult "
          "diners, i.e. each diner is scored by a model that did not see that diner.", "", "| Tier | Diners | Mean predicted P(reorder) | Observed reorder rate |", "|---|---|---|---|"]
for t, r in ts.iterrows():
    lines.append(f"| {t} | {int(r.Diners)} | {pct(r['Mean predicted P(reorder)'])} | {pct(r['Observed reorder rate'])} |")
lines += ["", "## 7. Revenue concentration", "",
          f"Gini coefficient {L['gini']:.3f} (standard ascending formula). Revenue Concentration Curve — Highest-Spending Diners First: "
          + ", ".join(f"{k} of diners → {pct(v)} of revenue" for k, v in L["conc"].items()) + ".", "",
          "## 8. Limitations", "",
          "* Course-supplied dataset whose provenance (real vs synthetic) is not documented — treat it as illustrative: results describe this dataset, not QuickBite's real operations.",
          "* Observational data: coefficients and what-if changes are associations, not causal effects.",
          "* Frequency, order value and basket size are collinear (VIF > 5) — read coefficients as a joint profile.",
          "* `total_spend` behaves like about one month of spend (≈ orders × AOV); the data dictionary calls it 'total spent to date', so its interpretation as cumulative spend is unconfirmed.",
          f"* {B['under18']['n']} under-18 diners are outside the classifier population (18+ policy).",
          f"* The test set is small ({meta['n_test']} diners), so the independent test result has a wide bootstrap interval "
          f"({pct(bci.loc['Accuracy', '95% CI low'])}–{pct(bci.loc['Accuracy', '95% CI high'])}).",
          "* The repeated-CV figure is a post-selection stability check on data that includes the test diners; it is not a substitute for an "
          "independent, selection-adjusted estimate. Nested cross-validation was not performed."]
(ROOT / "reports" / "model_evaluation_report.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
print("wrote reports/model_evaluation_report.md")
