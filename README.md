# QuickBite — Diner Intelligence

Behavioural segmentation, market-basket analysis and reorder prediction for QuickBite, delivered as an analysis notebook, a model artifact that plugs into the supplied dashboard, and a 9-page decision-support dashboard.

## Run it

```bash
pip install -r requirements.txt
jupyter nbconvert --to notebook --execute --inplace QuickBite_Analysis.ipynb   # or Run All in Jupyter
streamlit run app.py
```

**Re-run the notebook in your own environment first.** It regenerates `food_models.joblib` and `dashboard_bundle.joblib` so the pickled scikit-learn models match your installed version.

## What's in the folder

| Path | What it is |
|---|---|
| `QuickBite_Analysis.ipynb` | Full analysis: audit → cleaning → features → EDA → clustering (+ stability & significance) → Apriori → classifier (+ bootstrap CIs, repeated CV) → priority matrix → revenue concentration → campaign economics → what-if & tornado → artifact → validation → takeaway |
| `food_models.joblib` | The six-key contract `app.py` expects: `scaler`, `kmeans`, `segment_names`, `clf`, `features`, `reco` |
| `dashboard_bundle.joblib` | Pre-computed analytics for the management pages (kept separate so the contract file stays exact) |
| `app.py` | 9-page dashboard; its `analyse()` function is unchanged from the original |
| `app_original.py` | The supplied app, byte-identical — runs against `food_models.joblib` with no errors |
| `data/raw/`, `data/clean/` | Original CSVs (untouched) and validated datasets with audit flags |
| `reports/` | Data-quality report, issue log, and every notebook chart as PNG |

## Dashboard pages

1. **Executive Overview** — KPIs, management summary, segment economics, risk tiers, revenue concentration (Lorenz/Gini)
2. **Customer Segmentation** — profiles, strategy cards, K selection, cluster stability (ARI), Kruskal–Wallis significance, PCA
3. **Basket Intelligence** — opportunity matrix, lift ranking, per-segment rules, rule map, menu penetration
4. **Retention & Churn** — performance with bootstrap 95% CIs and repeated CV, drivers, calibrated risk tiers, watch-list
5. **Retention Economics** — ROI calculator: expected-value vs probability targeting, break-even success rate, sensitivity, target list
6. **Diner Intelligence** — single-diner scoring with explanations, plus **batch CSV scoring**
7. **What-If Simulator** — scenarios A–E, sensitivity curve, tornado chart, extrapolation warnings
8. **Recommendations** — takeaway, priority matrix, segment action matrix, 30-day plan
9. **Governance & Data Quality** — under-18 policy, live artifact checks, model card, feature contract, model comparison, DQ scorecard

## Under-18 policy

The age input runs **18–70**, as in the original app. The **20 diners under 18** (ages 9–17, all Budget Students) are **excluded from the classifier** (training, evaluation, scoring) and from the age input. They are not deleted: segmentation and basket analysis keep all 480 diners because age is not used there. Batch scoring flags any under-18 row as "Not scored — under 18".

## Headline results

- **Segments (K = 3, silhouette 0.571, bootstrap ARI 1.000):** Premium Foodies (27% of diners, 36% of revenue, 52% reorder), Family Feasters (31%, 30%, 15%), Budget Students (42%, 35%, 98%). All features differ by segment with large effects (Kruskal–Wallis ε² 0.36–0.88, p < 0.001).
- **Bundles (within-segment lift):** Cola + Dessert + Pizza → Garlic Bread (95%, 4.8×); Miso Soup + Sushi → Green Tea (92%, 3.9×); Salad + Steak → Wine (97%, 3.6×). Budget Students have no strong pairing (best 1.3×).
- **Reorder model (460 adult diners):** **85.8% ± 3.0% accuracy in repeated 5-fold CV** vs a 58.5% majority baseline, ROC-AUC 0.944. The held-out test split scored 90.2% (95% CI 83.7–95.7%) — quote the CV figure.
- **Priority:** Premium Foodies — 101 of 130 sit in the uncertain 25–75% band holding AED 88.4k of monthly spend.
- **Targeting:** rank diners by expected value of an offer (probability × spend × margin − cost), not by probability alone. Under tight economics every probability cut-off loses money while value ranking stays profitable.

## Caveats

- Logistic coefficients describe a joint profile: frequency, order value and basket size are strongly collinear (VIF > 5).
- Overall Apriori lifts (13–30×) are inflated because each segment orders from an almost separate menu; use within-segment lift.
- What-if results are model-based simulations, not causal estimates. The discount scenario reflects that discount users happen to be the loyal segment.
- Campaign economics use planning assumptions (offer cost, margin, success rate). With one success rate, value ranking favours Family Feasters; a segment-stratified A/B test should measure real win-back rates before budget is split.
