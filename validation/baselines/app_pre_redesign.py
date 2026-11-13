# app.py — QuickBite Diner Intelligence Dashboard
# ------------------------------------------------------------
# Run locally:   streamlit run app.py
# Needs:         food_models.joblib     (the six-key model contract, created by QuickBite_Analysis.ipynb)
#                dashboard_bundle.joblib (analytics for the management pages, created by the same notebook)
#
# Inference contract (unchanged from the supplied app.py):
#   segment  = kmeans.predict(scaler.transform(profile[FEATURES]))            # 5 clustering features
#   reorder  = clf.predict / clf.predict_proba(profile[FEATURES + ["age", "total_spend"]])  # 7 features
#   items    = reco[segment name]
# The dashboard never re-fits or hand-codes any preprocessing; it only calls the saved, fitted objects.
# ------------------------------------------------------------
from pathlib import Path

import joblib
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import streamlit as st

st.set_page_config(page_title="QuickBite Diner Intelligence", page_icon="🍔", layout="wide",
                   initial_sidebar_state="expanded")

BASE_DIR = Path(__file__).resolve().parent

# ════════════════════════════════════════════════════════════
# 1. Visual system
# ════════════════════════════════════════════════════════════
BG, PANEL, PANEL2 = "#0A1324", "#101D33", "#16274A"
LINE, GRID = "rgba(148,163,184,0.18)", "rgba(148,163,184,0.10)"
TEXT, MUTED, FAINT = "#E6ECF5", "#94A3B8", "#64748B"
GOLD, POS, CAUTION, RISK, STEEL = "#C9A227", "#2BB39A", "#E0A43A", "#E05A67", "#5B8FD6"
FONT = "IBM Plex Sans, Inter, -apple-system, Segoe UI, sans-serif"
SEG_COLORS_DARK = {"Premium Foodies": "#D4B04A", "Family Feasters": "#9A8BDB", "Budget Students": "#5B9BE0"}
TIER_COLORS = {"High retention likelihood": POS, "Moderate retention likelihood": "#7FC4B4",
               "At-risk": CAUTION, "High churn risk": RISK}

