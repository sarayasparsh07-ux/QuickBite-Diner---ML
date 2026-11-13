"""Write validation/approved_differences.json — the explicit whitelist used by run_validation.py.

  python build_approved_differences.py          (run once after a reviewed, intentional change; output is committed)

Every entry below was reviewed by hand and is tied to a CHANGELOG item. For each selector the script looks up the
observed difference and records its EXACT before and after values; it refuses to write the file if a selector matches
nothing, or matches more than one distinct before/after pair (i.e. nothing is ever approved "by pattern").
Approved numbers-in-text changes are hard-coded below and the script asserts they equal what is observed.
"""
import json
import re
import sys
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(HERE))
from bundle_snapshot import load_bundle, load_snapshot  # noqa: E402
from vcore import NUM, compare_bundles, compare_captures  # noqa: E402

BASE = ROOT / "validation" / "baselines"
COMPARISONS = {"received_vs_final": ("capture_v1_received.json", "bundle_v1_received.json.gz"),
               "previous_refinement_vs_final": ("capture_v2_previous_refinement.json", "bundle_v2_previous_refinement.json.gz"),
               "micro_refinement_vs_final": ("capture_v3_micro_refinement.json", "bundle_v3_micro_refinement.json.gz"),
               "final_polish_vs_final": ("capture_v4_final_polish.json", "bundle_v4_final_polish.json.gz"),
               "range_correction_vs_final": ("capture_v5_range_correction.json", "bundle_v5_range_correction.json.gz"),
               "dq_correction_vs_final": ("capture_v6_dq_correction.json", "bundle_v6_dq_correction.json.gz")}
DINER_LOOKUP = r"(diner:Look up an existing diner…|diner_id:.*|batch:.*)"   # pages that render the looked-up diner's note
GOV = "Governance & Data Quality"
RET = r"(Retention & Churn|watchlist:.*)"

