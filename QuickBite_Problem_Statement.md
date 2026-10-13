# 🍔 QuickBite — Know Your Diners
### In-Class Machine Learning Challenge (~2 hours)

**Files you are given:** `diners.csv`, `orders.csv`, `app.py` (a ready-made dashboard)
**What you build:** your own analysis (in a notebook) + wire your models into the dashboard
**Work:** individual · code is **yours to write** · run everything before the end of class

---

## 1. The Business

**QuickBite** is a food-delivery app. Management has the data but no insight, and they've given you a short brief:

> *"We don't really understand our diners. **Who are they? What do they order together? And who's about to stop ordering?** Use our data to tell us — and give us something we can actually use."*

Your mission is to turn their raw data into three answers and a working tool:

1. **Who are our diners?** → break them into clear **segments**
2. **What do they order together?** → find **item combinations** worth promoting (overall *and* per segment)
3. **Who will come back?** → predict which diners will **reorder** (and who is at risk of churning)
4. **Make it usable** → feed your models into the provided **dashboard** so a manager can type in a diner and instantly see their segment, reorder likelihood, and recommended items.

---

## 2. The Data

### `diners.csv` — one row per diner
| Column | Meaning |
|---|---|
| `diner_id` | Unique diner ID (links to `orders.csv`) |
| `age` | Age in years |
| `orders_per_month` | How often they order (frequency) |
| `avg_order_value` | Average spend per order (AED) |
| `avg_items_per_order` | Average number of items per order |
| `days_since_last_order` | Days since their last order (recency) |
| `discount_rate` | Share of their orders that used a discount (0–1) |
| `total_spend` | Total spent to date (AED) |
| `reordered` | **1 = ordered again (retained), 0 = did not (churned)** — your classification target |

### `orders.csv` — one row per item in an order (the "baskets")
| Column | Meaning |
|---|---|
| `order_id` | Unique order ID (one basket) |
| `diner_id` | Which diner placed it (links to `diners.csv`) |
| `item` | The menu item ordered |

---

## 3. What You Must Do

### Task 1 — Segment the diners (Clustering)
Group diners into segments based on their **behaviour** (how often they order, how much they spend, order size, recency, discount use).
- **Decide the number of segments yourself** — justify it using the **elbow method** and **silhouette score** (don't just guess).
- **Profile and name** each segment in plain business language (e.g., *budget students, families, premium foodies*).
- **Expected output:** your chosen number of segments, a short profile of each, and a business name for each.

### Task 2 — Find what's ordered together (Market-Basket / Apriori)
Run **association-rule mining** on `orders.csv`.
- Treat each `order_id` as one basket of items.
- Report the strongest rules by **lift**, and interpret the top 2–3 in business terms (*"customers who order X also order Y → promote them together"*).
- Then run it **per segment** — do families order differently from students?
- **Expected output:** a ranked list of rules (support, confidence, lift) + a one-line interpretation of the best ones, overall and per segment.

### Task 3 — Predict who reorders (Classification)
Build a model to predict `reordered` from a diner's profile.
- Use a proper **train/test split**; report **accuracy**, a **confusion matrix**, and compare to the baseline (always predicting the majority class).
- **Think about cost:** which mistake hurts QuickBite more — predicting a loyal diner will churn, or missing a diner who actually churns?
- **Expected output:** your model's accuracy vs. baseline, the confusion matrix, and a sentence on what kind of errors it makes.

### Task 4 — Wire it into the dashboard
Save your trained models so the provided `app.py` can load them, then run the dashboard and test it with a few diner profiles.
- **Expected output:** a running dashboard where typing a diner profile returns their **segment**, a **reorder prediction**, and **recommended items**.

---

## 4. Connecting to the Dashboard (the one interface you must follow)

`app.py` is already written for you — you only need to **save your models in the exact format it expects.** Train your models on these features, then save a file named **`food_models.joblib`** in the same folder as `app.py`, containing a dictionary with these keys:

| Key | What it holds |
|---|---|
| `scaler` | the fitted scaler you used for clustering |
| `kmeans` | your fitted clustering model |
| `segment_names` | a dict mapping each cluster number → your business name, e.g. `{0:'Families', 1:'Budget students', 2:'Premium foodies'}` |
| `clf` | your fitted reorder classifier |
| `features` | the list of clustering features, in order: `['orders_per_month','avg_order_value','avg_items_per_order','days_since_last_order','discount_rate']` |
| `reco` | a dict mapping each segment name → a short list of its most-ordered items |

> **Two rules so the dashboard works:**
> 1. Cluster on the **five `features` above**, in that order.
> 2. Train the **classifier** on those five features **plus `age` and `total_spend`** (the dashboard sends all seven).

Save with `joblib.dump({...}, 'food_models.joblib')`, then in a terminal run:
```
streamlit run app.py
```

---

## 5. What "Done" Looks Like (success criteria)

By the end of class you should be able to show:
- ✅ A justified number of segments, each named and profiled.
- ✅ A ranked set of basket rules, with the best ones interpreted — overall and per segment.
- ✅ A reorder classifier beating the baseline, with its confusion matrix read correctly.
- ✅ A **running dashboard** that takes a diner profile and returns segment + reorder + recommendations.
- ✅ A 3–4 sentence **business takeaway**: which segment to focus on, which bundle to promote, and how to use the reorder model.

---

## 6. Setup & Hints

**Install once (terminal):**
```
pip install pandas numpy matplotlib seaborn scikit-learn mlxtend streamlit joblib
```

**Hints (to keep you moving, not to do it for you):**
- **Scale your features** before clustering — the columns are on very different ranges (orders vs. AED).
- For **Apriori**, the baskets need to be in **one-item-per-column true/false ("one-hot") form** — one row per `order_id`, one column per item. `mlxtend` has `apriori` and `association_rules`.
- A rule is only interesting if its **lift > 1** (ordered together more than by chance).
- Watch the **class balance** in `reordered` before trusting accuracy — compare to always guessing the majority.
- Build the models **first**, save `food_models.joblib`, and wire the dashboard **last** (don't lose time on the app early).

---

## 7. Suggested Timing (2 hours)

| Time | Focus |
|---|---|
| 0:00–0:15 | Read the brief, load & explore the data |
| 0:15–0:45 | Task 1 — Clustering + name the segments |
| 0:45–1:15 | Task 2 — Apriori (overall + per segment) |
| 1:15–1:40 | Task 3 — Reorder classifier |
| 1:40–1:55 | Task 4 — Save models + run the dashboard |
| 1:55–2:00 | Business takeaway |

---

> **Remember:** the goal isn't just to run three algorithms — it's to **reach a decision for QuickBite.** Every result should mean something for the business.