st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Sans:wght@400;500;600;700&family=IBM+Plex+Mono:wght@500&display=swap');
html, body, [class*="css"], .stMarkdown, .stText, button, input, select, textarea {{ font-family: {FONT}; }}
.block-container {{ padding-top: 1.6rem; padding-bottom: 3rem; max-width: 1440px; }}
[data-testid="stSidebar"] {{ background: #081021; border-right: 1px solid {LINE}; }}
[data-testid="stSidebar"] .stRadio label p {{ font-size: 0.92rem; }}
h1, h2, h3 {{ letter-spacing: -0.01em; }}
hr {{ border-color: {LINE}; }}
.qb-brand {{ font-weight: 700; letter-spacing: .14em; font-size: .78rem; color: {GOLD}; text-transform: uppercase; }}
.qb-title {{ font-size: 1.85rem; font-weight: 700; color: {TEXT}; margin: .1rem 0 .15rem 0; }}
.qb-sub {{ color: {MUTED}; font-size: .95rem; margin-bottom: .6rem; }}
.qb-kicker {{ color: {GOLD}; font-size: .72rem; font-weight: 600; letter-spacing: .14em; text-transform: uppercase; margin-top: 1.4rem; }}
.qb-h {{ font-size: 1.15rem; font-weight: 600; color: {TEXT}; margin: .15rem 0 .2rem 0; padding-bottom: .35rem; border-bottom: 1px solid {LINE}; }}
.qb-desc {{ color: {MUTED}; font-size: .88rem; margin: .35rem 0 .7rem 0; }}
.kpi {{ background: {PANEL}; border: 1px solid {LINE}; border-radius: 6px; padding: 14px 16px 12px 16px; height: 100%; min-height: 112px; }}
.kpi-label {{ color: {MUTED}; font-size: .70rem; font-weight: 600; letter-spacing: .10em; text-transform: uppercase; }}
.kpi-value {{ color: {TEXT}; font-size: 1.62rem; font-weight: 600; margin-top: 6px; font-variant-numeric: tabular-nums; line-height: 1.15; }}
.kpi-value.sm {{ font-size: 1.18rem; }}
.kpi-sub {{ color: {MUTED}; font-size: .80rem; margin-top: 6px; line-height: 1.35; }}
.tone-pos {{ color: {POS}; }} .tone-caution {{ color: {CAUTION}; }} .tone-risk {{ color: {RISK}; }} .tone-gold {{ color: {GOLD}; }}
.note {{ border-left: 3px solid {STEEL}; background: rgba(91,143,214,0.08); padding: 10px 14px; border-radius: 0 6px 6px 0;
        color: {TEXT}; font-size: .88rem; margin: .4rem 0 .8rem 0; line-height: 1.5; }}
.note.caution {{ border-color: {CAUTION}; background: rgba(224,164,58,0.08); }}
.note.risk {{ border-color: {RISK}; background: rgba(224,90,103,0.08); }}
.note.pos {{ border-color: {POS}; background: rgba(43,179,154,0.08); }}
.note.gold {{ border-color: {GOLD}; background: rgba(201,162,39,0.07); }}
.narr {{ background: {PANEL}; border: 1px solid {LINE}; border-radius: 6px; padding: 16px 20px; line-height: 1.65; font-size: .93rem; }}
.narr b {{ color: {GOLD}; font-weight: 600; }}
.chip {{ display: inline-block; padding: 4px 11px; margin: 0 6px 6px 0; border-radius: 999px; border: 1px solid {LINE};
        background: {PANEL2}; font-size: .84rem; color: {TEXT}; }}
.badge {{ display: inline-block; padding: 2px 9px; border-radius: 4px; font-size: .72rem; font-weight: 600; letter-spacing: .06em; }}
.b-pass {{ background: rgba(43,179,154,.15); color: {POS}; border: 1px solid rgba(43,179,154,.4); }}
.b-review {{ background: rgba(224,164,58,.13); color: {CAUTION}; border: 1px solid rgba(224,164,58,.4); }}
.b-fail {{ background: rgba(224,90,103,.13); color: {RISK}; border: 1px solid rgba(224,90,103,.4); }}
.segcard {{ background: {PANEL}; border: 1px solid {LINE}; border-top: 3px solid var(--c); border-radius: 6px; padding: 14px 16px; height: 100%; }}
.segcard h4 {{ margin: 0 0 4px 0; font-size: 1.02rem; color: {TEXT}; }}
.segcard .meta {{ color: {MUTED}; font-size: .80rem; margin-bottom: 8px; }}
.segcard p {{ font-size: .85rem; color: {TEXT}; margin: 6px 0; line-height: 1.45; }}
.segcard .lbl {{ color: {MUTED}; font-size: .68rem; letter-spacing: .1em; text-transform: uppercase; font-weight: 600; }}
.bigprob {{ font-size: 3.0rem; font-weight: 700; line-height: 1; font-variant-numeric: tabular-nums; }}
.foot {{ color: {FAINT}; font-size: .76rem; margin-top: 2rem; border-top: 1px solid {LINE}; padding-top: .7rem; }}
</style>
""", unsafe_allow_html=True)


# ── formatting helpers ──────────────────────────────────────
def aed(x, d=0):
    return f"AED {x:,.{d}f}"


def pct(x, d=0):
    return f"{x * 100:.{d}f}%"


def pp(x, d=1):
    return f"{x:+.{d}f} pp"


def pretty(item):
    return str(item).replace("_", " ").title()


def kpi(col, label, value, sub="", tone="", small=False, help_text=None):
    title = f' title="{help_text}"' if help_text else ""
    col.markdown(f'<div class="kpi"{title}><div class="kpi-label">{label}</div>'
                 f'<div class="kpi-value {"sm" if small else ""} {("tone-" + tone) if tone else ""}">{value}</div>'
                 f'<div class="kpi-sub">{sub}</div></div>', unsafe_allow_html=True)


def section(title, kicker=None, desc=None):
    if kicker:
        st.markdown(f'<div class="qb-kicker">{kicker}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="qb-h">{title}</div>', unsafe_allow_html=True)
    if desc:
        st.markdown(f'<div class="qb-desc">{desc}</div>', unsafe_allow_html=True)


def note(text, kind=""):
    st.markdown(f'<div class="note {kind}">{text}</div>', unsafe_allow_html=True)


def page_header(title, sub):
    st.markdown(f'<div class="qb-brand">QuickBite · Diner Intelligence</div><div class="qb-title">{title}</div>'
                f'<div class="qb-sub">{sub}</div>', unsafe_allow_html=True)


def badge(status):
    s = str(status).upper()
    cls = "b-pass" if s.startswith("PASS") and "REVIEW" not in s else ("b-fail" if s.startswith("FAIL") else "b-review")
    return f'<span class="badge {cls}">{s}</span>'


def style_fig(fig, title=None, height=360, xt=None, yt=None, legend=True, legend_title=None, legend_inside=None):
    fig.update_layout(
        template="none", paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", height=height,
        font=dict(family=FONT, color=TEXT, size=12),
        title=dict(text=title, x=0, xanchor="left", y=0.98, yanchor="top", font=dict(size=14, color=TEXT)) if title else None,
        margin=dict(l=8, r=12, t=(92 if legend else 58) if title else (40 if legend else 16), b=8), showlegend=legend,
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="left", x=0, bgcolor="rgba(0,0,0,0)", font=dict(color=MUTED, size=11),
                    title=dict(text=f"<b>{legend_title}</b>  " if legend_title else "", font=dict(color=TEXT, size=11))),
        hoverlabel=dict(bgcolor=PANEL2, bordercolor=GOLD, font=dict(family=FONT, color=TEXT, size=12)),
    )
    if legend_inside:                       # e.g. "br", "tl": place a vertical legend inside the plot area (narrow charts)
        x_, xa = (0.98, "right") if legend_inside[1] == "r" else (0.02, "left")
        y_, ya = (0.02, "bottom") if legend_inside[0] == "b" else (0.98, "top")
        fig.update_layout(legend=dict(orientation="v", x=x_, xanchor=xa, y=y_, yanchor=ya, bgcolor="rgba(10,19,36,0.85)",
                                      bordercolor=LINE, borderwidth=1), margin=dict(t=58 if title else 16))
    fig.update_xaxes(title=xt, gridcolor=GRID, zerolinecolor=GRID, linecolor=LINE, tickfont=dict(color=MUTED),
                     title_font=dict(color=MUTED, size=12), automargin=True)
    fig.update_yaxes(title=yt, gridcolor=GRID, zerolinecolor=GRID, linecolor=LINE, tickfont=dict(color=MUTED),
                     title_font=dict(color=MUTED, size=12), automargin=True)
    return fig


def show(fig, key=None):
    cfg = {"displayModeBar": False, "displaylogo": False}
    fig.update_traces(cliponaxis=False, selector=dict(type="bar"))       # never clip value labels at the plot edge
    fig.update_traces(cliponaxis=False, selector=dict(type="scatter"))
    try:
        st.plotly_chart(fig, width="stretch", config=cfg, key=key)
    except TypeError:                               # older Streamlit
        st.plotly_chart(fig, use_container_width=True, config=cfg, key=key)


def table(df, height=None, column_config=None):
    kw = dict(hide_index=True, column_config=column_config)
    if height:
        kw["height"] = height
    try:
        st.dataframe(df, width="stretch", **kw)
    except TypeError:
        st.dataframe(df, use_container_width=True, **kw)


# ════════════════════════════════════════════════════════════
# 2. Load models (exact contract) and the analytics bundle
# ════════════════════════════════════════════════════════════
@st.cache_resource
def load_models():
    return joblib.load(BASE_DIR / "food_models.joblib")


def _restore(obj):
    if isinstance(obj, dict):
        if "__df__" in obj:
            s = obj["__df__"]
            return pd.DataFrame(s["data"], index=s["index"], columns=s["columns"])
        if "__series__" in obj:
            s = obj["__series__"]
            return pd.Series(s["data"], index=s["index"], name=s["name"])
        return {k: _restore(v) for k, v in obj.items()}
    if isinstance(obj, list):
        return [_restore(v) for v in obj]
    if isinstance(obj, tuple):
        return tuple(_restore(v) for v in obj)
    return obj


@st.cache_resource
def load_bundle():
    path = BASE_DIR / "dashboard_bundle.joblib"
    return _restore(joblib.load(path)) if path.exists() else None


try:
    M = load_models()
except FileNotFoundError:
    st.error("`food_models.joblib` was not found next to app.py. Run **QuickBite_Analysis.ipynb** top to bottom to create it.")
    st.stop()
except Exception as exc:  # e.g. scikit-learn version mismatch when unpickling
    st.error(f"Could not load `food_models.joblib` ({type(exc).__name__}: {exc}). Re-run the notebook in this "
             "environment so the models are saved with your installed scikit-learn version.")
    st.stop()

missing = {"scaler", "kmeans", "segment_names", "clf", "features", "reco"} - set(M)
if missing:
    st.error(f"`food_models.joblib` is missing keys: {sorted(missing)}")
    st.stop()

scaler, kmeans = M["scaler"], M["kmeans"]
seg_names, clf, FEATURES, reco = M["segment_names"], M["clf"], M["features"], M["reco"]
CLF_FEATURES = FEATURES + ["age", "total_spend"]
B = load_bundle()


def analyse(profile: dict):
    """Return (segment name, reorder yes/no, reorder probability, recommended items). Unchanged from the supplied app.py."""
    row = pd.DataFrame([profile])
    seg = int(kmeans.predict(scaler.transform(row[FEATURES]))[0])
    name = seg_names.get(seg, f"Segment {seg}")
    reorder = int(clf.predict(row[FEATURES + ["age", "total_spend"]])[0])
    prob = float(clf.predict_proba(row[FEATURES + ["age", "total_spend"]])[0][1])
    return name, reorder, prob, reco.get(name, [])


# ── analytics helpers built on the saved, fitted objects ────
LABELS = {"orders_per_month": "Orders per month", "avg_order_value": "Avg order value (AED)",
          "avg_items_per_order": "Avg items per order", "days_since_last_order": "Days since last order",
          "discount_rate": "Discount usage rate", "age": "Age (years)", "total_spend": "Total spend (AED)"}
SEG_ORDER = B["seg_order"] if B else list(seg_names.values())
SC = {s: SEG_COLORS_DARK.get(s, STEEL) for s in SEG_ORDER}
RISK_TIERS = [(0.75, "High retention likelihood", "Loyalty reward / premium upsell — no discount needed"),
              (0.50, "Moderate retention likelihood", "Personalised promotion on segment favourites"),
              (0.25, "At-risk", "Targeted retention offer within 7 days"),
              (0.00, "High churn risk", "Win-back offer on favourite bundle + reminder")]
if B:
    RISK_TIERS = [(t[0], t[1], t[2]) for t in B["risk_tiers"]]


def risk_tier(p):
    for lo, label, action in RISK_TIERS:
        if p >= lo:
            return label, action
    return RISK_TIERS[-1][1], RISK_TIERS[-1][2]


def contributions(profile):
    """Exact per-feature log-odds contributions for the logistic pipeline, relative to an average diner (z = 0)."""
    try:
        sc, lr = clf.named_steps["scaler"], clf.named_steps["classifier"]
        z = sc.transform(pd.DataFrame([profile])[CLF_FEATURES])[0]
        return pd.Series(lr.coef_[0] * z, index=CLF_FEATURES)
    except Exception:
        return None


def num(v):
    v = float(v)
    return f"{v:,.0f}" if v.is_integer() else f"{v:,.2f}"


def extrapolation(profile):
    if not B:
        return []
    return [f"{LABELS[f]} = {num(profile[f])} (training range {num(lo)}–{num(hi)})"
            for f, (lo, hi) in B["train_ranges"].items() if not lo <= profile[f] <= hi]


def atypical_for_segment(profile):
    row = pd.DataFrame([profile])
    z = scaler.transform(row[FEATURES])
    c = int(kmeans.predict(z)[0])
    dist = float(np.linalg.norm(z[0] - kmeans.cluster_centers_[c]))
    return bool(B) and dist > B["centroid_dist_p95"], dist


def preset_profiles():
    base = {"App default (typical diner)": dict(age=28, orders_per_month=8, avg_order_value=90.0, avg_items_per_order=3,
                                               days_since_last_order=10, discount_rate=0.30, total_spend=800.0)}
    if B:
        d = B["diners"]
        d = d[d.include_in_classifier]
        for s in SEG_ORDER:
            m = d[d.segment == s][CLF_FEATURES].median()
            base[f"Typical {s[:-1] if s.endswith('s') else s}"] = _clean_profile(m.to_dict())
        lapsed = d[(d.segment == "Family Feasters") & (d.reordered == 0)][CLF_FEATURES].median()
        base["Lapsed Family Feaster"] = _clean_profile(lapsed.to_dict())
        coin = d[(d.segment == "Premium Foodies") & d.reorder_prob_oof.between(0.4, 0.6)][CLF_FEATURES].median()
        if not coin.isna().any():
            base["Uncertain Premium Foodie (coin-flip)"] = _clean_profile(coin.to_dict())
    return base


def _clean_profile(p):
    return dict(age=int(round(p["age"])), orders_per_month=int(round(p["orders_per_month"])),
                avg_order_value=float(round(p["avg_order_value"], 0)), avg_items_per_order=int(round(p["avg_items_per_order"])),
                days_since_last_order=int(round(p["days_since_last_order"])), discount_rate=float(round(p["discount_rate"] * 20) / 20),
                total_spend=float(round(p["total_spend"] / 10) * 10))


PRESETS = preset_profiles()

# Input ranges: identical to the supplied app.py. Age stays 18–70 — under-18 diners are outside the classifier (18+ policy).
INPUT_SPEC = {"age": (18, 70, 1), "orders_per_month": (1, 20, 1), "avg_order_value": (15.0, 250.0, 1.0),
              "avg_items_per_order": (1, 10, 1), "days_since_last_order": (0, 60, 1), "discount_rate": (0.0, 1.0, 0.05),
              "total_spend": (50.0, 20000.0, 50.0)}


def linked_spend(base, after):
    """total_spend ≈ orders × AOV in the data (ratio 0.85–1.15), so scale the diner's own total spend proportionally."""
    denom = base["orders_per_month"] * base["avg_order_value"]
    return float(base["total_spend"] * after["orders_per_month"] * after["avg_order_value"] / denom) if denom else base["total_spend"]


def profile_inputs(prefix, container, defaults, linked_base=None):
    """Seven inputs bound to session state. Returns the profile dict in raw business units.
    With linked_base, total spend is derived from the base diner instead of being a free input."""
    for f, v in defaults.items():
        st.session_state.setdefault(f"{prefix}_{f}", v)
    c = container
    vals = {}
    for f in ["orders_per_month", "avg_order_value", "avg_items_per_order", "days_since_last_order", "discount_rate", "age"]:
        lo, hi, step = INPUT_SPEC[f]
        key = f"{prefix}_{f}"
        st.session_state[key] = type(lo)(min(max(st.session_state[key], lo), hi))
        vals[f] = c.slider(LABELS[f], lo, hi, step=step, key=key)
    lo, hi, step = INPUT_SPEC["total_spend"]
    key = f"{prefix}_total_spend"
    if linked_base is not None:
        vals["total_spend"] = linked_spend(linked_base, vals)
        c.markdown(f"<div class='qb-desc'><b>{LABELS['total_spend']}</b> (linked): {aed(vals['total_spend'])}<br>"
                   f"Scaled from the base diner's {aed(linked_base['total_spend'])} in line with orders × AOV.</div>", unsafe_allow_html=True)
        return {k: vals[k] for k in ["age", "orders_per_month", "avg_order_value", "avg_items_per_order",
                                     "days_since_last_order", "discount_rate", "total_spend"]}
    st.session_state[key] = float(min(max(st.session_state[key], lo), hi))
    vals["total_spend"] = c.number_input(LABELS["total_spend"], lo, hi, step=step, key=key,
                                         help="In the data, total spend ≈ orders per month × average order value (about one month of spend).")
    return {k: vals[k] for k in ["age", "orders_per_month", "avg_order_value", "avg_items_per_order",
                                 "days_since_last_order", "discount_rate", "total_spend"]}


def set_profile(prefix, profile):
    for f, v in profile.items():
        lo, hi, _ = INPUT_SPEC[f]
        st.session_state[f"{prefix}_{f}"] = type(lo)(min(max(v, lo), hi))


def no_bundle_notice():
    note("This page needs <code>dashboard_bundle.joblib</code>. Run <b>QuickBite_Analysis.ipynb</b> top to bottom to create it. "
         "The <b>Diner Intelligence</b> page works with <code>food_models.joblib</code> alone.", "caution")


# ════════════════════════════════════════════════════════════
# 3. Pages
# ════════════════════════════════════════════════════════════
def page_overview():
    page_header("Executive Overview", "Who QuickBite's diners are, what they're worth, and where retention risk sits.")
    if not B:
        return no_bundle_notice()
    d, P, E = B["diners"], B["seg_profile"], B["seg_econ"]
    scored = d[d.reorder_prob_oof.notna()]
    at_risk = scored[scored.reorder_prob_oof < 0.5]
    opp = B["basket_opportunity"]
    top = opp.sort_values("Lift", ascending=False).iloc[0]
    hv = E["value"].idxmax()
    mv = E["movable_value"].idxmax()

    c = st.columns(5)
    kpi(c[0], "Total diners", f"{len(d):,}", f"{B['meta']['n_baskets']:,} baskets · {B['meta']['n_items']} menu items")
    kpi(c[1], "Retention rate", pct(d.reordered.mean()), f"Churn {pct(1 - d.reordered.mean())} · did not reorder", "pos")
    kpi(c[2], "Adult diners at risk", f"{len(at_risk):,}", f"of {len(scored)} scored (18+) · P(reorder) &lt; 50% · {aed(at_risk.est_monthly_spend.sum())} monthly spend",
        "risk", help_text="Out-of-fold probabilities: each diner scored by a model that did not see them in training. Under-18 diners are not scored.")
    kpi(c[3], "Monthly spend / diner", aed(d.est_monthly_spend.mean()),
        f"{d.orders_per_month.mean():.1f} orders/month × {aed(d.avg_order_value.mean())} AOV")
    rcv = B["validation"]["repeated_cv"]
    kpi(c[4], "Model accuracy", pct(rcv["acc_mean"], 1),
        f"Repeated CV ± {pct(rcv['acc_sd'], 1)} · baseline {pct(rcv['baseline'], 1)} · AUC {rcv['auc_mean']:.2f}", "pos")

    st.write("")
    c = st.columns([1, 1, 1.25])
    kpi(c[0], "Highest-value segment", hv, f"{aed(E.loc[hv, 'value'])} per diner / month · {pct(P.loc[hv, 'Share of monthly revenue'])} of revenue", "gold", small=True)
    kpi(c[1], "Largest movable value", mv, f"{int(E.loc[mv, 'movable_diners'])} diners at 25–75% hold {aed(E.loc[mv, 'movable_value'])} / month", "caution", small=True)
    kpi(c[2], "Top bundle (highest in-segment lift)", f"{top['If basket has (A)']} → {top['Recommend (B)']}",
        f"{top['Segment']} · {pct(top['Confidence'])} confidence · lift {top['Lift']:.1f}×", small=True)

    u18 = B["under18"]
    note(f"<b>Data scope.</b> Segmentation and basket analysis use all {len(d)} diners. The reorder classifier and every probability on this "
         f"dashboard cover the <b>{len(scored)} adult diners (18+)</b>; the {u18['n']} under-18 diners are excluded from the classifier and the age "
         "input under the 18+ policy (see Governance &amp; Data Quality).", "")
    section("Management summary", "Situation")
    largest = P.loc[SEG_ORDER, "Diners"].idxmax()
    fam = "Family Feasters"
    prem_bundle = opp[opp.Segment == hv].iloc[0]
    st.markdown(f"""<div class="narr">
    QuickBite's diner base is concentrated in <b>{largest}</b> ({pct(P.loc[largest, 'Share of diners'])} of diners), who reorder almost always
    ({pct(P.loc[largest, 'Reorder rate'])}) but spend the least per order. The <b>highest-value segment is {hv}</b> at {aed(E.loc[hv, 'value'])} per diner
    per month ({pct(P.loc[hv, 'Share of monthly revenue'])} of revenue), yet only {pct(P.loc[hv, 'Reorder rate'])} of them reorder.
    The <b>strongest cross-sell opportunity</b> is {top['If basket has (A)']} → {top['Recommend (B)']} for {top['Segment']} ({pct(top['Confidence'])} of the time, {top['Lift']:.1f}× chance);
    for {hv}, {prem_bundle['If basket has (A)']} → {prem_bundle['Recommend (B)']} ({pct(prem_bundle['Confidence'])}, {prem_bundle['Lift']:.1f}×).
    The <b>most important retention risk</b> is {mv}: {int(E.loc[mv, 'movable_diners'])} diners holding {aed(E.loc[mv, 'movable_value'])} of monthly spend sit in the
    uncertain 25–75% probability band. {fam} churn most ({pct(P.loc[fam, 'Churn rate'])}) but {int(E.loc[fam, 'lapsed_diners'])} of {int(E.loc[fam, 'diners_n'])} are already below 25%.
    <b>Management should prioritise</b> protecting {hv} with loyalty perks and premium bundles, run a selective win-back for the highest-value lapsed families,
    and serve {largest} efficiently with less discounting.</div>""", unsafe_allow_html=True)

    section("Segment economics", "Portfolio")
    c1, c2 = st.columns(2)
    with c1:
        fig = go.Figure()
        fig.add_bar(name="Share of diners", x=SEG_ORDER, y=P.loc[SEG_ORDER, "Share of diners"], marker_color=FAINT,
                    text=[pct(v) for v in P.loc[SEG_ORDER, "Share of diners"]], textposition="outside",
                    hovertemplate="%{x}<br>Share of diners: %{y:.1%}<extra></extra>")
        fig.add_bar(name="Share of est. monthly revenue", x=SEG_ORDER, y=P.loc[SEG_ORDER, "Share of monthly revenue"],
                    marker_color=[SC[s] for s in SEG_ORDER], text=[pct(v) for v in P.loc[SEG_ORDER, "Share of monthly revenue"]],
                    textposition="outside", hovertemplate="%{x}<br>Share of revenue: %{y:.1%}<extra></extra>")
        style_fig(fig, "Share of diners vs share of revenue by segment", xt="Segment", yt="Share of total (%)", height=360, legend_title="Measure")
        fig.update_yaxes(tickformat=".0%", range=[0, 0.55])
        fig.update_layout(barmode="group", bargap=0.35)
        show(fig, "ov_conc")
    with c2:
        rr = P.loc[SEG_ORDER, "Reorder rate"]
        fig = go.Figure(go.Bar(x=SEG_ORDER, y=rr, marker_color=[SC[s] for s in SEG_ORDER], text=[pct(v) for v in rr],
                               textposition="outside", hovertemplate="%{x}<br>Reorder rate: %{y:.1%}<extra></extra>"))
        fig.add_hline(y=d.reordered.mean(), line_dash="dash", line_color=MUTED)
        style_fig(fig, f"Retention by segment (dashed line = all diners, {pct(d.reordered.mean())})", xt="Segment", yt="Reorder rate (%)",
                  height=360, legend=False)
        fig.update_yaxes(tickformat=".0%", range=[0, 1.12])
        show(fig, "ov_ret")

    c1, c2 = st.columns(2)
    with c1:
        tiers = [t[1] for t in RISK_TIERS][::-1]
        fig = go.Figure()
        for s in SEG_ORDER:
            cnt = scored[scored.segment == s].risk_tier.value_counts().reindex(tiers).fillna(0)
            fig.add_bar(name=s, y=tiers, x=cnt.values, orientation="h", marker_color=SC[s],
                        text=[int(v) if v >= 6 else "" for v in cnt.values], textposition="inside", insidetextanchor="middle",
                        textfont=dict(color=BG), hovertemplate=f"{s}<br>%{{y}}: %{{x}} diners<extra></extra>")
        totals = scored.risk_tier.value_counts().reindex(tiers).fillna(0)
        for t_, v_ in totals.items():
            fig.add_annotation(x=v_, y=t_, text=f"<b>{int(v_)}</b> ({pct(v_ / len(scored))})", showarrow=False, xanchor="left", xshift=6,
                               font=dict(color=TEXT, size=11))
        style_fig(fig, f"Risk-tier composition by segment ({len(scored)} adult diners, out-of-fold)", xt="Number of diners", yt="Risk tier",
                  height=360, legend_title="Segment")
        fig.update_layout(barmode="stack")
        fig.update_xaxes(range=[0, totals.max() * 1.3])
        show(fig, "ov_tiers")
    with c2:
        f = B["item_freq"].head(8)[::-1]
        fig = go.Figure(go.Bar(x=f.values, y=[pretty(i) for i in f.index], orientation="h", marker_color=STEEL,
                               text=[pct(v) for v in f.values], textposition="outside",
                               hovertemplate="%{y}: in %{x:.1%} of baskets<extra></extra>"))
        style_fig(fig, f"Top 8 products — share of all {B['meta']['n_baskets']:,} baskets", xt="Share of baskets containing the item (%)",
                  yt="Menu item", height=360, legend=False)
        fig.update_xaxes(tickformat=".0%", range=[0, f.max() * 1.18])
        show(fig, "ov_items")

    section("Revenue concentration", "Portfolio risk", "How dependent is QuickBite on its top spenders? Diners ranked from highest to lowest estimated monthly spend.")
    L = B["lorenz"]
    c1, c2 = st.columns([1.4, 1])
    with c1:
        fig = go.Figure()
        fig.add_scatter(x=[0, 1], y=[0, 1], mode="lines", line=dict(dash="dash", color=FAINT), name="Perfect equality (Gini 0)")
        fig.add_scatter(x=L["pop"], y=L["rev"], mode="lines", line=dict(color=GOLD, width=3), name=f"QuickBite diners (Gini {L['gini']:.2f})",
                        hovertemplate="Top %{x:.0%} of diners → %{y:.0%} of revenue<extra></extra>")
        for k_, q_ in zip(L["conc"], (0.1, 0.2, 0.5)):
            fig.add_scatter(x=[q_], y=[L["conc"][k_]], mode="markers+text", marker=dict(size=10, color=GOLD, line=dict(color=TEXT, width=1)),
                            text=[f"{k_} → {pct(L['conc'][k_])} of revenue"], textposition="bottom right", textfont=dict(color=TEXT, size=11),
                            showlegend=False, hoverinfo="skip")
        style_fig(fig, "Lorenz curve — cumulative revenue by share of diners", xt="Cumulative share of diners (highest spenders first)",
                  yt="Cumulative share of est. monthly revenue", height=380, legend_title="Curve")
        fig.update_xaxes(tickformat=".0%"); fig.update_yaxes(tickformat=".0%")
        show(fig, "ov_lorenz")
    with c2:
        mix = L["top20_mix"]
        fig = go.Figure(go.Bar(x=list(mix.index), y=mix.values, marker_color=[SC[s] for s in mix.index], text=[pct(v) for v in mix.values],
                               textposition="outside", hovertemplate="%{x}: %{y:.0%} of the top-20% spenders<extra></extra>"))
        style_fig(fig, "Segment mix of the top 20% spenders", xt="Segment", yt="Share of top-20% diners (%)", height=380, legend=False)
        fig.update_yaxes(tickformat=".0%", range=[0, max(mix.max() * 1.2, .1)])
        show(fig, "ov_top20")
    note(f"Revenue is only mildly concentrated (Gini {L['gini']:.2f}; the top 20% of diners generate {pct(L['conc']['Top 20%'])} of revenue), "
         f"so QuickBite does not depend on a few large accounts — churn matters in aggregate. {pct(mix.max())} of the top fifth are "
         f"{mix.idxmax()}, reinforcing them as the segment to protect.", "gold")


def page_segmentation():
    page_header("Customer Segmentation", "K-Means on five behavioural features (scaled), with K chosen by elbow and silhouette evidence.")
    if not B:
        return no_bundle_notice()
    d, P, k = B["diners"], B["seg_profile"], B["k_eval"]
    best = k.loc[k.Silhouette.idxmax()]
    c = st.columns(4)
    kpi(c[0], "Segments (K)", f"{B['meta']['K']}", "Chosen on elbow + silhouette + business fit")
    kpi(c[1], "Silhouette score", f"{best.Silhouette:.3f}", f"Highest of K = 2–8 · next best {k.Silhouette.nlargest(2).iloc[-1]:.3f}", "pos")
    kpi(c[2], "Variance shown in 2-D", pct(sum(B["pca_var"])), "PCA projection used only for visualisation")
    kpi(c[3], "Features clustered", "5", "Frequency · ticket · basket · recency · discount")

    t1, t2, t3 = st.tabs(["Segment profiles & strategy", "Choosing K", "Behavioural detail"])
    with t1:
        section("Who are QuickBite's diners?", desc="Names describe observed behaviour (plus average age and menu); 'student' and 'family' are behavioural personas, not recorded attributes.")
        cols = st.columns(3)
        strat = B["seg_strategy"]
        for col, s in zip(cols, SEG_ORDER):
            r = P.loc[s]
            col.markdown(f"""<div class="segcard" style="--c:{SC[s]}"><h4>{s}</h4>
            <div class="meta">{int(r.Diners)} diners · {pct(r['Share of diners'])} of base · {pct(r['Share of monthly revenue'])} of revenue</div>
            <div class="lbl">Who they are</div><p>{strat[s]['who']}</p>
            <div class="lbl">Value · Risk</div><p>{aed(r['Est. monthly spend (AED)'])}/month per diner · reorder {pct(r['Reorder rate'])}. {strat[s]['risk']}</p>
            <div class="lbl">Discounts · Loyalty</div><p>{strat[s]['discounts']} {strat[s]['loyalty']}</p>
            <div class="lbl">Management action</div><p style="color:{SC[s]}">{strat[s]['action']}</p></div>""", unsafe_allow_html=True)

        section("Segment profile vs overall average", "Profile")
        rows = ["Diners", "Share of diners", "Orders / month", "Avg order value (AED)", "Items / order", "Days since last order",
                "Discount usage", "Total spend (AED)", "Est. monthly spend (AED)", "Spend per item (AED)", "Avg age", "Reorder rate",
                "Churn rate", "Share of monthly revenue"]
        fmt = {"Diners": lambda v: f"{v:,.0f}", "Share of diners": pct, "Orders / month": lambda v: f"{v:.1f}",
               "Avg order value (AED)": aed, "Items / order": lambda v: f"{v:.1f}", "Days since last order": lambda v: f"{v:.1f} days",
               "Discount usage": pct, "Total spend (AED)": aed, "Est. monthly spend (AED)": aed, "Spend per item (AED)": aed,
               "Avg age": lambda v: f"{v:.0f} yrs", "Reorder rate": pct, "Churn rate": pct, "Share of monthly revenue": pct}
        disp = pd.DataFrame({"Metric": rows})
        for s in SEG_ORDER + ["All diners"]:
            disp[s] = [fmt[r](P.loc[s, r]) for r in rows]
        table(disp, height=528)

        idx = B["seg_index"].loc[SEG_ORDER]
        fig = go.Figure(go.Heatmap(z=idx.values, x=list(idx.columns), y=SEG_ORDER, zmid=100,
                                   colorscale=[[0, "#3B6FB6"], [0.5, "#1B2A47"], [1, "#C9A227"]],
                                   text=idx.values.astype(int), texttemplate="%{text}", textfont=dict(color=TEXT),
                                   hovertemplate="%{y}<br>%{x}: index %{z:.0f} (100 = overall average)<extra></extra>",
                                   colorbar=dict(title=dict(text="Index", font=dict(color=MUTED)), tickfont=dict(color=MUTED))))
        style_fig(fig, "Behavioural fingerprint — index vs overall average (100 = average; >100 above, <100 below)",
                  xt="Behavioural metric", yt="Segment", height=320, legend=False)
        fig.update_xaxes(showgrid=False)
        fig.update_yaxes(showgrid=False, autorange="reversed")
        show(fig, "seg_heat")

        section("Size, value and retention", "Segment economics")
        cc = st.columns(3)
        for col, metric, ttl, yt, fmt_ in [(cc[0], "Diners", "Segment size", "Number of diners", lambda v: f"{v:.0f} ({pct(v / P.loc['All diners', 'Diners'])})"),
                                          (cc[1], "Est. monthly spend (AED)", "Est. monthly spend per diner", "AED per diner per month", aed),
                                          (cc[2], "Reorder rate", "Reorder rate", "Share of diners who reordered (%)", pct)]:
            vals = P.loc[SEG_ORDER, metric]
            fig = go.Figure(go.Bar(x=SEG_ORDER, y=vals, marker_color=[SC[x] for x in SEG_ORDER], text=[fmt_(v) for v in vals],
                                   textposition="outside", hovertemplate="%{x}: %{text}<extra></extra>"))
            if metric == "Reorder rate":
                fig.add_hline(y=P.loc["All diners", metric], line_dash="dash", line_color=MUTED)
                ttl = f"Reorder rate (dashed = all diners, {pct(P.loc['All diners', metric])})"
                fig.update_yaxes(tickformat=".0%")
            style_fig(fig, ttl, xt="Segment", yt=yt, height=320, legend=False)
            fig.update_yaxes(range=[0, vals.max() * 1.2])
            with col:
                show(fig, f"seg_bar_{metric}")

        section("Are the segments statistically distinct?", "Validation",
                "Kruskal–Wallis tests (non-parametric ANOVA) per feature, with effect size ε² (≥ 0.26 = large); χ² test of reorder rate by segment.")
        kw = B["validation"]["kw_tests"]; ch = B["validation"]["chi2"]
        c1, c2 = st.columns([1.35, 1])
        with c1:
            kws = kw.sort_values("Effect size ε²")
            fig = go.Figure(go.Bar(x=kws["Effect size ε²"], y=kws.Feature, orientation="h",
                                   marker_color=[STEEL if u else FAINT for u in kws["Used in clustering"]],
                                   text=[f"ε² {e:.2f} · p {'< 0.001' if pv < 0.001 else f'= {pv:.3f}'}" for e, pv in zip(kws['Effect size ε²'], kws['p-value'])],
                                   textposition="outside", hovertemplate="%{y}: ε² = %{x:.3f}<extra></extra>"))
            fig.add_vline(x=0.26, line_dash="dot", line_color=GOLD, annotation_text="large effect ≥ 0.26", annotation_font_color=GOLD,
                          annotation_position="top right")
            style_fig(fig, "Effect size of segment on each feature (blue = clustering feature, grey = not used)",
                      xt="Effect size ε² (share of rank variance explained by segment)", yt="Feature", height=340, legend=False)
            fig.update_xaxes(range=[0, 1.25])
            show(fig, "seg_kw")
        with c2:
            st.write("")
            kpi(st, "Reorder rate × segment", f"χ²({int(ch['dof'])}) = {ch['chi2']:.0f}",
                f"p = {ch['p']:.1e} · Cramér's V = {ch['cramers_v']:.2f} (strong association)", "pos", small=True)
            st.write("")
            note("All seven features differ across segments with <b>large</b> effects (p &lt; 0.001), including age and total spend, which "
                 "were not used to build the segments — independent evidence that the personas are real. Reorder behaviour is also "
                 "strongly tied to segment (Cramér's V shown).", "pos")

    with t2:
        section("Evidence for K = 3", desc="All four criteria agree; K = 4 only splits Family Feasters by recency, which is a churn signal the classifier already uses rather than a new persona.")
        c1, c2 = st.columns(2)
        for col, metric, ttl, yt in [(c1, "Inertia", "Elbow method — within-cluster sum of squares", "Inertia (scaled units²)"),
                                     (c2, "Silhouette", "Silhouette score by K (higher = better separated)", "Mean silhouette score")]:
            fig = go.Figure(go.Scatter(x=k.K, y=k[metric], mode="lines+markers+text", line=dict(color=STEEL, width=2),
                                       marker=dict(size=9, color=[GOLD if kk == 3 else STEEL for kk in k.K]),
                                       text=[f"{v:,.0f}" if metric == "Inertia" else f"{v:.3f}" for v in k[metric]],
                                       textposition="top center", textfont=dict(color=TEXT, size=11), name=metric,
                                       hovertemplate="K = %{x}<br>" + metric + ": %{y:.3f}<extra></extra>"))
            fig.add_annotation(x=3, y=float(k.set_index("K").loc[3, metric]), text="<b>Chosen K = 3</b>", showarrow=True, arrowcolor=GOLD,
                               font=dict(color=GOLD), ax=-70 if metric == "Inertia" else 60, ay=40 if metric == "Inertia" else -35)
            style_fig(fig, ttl, xt="Number of segments (K)", yt=yt, height=340, legend=False)
            fig.update_xaxes(dtick=1)
            fig.update_yaxes(range=[0 if metric == "Inertia" else k[metric].min() * .85, k[metric].max() * 1.15])
            with col:
                show(fig, f"k_{metric}")
        kd = k.copy()
        disp = pd.DataFrame({"K": kd.K.astype(int), "Inertia": kd.Inertia.map(lambda v: f"{v:,.1f}"),
                             "Inertia drop vs K−1": kd["Inertia drop vs K-1"].map(lambda v: "—" if pd.isna(v) else pct(v)),
                             "Silhouette ↑": kd.Silhouette.map(lambda v: f"{v:.3f}"), "Davies–Bouldin ↓": kd["Davies-Bouldin"].map(lambda v: f"{v:.3f}"),
                             "Calinski–Harabasz ↑": kd["Calinski-Harabasz"].map(lambda v: f"{v:,.0f}"), "Smallest segment": kd["Smallest cluster"].astype(int)})
        table(disp)
        note("Features are standardised before clustering: unscaled, average order value (range ≈ AED 190) would dominate discount "
             "usage (range ≈ 0.9) in the Euclidean distance K-Means uses.", "")

        section("Are the segments stable?", "Robustness", "K-Means re-fitted on 200 bootstrap resamples and 50 random seeds; agreement with the final "
                "segments measured by the Adjusted Rand Index (1 = identical, 0 = chance).")
        cs = B["validation"]["cluster_stability"]
        stab = {"Bootstrap mean ARI (200 re-fits)": cs["boot_mean"], "Bootstrap worst-5% ARI": cs["boot_p5"],
                "Seed re-runs mean ARI (50)": cs["seed_mean"], "Seed re-runs identical (share)": cs["seed_share_perfect"]}
        fig = go.Figure(go.Bar(x=list(stab), y=list(stab.values()), marker_color=[STEEL, STEEL, FAINT, FAINT],
                               text=[pct(v) if "share" in k_ else f"{v:.3f}" for k_, v in stab.items()], textposition="outside",
                               hovertemplate="%{x}: %{text}<extra></extra>"))
        fig.add_hline(y=0.9, line_dash="dot", line_color=GOLD, annotation_text="highly stable ≥ 0.90", annotation_font_color=GOLD, annotation_position="bottom right")
        style_fig(fig, "Cluster stability — agreement with the final segments", xt="Stability test", yt="Adjusted Rand Index / share", height=330, legend=False)
        fig.update_yaxes(range=[0, 1.18])
        show(fig, "seg_stab")
        note(f"Every bootstrap re-fit and every random seed reproduced the same three segments (mean ARI {cs['boot_mean']:.3f}). "
             "The segmentation is not an artefact of the sample or the initialisation.", "pos")

    with t3:
        c1, c2 = st.columns(2)
        with c1:
            fig = go.Figure()
            for s in SEG_ORDER:
                ss = d[d.segment == s]
                fig.add_scatter(x=ss.pc1, y=ss.pc2, mode="markers", name=f"{s} ({len(ss)})", marker=dict(color=SC[s], size=6, opacity=.65),
                                customdata=np.c_[ss.diner_id, ss.orders_per_month, ss.avg_order_value],
                                hovertemplate="%{customdata[0]}<br>%{customdata[1]} orders/month · AED %{customdata[2]:.0f} AOV<extra>" + s + "</extra>")
                fig.add_scatter(x=[ss.pc1.mean()], y=[ss.pc2.mean()], mode="markers+text", marker=dict(symbol="x", size=14, color=SC[s], line=dict(color=TEXT, width=1)),
                                text=[f"<b>{s}</b><br>{len(ss)} diners · {pct(len(ss) / len(d))}"], textposition="top center",
                                textfont=dict(color=TEXT, size=11), showlegend=False, hoverinfo="skip")
            v = B["pca_var"]
            style_fig(fig, "PCA projection of the five scaled features (✕ = segment centre)", xt=f"Principal component 1 ({pct(v[0], 1)} of variance)",
                      yt=f"Principal component 2 ({pct(v[1], 1)} of variance)", height=420, legend_title="Segment (diners)")
            show(fig, "seg_pca")
        with c2:
            fig = go.Figure()
            for s in SEG_ORDER:
                ss = d[d.segment == s]
                fig.add_scatter(x=ss.orders_per_month, y=ss.avg_order_value, mode="markers", name=s,
                                marker=dict(color=SC[s], size=6, opacity=.6),
                                hovertemplate="%{x} orders/month<br>AED %{y:.0f} average order<extra>" + s + "</extra>")
                fig.add_scatter(x=[ss.orders_per_month.mean()], y=[ss.avg_order_value.mean()], mode="markers+text",
                                marker=dict(symbol="x", size=14, color=SC[s], line=dict(color=TEXT, width=1)),
                                text=[f"<b>{ss.orders_per_month.mean():.1f}/mo · {aed(ss.avg_order_value.mean())}</b>"], textposition="top center",
                                textfont=dict(color=TEXT, size=11), showlegend=False, hoverinfo="skip")
            style_fig(fig, "Spend vs frequency (✕ = segment mean)", xt="Orders per month", yt="Average order value (AED)", height=420, legend_title="Segment")
            show(fig, "seg_freq")
        feat = st.radio("Compare distribution of", list(LABELS), format_func=lambda f: LABELS[f], horizontal=True, key="seg_box")
        fig = go.Figure()
        for s in SEG_ORDER:
            vals = d[d.segment == s][feat]
            fig.add_box(y=vals, name=s, marker_color=SC[s], boxmean=True, line=dict(width=1.5))
            fig.add_annotation(x=s, y=vals.max(), text=f"median {num(vals.median())} · mean {num(vals.mean())}", showarrow=False,
                               yshift=16, font=dict(color=TEXT, size=11))
        style_fig(fig, f"{LABELS[feat]} by segment (box = middle 50%, line = median, dashed = mean)", xt="Segment", yt=LABELS[feat], height=380, legend=False)
        show(fig, "seg_box_fig")


def page_basket():
    page_header("Basket Intelligence", "Apriori association rules — overall and within each segment. One order = one basket.")
    if not B:
        return no_bundle_notice()
    meta, opp, ra = B["meta"], B["basket_opportunity"], B["rules_all"]
    n_strat = int((ra.tier == "Strategic").sum())
    c = st.columns(4)
    kpi(c[0], "Baskets analysed", f"{meta['n_baskets']:,}", f"{meta['n_order_rows']:,} order-item rows")
    kpi(c[1], "Menu items", f"{meta['n_items']}", f"Avg basket {meta['n_order_rows'] / meta['n_baskets']:.1f} items")
    kpi(c[2], "Overall rules (lift > 1)", f"{len(ra)}", f"{n_strat} strategic: support ≥ 5%, confidence ≥ 60%, lift ≥ 1.2", "pos")
    kpi(c[3], "Strongest in-segment lift", f"{opp.Lift.max():.1f}×", f"{opp.sort_values('Lift').iloc[-1]['Segment']}")

    section("Basket opportunity matrix", "Executive view",
            "Only decision-grade rules: within-segment, ≥ 10% support, ≥ 60% confidence. Hover the full rules below for definitions.")
    disp = pd.DataFrame({"Segment": opp.Segment, "If the basket has (A)": opp["If basket has (A)"], "Recommend (B)": opp["Recommend (B)"],
                         "Support": opp.Support.map(pct), "Confidence": opp.Confidence.map(pct), "Lift": opp.Lift.map(lambda v: f"{v:.2f}×"),
                         "Business opportunity": [f"Set menu {a} + {b}; prompt {b} at checkout" if l >= 1.5 else
                                                  "Weak link — offer a fixed-price meal deal, not a cross-sell"
                                                  for a, b, l in zip(opp["If basket has (A)"], opp["Recommend (B)"], opp.Lift)]})
    table(disp, column_config={
        "Support": st.column_config.TextColumn(help="Share of the segment's baskets containing both A and B."),
        "Confidence": st.column_config.TextColumn(help="Of baskets containing A, the share that also contain B."),
        "Lift": st.column_config.TextColumn(help="How many times more often A and B appear together than if they were independent. 1.0× = no association."),
    })
    ob = opp.sort_values("Lift")
    fig = go.Figure(go.Bar(x=ob.Lift, y=[f"{a} → {b}  ({sg})" for a, b, sg in zip(ob["If basket has (A)"], ob["Recommend (B)"], ob.Segment)],
                           orientation="h", marker_color=[SC[sg] for sg in ob.Segment],
                           text=[f"lift {l:.2f}× · {pct(c)} confidence · {pct(sp)} support" for l, c, sp in zip(ob.Lift, ob.Confidence, ob.Support)],
                           textposition="outside", hovertemplate="%{y}<br>Lift %{x:.2f}×: the pair occurs together %{x:.2f}× as often as expected under independence<extra></extra>"))
    fig.add_vline(x=1, line_dash="dash", line_color=RISK)
    fig.add_vline(x=1.5, line_dash="dot", line_color=MUTED)
    style_fig(fig, "Decision-grade bundles by within-segment lift (red dashed = 1.0, no association · dotted = 1.5, worth a prompt)",
              xt="Lift (× chance co-occurrence)", yt="Rule (segment)",
              height=330, legend=False)
    fig.update_xaxes(range=[0, ob.Lift.max() * 1.75])
    show(fig, "bk_opp_bar")
    note("<b>Why overall lift is not used for decisions.</b> Each segment orders from an almost separate menu, so across all baskets "
         "items bought by the same customer type look 13–30× 'associated'. That measures <i>who</i> is ordering, not <i>what</i> goes "
         "together. Within-segment lift isolates the genuine bundling opportunity.", "caution")

    t1, t2, t3 = st.tabs(["Rules by segment", "Overall rules", "Menu penetration"])
    with t1:
        seg = st.radio("Segment", SEG_ORDER, horizontal=True, key="bk_seg")
        c1, c2 = st.columns([1, 1.6])
        sm = B["share_mat"][seg].sort_values(ascending=True)
        sm = sm[sm > 0]
        with c1:
            fig = go.Figure(go.Bar(x=sm.values, y=sm.index, orientation="h", marker_color=SC[seg], text=[pct(v) for v in sm.values],
                                   textposition="outside", hovertemplate="%{y}: in %{x:.0%} of this segment's baskets<extra></extra>"))
            style_fig(fig, f"What {seg} order ({B['seg_baskets'][seg]:,} baskets)", xt="Share of the segment's baskets containing the item (%)",
                      yt="Menu item", height=400, legend=False)
            fig.update_xaxes(tickformat=".0%", range=[0, sm.max() * 1.25])
            show(fig, "bk_pen")
        with c2:
            r = B["seg_rules"][seg]
            rd = pd.DataFrame({"If basket has": r.antecedent, "→ also contains": r.consequent, "Support": r.support.map(pct),
                               "Confidence": r.confidence.map(pct), "Lift": r.lift.map(lambda v: f"{v:.2f}×"), "Tier": r.tier})
            st.markdown(f'<div class="qb-desc">{B["seg_baskets"][seg]:,} baskets · {len(r)} distinct rules (mirror-image rules collapsed)</div>', unsafe_allow_html=True)
            table(rd, height=350)
        best = r[r.tier == "Strategic"].head(1)
        if len(best):
            b = best.iloc[0]
            kind = "pos" if b.lift >= 1.5 else "caution"
            msg = (f"<b>{seg}:</b> baskets with {b.antecedent} also contain {b.consequent} {pct(b.confidence)} of the time — "
                   f"{b.lift:.2f}× what independence would predict, in {pct(b.support, 1)} of baskets.")
            if b.lift < 1.5:
                msg += " The association is weak because the item is already near-universal for this segment — a fixed-price meal deal fits better than a cross-sell prompt."
            note(msg, kind)
    with t2:
        r = ra.copy()
        r["explain"] = [f"Lift {l:.2f} means the pair occurs together about {l:.2f}× as often as expected under independence."
                        for l in r.lift]
        fig = go.Figure()
        for tier, colr in [("Strategic", POS), ("Low support — test only", CAUTION), ("Low confidence", FAINT), ("No real association (lift ≈ 1)", RISK)]:
            rr = r[r.tier == tier]
            if rr.empty:
                continue
            fig.add_scatter(x=rr.support, y=rr.confidence, mode="markers", name=tier,
                            marker=dict(size=np.clip(rr.lift * 1.4, 6, 40), color=colr, opacity=.75, line=dict(width=.5, color=BG)),
                            customdata=np.c_[rr.antecedent, rr.consequent, rr.lift, rr.explain],
                            hovertemplate="<b>%{customdata[0]} → %{customdata[1]}</b><br>Support %{x:.1%} · Confidence %{y:.0%}<br>"
                                          "%{customdata[3]}<extra></extra>")
        fig.add_vline(x=0.05, line_dash="dot", line_color=MUTED)
        fig.add_hline(y=0.60, line_dash="dot", line_color=MUTED)
        top_lab = r[r.tier == "Strategic"].sort_values("lift", ascending=False).drop_duplicates(subset=["support", "confidence"]).head(5)
        for _, x in top_lab.iterrows():
            fig.add_annotation(x=x.support, y=x.confidence, text=f"{x.antecedent} → {x.consequent}<br>lift {x.lift:.1f}×", showarrow=True,
                               arrowcolor=MUTED, ax=60, ay=-28, font=dict(color=TEXT, size=10), bgcolor="rgba(16,29,51,0.85)")
        fig.add_annotation(x=0.05, y=0.02, yref="paper", text="support 5%", showarrow=False, xanchor="left", font=dict(color=MUTED, size=10))
        fig.add_annotation(x=1, xref="paper", y=0.60, text="confidence 60%", showarrow=False, xanchor="right", yshift=8, font=dict(color=MUTED, size=10))
        style_fig(fig, "Rule map — support × confidence (bubble size = lift; dotted lines = strategic thresholds)",
                  xt="Support (share of all baskets containing both items)", yt="Confidence (share of A-baskets that also contain B)",
                  height=460, legend_title="Rule tier")
        fig.update_xaxes(tickformat=".0%")
        fig.update_yaxes(tickformat=".0%")
        show(fig, "bk_map")
        so = B["strategic_overall"]
        section("Strongest strategic overall rules", desc="Distinct item sets only (nested duplicates removed).")
        for _, x in so.iterrows():
            st.markdown(f"- Baskets with **{x.antecedent}** also contain **{x.consequent}** {pct(x.confidence)} of the time "
                        f"({x.lift:.1f}× independence; {pct(x.support, 1)} of baskets).")
        hi = ra.iloc[0]
        note(f"Highest raw lift: {hi.antecedent} → {hi.consequent} ({hi.lift:.1f}×) — but only {pct(hi.support, 1)} of baskets. "
             "A niche pairing worth testing, not a headline bundle.", "caution")
        with st.expander("All overall rules (detailed table)"):
            table(pd.DataFrame({"If basket has": ra.antecedent, "→ also contains": ra.consequent, "Support": ra.support.map(lambda v: pct(v, 1)),
                                "Confidence": ra.confidence.map(pct), "Lift": ra.lift.map(lambda v: f"{v:.2f}×"), "Tier": ra.tier}), height=420)
    with t3:
        sm = B["share_mat"][SEG_ORDER]
        fig = go.Figure(go.Heatmap(z=sm.values, x=SEG_ORDER, y=list(sm.index), colorscale=[[0, PANEL], [1, STEEL]],
                                   text=[[pct(v) if v > 0 else "—" for v in row] for row in sm.values], texttemplate="%{text}",
                                   textfont=dict(color=TEXT), hovertemplate="%{y} in %{z:.0%} of %{x} baskets<extra></extra>",
                                   colorbar=dict(tickformat=".0%", tickfont=dict(color=MUTED))))
        style_fig(fig, "Menu penetration — share of each segment's baskets containing the item", xt="Segment", yt="Menu item", height=580, legend=False)
        fig.update_xaxes(showgrid=False, side="top")
        fig.update_yaxes(showgrid=False, autorange="reversed")
        show(fig, "bk_heat")
        note("Only Cola, Salad and Pasta are bought by more than one segment. Every other item is effectively segment-exclusive — "
             "menu promotions should be targeted by segment, not broadcast.")


def page_retention():
    page_header("Retention & Churn", "Logistic-regression reorder model: performance, error economics, drivers and the risk watch-list.")
    if not B:
        return no_bundle_notice()
    m, cm, d = B["metrics"], np.array(B["cm"]), B["diners"]
    V = B["validation"]; rcv = V["repeated_cv"]; bci = V["bootstrap_ci"].set_index("Metric")
    u18 = B["under18"]
    c = st.columns(6)
    kpi(c[0], "Expected accuracy", pct(rcv["acc_mean"], 1), f"Repeated 5-fold CV (50 fits) ± {pct(rcv['acc_sd'], 1)} · baseline {pct(rcv['baseline'], 1)}", "pos")
    kpi(c[1], "Test-split accuracy", pct(m["Accuracy"], 1),
        f"95% CI {pct(bci.loc['Accuracy', '95% CI low'], 1)}–{pct(bci.loc['Accuracy', '95% CI high'], 1)} · {pp(m['Lift over baseline (pp)'])} vs baseline")
    kpi(c[2], "ROC-AUC", f"{rcv['auc_mean']:.3f}", f"CV mean · test {m['ROC-AUC']:.3f} (0.5 = random)")
    kpi(c[3], "Churners caught", pct(m["Churn recall (churners caught)"]),
        f"Test recall · 95% CI {pct(bci.loc['Churn recall', '95% CI low'])}–{pct(bci.loc['Churn recall', '95% CI high'])}")
    kpi(c[4], "Precision", pct(m["Precision (reorder)"]), f"Of predicted reorders · F1 {m['F1 (reorder)']:.3f}")
    kpi(c[5], "Scope", f"{B['meta']['n_model_rows']} adults", f"{int(m['Test observations'])} in test · {u18['n']} under-18 excluded", "caution")
    note(f"Expected real-world accuracy is <b>{pct(rcv['acc_mean'], 1)}</b> (repeated cross-validation), "
         f"<b>{(rcv['acc_mean'] - rcv['baseline']) * 100:.1f} percentage points</b> above the majority-class baseline of {pct(rcv['baseline'], 1)}. "
         f"The single held-out test split scored {pct(m['Accuracy'], 1)}; its bootstrap 95% interval "
         f"({pct(bci.loc['Accuracy', '95% CI low'], 1)}–{pct(bci.loc['Accuracy', '95% CI high'], 1)}) shows that one split is a noisy draw, "
         "so the cross-validated figure is the one to quote. Model choice was made on cross-validation, not the test split.", "pos")

    section("Model performance", "Evaluation", "Test set = 20% stratified hold-out of adult diners; calibration uses out-of-fold predictions for all adult diners.")
    c1, c2, c3 = st.columns([1, 1, 1])
    with c1:
        abbr = [["TN", "FP"], ["FN", "TP"]]
        rowp = cm / cm.sum(axis=1, keepdims=True)
        txt = [[f"<b>{abbr[i][j]}: {cm[i, j]}</b><br>{pct(rowp[i, j])} of row" for j in range(2)] for i in range(2)]
        fig = go.Figure(go.Heatmap(z=cm, x=["Pred. churn", "Pred. reorder"], y=["Actual churn", "Actual reorder"],
                                   text=txt, texttemplate="%{text}", textfont=dict(color=TEXT, size=13), showscale=False,
                                   colorscale=[[0, PANEL2], [1, "#2E5C9A"]], hovertemplate="%{y} · %{x}: %{z} diners<extra></extra>"))
        style_fig(fig, f"Confusion matrix (test, n = {int(m['Test observations'])})", xt="Model prediction", yt="Actual outcome", height=360, legend=False)
        fig.update_xaxes(showgrid=False)
        fig.update_yaxes(showgrid=False, autorange="reversed")
        show(fig, "rt_cm")
    tn, fp_, fn, tp = cm.ravel()
    c1.caption("TN = churn caught · FP = churner missed (costly) · FN = loyal diner flagged · TP = reorder confirmed. "
               "'% of row' = share of that actual class.")
    with c2:
        fpr, tpr = B["roc"]
        fig = go.Figure()
        fig.add_scatter(x=[0, 1], y=[0, 1], mode="lines", line=dict(dash="dash", color=FAINT), name="Random (AUC 0.500)")
        fig.add_scatter(x=fpr, y=tpr, mode="lines", line=dict(color=GOLD, width=2.5), name=f"Logistic regression (AUC {m['ROC-AUC']:.3f})",
                        hovertemplate="False-positive rate %{x:.0%}<br>True-positive rate %{y:.0%}<extra></extra>")
        ofpr, otpr = fp_ / (fp_ + tn), tp / (tp + fn)
        fig.add_scatter(x=[ofpr], y=[otpr], mode="markers+text", marker=dict(size=11, color=CAUTION, line=dict(color=TEXT, width=1)),
                        text=[f"0.5 cut-off: TPR {pct(otpr)} · FPR {pct(ofpr)}"], textposition="bottom right", textfont=dict(color=TEXT, size=11),
                        name="Operating point (0.5)")
        fig.add_annotation(x=0.55, y=0.55, text=f"<b>AUC = {m['ROC-AUC']:.3f}</b>", showarrow=False, font=dict(color=GOLD, size=16))
        style_fig(fig, "ROC curve — test set", xt="False-positive rate", yt="True-positive rate", height=360, legend_inside="br")
        fig.update_xaxes(tickformat=".0%"); fig.update_yaxes(tickformat=".0%")
        show(fig, "rt_roc")
    with c3:
        mp, fpos = B["calibration"]
        lab, last = [], -1
        for x_, y_ in zip(mp, fpos):
            if x_ - last >= 0.07:
                lab.append(f"{pct(x_)}→{pct(y_)}"); last = x_
            else:
                lab.append("")
        fig = go.Figure()
        fig.add_scatter(x=[0, 1], y=[0, 1], mode="lines", line=dict(dash="dash", color=FAINT), name="Perfect calibration")
        fig.add_scatter(x=mp, y=fpos, mode="lines+markers+text", line=dict(color=POS, width=2.5), name="Model (predicted→observed)",
                        text=lab, textposition="bottom right", textfont=dict(color=TEXT, size=10),
                        hovertemplate="Predicted %{x:.0%} → observed %{y:.0%}<extra></extra>")
        style_fig(fig, "Calibration — predicted vs observed", xt="Mean predicted P(reorder), 8 bins", yt="Observed reorder rate",
                  height=360, legend_inside="tl")
        fig.update_xaxes(tickformat=".0%"); fig.update_yaxes(tickformat=".0%")
        show(fig, "rt_cal")
    c1, c2 = st.columns(2)
    with c1:
        note(f"<b>False positive — {fp_} diners:</b> predicted to reorder, but churned. QuickBite takes no action and loses roughly a month of spend "
             f"(≈ {aed(d.est_monthly_spend.mean())} on average). <b>This is the costlier error.</b>", "risk")
    with c2:
        note(f"<b>False negative — {fn} diners:</b> predicted to churn, but reordered. The cost is an unnecessary retention offer — "
             "a discount on one order. Cheaper, so the model should be used to rank diners rather than only at the 0.5 cut-off.", "caution")

    section("How precise are these numbers?", "Uncertainty", "Bootstrap 95% confidence intervals on the 92-diner test set (2,000 resamples) and the spread of "
            "50 repeated cross-validation fits.")
    c1, c2 = st.columns([1.2, 1])
    with c1:
        bc = V["bootstrap_ci"]
        bc = bc[bc.Metric != "Lift over baseline (pp)"].iloc[::-1]
        fig = go.Figure(go.Scatter(x=bc["Point estimate"], y=bc.Metric, mode="markers+text", marker=dict(size=11, color=GOLD),
                                   error_x=dict(type="data", symmetric=False, array=bc["95% CI high"] - bc["Point estimate"],
                                                arrayminus=bc["Point estimate"] - bc["95% CI low"], color=MUTED, thickness=2, width=6),
                                   text=[f"{pct(p_, 1)} (95% CI {pct(l_, 1)}–{pct(h_, 1)})" for p_, l_, h_ in
                                         zip(bc["Point estimate"], bc["95% CI low"], bc["95% CI high"])],
                                   textposition="top center", textfont=dict(color=TEXT, size=11), name="Point estimate ± 95% CI"))
        fig.add_vline(x=m["Baseline accuracy"], line_dash="dash", line_color=CAUTION, annotation_text=f"majority baseline {pct(m['Baseline accuracy'], 1)}",
                      annotation_font_color=CAUTION, annotation_position="bottom right")
        style_fig(fig, "Test-set metrics with bootstrap 95% confidence intervals", xt="Metric value", yt="Metric", height=400, legend=False)
        fig.update_xaxes(tickformat=".0%", range=[0.45, 1.12])
        fig.update_yaxes(range=[-0.6, len(bc) - 0.2])
        show(fig, "rt_ci")
    with c2:
        cvs = V["cv_scores"]
        fig = go.Figure()
        for col_, colr in [("Accuracy", STEEL), ("ROC-AUC", GOLD)]:
            fig.add_box(y=cvs[col_], name=col_, marker_color=colr, boxpoints="all", jitter=.4, pointpos=0, boxmean=True)
            fig.add_annotation(x=col_, y=cvs[col_].max(), text=f"mean {pct(cvs[col_].mean(), 1)} ± {pct(cvs[col_].std(), 1)}",
                               showarrow=False, yshift=16, font=dict(color=TEXT, size=11))
        fig.add_hline(y=rcv["baseline"], line_dash="dash", line_color=CAUTION, annotation_text=f"baseline {pct(rcv['baseline'], 1)}",
                      annotation_font_color=CAUTION, annotation_position="bottom right")
        style_fig(fig, "Repeated 5-fold CV — 50 out-of-sample fits", xt="Metric", yt="Score on held-out fold", height=360, legend=False)
        fig.update_yaxes(tickformat=".0%", range=[0.55, 1.03])
        show(fig, "rt_cv")

    section("What drives predicted reorder?", "Drivers", "Associations learned from historical data — not causal effects. Frequency, order value and basket size are strongly collinear, so read the coefficients as a joint profile.")
    imp = B["importance"]
    c1, c2 = st.columns(2)
    with c1:
        co = imp["Coefficient (per 1 SD, log-odds)"].sort_values()
        orat = imp.loc[co.index, "Odds ratio per 1 SD"]
        fig = go.Figure(go.Bar(x=co.values, y=[LABELS[i] for i in co.index], orientation="h", marker_color=[POS if v > 0 else RISK for v in co.values],
                               text=[f"{v:+.2f} (odds ×{o:.2f})" for v, o in zip(co.values, orat)], textposition="outside",
                               customdata=orat, hovertemplate="%{y}<br>%{x:+.2f} log-odds per 1 SD · odds × %{customdata:.2f}<extra></extra>"))
        fig.add_vline(x=0, line_color=MUTED)
        lim = float(np.abs(co).max()) * 2.5
        style_fig(fig, "Logistic coefficients (green = raises, red = lowers P(reorder))", xt="Change in log-odds of reorder per +1 standard deviation",
                  yt="Feature", height=350, legend=False)
        fig.update_xaxes(range=[-lim, lim])
        show(fig, "rt_coef")
    with c2:
        pi = imp["Permutation importance (AUC drop)"].sort_values()
        fig = go.Figure(go.Bar(x=pi.values, y=[LABELS[i] for i in pi.index], orientation="h", marker_color=STEEL,
                               error_x=dict(type="data", array=imp.loc[pi.index, "Permutation sd"].values, color=MUTED, thickness=1),
                               hovertemplate="%{y}<br>AUC drops by %{x:.3f} when shuffled<extra></extra>"))
        for f_, v_ in pi.items():
            fig.add_annotation(x=max(v_, 0) + imp.loc[f_, "Permutation sd"], y=LABELS[f_], text=f"{v_:.3f}", showarrow=False, xanchor="left",
                               xshift=6, font=dict(color=TEXT, size=11))
        style_fig(fig, "Permutation importance (test set, 50 shuffles; whisker = ±1 SD)", xt="Drop in ROC-AUC when the feature is shuffled",
                  yt="Feature", height=350, legend=False)
        fig.update_xaxes(range=[min(0, float(pi.min()) - 0.01), float(pi.max()) * 1.5])
        show(fig, "rt_perm")
    rec_or = imp.loc["days_since_last_order", "Odds ratio per 1 SD"]
    note(f"<b>Recency is the dominant early-warning signal</b>: each extra ~7 days since the last order (1 SD) multiplies the odds of reordering by "
         f"about {rec_or:.2f}, holding the other inputs fixed. Frequent, low-ticket, discount-using diners are the profile most associated with returning.")

    section("Risk framework", "Retention operations", "Out-of-fold probabilities for the adult diners: every diner is scored by a model that never saw them.")
    ts = B["tier_summary"]
    tiers = [t[1] for t in RISK_TIERS]
    disp = pd.DataFrame({"Risk tier": tiers, "Probability band": ["≥ 75%", "50–75%", "25–50%", "< 25%"],
                         "Diners": [int(ts.loc[t, "Diners"]) for t in tiers],
                         "Mean predicted": [pct(ts.loc[t, "Mean predicted P(reorder)"]) for t in tiers],
                         "Observed reorder": [pct(ts.loc[t, "Observed reorder rate"]) for t in tiers],
                         "Monthly spend": [aed(ts.loc[t, "Est. monthly spend at stake (AED)"]) for t in tiers],
                         "Intervention": [t[2] for t in RISK_TIERS]})
    table(disp)
    c1, c2 = st.columns(2)
    with c1:
        fig = go.Figure()
        fig.add_bar(x=tiers, y=[ts.loc[t, "Mean predicted P(reorder)"] for t in tiers], name="Mean predicted P(reorder)", marker_color=STEEL,
                    text=[pct(ts.loc[t, "Mean predicted P(reorder)"]) for t in tiers], textposition="outside")
        fig.add_bar(x=tiers, y=[ts.loc[t, "Observed reorder rate"] for t in tiers], name="Observed reorder rate", marker_color=POS,
                    text=[pct(ts.loc[t, "Observed reorder rate"]) for t in tiers], textposition="outside")
        style_fig(fig, "Calibration by risk tier — predicted vs observed", xt="Risk tier", yt="Reorder rate (%)", height=350, legend_title="Series")
        fig.update_layout(barmode="group"); fig.update_yaxes(tickformat=".0%", range=[0, 1.15])
        show(fig, "rt_tierbar")
    with c2:
        sc = d[d.reorder_prob_oof.notna()]
        fig = go.Figure()
        for y, colr, nm in [(1, POS, "Actually reordered"), (0, RISK, "Actually churned")]:
            fig.add_histogram(x=sc[sc.reordered == y].reorder_prob_oof, name=nm, marker_color=colr, opacity=.7, xbins=dict(start=0, end=1, size=0.1),
                              texttemplate="%{y}", textposition="outside", textfont=dict(color=TEXT, size=10))
        for t in [0.25, 0.5, 0.75]:
            fig.add_vline(x=t, line_dash="dot", line_color=MUTED)
        style_fig(fig, "Predicted P(reorder) by actual outcome (dotted = tier cut-offs 25/50/75%)", xt="Out-of-fold P(reorder), 10-point bins",
                  yt="Number of diners", height=350, legend_inside="tl")
        fig.update_layout(barmode="group")
        fig.update_xaxes(tickformat=".0%")
        show(fig, "rt_hist")
    note("Bands are monotone and well calibrated: observed reorder rates track the mean prediction in every tier "
         f"(e.g. {pct(ts.loc['High churn risk', 'Mean predicted P(reorder)'])} predicted vs "
         f"{pct(ts.loc['High churn risk', 'Observed reorder rate'])} observed in the highest-risk band). Most scores sit near 0% or 100%, "
         "so the uncertain middle band is small — and that is where retention spend has the most leverage.", "")

    tt = B["threshold_table"]
    c1, c2 = st.columns([1, 1.05])
    with c1:
        fig = go.Figure()
        x = [f"< {pct(v)}" for v in tt.iloc[:, 0]]
        fig.add_bar(x=x, y=tt["Churners caught"], name="Churners caught", marker_color=POS, text=[pct(v) for v in tt["Churners caught"]], textposition="outside")
        fig.add_bar(x=x, y=tt["Loyal diners sent an offer"], name="Loyal diners sent an offer (wasted)", marker_color=CAUTION,
                    text=[pct(v) for v in tt["Loyal diners sent an offer"]], textposition="outside")
        style_fig(fig, "Targeting trade-off by at-risk cut-off", xt="Flag diner as at-risk if P(reorder) is …", yt="Share of each group (%)",
                  height=340, legend_title="Measure")
        fig.update_yaxes(tickformat=".0%", range=[0, 1.15])
        fig.update_layout(barmode="group")
        show(fig, "rt_thr")
    with c2:
        st.write("")
        note("Raising the at-risk cut-off catches more churners at the cost of more offers to loyal diners. A probability cut-off alone ignores "
             "how much each diner is worth — the <b>Retention Economics</b> page converts this trade-off into AED and finds the profit-maximising "
             "targeting rule. These figures use out-of-fold scores.", "gold")

    section("At-risk watch-list", "Action", "Diners below 50% predicted reorder probability, ranked by estimated monthly spend at stake.")
    wl = d[d.reorder_prob_oof < 0.5].copy()
    wl["at_stake"] = wl.est_monthly_spend * (1 - wl.reorder_prob_oof)
    wl = wl.sort_values("at_stake", ascending=False)
    seg_f = st.multiselect("Filter segments", SEG_ORDER, default=SEG_ORDER, key="wl_seg")
    wl = wl[wl.segment.isin(seg_f)]
    out = pd.DataFrame({"Diner": wl.diner_id, "Segment": wl.segment, "P(reorder)": (wl.reorder_prob_oof * 100).round(1),
                        "Risk tier": wl.risk_tier, "Days since last order": wl.days_since_last_order,
                        "Est. monthly spend (AED)": wl.est_monthly_spend.round(0), "Expected spend at stake (AED)": wl.at_stake.round(0),
                        "Suggested intervention": [risk_tier(p)[1] for p in wl.reorder_prob_oof]})
    table(out, height=360, column_config={
        "P(reorder)": st.column_config.ProgressColumn("P(reorder) %", min_value=0, max_value=100, format="%.0f%%"),
        "Est. monthly spend (AED)": st.column_config.NumberColumn(format="%.0f"),
        "Expected spend at stake (AED)": st.column_config.NumberColumn(format="%.0f", help="Monthly spend × (1 − P(reorder))."),
    })
    st.download_button("Download watch-list (CSV)", out.to_csv(index=False).encode(), "quickbite_at_risk_watchlist.csv", "text/csv")


def render_scoring(profile, show_actual=None):
    """Shared result panel for one diner profile."""
    name, reorder, prob, items = analyse(profile)
    tier, action = risk_tier(prob)
    tcol = TIER_COLORS.get(tier, STEEL)
    c = st.columns([1.05, 1.15, 1.2])
    strat = B["seg_strategy"].get(name, {}) if B else {}
    c[0].markdown(f'<div class="kpi" style="border-top:3px solid {SC.get(name, STEEL)}"><div class="kpi-label">Diner segment</div>'
                  f'<div class="kpi-value sm" style="color:{SC.get(name, TEXT)}">{name}</div>'
                  f'<div class="kpi-sub">{strat.get("who", "")}</div></div>', unsafe_allow_html=True)
    c[1].markdown(f'<div class="kpi"><div class="kpi-label">Will reorder?</div>'
                  f'<div style="display:flex;align-items:baseline;gap:14px;margin-top:6px"><span class="bigprob" style="color:{tcol}">{prob * 100:.0f}%</span>'
                  f'<span style="font-size:1.05rem;font-weight:600;color:{POS if reorder else RISK}">{"Yes — likely to reorder" if reorder else "At risk of churning"}</span></div>'
                  f'<div class="kpi-sub">Predicted reorder probability (0.5 cut-off for Yes / At-risk)</div></div>', unsafe_allow_html=True)
    c[2].markdown(f'<div class="kpi" style="border-left:3px solid {tcol}"><div class="kpi-label">Risk category · Retention recommendation</div>'
                  f'<div class="kpi-value sm" style="color:{tcol}">{tier}</div><div class="kpi-sub" style="color:{TEXT}">{action}</div></div>',
                  unsafe_allow_html=True)
    if show_actual is not None:
        act, oof = show_actual
        note(f"<b>Actual outcome for this diner:</b> {'reordered' if act == 1 else 'did not reorder'}. "
             f"Out-of-fold probability (from a model that never saw this diner): {pct(oof) if pd.notna(oof) else 'not scored (invalid age)'}. "
             "The live score above uses the final model, which was trained on 80% of diners and may include this one.", "")

    ext = extrapolation(profile)
    atyp, _ = atypical_for_segment(profile)
    if ext:
        note("<b>Extrapolation warning:</b> outside the range the models were trained on — " + "; ".join(ext) +
             ". Treat the score as indicative only.", "caution")
    elif atyp:
        note(f"<b>Atypical profile:</b> further from the {name} centre than 95% of real diners in that segment. "
             "Segment assignment and score are less reliable.", "caution")

    st.write("")
    left, right = st.columns([1, 1.1])
    with left:
        section("Recommended items", desc="<b>Segment-based</b>: the most-ordered items of this diner's segment — not personalised to the individual's order history.")
        share = B["share_mat"] if B else None
        chips = ""
        for it in items:
            s = (f" · in {pct(share.loc[pretty(it), name])} of baskets" if share is not None and pretty(it) in share.index else "")
            chips += f'<span class="chip">{pretty(it)}<span style="color:{MUTED}">{s}</span></span>'
        st.markdown(chips or "—", unsafe_allow_html=True)
        if B:
            opp = B["basket_opportunity"]
            opp = opp[opp.Segment == name]
            strong = opp[opp.Lift >= 1.5]
            if len(strong):
                st.markdown("<div class='qb-desc' style='margin-top:.6rem'>Decision-grade bundles for this segment (within-segment Apriori):</div>",
                            unsafe_allow_html=True)
                for _, o in strong.iterrows():
                    st.markdown(f"- **{o['If basket has (A)']}** in cart → suggest **{o['Recommend (B)']}** · "
                                f"{pct(o['Confidence'])} of the time, {o['Lift']:.1f}× chance")
            else:
                st.markdown("<div class='qb-desc' style='margin-top:.6rem'>No strong cross-sell pairs in this segment (best lift "
                            f"{opp.Lift.max():.2f}×) — these items are bought together by default, so a fixed-price meal deal fits better "
                            "than a cross-sell prompt.</div>", unsafe_allow_html=True)

        section("Customer economics", desc="Estimated from the profile; total spend in the data ≈ one month of spend.")
        ms = profile["orders_per_month"] * profile["avg_order_value"]
        seg_avg = B["seg_profile"].loc[name, "Est. monthly spend (AED)"] if B else None
        cc = st.columns(3)
        kpi(cc[0], "Monthly", aed(ms), f"Est. spend · segment avg {aed(seg_avg)}" if seg_avg else "Est. spend", small=True)
        kpi(cc[1], "Risk-weighted", aed(ms * prob), "Spend × P(reorder)", small=True)
        kpi(cc[2], "At risk", aed(ms * (1 - prob)), "Spend × (1 − P)", "risk" if prob < .5 else "", small=True)
    with right:
        contrib = contributions(profile)
        if contrib is not None:
            section("Why this prediction", desc="Each input's push on the log-odds of reordering, relative to an average diner. Associations, not causes.")
            cs = contrib.sort_values()
            fig = go.Figure(go.Bar(x=cs.values, y=[f"{LABELS[f]}: {num(profile[f])}" for f in cs.index], orientation="h",
                                   marker_color=[POS if v > 0 else RISK for v in cs.values],
                                   text=[f"{v:+.2f}" for v in cs.values], textposition="outside",
                                   hovertemplate="%{y}<br>%{x:+.2f} log-odds vs an average diner<extra></extra>"))
            fig.add_vline(x=0, line_color=MUTED)
            lim = float(cs.abs().max()) * 1.45 + 0.1
            style_fig(fig, None, xt="Log-odds vs average diner (red = churn, green = reorder)",
                      yt="Input (this diner's value)", height=320, legend=False)
            fig.update_xaxes(range=[-lim, lim])
            show(fig, f"contrib_{name}_{prob:.4f}")
            up, down = contrib.idxmax(), contrib.idxmin()
            why = (f"The score is driven most by <b>{LABELS[down].lower()}</b> (pulling towards churn) and <b>{LABELS[up].lower()}</b> "
                   f"(pulling towards reorder). ")
            if prob < 0.5:
                why += (f"This diner looks like a <b>{tier.lower()}</b> case: {aed(ms * (1 - prob))} of monthly spend is exposed. "
                        f"Act now with: {action.lower()}.")
            else:
                why += f"Retention looks secure; focus on value growth — {action.lower()}."
            note("<b>Why this matters.</b> " + why, "gold" if prob >= .5 else "risk")
    return name, prob


def campaign_eval(df, mask, offer_cost, margin, s_unc, s_lapsed, horizon):
    """Expected economics of offering a retention incentive to the diners in `mask` (calibrated out-of-fold probabilities)."""
    t = df[mask]
    succ = np.where(t.reorder_prob_oof >= 0.25, s_unc, s_lapsed)
    gain = (1 - t.reorder_prob_oof) * succ * t.est_monthly_spend * horizon * margin
    cost = offer_cost * len(t)
    denom = ((1 - t.reorder_prob_oof) * t.est_monthly_spend * horizon * margin).sum()
    return {"n": len(t), "cost": cost, "margin": float(gain.sum()), "net": float(gain.sum() - cost),
            "roi": (gain.sum() - cost) / cost if cost else np.nan, "saved": float(((1 - t.reorder_prob_oof) * succ).sum()),
            "breakeven_success": cost / denom if denom else np.nan}


def page_economics():
    page_header("Retention Economics", "Turn churn scores into an AED decision: who is worth a retention offer, and what is the campaign worth?")
    if not B:
        return no_bundle_notice()
    note("<b>Planning tool.</b> Probabilities are the model's calibrated out-of-fold scores for adult diners. Offer cost, margin, success rate and "
         "months recovered are <b>management assumptions</b>, not estimates from this data — the success rate in particular should be measured "
         "with an A/B test before budget is committed.", "caution")
    dfl = B["roi_defaults"]
    d = B["diners"]
    d = d[d.reorder_prob_oof.notna()].copy()
    c = st.columns(5)
    offer = c[0].number_input("Offer cost per diner (AED)", 0.0, 200.0, float(dfl["offer_cost"]), 5.0, key="ec_cost",
                              help="Cost of the incentive sent to each targeted diner, e.g. a discount voucher.")
    margin = c[1].slider("Gross margin on recovered spend", 0.05, 0.60, float(dfl["margin"]), 0.01, format="%.2f", key="ec_margin",
                         help="Share of recovered spend that is profit after food, delivery and commission costs.")
    s_unc = c[2].slider("Success rate — uncertain diners (P ≥ 25%)", 0.0, 0.5, float(dfl["success"]), 0.01, format="%.2f", key="ec_su",
                        help="Share of would-be churners in the 25–100% band who are retained because of the offer.")
    s_lap = c[3].slider("Success rate — lapsed diners (P < 25%)", 0.0, 0.5, float(dfl["success"]), 0.01, format="%.2f", key="ec_sl",
                        help="Win-back is usually harder for diners who have largely lapsed. Lower this to test that assumption.")
    horizon = c[4].slider("Months of spend recovered", 1, 12, int(dfl["horizon"]), 1, key="ec_h")
    c1, c2 = st.columns([1.2, 1])
    rule = c1.radio("Targeting rule", ["Expected-value ranking (recommended)", "Probability cut-off"], horizontal=True, key="ec_rule")
    segs = c2.multiselect("Segments in scope", SEG_ORDER, default=SEG_ORDER, key="ec_segs")
    d = d[d.segment.isin(segs)]
    if d.empty:
        st.info("Select at least one segment.")
        return
    succ = np.where(d.reorder_prob_oof >= 0.25, s_unc, s_lap)
    d["exp_value"] = (1 - d.reorder_prob_oof) * succ * d.est_monthly_spend * horizon * margin - offer
    grid = np.round(np.arange(0.05, 1.0001, 0.05), 2)
    curve = pd.DataFrame([dict(threshold=t, **campaign_eval(d, d.reorder_prob_oof < t, offer, margin, s_unc, s_lap, horizon)) for t in grid])
    best = curve.loc[curve.net.idxmax()]
    ev_res = campaign_eval(d, d.exp_value > 0, offer, margin, s_unc, s_lap, horizon)
    if rule.startswith("Probability"):
        thr = st.slider("Target diners with P(reorder) below", 0.05, 1.0, float(best.threshold), 0.05, format="%.2f", key="ec_thr")
        mask = d.reorder_prob_oof < thr
        res = campaign_eval(d, mask, offer, margin, s_unc, s_lap, horizon)
    else:
        mask = d.exp_value > 0
        res = ev_res

    k = st.columns(6)
    kpi(k[0], "Diners targeted", f"{res['n']:,}", f"of {len(d):,} adult diners in scope")
    kpi(k[1], "Campaign cost", aed(res["cost"]), f"{aed(offer)} × {res['n']:,}")
    kpi(k[2], "Expected diners retained", f"{res['saved']:.1f}", "Σ P(churn) × success rate")
    kpi(k[3], "Expected margin recovered", aed(res["margin"]), f"{horizon} month(s) × {pct(margin)} margin")
    kpi(k[4], "Net value", aed(res["net"]), f"ROI {pct(res['roi']) if res['cost'] else '—'}", "pos" if res["net"] > 0 else "risk")
    kpi(k[5], "Break-even success rate", pct(res["breakeven_success"], 1) if pd.notna(res["breakeven_success"]) else "—",
        "Success needed for net value = 0", "caution")

    c1, c2 = st.columns([1.35, 1])
    with c1:
        fig = go.Figure()
        fig.add_scatter(x=curve.threshold, y=curve.margin, mode="lines+markers", name="Expected margin recovered", line=dict(color=POS))
        fig.add_scatter(x=curve.threshold, y=curve.cost, mode="lines+markers", name="Campaign cost", line=dict(color=RISK))
        fig.add_scatter(x=curve.threshold, y=curve.net, mode="lines+markers", name="Net value (margin − cost)", line=dict(color=GOLD, width=3),
                        hovertemplate="Cut-off P < %{x:.2f}<br>Net value AED %{y:,.0f}<extra></extra>")
        fig.add_hline(y=ev_res["net"], line_dash="dash", line_color=STEEL)
        fig.add_annotation(x=0.98, xref="paper", y=ev_res["net"], text=f"Expected-value ranking: {aed(ev_res['net'])} ({ev_res['n']} diners)",
                           showarrow=False, xanchor="right", yshift=12, font=dict(color=STEEL, size=11), bgcolor="rgba(10,19,36,0.85)")
        fig.add_hline(y=0, line_color=MUTED)
        fig.add_scatter(x=[best.threshold], y=[best.net], mode="markers", marker=dict(size=13, color=GOLD, line=dict(color=TEXT, width=1)),
                        name="Best probability cut-off")
        fig.add_annotation(x=best.threshold, y=best.net, text=f"Best cut-off P < {best.threshold:.2f}<br>{aed(best.net)} · {int(best.n)} diners",
                           showarrow=True, arrowcolor=GOLD, ax=70, ay=60, font=dict(color=GOLD, size=11), bgcolor="rgba(10,19,36,0.85)")
        style_fig(fig, "Campaign value by probability cut-off vs expected-value ranking", xt="Target diners with predicted P(reorder) below …",
                  yt="AED (one campaign)", height=420, legend_title="Series")
        fig.update_xaxes(tickformat=".0%"); fig.update_yaxes(tickformat=",.0f")
        show(fig, "ec_curve")
    with c2:
        t = d[mask]
        g = t.groupby("segment").agg(n=("diner_id", "size"), net=("exp_value", "sum")).reindex(SEG_ORDER).dropna(how="all").fillna(0)
        if rule.startswith("Probability"):
            succ_t = np.where(t.reorder_prob_oof >= 0.25, s_unc, s_lap)
            t = t.assign(net_=(1 - t.reorder_prob_oof) * succ_t * t.est_monthly_spend * horizon * margin - offer)
            g = t.groupby("segment").agg(n=("diner_id", "size"), net=("net_", "sum")).reindex(SEG_ORDER).dropna(how="all").fillna(0)
        fig = go.Figure(go.Bar(x=list(g.index), y=g.net, marker_color=[SC[x] for x in g.index],
                               text=[f"{aed(v)}<br>{int(n_)} diners" for v, n_ in zip(g.net, g.n)], textposition="outside",
                               hovertemplate="%{x}: net %{y:,.0f} AED<extra></extra>"))
        fig.add_hline(y=0, line_color=MUTED)
        style_fig(fig, "Net value of the chosen campaign by segment", xt="Segment", yt="Expected net value (AED)", height=420, legend=False)
        lo_, hi_ = float(min(g.net.min(), 0)), float(max(g.net.max(), 1))
        fig.update_yaxes(range=[lo_ * 1.3 if lo_ < 0 else 0, hi_ * 1.3], tickformat=",.0f")
        show(fig, "ec_seg")

    c1, c2 = st.columns([1.35, 1])
    with c1:
        srates = np.round(np.arange(0.0, 0.41, 0.02), 2)
        rows = []
        for sr in srates:
            ev = (1 - d.reorder_prob_oof) * sr * d.est_monthly_spend * horizon * margin - offer
            rows.append({"s": sr, "ev_net": float(ev[ev > 0].sum()), "all_net": float(ev[d.reorder_prob_oof < 0.5].sum())})
        sens = pd.DataFrame(rows)
        fig = go.Figure()
        fig.add_scatter(x=sens.s, y=sens.ev_net, mode="lines+markers", name="Expected-value ranking", line=dict(color=GOLD, width=3))
        fig.add_scatter(x=sens.s, y=sens.all_net, mode="lines+markers", name="Offer to every diner with P < 50%", line=dict(color=STEEL))
        for _, r_ in sens.iloc[::5].iterrows():                      # label every 10 percentage points of success rate
            fig.add_annotation(x=r_.s, y=r_.ev_net, text=aed(r_.ev_net), showarrow=False, yshift=14, font=dict(color=TEXT, size=10))
            fig.add_annotation(x=r_.s, y=r_.all_net, text=aed(r_.all_net), showarrow=False, yshift=-14, font=dict(color=STEEL, size=10))
        fig.add_hline(y=0, line_color=MUTED)
        style_fig(fig, "Sensitivity to the success rate (same rate for all diners)", xt="Assumed success rate of the offer",
                  yt="Net value (AED)", height=380, legend_title="Targeting")
        fig.update_xaxes(tickformat=".0%"); fig.update_yaxes(tickformat=",.0f")
        show(fig, "ec_sens")
    with c2:
        st.write("")
        gain = ev_res["net"] - best.net
        note(f"<b>Rank by expected value, not by probability.</b> With these assumptions, expected-value ranking yields {aed(ev_res['net'])} "
             f"vs {aed(best.net)} for the best single probability cut-off ({'+' if gain >= 0 else ''}{aed(gain)}). It skips low-spend diners and "
             "diners likely to reorder anyway, whose expected recovery cannot repay the offer. When offers are cheap and effective the two "
             "converge; when economics are tight, probability cut-offs lose money while value ranking stays profitable.", "gold")
        note("<b>The open question an A/B test must answer:</b> with one success rate, value ranking favours Family Feasters (high churn "
             "probability). If lapsed diners respond less, lower the lapsed success rate above and watch the budget shift to Premium Foodies.", "")

    section("Target list", "Action", "Diners selected by the current rule, ranked by expected net value of the offer.")
    tl = d[mask].sort_values("exp_value", ascending=False)
    out = pd.DataFrame({"Diner": tl.diner_id, "Segment": tl.segment, "P(reorder) %": (tl.reorder_prob_oof * 100).round(1),
                        "Est. monthly spend (AED)": tl.est_monthly_spend.round(0), "Expected net value of offer (AED)": tl.exp_value.round(1),
                        "Suggested intervention": [risk_tier(p_)[1] for p_ in tl.reorder_prob_oof]})
    table(out, height=330, column_config={"P(reorder) %": st.column_config.ProgressColumn("P(reorder) %", min_value=0, max_value=100, format="%.0f%%")})
    st.download_button("Download target list (CSV)", out.to_csv(index=False).encode(), "quickbite_retention_targets.csv", "text/csv")


def under18_note(compact=False):
    """Visible statement of the 18+ policy wherever diners are scored."""
    n = B["under18"]["n"] if B else 20
    txt = (f"<b>18+ policy:</b> the age input runs 18–70, as in the original app. The <b>{n} diners under 18</b> in the data "
           "(ages 9–17) are <b>not in the age slider and not in the classifier</b> — they were excluded from training, evaluation "
           "and scoring. They remain in segmentation and basket analysis, where age is not used.")
    if compact:
        txt = f"Age input 18–70. The {n} under-18 diners are excluded from the classifier and this slider (18+ policy)."
    if compact:
        st.caption(txt)
    else:
        note(txt, "caution")


def score_frame(df):
    """Vectorised version of the app.py pathway for many diners. Under-18 or incomplete rows are flagged, not scored."""
    out = df.copy()
    missing = [c for c in CLF_FEATURES if c not in out.columns]
    if missing:
        raise ValueError(f"Missing required columns: {', '.join(missing)}")
    for c in CLF_FEATURES:
        out[c] = pd.to_numeric(out[c], errors="coerce")
    ok = out[CLF_FEATURES].notna().all(axis=1) & (out.age >= INPUT_SPEC["age"][0])
    out["status"] = np.where(out[CLF_FEATURES].isna().any(axis=1), "Not scored — missing / non-numeric value",
                             np.where(out.age < INPUT_SPEC["age"][0], "Not scored — under 18 (18+ policy)", "Scored"))
    out["segment"], out["p_reorder"], out["will_reorder"], out["risk_tier"], out["action"], out["recommended_items"] = None, np.nan, None, None, None, None
    if ok.any():
        X = out.loc[ok, CLF_FEATURES]
        seg = kmeans.predict(scaler.transform(X[FEATURES]))
        prob = clf.predict_proba(X[FEATURES + ["age", "total_spend"]])[:, 1]
        pred = clf.predict(X[FEATURES + ["age", "total_spend"]])
        names = [seg_names.get(int(c), f"Segment {c}") for c in seg]
        out.loc[ok, "segment"] = names
        out.loc[ok, "p_reorder"] = prob
        out.loc[ok, "will_reorder"] = np.where(pred == 1, "Yes", "At risk")
        out.loc[ok, "risk_tier"] = [risk_tier(p_)[0] for p_ in prob]
        out.loc[ok, "action"] = [risk_tier(p_)[1] for p_ in prob]
        out.loc[ok, "recommended_items"] = [", ".join(pretty(i) for i in reco.get(n_, [])) for n_ in names]
        if B:
            out["outside_training_range"] = ""
            out.loc[ok, "outside_training_range"] = [", ".join(LABELS[f] for f, (lo, hi) in B["train_ranges"].items()
                                                               if not lo <= r_[f] <= hi) for _, r_ in X.iterrows()]
    return out


def page_diner():
    page_header("Diner Intelligence", "Score one diner interactively, or upload a file of diners and score them all at once.")
    tab1, tab2 = st.tabs(["Score one diner", "Batch scoring (CSV upload)"])
    with tab1:
        opts = list(PRESETS) + (["Look up an existing diner…"] if B else [])
        st.session_state.setdefault("dn_preset", opts[0])

        def _apply():
            choice = st.session_state["dn_preset"]
            st.session_state["dn_loaded"] = None
            if choice in PRESETS:
                set_profile("dn", PRESETS[choice])

        left, right = st.columns([0.9, 2.6], gap="large")
        with left:
            with st.container(border=True):
                st.markdown('<div class="kpi-label">Diner profile</div>', unsafe_allow_html=True)
                st.selectbox("Start from", opts, key="dn_preset", on_change=_apply)
                actual = None
                if st.session_state["dn_preset"] == "Look up an existing diner…":
                    dd = B["diners"][B["diners"].include_in_classifier.astype(bool)].sort_values("diner_id")
                    did = st.selectbox("Diner ID (adult diners only)", dd.diner_id.tolist(), key="dn_id",
                                       help=f"{B['under18']['n']} under-18 diners are not listed: they are outside the classifier (18+ policy).")
                    if st.session_state.get("dn_loaded") != did:
                        r = dd.set_index("diner_id").loc[did]
                        set_profile("dn", {f: (float(r[f]) if f in ("avg_order_value", "discount_rate", "total_spend") else int(r[f])) for f in CLF_FEATURES})
                        st.session_state["dn_loaded"] = did
                    r = dd.set_index("diner_id").loc[did]
                    actual = (int(r.reordered), r.reorder_prob_oof)
                profile = profile_inputs("dn", st, PRESETS[opts[0]])
                under18_note(compact=True)
        with right:
            render_scoring(profile, actual)
    with tab2:
        section("Score a file of diners", desc="Runs exactly the same saved models and app.py pathway on every row. "
                "Required columns: " + ", ".join(f"<code>{c}</code>" for c in CLF_FEATURES) + " (an ID column such as <code>diner_id</code> is kept if present).")
        under18_note()
        template = pd.DataFrame([dict(diner_id="NEW001", **PRESETS[list(PRESETS)[0]])])
        if B:
            ex = B["diners"][B["diners"].include_in_classifier.astype(bool)].sample(8, random_state=7)[["diner_id"] + CLF_FEATURES]
            template = pd.concat([template, ex, B["diners"][B["diners"].age < 18].head(2)[["diner_id"] + CLF_FEATURES]], ignore_index=True)
        c1, c2 = st.columns([1, 2])
        c1.download_button("Download example CSV (11 rows, incl. 2 under-18)", template.to_csv(index=False).encode(),
                           "quickbite_scoring_template.csv", "text/csv")
        up = c2.file_uploader("Upload diners CSV", type=["csv"], key="batch_csv")
        use_example = c1.checkbox("Score the example file instead", key="batch_example")
        src = None
        if up is not None:
            try:
                src = pd.read_csv(up)
            except Exception as exc:
                st.error(f"Could not read the file: {exc}")
        elif use_example:
            src = template
        if src is not None:
            try:
                res = score_frame(src)
            except ValueError as exc:
                st.error(str(exc))
                return
            scored_ = res[res.status == "Scored"]
            cc = st.columns(5)
            kpi(cc[0], "Rows uploaded", f"{len(res):,}", "")
            kpi(cc[1], "Scored", f"{len(scored_):,}", f"{pct(len(scored_) / max(len(res), 1))} of rows", "pos")
            kpi(cc[2], "Not scored — under 18", f"{int((res.status.str.contains('under 18')).sum())}", "18+ policy", "caution")
            kpi(cc[3], "Predicted at risk", f"{int((scored_.p_reorder < 0.5).sum())}", "P(reorder) &lt; 50%", "risk")
            kpi(cc[4], "Mean P(reorder)", pct(scored_.p_reorder.mean()) if len(scored_) else "—", "Scored rows only")
            show_cols = [c for c in ["diner_id", "status", "segment", "p_reorder", "will_reorder", "risk_tier", "action",
                                     "recommended_items", "outside_training_range"] if c in res.columns]
            disp = res[show_cols].copy()
            disp["p_reorder"] = (disp.p_reorder * 100).round(1)
            table(disp, height=380, column_config={"p_reorder": st.column_config.ProgressColumn("P(reorder) %", min_value=0, max_value=100, format="%.1f%%")})
            if len(scored_):
                cnt = scored_.groupby(["segment", "risk_tier"]).size().unstack(fill_value=0).reindex(columns=[t[1] for t in RISK_TIERS], fill_value=0)
                fig = go.Figure()
                for t in [t_[1] for t_ in RISK_TIERS]:
                    fig.add_bar(name=t, x=list(cnt.index), y=cnt[t], marker_color=TIER_COLORS[t], text=cnt[t], textposition="inside",
                                hovertemplate="%{x} · " + t + ": %{y} diners<extra></extra>")
                style_fig(fig, "Scored diners by segment and risk tier", xt="Segment", yt="Number of scored diners", height=330, legend_title="Risk tier")
                fig.update_layout(barmode="stack")
                show(fig, "batch_fig")
            st.download_button("Download scored file (CSV)", res.to_csv(index=False).encode(), "quickbite_scored_diners.csv", "text/csv")


SCENARIO_LIBRARY = {
    "Custom": None,
    "A · Retention intervention": ("Lapsed Family Feaster", {"days_since_last_order": 10},
                                   "What if an at-risk diner orders again within a shorter recency window?"),
    "B · Discount strategy": ("Typical Premium Foodie", {"discount_rate": 0.40}, "What if discount usage increases?"),
    "C · Higher engagement": ("Typical Premium Foodie", {"orders_per_month": "+3"}, "What if monthly order frequency increases?"),
    "D · Premium behaviour": ("Typical Budget Student", {"avg_order_value": "x1.5"}, "What if average order value increases?"),
    "E · Recovery": ("Lapsed Family Feaster", {"days_since_last_order": 3, "orders_per_month": "+1"},
                     "What if a high-risk diner moves from high recency to recent activity?"),
}


def page_whatif():
    page_header("What-If Simulator", "Change a diner's behaviour and see how the saved models respond.")
    note("<b>Model-based scenario simulations, not causal estimates.</b> The change in probability shows what the model associates with "
         "reordering in historical data. It does not prove that changing a behaviour would cause a diner to return — validate with an A/B test.", "caution")
    st.session_state.setdefault("wi_scen", "A · Retention intervention" if "Lapsed Family Feaster" in PRESETS else "Custom")
    st.session_state.setdefault("wi_base", "Lapsed Family Feaster" if "Lapsed Family Feaster" in PRESETS else list(PRESETS)[0])
    st.session_state.setdefault("wi_link", True)

    def _resolve(base, changes):
        after = dict(base)
        for k, v in changes.items():
            if isinstance(v, str) and v.startswith("+"):
                after[k] = base[k] + float(v[1:])
            elif isinstance(v, str) and v.startswith("x"):
                after[k] = round(base[k] * float(v[1:]), 0)
            else:
                after[k] = v
        return after

    def _load_scenario():
        sc = SCENARIO_LIBRARY.get(st.session_state["wi_scen"])
        if sc and sc[0] in PRESETS:
            st.session_state["wi_base"] = sc[0]
            base = PRESETS[sc[0]]
            after = _resolve(base, sc[1])
            set_profile("wi", after)

    def _load_base():
        set_profile("wi", PRESETS[st.session_state["wi_base"]])
        st.session_state["wi_scen"] = "Custom"

    if "wi_orders_per_month" not in st.session_state:
        if SCENARIO_LIBRARY.get(st.session_state["wi_scen"]):
            _load_scenario()
        else:
            set_profile("wi", PRESETS[st.session_state["wi_base"]])

    c1, c2, c3 = st.columns([1.2, 1.2, 1])
    c1.selectbox("Scenario template", list(SCENARIO_LIBRARY), key="wi_scen", on_change=_load_scenario)
    c2.selectbox("Base diner (before)", list(PRESETS), key="wi_base", on_change=_load_base)
    c3.write("")
    c3.checkbox("Link total spend to orders × AOV", key="wi_link",
                help="In the data, total spend ≈ orders per month × average order value for every diner (ratio 0.85–1.15). "
                     "When linked, the diner's total spend scales in proportion to frequency × order value.")
    sc = SCENARIO_LIBRARY.get(st.session_state["wi_scen"])
    if sc:
        st.markdown(f"<div class='qb-desc'><b style='color:{GOLD}'>{st.session_state['wi_scen']}:</b> {sc[2]}</div>", unsafe_allow_html=True)

    base = PRESETS[st.session_state["wi_base"]]
    left, right = st.columns([0.9, 2.6], gap="large")
    with left:
        with st.container(border=True):
            st.markdown('<div class="kpi-label">Scenario profile (after)</div>', unsafe_allow_html=True)
            after = profile_inputs("wi", st, base, linked_base=base if st.session_state["wi_link"] else None)
            st.button("Reset to base diner", on_click=_load_base)

    s0, r0, p0, i0 = analyse(base)
    s1, r1, p1, i1 = analyse(after)
    t0, _ = risk_tier(p0)
    t1, a1 = risk_tier(p1)
    ms0, ms1 = base["orders_per_month"] * base["avg_order_value"], after["orders_per_month"] * after["avg_order_value"]
    with right:
        c = st.columns([1, 1, 0.9])
        for col, lbl, s, p, t, ms in [(c[0], "Before", s0, p0, t0, ms0), (c[1], "After (scenario)", s1, p1, t1, ms1)]:
            col.markdown(f'<div class="kpi"><div class="kpi-label">{lbl}</div>'
                         f'<div class="bigprob" style="margin-top:6px;color:{TIER_COLORS.get(t, STEEL)}">{p * 100:.0f}%</div>'
                         f'<div class="kpi-sub"><b style="color:{TIER_COLORS.get(t, STEEL)}">{t}</b><br>Segment: <span style="color:{SC.get(s, TEXT)}">{s}</span>'
                         f'<br>Est. monthly spend {aed(ms)} · risk-weighted {aed(ms * p)}</div></div>', unsafe_allow_html=True)
        delta = (p1 - p0) * 100
        dc = POS if delta > 0.5 else (RISK if delta < -0.5 else MUTED)
        c[2].markdown(f'<div class="kpi"><div class="kpi-label">Change in P(reorder)</div>'
                      f'<div class="bigprob" style="margin-top:6px;color:{dc}">{delta:+.1f}<span style="font-size:1.2rem"> pp</span></div>'
                      f'<div class="kpi-sub">{"Tier unchanged" if t0 == t1 else f"Tier: {t0} → {t1}"}'
                      f'{"" if s0 == s1 else f"<br><b style=color:{CAUTION}>Segment changes: {s0} → {s1}</b>"}</div></div>', unsafe_allow_html=True)

        changed = [f for f in CLF_FEATURES if abs(after[f] - base[f]) > 1e-9]
        if changed:
            st.markdown("<div class='qb-desc' style='margin-top:.8rem'>Changed inputs: " + " · ".join(
                f"<b>{LABELS[f]}</b> {num(base[f])} → {num(after[f])}" for f in changed) + "</div>", unsafe_allow_html=True)
        else:
            st.markdown("<div class='qb-desc' style='margin-top:.8rem'>No inputs changed yet — adjust the scenario sliders.</div>", unsafe_allow_html=True)

        warns = extrapolation(after)
        if B and changed:
            dseg = B["diners"][B["diners"].segment == s0]
            out_seg = [f"{LABELS[f]} {num(after[f])} (observed {s0}: {num(dseg[f].min())}–{num(dseg[f].max())})"
                       for f in changed if not dseg[f].min() <= after[f] <= dseg[f].max()]
            if out_seg:
                note(f"<b>Beyond observed {s0} behaviour:</b> " + "; ".join(out_seg) + ". The model is extrapolating from other segments' "
                     "behaviour, so treat the change as an upper bound, not a forecast.", "caution")
        if warns:
            note("<b>Outside the training data:</b> " + "; ".join(warns) + ".", "risk")
        if s1 != s0 and i1 != i0:
            st.markdown(f"<div class='qb-desc'>Recommended items shift with the segment: {', '.join(pretty(i) for i in i0)} → "
                        f"<b>{', '.join(pretty(i) for i in i1)}</b></div>", unsafe_allow_html=True)
        st.markdown(f"<div class='qb-desc'>Suggested action after scenario: <b style='color:{TEXT}'>{a1}</b></div>", unsafe_allow_html=True)

        section("Sensitivity — one input at a time", desc="Predicted reorder probability as the selected input varies, all other inputs held at the scenario values.")
        feat = st.radio("Vary", [f for f in CLF_FEATURES], format_func=lambda f: LABELS[f], horizontal=True, key="wi_sens",
                        index=CLF_FEATURES.index("days_since_last_order"))
        lo, hi, _ = INPUT_SPEC[feat]
        grid = np.linspace(lo, hi, 80)
        rows = []
        for g in grid:
            pr = dict(after)
            pr[feat] = g
            if st.session_state["wi_link"] and feat in ("orders_per_month", "avg_order_value"):
                pr["total_spend"] = linked_spend(base, pr)
            rows.append(pr)
        X = pd.DataFrame(rows)
        probs = clf.predict_proba(X[CLF_FEATURES])[:, 1]
        fig = go.Figure()
        if B:
            dseg = B["diners"][B["diners"].segment == s1]
            fig.add_vrect(x0=dseg[feat].min(), x1=dseg[feat].max(), fillcolor=SC.get(s1, STEEL), opacity=0.10, line_width=0,
                          annotation_text=f"Observed {s1} range", annotation_position="top left", annotation_font_color=MUTED)
        for y_, colr, lbl in [(0.25, RISK, "25% · high churn risk below"), (0.5, CAUTION, "50% · Yes / At-risk"), (0.75, POS, "75% · high retention above")]:
            fig.add_hline(y=y_, line_dash="dot", line_color=colr, opacity=.6, annotation_text=lbl, annotation_font_color=colr,
                          annotation_position="top right", annotation_font_size=10)
        fig.add_scatter(x=grid, y=probs, mode="lines", line=dict(color=GOLD, width=2.5), name="P(reorder) as input varies",
                        hovertemplate=LABELS[feat] + " %{x:,.2f}<br>P(reorder) %{y:.0%}<extra></extra>")
        fig.add_scatter(x=[base[feat]], y=[p0], mode="markers+text", marker=dict(size=11, color=MUTED, line=dict(color=TEXT, width=1)), name="Before",
                        text=[f"Before: {num(base[feat])} → {pct(p0)}"], textposition="top left", textfont=dict(color=TEXT, size=11))
        fig.add_scatter(x=[after[feat]], y=[p1], mode="markers+text", marker=dict(size=12, color=GOLD, line=dict(color=TEXT, width=1)), name="After",
                        text=[f"After: {num(after[feat])} → {pct(p1)}"], textposition="bottom right", textfont=dict(color=GOLD, size=11))
        style_fig(fig, f"P(reorder) vs {LABELS[feat].lower()} (other inputs at scenario values)", xt=LABELS[feat], yt="Predicted P(reorder) (%)",
                  height=360, legend_title="Series")
        fig.update_yaxes(tickformat=".0%", range=[0, 1.02])
        show(fig, "wi_sens_fig")

        section("Tornado — which inputs move this diner most?", desc="Each input moved one standard deviation down and up from the scenario profile "
                "(others fixed, clipped to the input range). Bars show the change in P(reorder) in percentage points. Model associations, not causal effects.")
        try:
            sd = pd.Series(clf.named_steps["scaler"].scale_, index=CLF_FEATURES)      # learned, persisted training SDs
        except Exception:
            sd = None
        if sd is not None:
            rows = []
            for f in CLF_FEATURES:
                lo_, hi_, _ = INPUT_SPEC[f]
                pl, ph = dict(after), dict(after)
                pl[f] = max(after[f] - sd[f], lo_); ph[f] = min(after[f] + sd[f], hi_)
                ql = clf.predict_proba(pd.DataFrame([pl])[CLF_FEATURES])[0, 1]
                qh = clf.predict_proba(pd.DataFrame([ph])[CLF_FEATURES])[0, 1]
                rows.append((f, pl[f], ph[f], (ql - p1) * 100, (qh - p1) * 100))
            tdf = pd.DataFrame(rows, columns=["f", "lv", "hv", "lo", "hi"])
            tdf["rng"] = (tdf.hi - tdf.lo).abs()
            tdf = tdf.sort_values("rng")
            ylab = [f"{LABELS[f]} ({num(lv)} ↔ {num(hv)})" for f, lv, hv in zip(tdf.f, tdf.lv, tdf.hv)]
            fig = go.Figure()
            fig.add_bar(y=ylab, x=tdf.lo, orientation="h", name="Input lowered by 1 SD", marker_color="#8FA6C8",
                        text=[f"−1 SD: {v:+.1f} pp" for v in tdf.lo], textposition="outside")
            fig.add_bar(y=ylab, x=tdf.hi, orientation="h", name="Input raised by 1 SD", marker_color="#2E5C9A",
                        text=[f"+1 SD: {v:+.1f} pp" for v in tdf.hi], textposition="outside")
            fig.add_vline(x=0, line_color=TEXT)
            lim = float(max(tdf.lo.abs().max(), tdf.hi.abs().max(), 1)) * 1.7
            style_fig(fig, f"Tornado around the scenario diner (P(reorder) = {pct(p1)})",
                      xt="Change in P(reorder), percentage points (← lowers · raises →)",
                      yt="Input (value at −1 SD ↔ +1 SD)", height=380, legend_title="Shock to the input")
            fig.update_layout(barmode="overlay")
            fig.update_xaxes(range=[-lim, lim])
            show(fig, "wi_tornado")

    if B:
        section("Standard scenario library", "Reference", "Computed in the analysis notebook from segment-median diners.")
        s = B["scenarios"]
        table(pd.DataFrame({"Scenario": s.Scenario.str.split(" — ").str[0], "Base diner": s["Base segment"],
                            "Changed inputs": s["Changed inputs"], "Before": s["Before P(reorder)"].map(pct),
                            "After": s["After P(reorder)"].map(pct), "Change": s["Change (pp)"].map(pp),
                            "Tier after": s["Tier after"],
                            "In range?": s["Within segment's observed range?"].str.replace(" — extrapolation", " (extrapol.)")}))
        sB = s.iloc[1]
        pmax = B["diners"].loc[B["diners"].segment == "Premium Foodies", "discount_rate"].max()
        note(f"<b>How to read B:</b> raising a Premium Foodie's discount use to 40% lifts the score {sB['Change (pp)']:+.0f} pp, but no Premium Foodie "
             f"uses discounts that much (max {pct(pmax)}) and heavy discount use is the hallmark of Budget Students, who almost always reorder. "
             "The model has learned 'discount users are the loyal segment' — a correlation, not evidence that discounts retain premium diners.", "")


def page_recommendations():
    page_header("Management Recommendations", "Where to act first — value × risk — and what to do in each segment.")
    if not B:
        return no_bundle_notice()
    E, d = B["seg_econ"], B["diners"]
    section("Executive recommendation", "Business takeaway")
    tk = B["takeaway"]
    parts = tk.split("**")
    html = "".join(f"<b>{p}</b>" if i % 2 else p for i, p in enumerate(parts))
    html = html.replace(" <b>2.", "<br><br><b>2.").replace(" <b>3.", "<br><br><b>3.").replace(" <b>4.", "<br><br><b>4.")
    st.markdown(f'<div class="narr">{html}</div>', unsafe_allow_html=True)

    section("Priority matrix — business value × retention risk", "Prioritisation",
            "Dividers at the diner-weighted averages (value and churn). Bubble size = monthly spend in the uncertain 25–75% band — the value retention spend can move.")
    c1, c2 = st.columns([1.5, 1])
    with c1:
        fig = go.Figure()
        vx, ry = B["value_cut"], B["risk_cut"]
        xmin, xmax = E.value.min() * .85, E.value.max() * 1.12
        for x0, x1, y0, y1, lbl, colr in [(vx, xmax, ry, 1.05, "IMMEDIATE INTERVENTION", RISK), (vx, xmax, -.08, ry, "PROTECT & RETAIN", POS),
                                          (xmin, vx, ry, 1.05, "SELECTIVE RETENTION", CAUTION), (xmin, vx, -.08, ry, "AUTOMATE & MAINTAIN", FAINT)]:
            fig.add_shape(type="rect", x0=x0, x1=x1, y0=y0, y1=y1, fillcolor=colr, opacity=.05, line_width=0)
            fig.add_annotation(x=x1 if x0 == vx else x0, y=y1 - .03 if y1 > .9 else y0 + .03, text=lbl, showarrow=False,
                               xanchor="right" if x0 == vx else "left", font=dict(size=10, color=colr))
        for s, r in E.iterrows():
            size = max(14, np.sqrt(max(r.movable_value, 1)) / 4.5)
            fig.add_scatter(x=[r.value], y=[r.churn], mode="markers+text", name=s,
                            text=[f"<b>{s}</b><br>{aed(r.value)}/diner · {pct(r.churn)} churn<br>movable {aed(r.movable_value)} · #{int(r.intervention_rank)}"],
                            textposition="bottom center" if r.churn > .6 else "top center",
                            textfont=dict(color=SC[s], size=11), marker=dict(size=size, color=SC[s], opacity=.85, line=dict(color=BG, width=1)),
                            hovertemplate=(f"<b>{s}</b><br>Value {aed(r.value)}/diner/month<br>Churn {pct(r.churn)}<br>"
                                           f"Movable value {aed(r.movable_value)} ({int(r.movable_diners)} diners)<br>"
                                           f"Gross spend at risk {aed(r.revenue_at_risk)}<extra></extra>"))
        fig.add_vline(x=vx, line_dash="dash", line_color=MUTED, annotation_text=f"avg value {aed(vx)}", annotation_font_color=MUTED,
                      annotation_position="bottom right")
        fig.add_hline(y=ry, line_dash="dash", line_color=MUTED, annotation_text=f"avg churn {pct(ry)}", annotation_font_color=MUTED,
                      annotation_position="top left")
        style_fig(fig, "Priority matrix (bubble size = movable monthly spend; # = intervention rank)", xt="Est. monthly spend per diner (AED)",
                  yt="Churn rate (share who did not reorder)", height=470, legend=False)
        fig.update_yaxes(tickformat=".0%", range=[-.12, 1.08])
        fig.update_xaxes(range=[xmin, xmax])
        show(fig, "rec_pm")
    with c2:
        disp = pd.DataFrame({"#": E.intervention_rank.astype(int), "Segment": E.index, "Churn": E.churn.map(pct),
                             "Gross at risk": E.revenue_at_risk.map(aed), "Movable value": E.movable_value.map(aed)}).sort_values("#")
        table(disp)
        note("Family Feasters carry the largest <i>gross</i> spend at risk, but most are already below 25% — largely lapsed. "
             "Premium Foodies hold most of the <i>movable</i> value, so they rank first for retention budget.", "gold")

    section("Segment action matrix", "Decisions")
    sa = B["segment_action"]
    table(pd.DataFrame({"Segment": sa.Segment, "Value (AED / diner / month)": sa["Value (est. AED / diner / month)"].map(aed),
                        "Retention risk": sa["Retention risk (churn rate)"].map(pct), "Key behaviour": sa["Key behaviour"],
                        "Best bundle": sa["Best bundle"], "Quadrant": sa.Quadrant, "Recommended action": sa["Recommended action"]}))

    section("30-day operating plan", "Execution")
    prem_at = int(((d.segment == "Premium Foodies") & (d.reorder_prob_oof < 0.6)).sum())
    fam_top = int(((d.segment == "Family Feasters") & (d.reorder_prob_oof < 0.5)).sum())
    plan = pd.DataFrame([
        ("Week 1", "Score all diners with the reorder model; publish the at-risk watch-list", "CRM / Analytics", "Watch-list refreshed weekly"),
        ("Week 1–2", f"Premium Foodies below 60% probability ({prem_at} diners): loyalty perk + premium pairing (steak + salad + wine; sushi + miso + green tea)",
         "Marketing", "Reorder within 30 days vs hold-out"),
        ("Week 2", f"Family Feasters below 50% ({fam_top} diners): weekend 'pizza night' bundle offer to the top quartile by monthly spend only",
         "Marketing", "Win-back rate & offer cost per reactivation"),
        ("Week 2–3", "Budget Students: replace %-discounts with a fixed-price wrap + fries + cola deal", "Pricing", "Discount cost per order; reorder rate stays ≥ 95%"),
        ("Week 4", "Read out A/B tests (randomised hold-out in every campaign) before scaling budget", "Analytics", "Incremental reorder uplift (causal)"),
    ], columns=["When", "Action", "Owner", "Success metric"])
    table(plan)


def page_governance():
    page_header("Model Governance & Data Quality", "What the models are, what they were trained on, and whether the data and artifact can be trusted.")
    checks = [
        ("Artifact keys", set(M) == {"scaler", "kmeans", "segment_names", "clf", "features", "reco"}),
        ("Clustering features = 5, contract order", list(FEATURES) == ["orders_per_month", "avg_order_value", "avg_items_per_order", "days_since_last_order", "discount_rate"]),
        ("Cluster scaler expects 5 features", getattr(scaler, "n_features_in_", None) == 5),
        ("Classifier expects 7 features (5 + age, total spend)", getattr(clf, "n_features_in_", None) == 7),
        ("Classifier feature order matches contract", list(getattr(clf, "feature_names_in_", CLF_FEATURES)) == CLF_FEATURES),
        ("Independent preprocessing (cluster scaler ≠ classifier scaler)", getattr(clf, "named_steps", {}).get("scaler", None) is not scaler),
        ("Every cluster has a business name", set(seg_names) == set(range(kmeans.n_clusters))),
        ("Every segment has recommendations", all(reco.get(n) for n in seg_names.values())),
    ]
    try:
        _ = analyse(PRESETS[list(PRESETS)[0]])
        checks.append(("Live inference via app.py pathway", True))
    except Exception:
        checks.append(("Live inference via app.py pathway", False))
    ok = all(v for _, v in checks)
    c = st.columns(4)
    kpi(c[0], "Artifact status", "PASS" if ok else "FAIL", f"{sum(v for _, v in checks)}/{len(checks)} live checks", "pos" if ok else "risk")
    if B:
        kpi(c[1], "Data-quality status", B["dq"]["status"].title(), f"{B['under18']['n']} under-18 diners out of classifier scope; all else PASS", "caution", small=True)
        kpi(c[2], "Last model training", B["meta"]["trained_at"], f"scikit-learn {B['meta']['sklearn']} · seed {B['meta']['seed']}", small=True)
        kpi(c[3], "Training data", f"{B['meta']['n_diners']} diners", f"{B['meta']['n_model_rows']} in classifier · {B['meta']['n_baskets']:,} baskets")

    if B:
        u = B["under18"]
        section("Under-18 diners — not in the app slider and not in the classifier", "18+ policy",
                "QuickBite's dashboard input and reorder model cover adult accounts only. These diners are documented, not deleted.")
        under18_note()
        c1, c2 = st.columns(2)
        with c1:
            ages = u["ages"]
            fig = go.Figure(go.Bar(x=[str(a) for a in ages.index], y=ages.values, marker_color=[RISK if a < 13 else CAUTION for a in ages.index],
                                   text=ages.values, textposition="outside", hovertemplate="Age %{x}: %{y} diners<extra></extra>"))
            style_fig(fig, f"Excluded diners by age ({u['n']} total)", xt="Age (years) — red = implausible (< 13)", yt="Number of diners",
                      height=320, legend=False)
            fig.update_yaxes(range=[0, ages.max() * 1.3])
            show(fig, "gv_u18_age")
        with c2:
            sg = u["segments"]
            fig = go.Figure(go.Bar(x=list(sg.index), y=sg.values, marker_color=[SC[x] for x in sg.index],
                                   text=[f"{v} ({pct(v / max(u['n'], 1))})" for v in sg.values], textposition="outside",
                                   hovertemplate="%{x}: %{y} under-18 diners<extra></extra>"))
            style_fig(fig, "Excluded diners by segment", xt="Segment", yt="Number of under-18 diners", height=320, legend=False)
            fig.update_yaxes(range=[0, max(sg.max(), 1) * 1.3])
            show(fig, "gv_u18_seg")
        if True:
            scope = pd.DataFrame([
                ("Age input (slider)", "18–70", "Not available"),
                ("Reorder classifier — training & test", f"{B['meta']['n_model_rows']} diners", "Excluded"),
                ("Probabilities, risk tiers, watch-list, ROI", "Scored", "Not scored"),
                ("Batch scoring upload", "Scored", "Flagged 'Not scored — under 18'"),
                ("Segmentation (K-Means)", "Included", "Included (age not used)"),
                ("Market-basket analysis", "Included", "Included (age not used)"),
            ], columns=["Component", "Adults (18+)", f"Under-18 ({u['n']})"])
            table(scope)
            st.caption(f"Under-18 diners' observed reorder rate: {pct(u['reorder_rate'])}. Excluding them is a scope decision, "
                       "not a data-cleaning deletion — no values were changed or imputed.")

    section("Live artifact checks", "Model–dashboard contract")
    table(pd.DataFrame({"Check": [c_ for c_, _ in checks], "Status": ["PASS" if v else "FAIL" for _, v in checks]}))
    if not B:
        return no_bundle_notice()
    meta, m = B["meta"], B["metrics"]
    section("Model card", "Governance")
    card = pd.DataFrame([
        ("Business question", "Segment diners · find bundles · predict reorder"),
        ("Target", meta["target"]),
        ("Segmentation model", meta["cluster_model"]),
        ("Reorder model", meta["model_type"]),
        ("Train / test split", f"{meta['split']} → {meta['n_train']} train · {meta['n_test']} test"),
        ("Baseline", f"Majority class (always 'reorder') = {pct(m['Baseline accuracy'], 1)}"),
        ("Test performance", f"Accuracy {pct(m['Accuracy'], 1)} · ROC-AUC {m['ROC-AUC']:.3f} · F1 {m['F1 (reorder)']:.3f} · Brier {m['Brier score']:.3f}"),
        ("Population scores", "Out-of-fold (5-fold CV) probabilities for KPIs, tiers and the watch-list"),
        ("Scope / exclusions", f"18+ policy: {B['under18']['n']} under-18 diners (ages 9–17) excluded from classifier training, evaluation, scoring and the "
                               "age input; retained for segmentation and baskets"),
        ("Robustness", f"Repeated 5-fold CV (50 fits): accuracy {pct(B['validation']['repeated_cv']['acc_mean'], 1)} ± "
                       f"{pct(B['validation']['repeated_cv']['acc_sd'], 1)}, AUC {B['validation']['repeated_cv']['auc_mean']:.3f}; "
                       f"cluster stability ARI {B['validation']['cluster_stability']['boot_mean']:.3f} (200 bootstrap re-fits)"),
        ("Association rules", f"Apriori · min support {pct(meta['min_support_overall'])} overall, {pct(meta['min_support_segment'])} per segment · lift > 1"),
        ("Known limitations", "Multicollinear inputs (VIF > 5); total spend ≈ one month of spend; orders.csv is a basket sample; associations are not causal"),
    ], columns=["Item", "Detail"])
    table(card)

    section("Feature contract", "Inputs")
    tr = B["train_ranges"]
    fc = pd.DataFrame({"Feature": CLF_FEATURES, "Business meaning": [LABELS[f] for f in CLF_FEATURES],
                       "Clustering (5)": ["✓" if f in FEATURES else "" for f in CLF_FEATURES], "Classifier (7)": ["✓"] * 7,
                       "Training range": [f"{num(tr[f][0])} – {num(tr[f][1])}" for f in CLF_FEATURES],
                       "Dashboard input range": [f"{INPUT_SPEC[f][0]:,} – {INPUT_SPEC[f][1]:,}" for f in CLF_FEATURES]})
    table(fc)
    note("Inputs outside the training range trigger an extrapolation warning on the scoring and what-if pages. "
         "The dashboard always shows raw business units; only the fitted pipelines see scaled values.")

    section("Model comparison (selection on cross-validation)", "Model selection")
    mc = B["model_comparison"]
    table(pd.DataFrame({"Model": mc.Model, "CV accuracy": mc["CV accuracy"].map(lambda v: pct(v, 1)),
                        "CV ROC-AUC": mc["CV ROC-AUC"].map(lambda v: f"{v:.3f}"), "Test accuracy": mc["Test accuracy"].map(lambda v: pct(v, 1)),
                        "Test ROC-AUC": mc["Test ROC-AUC"].map(lambda v: f"{v:.3f}"),
                        "Test Brier ↓": mc["Test Brier (lower = better calibrated)"].map(lambda v: f"{v:.3f}"),
                        "Interpretable": mc.Interpretable.map(lambda v: "Yes" if v else "No")}))
    fig = go.Figure()
    for col_, colr, nm in [("CV accuracy", STEEL, "CV accuracy"), ("CV ROC-AUC", GOLD, "CV ROC-AUC")]:
        fig.add_bar(x=mc.Model, y=mc[col_], name=nm, marker_color=colr, text=[pct(v, 1) for v in mc[col_]], textposition="outside")
    fig.add_hline(y=m["Baseline accuracy"], line_dash="dash", line_color=CAUTION, annotation_text=f"majority baseline {pct(m['Baseline accuracy'], 1)}",
                  annotation_font_color=CAUTION, annotation_position="bottom right")
    style_fig(fig, "Candidate models — 5-fold cross-validation on the training set", xt="Model", yt="Score (%)", height=340, legend_title="Metric")
    fig.update_layout(barmode="group"); fig.update_yaxes(tickformat=".0%", range=[0.5, 1.05])
    show(fig, "gv_models")

    section("Data-quality scorecard", "Data")
    dq = B["dq"]
    st.markdown(f"Overall status: {badge(dq['status'])}", unsafe_allow_html=True)
    scd = dq["scorecard"].copy()
    table(scd)
    c1, c2 = st.columns([1, 1])
    with c1:
        section("Reconciliation — diners.csv ↔ orders.csv")
        table(dq["recon"])
    with c2:
        section("Duplicate grains tested")
        table(pd.DataFrame([("Level 1", "order_id + diner_id + item (exact row)", "0"), ("Level 2", "order_id + item (item twice in a basket)", "0"),
                            ("Level 3", "order_id → exactly one diner_id", "0"),
                            ("Not a duplicate", "Repeated order_id across rows = valid multi-item basket", "—")],
                           columns=["Grain", "Definition", "Violations"]))
    section("Issue log & treatments")
    table(dq["issue_log"], height=380)


# ════════════════════════════════════════════════════════════
# 4. Navigation
# ════════════════════════════════════════════════════════════
PAGES = {
    "Executive Overview": page_overview,
    "Customer Segmentation": page_segmentation,
    "Basket Intelligence": page_basket,
    "Retention & Churn": page_retention,
    "Retention Economics": page_economics,
    "Diner Intelligence": page_diner,
    "What-If Simulator": page_whatif,
    "Recommendations": page_recommendations,
    "Governance & Data Quality": page_governance,
}
with st.sidebar:
    st.markdown(f'<div class="qb-brand" style="margin-top:.3rem">QuickBite</div>'
                f'<div style="font-size:1.15rem;font-weight:600;color:{TEXT};margin-bottom:1rem">Diner Intelligence</div>',
                unsafe_allow_html=True)
    page = st.radio("Navigate", list(PAGES), key="nav", label_visibility="collapsed")
    st.markdown("<hr>", unsafe_allow_html=True)
    if B:
        st.markdown(f"<div style='color:{MUTED};font-size:.78rem;line-height:1.6'>"
                    f"Models trained {B['meta']['trained_at']}<br>{B['meta']['n_diners']} diners · K = {B['meta']['K']} · "
                    f"Logistic regression<br>Accuracy {pct(B['metrics']['Accuracy'])} · AUC {B['metrics']['ROC-AUC']:.2f}<br>"
                    f"Data quality: {B['dq']['status'].title()}</div>", unsafe_allow_html=True)
    else:
        st.caption("Analytics bundle not found — only Diner Intelligence is available.")

PAGES[page]()
st.markdown('<div class="foot">Segments, reorder model and recommendations come from the models trained in QuickBite_Analysis.ipynb '
            '(food_models.joblib). Predictions are statistical associations, not causal estimates.</div>', unsafe_allow_html=True)