# (code, id, reason, record kind, selector)
SELECTORS = [
    ("M3", "fix2-title", "Fix 2: chart renamed from 'Lorenz curve' (it ranks highest spenders first)", "chart_layout", dict(chart="ov_lorenz", field="title")),
    ("M3", "fix2-subtitle", "Fix 2: explanatory subtitle added", "chart_layout", dict(chart="ov_lorenz", field="subtitle")),
    ("P1", "tiers-legend-title", "Legend title 'Segment' dropped so the legend wraps on narrow cards; chart title still says 'by segment'", "chart_layout", dict(chart="ov_tiers", field="legend_title")),
    ("P1", "tier-glyphs-overview", "Risk-tier axis labels gain ▲△▽▼ (categories themselves unchanged)", "chart_layout", dict(chart="ov_tiers", field="yaxis.ticktext")),
    ("P1", "tier-glyphs-retention", "Risk-tier axis labels gain ▲△▽▼ (categories themselves unchanged)", "chart_layout", dict(chart="rt_tierbar", field="xaxis.ticktext")),
    ("P1", "kw-title", "Title shortened to fit a half-width card (colour legend wording)", "chart_layout", dict(chart="seg_kw", field="title")),
    ("P1", "wrap-hyphen-fix-tiers", "Previous submission's title wrapping split 'out-of-fold' at a hyphen ('out- of-fold'); wrapping no longer breaks on hyphens",
     "chart_layout", dict(chart="ov_tiers", field="title")),
    ("P1", "wrap-hyphen-fix-hist", "Previous submission's title wrapping split 'cut-offs' at a hyphen ('cut- offs'); wrapping no longer breaks on hyphens",
     "chart_layout", dict(chart="rt_hist", field="title")),
    ("M2", "rcv-chart-title", "Repeated-CV chart labelled as a post-selection stability check", "chart_layout", dict(chart="rt_cv", field="title")),
    ("M1", "gv-baseline-line", "Governance selection-CV chart: baseline line is now the training-set majority share (matched to training-fold CV)", "chart_layout", dict(chart="gv_models", field="annotations")),
    ("M2", "kpi-rocauc-context", "ROC-AUC KPI context names repeated CV and held-out test explicitly", "kpi", dict(label="ROC-AUC", field="context", where=RET)),
    ("M2", "kpi-test-context", "Test-split KPI context names its own (test) baseline", "kpi", dict(label="Test-split accuracy", field="context", where=RET)),
    ("P1", "batch-tier-names-1", "Tier legend names gain glyphs", "trace", dict(chart="batch_fig", field="name", trace="High retention likelihood")),
    ("P1", "batch-tier-names-2", "Tier legend names gain glyphs", "trace", dict(chart="batch_fig", field="name", trace="Moderate retention likelihood")),
    ("P1", "batch-tier-names-3", "Tier legend names gain glyphs", "trace", dict(chart="batch_fig", field="name", trace="At-risk")),
    ("P1", "batch-tier-names-4", "Tier legend names gain glyphs", "trace", dict(chart="batch_fig", field="name", trace="High churn risk")),
    ("P1", "gv-hatched-name", "Legend notes the hatch texture", "trace", dict(chart="gv_models", field="name", trace="CV accuracy")),
    ("P1", "hist-hatched-name", "Legend notes the hatch texture", "trace", dict(chart="rt_hist", field="name", trace="Actually churned")),
    ("P1", "tornado-hatched-name", "Legend notes the hatch texture", "trace", dict(chart="wi_tornado", field="name", trace="Input lowered by 1 SD")),
    ("M2", "model-card-test-row", "Model card: test row labelled as the independent held-out evaluation", "table_row", dict(where="Governance & Data Quality", detail_re=r"table 3, row 7")),
    ("M2", "model-card-stability-row", "Model card: repeated CV labelled as a post-selection stability check (not independent, no nested CV) with its baseline", "table_row", dict(where="Governance & Data Quality", detail_re=r"table 3, row 10")),
    ("M2", "takeaway", "Business takeaway: test accuracy paired with the test baseline, repeated CV with its own baseline", "value", dict(where="/takeaway")),
    ("P1", "nb-seg-colour-ff", "Notebook (light) figure colour; not read by the dashboard", "value", dict(where="/seg_colors/Family Feasters")),
    ("P1", "nb-seg-colour-bs", "Notebook (light) figure colour; not read by the dashboard", "value", dict(where="/seg_colors/Budget Students")),
    ("P1", "nb-tier-colour", "Notebook moderate-tier colour; not read by the dashboard", "value", dict(where="/risk_tiers[1][3]")),
    # Final documentation consistency: DQ-01 / DQ-05 corrected at the source (build/notebook_source.py), notebook re-executed.
    # Only these two issue-log rows, at these exact locations; every 'after' must equal reports/data_quality_issue_log.csv.
    ("DQ01", "dq01-bundle-row", "DQ-01 population text: 460 classifier-eligible adults (368 training + 92 held-out test), not "
     "'trained on 460'", "df_row", dict(where="/dq/issue_log", id_value="DQ-01")),
    ("DQ05", "dq05-bundle-row", "DQ-05: observed adult classifier range wording (460 eligible adults); Quantity '6 of 7 classifier input "
     "controls', independently recalculated from INPUT_SPEC and the observed adult range; values stay permitted", "df_row",
     dict(where="/dq/issue_log", id_value="DQ-05")),
    ("DQ01", "dq01-governance-row", "Governance issue log shows the corrected DQ-01 row (from the regenerated bundle)", "table_row",
     dict(where="Governance & Data Quality", detail_re=r"table 9, row 1$")),
    ("DQ05", "dq05-governance-row", "Governance issue log shows the corrected DQ-05 row (from the regenerated bundle; the runtime "
     "substitution is removed)", "table_row", dict(where="Governance & Data Quality", detail_re=r"table 9, row 5$")),
]
DQ_CODES = ("DQ01", "DQ05")
# T2 column relabels: (id, page/state regex, old heading, new heading) — every cell value must be identical under the new heading
COLUMN_RELABELS = [
    ("feature-contract-range-heading", "Governance & Data Quality", "Training range", "Observed adult classifier range"),
    ("batch-display-range-heading", r"batch:.*", "outside_training_range", "Outside observed adult range"),
]
KPI_RENAMES = [   # (code, id, reason, page, label before, label after, value may be re-formatted with the same number)
    ("M2", "kpi-overview-rename", "Overview KPI renamed: the 85.8% is a repeated-CV stability result, not 'model accuracy' in general",
     "Executive Overview", "Model accuracy", "Repeated-CV accuracy", False),
    ("M2", "kpi-retention-rename", "Retention KPI renamed from 'Expected accuracy' (it is not an independent expected-performance estimate)",
     RET, "Expected accuracy", "Repeated-CV accuracy", False),
    ("T1", "kpi-governance-population", "Governance KPI renamed from 'Training data' (480 is the analysis population, not the classifier "
     "training set); the context now gives 480 diners · 460 adult classifier population · 368 training · 92 test observations",
     GOV, "Training data", "Analysis population", True),
]
# numbers that may (dis)appear in visible text beyond the training-timestamp digits — reviewed, per comparison and page
TEXT_NUMBERS = {
    "received_vs_final": [
        ("added", DINER_LOOKUP, "T2", "final-model-training-count", ["368", "460"]),
        ("added", GOV, "T1", "governance-population-terms", ["368", "368", "460", "480", "92", "92"]),
        ("lost", GOV, "T1", "governance-population-terms", ["1980"]),
        ("added", RET, "M2", "retention-note", ["3.0", "368", "460", "5", "58.7", "58.7", "92"]),
        ("lost", RET, "M2", "retention-note", ["27.3"]),
        ("added", "Governance & Data Quality", "M1T", "governance-protocol-text", ["368", "5", "92"]),
        ("added", "Recommendations", "M2", "takeaway-text", ["0.97", "3.0", "58.5", "58.7", "83.7", "85.8", "90.2", "92", "95", "95.7"]),
        ("lost", "Recommendations", "M2", "takeaway-text", ["0.94", "59", "86", "90"]),
    ],
    "previous_refinement_vs_final": [
        ("added", DINER_LOOKUP, "T2", "final-model-training-count", ["368", "460"]),
        ("added", GOV, "T1", "governance-population-terms", ["368", "368", "460", "480", "92", "92"]),
        ("lost", GOV, "T1", "governance-population-terms", ["1980"]),
        ("added", RET, "M2", "retention-note", ["3.0", "368", "460", "5", "58.7", "58.7", "92"]),
        ("lost", RET, "M2", "retention-note", ["27.3"]),
        ("added", "Recommendations", "M2", "takeaway-text", ["0.97", "3.0", "58.5", "58.7", "83.7", "85.8", "90.2", "92", "95", "95.7"]),
        ("lost", "Recommendations", "M2", "takeaway-text", ["0.94", "59", "86", "90"]),
    ],
    "range_correction_vs_final": [],   # DQ text lives in tables; the only text numbers that change are the timestamp digits (TS)
    "dq_correction_vs_final": [],      # DQ-05 quantity lives in a table; only the timestamp digits change in text (TS)
    "final_polish_vs_final": [   # final micro-correction only: the looked-up diner's note names the 368 / 460 populations
        ("added", DINER_LOOKUP, "T2", "final-model-training-count", ["368", "460"]),
    ],
    "micro_refinement_vs_final": [   # final submission polish only: the Governance KPI context and the training-range definition
        ("added", DINER_LOOKUP, "T2", "final-model-training-count", ["368", "460"]),
        ("added", GOV, "T1", "governance-population-terms", ["368", "368", "460", "480", "92", "92"]),
        ("lost", GOV, "T1", "governance-population-terms", ["1980"]),
    ],
}
M1_SPEC = {  # exact schemas, taken from the frozen received bundle / capture and the final ones (asserted below)
    "bundle_columns_before": ["Model", "CV accuracy", "CV accuracy (sd)", "CV ROC-AUC", "Test accuracy", "Test ROC-AUC",
                              "Test Brier (lower = better calibrated)", "Interpretable"],
    "bundle_columns_after": ["Model", "CV accuracy", "CV accuracy (sd)", "CV precision (reorder)", "CV recall (reorder)", "CV F1 (reorder)",
                             "CV ROC-AUC", "CV Brier (lower = better calibrated)", "Interpretable"],
    "table_columns_before": ["Model", "CV accuracy", "CV ROC-AUC", "Test accuracy", "Test ROC-AUC", "Test Brier ↓", "Interpretable"],
    "table_columns_after": ["Model", "Selected", "CV accuracy", "CV precision", "CV recall", "CV F1", "CV ROC-AUC ↑", "CV Brier ↓", "Interpretable"],
    "shared_bundle_columns": ["Model", "CV accuracy", "CV accuracy (sd)", "CV ROC-AUC", "Interpretable"],
}
PALETTE = ["#0B1020", "#101A2D", "#152238", "#1B2B43", "#2B405C", "#F4F7FC", "#A8B6CB", "#8A99B0", "#45E3C1", "#A5E4FF",
           "#5B84FF", "#D98CF2", "#FFC76B", "#FF7D91", "#3A66E8", "#789BFF"]


def matches(r, kind, sel):
    if r["kind"] != kind:
        return False
    for k in ("chart", "field", "label", "trace"):
        if k in sel and r.get(k) != sel[k]:
            return False
    if "where" in sel and not re.fullmatch(sel["where"] if kind != "value" else re.escape(sel["where"]), r["where"]):
        return False
    if "detail_re" in sel and not re.match(sel["detail_re"], r["detail"]):
        return False
    if "id_value" in sel and not (isinstance(r["_before"], dict) and r["_before"].get("ID") == sel["id_value"]):
        return False
    return True


def main():
    exact, seen_ids = [], set()
    final_cap = json.loads((ROOT / "validation" / "captures" / "capture_final.json").read_text())
    final_bundle = load_bundle(ROOT / "dashboard_bundle.joblib")
    text_specs = []
    for comp, (capf, bunf) in COMPARISONS.items():
        cap_d, _ = compare_captures(json.loads((BASE / capf).read_text()), final_cap)
        base_b = load_snapshot(BASE / bunf)
        bun_d = compare_bundles(base_b, final_bundle)
        recs = cap_d + bun_d
        for code, id_, reason, kind, sel in SELECTORS:
            hits = [r for r in recs if matches(r, kind, sel)]
            if not hits:
                continue                              # this change does not occur in this comparison
            pairs = {json.dumps([h["_before"], h["_after"]], sort_keys=True, ensure_ascii=False) for h in hits}
            assert len(pairs) == 1, f"{comp}/{id_}: {len(pairs)} distinct before/after pairs — refine the selector"
            b, a = json.loads(pairs.pop())
            entry = {"id": id_, "code": code, "reason": reason, "kind": kind, "applies_to": [comp], "before": b, "after": a,
                     **{k: v for k, v in sel.items() if k != "detail_re"}}
            if kind == "value":
                entry["where"] = re.escape(sel["where"])
            if "detail_re" in sel:
                entry["detail_re"] = sel["detail_re"]
            twin = next((e for e in exact if e["id"] == id_ and e["before"] == b and e["after"] == a), None)
            if twin:
                twin["applies_to"].append(comp)
            else:
                exact.append(entry)
            seen_ids.add(id_)
        # numbers in text: what is observed beyond the timestamp digits must equal the reviewed lists exactly
        ts_old, ts_new = base_b["meta"]["trained_at"], final_bundle["meta"]["trained_at"]
        old, new = set(NUM.findall(ts_old)), set(NUM.findall(ts_new))
        # several reviewed specs may share a page (one per approved change): their UNION must equal the observation exactly
        groups = {}
        for kind, where, code, id_, nums in TEXT_NUMBERS[comp]:
            groups.setdefault((kind, where), []).append(nums)
            text_specs.append({"applies_to": comp, "kind": kind, "where": where, "code": code, "id": id_, "numbers": sorted(nums)})
        for (kind, where), lists in groups.items():
            k = "text_numbers_added" if kind == "added" else "text_numbers_lost"
            obs = {json.dumps(sorted(x for x in (r["_after"] if kind == "added" else r["_before"]) if x not in (new if kind == "added" else old)))
                   for r in cap_d if r["kind"] == k and re.fullmatch(where, r["where"])}
            obs.discard("[]")
            assert obs == {json.dumps(sorted(x for l_ in lists for x in l_))}, f"{comp}/{where}/{kind}: observed {obs}"
        if comp == "received_vs_final":
            mc_b, mc_a = base_b["model_comparison"]["__df__"]["columns"], final_bundle["model_comparison"]["__df__"]["columns"]
            assert (mc_b, mc_a) == (M1_SPEC["bundle_columns_before"], M1_SPEC["bundle_columns_after"]), (mc_b, mc_a)
    relabels, seen_rl = [], set()
    for comp, (capf, _) in COMPARISONS.items():
        cap_d, _ = compare_captures(json.loads((BASE / capf).read_text()), final_cap)
        for id_, where, old_h, new_h in COLUMN_RELABELS:
            hits = [r for r in cap_d if r["kind"] == "table_schema" and re.fullmatch(where, r["where"]) and old_h in r["_before"]
                    and new_h in r["_after"]]
            if not hits:
                continue
            seen_rl.add(id_)
            e = next((x for x in relabels if x["id"] == id_), None)
            if e:
                e["applies_to"].append(comp)
            else:
                relabels.append({"id": id_, "code": "T2", "where": where, "from": old_h, "to": new_h, "applies_to": [comp],
                                 "reason": "display heading corrected to 'observed adult' terminology; values must be identical"})
    assert seen_rl == {x[0] for x in COLUMN_RELABELS}, f"relabels not observed: {set(x[0] for x in COLUMN_RELABELS) - seen_rl}"
    # content test for the DQ entries: the approved 'after' must be exactly the authoritative issue-log row
    import csv
    with open(ROOT / "reports" / "data_quality_issue_log.csv", newline="", encoding="utf-8") as f:
        rows = list(csv.reader(f))
    auth = {r[0]: dict(zip(rows[0], r)) for r in rows[1:]}
    import dq_consistency as q
    calc = q.dq05_calculation(q.app_input_spec(ROOT), q.recount(ROOT)["ranges"])     # independent of every issue-log file
    assert calc["complete"], calc
    for e in exact:
        if e["code"] in DQ_CODES:
            assert e["after"] == auth[e["after"]["ID"]], f"{e['id']}: approved 'after' differs from the issue-log CSV"
            assert e["before"]["ID"] == e["after"]["ID"] == {"DQ01": "DQ-01", "DQ05": "DQ-05"}[e["code"]], e["id"]
            if e["code"] == "DQ05":
                assert e["after"]["Quantity"] == calc["quantity"], f"{e['id']}: Quantity {e['after']['Quantity']!r} != {calc['quantity']!r}"
                if "dq_correction_vs_final" in e["applies_to"] and len(e["applies_to"]) == 1:
                    changed = sorted(c for c in e["after"] if e["after"][c] != e["before"][c])
                    assert changed == ["Quantity", "Treatment"], f"{e['id']}: unexpected fields changed {changed}"
    missing = {s[1] for s in SELECTORS} - seen_ids
    assert not missing, f"selectors that matched nothing: {missing}"
    out = {"_doc": "Explicit whitelist of approved differences. Generated by build_approved_differences.py from reviewed selectors; "
                   "each 'exact' entry holds the exact before/after values. See CHANGELOG.md for the reason behind every code.",
           "exact": exact, "kpi_renames": [], "column_relabels": relabels, "text_numbers": text_specs, "m1": M1_SPEC, "palette": PALETTE,
           "palette_rgb": [[int(h[i:i + 2], 16) for i in (1, 3, 5)] for h in PALETTE],
           "style_keys": ["symbol", "opacity", "width", "dash", "shape", "fillmode", "solidity"]}
    fc = final_cap
    for code, id_, reason, where, lb, la, reformat in KPI_RENAMES:
        snaps = [(n, s) for g in ("pages", "states") for n, s in fc[g].items() if re.fullmatch(where, n)]
        val_ctx = {tuple(s["kpis"][la]) for _, s in snaps if la in s["kpis"]}
        assert len(val_ctx) == 1, (id_, val_ctx)
        value, ctx_after = val_ctx.pop()
        base_ctx = {tuple(s["kpis"][lb]) for comp, (capf, _) in COMPARISONS.items()
                    for g in ("pages", "states") for n, s in json.loads((BASE / capf).read_text())[g].items()
                    if re.fullmatch(where, n) and lb in s["kpis"]}
        assert len(base_ctx) == 1, (id_, base_ctx)
        bval, ctx_before = base_ctx.pop()
        entry = {"id": id_, "code": code, "reason": reason, "where": where, "label_before": lb, "label_after": la}
        if reformat:   # only the unit word may go: the number itself must be identical ('480 diners' → '480')
            assert NUM.findall(bval) == NUM.findall(value) and NUM.findall(value), f"{id_}: KPI number changed {bval} → {value}"
            entry.update(value_before=bval, value_after=value)
        else:
            assert bval == value, f"{id_}: KPI value changed {bval} → {value}"
            entry["value"] = value
        out["kpi_renames"].append({**entry, "context_before": ctx_before, "context_after": ctx_after})
    (ROOT / "validation" / "approved_differences.json").write_text(json.dumps(out, indent=1, ensure_ascii=False))
    print(f"wrote {len(exact)} exact entries, {len(out['kpi_renames'])} KPI renames, {len(text_specs)} text-number specs")


if __name__ == "__main__":
    main()
