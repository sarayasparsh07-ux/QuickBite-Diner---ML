"""Browser-level test of the batch CSV workflow (Diner Intelligence → Batch scoring) in a real Chromium browser.

  streamlit run app.py                                   # in another terminal (default http://localhost:8501; override with QB_URL)
  python browser_upload_test.py <out_dir> [<reference_dir>]   # optional tool: needs playwright==1.63.0 + chromium (as shots.py)

With <reference_dir> (e.g. validation/baselines/batch_export_v4_final_polish), the files downloaded through the browser
are also compared BYTE FOR BYTE with an earlier version's downloads (template.csv, scored_<case>.csv): proof that the
export schema, the outside_training_range field and every prediction are unchanged.

What it does, entirely through the browser, exactly as a user would:
  1. opens the dashboard, goes to Diner Intelligence → "Batch scoring (CSV upload)";
  2. clicks "Download example CSV" and saves the file the browser downloads (the template);
  3. builds test files from that template: valid rows + 3 hand-written diners + an extra user column + one non-numeric and
     one blank value (mixed file); missing required column; 0-byte file; header-only file; under-18-only file;
  4. for each file: clicks the uploader's "Browse files" button, answers the browser's file chooser with the file, waits for
     the result, reads the KPI cards / error messages, and — when offered — clicks "Download scored file (CSV)";
  5. checks the downloaded scored file against an INDEPENDENT recomputation from food_models.joblib (not app.py):
     every row accounted for and in order, identifiers and user columns preserved, the documented output columns appended,
     status per row (scored / under 18 / missing or non-numeric), segment, P(reorder) (exact), predicted class, risk tier
     (documented cut-offs 75 / 50 / 25 %) and recommended items, and that the KPI cards match the file.
Writes <out_dir>/browser_upload_test_results.json (PASS / FAIL per check) and keeps the downloaded files under <out_dir>.

Scope: the operating system's own file dialog is not drawn in a headless browser — Playwright answers the browser's
file-chooser request instead. Everything after that (upload, server-side read, scoring, rendering, download) is the real
path. A person clicking through the procedure in README §G on their own computer is a separate, manual test.
"""
import json
import math
import os
import re
import sys
import time
from datetime import datetime
from pathlib import Path

import joblib
import numpy as np
import pandas as pd
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[2]
OUT = Path(sys.argv[1]).resolve()
REF = Path(sys.argv[2]).resolve() if len(sys.argv) > 2 else None
URL = os.environ.get("QB_URL", "http://localhost:8501")
CLF_FEATURES = ["age", "orders_per_month", "avg_order_value", "avg_items_per_order", "days_since_last_order", "discount_rate", "total_spend"]
APPENDED = ["status", "segment", "p_reorder", "will_reorder", "risk_tier", "action", "recommended_items", "outside_training_range"]
ST_SCORED, ST_U18, ST_BAD = "Scored", "Not scored — under 18 (18+ policy)", "Not scored — missing / non-numeric value"
results = []


def check(case, name, ok, detail=""):
    results.append({"case": case, "check": name, "result": "PASS" if ok else "FAIL", "detail": detail})
    print(("PASS " if ok else "FAIL ") + f"[{case}] {name}" + ("" if ok else f" — {detail}"), flush=True)


# ───────────────────────── independent expectation (saved model artifact only) ─────────────────────────
M = joblib.load(ROOT / "food_models.joblib")
BUNDLE = joblib.load(ROOT / "dashboard_bundle.joblib")
CUTS = [(float(t[0]), t[1]) for t in BUNDLE["risk_tiers"]]
assert [c for c, _ in CUTS] == [0.75, 0.50, 0.25, 0.0], CUTS          # the documented cut-offs


def expected(df):
    """Status and predictions for each row, computed from food_models.joblib directly."""
    num = df[CLF_FEATURES].apply(pd.to_numeric, errors="coerce")
    status = np.where(num.isna().any(axis=1), ST_BAD, np.where(num.age < 18, ST_U18, ST_SCORED))
    exp = pd.DataFrame({"status": status}, index=df.index)
    ok = exp.status == ST_SCORED
    if ok.any():
        X = num.loc[ok]
        seg = M["kmeans"].predict(M["scaler"].transform(X[M["features"]]))
        Xc = X[list(M["clf"].feature_names_in_)]
        exp.loc[ok, "segment"] = [M["segment_names"][int(c)] for c in seg]
        exp.loc[ok, "p_reorder"] = M["clf"].predict_proba(Xc)[:, 1]
        exp.loc[ok, "will_reorder"] = np.where(M["clf"].predict(Xc) == 1, "Yes", "At risk")
        exp.loc[ok, "risk_tier"] = [next(lab for cut, lab in CUTS if p >= cut) for p in exp.loc[ok, "p_reorder"]]
        exp.loc[ok, "n_items"] = [len(M["reco"][s]) for s in exp.loc[ok, "segment"]]
    return exp


# ───────────────────────── browser helpers ─────────────────────────
def open_batch(pg):
    pg.goto(URL)
    pg.wait_for_selector("[data-testid=stSidebar]", timeout=90000)
    time.sleep(4)
    pg.locator("[data-testid=stSidebar] label").filter(has_text="Diner Intelligence").first.dispatch_event("click")
    pg.get_by_role("tab", name="Batch scoring (CSV upload)").wait_for(timeout=60000)
    pg.get_by_role("tab", name="Batch scoring (CSV upload)").click()
    pg.locator("[data-testid=stFileUploader]").wait_for(timeout=60000)
    time.sleep(1.5)


def wait_idle(pg, timeout=60):
    """Streamlit shows a status widget while the script reruns; wait for it to disappear and the page to settle."""
    end = time.time() + timeout
    time.sleep(1.0)
    while time.time() < end:
        if not pg.locator("[data-testid=stStatusWidget]").count():
            time.sleep(1.0)
            if not pg.locator("[data-testid=stStatusWidget]").count():
                return
        time.sleep(0.3)


def upload(pg, path):
    """Click the real 'Browse files' button; answer the browser's file chooser with <path>."""
    with pg.expect_file_chooser(timeout=30000) as fc:
        pg.locator("[data-testid=stFileUploader] button").filter(has_text=re.compile("Browse|Upload", re.I)).first.click()
    fc.value.set_files(str(path))
    end = time.time() + 90
    while time.time() < end:
        if pg.locator(".qf-kpi .k-label").filter(has_text="Rows uploaded").count() or pg.locator("[data-testid=stAlert]").count() \
                or pg.locator("[data-testid=stException]").count():
            break
        time.sleep(0.5)
    wait_idle(pg)


def kpis(pg):
    out = {}
    for card in pg.locator(".qf-kpi").all():
        try:
            # text_content, not inner_text: the label is upper-cased by CSS on screen, the DOM text is the real label
            out[card.locator(".k-label").text_content().strip()] = card.locator(".k-value").text_content().strip()
        except Exception:  # noqa: BLE001
            pass
    return out


def alerts(pg):
    return [a.inner_text().strip() for a in pg.locator("[data-testid=stAlert]").all()]


def exceptions(pg):
    return [a.inner_text().strip()[:300] for a in pg.locator("[data-testid=stException]").all()]


def download(pg, label, dest):
    btn = pg.locator("[data-testid=stDownloadButton] button").filter(has_text=label)
    if not btn.count():
        return None
    with pg.expect_download(timeout=30000) as d:
        btn.first.click()
    d.value.save_as(str(dest))
    return dest


# ───────────────────────── run ─────────────────────────
def main():
    inputs, downloads = OUT / "inputs", OUT / "downloads"
    inputs.mkdir(parents=True, exist_ok=True); downloads.mkdir(parents=True, exist_ok=True)
    with sync_playwright() as p:
        browser = p.chromium.launch()
        ctx = browser.new_context(accept_downloads=True, viewport={"width": 1440, "height": 1000})
        pg = ctx.new_page()
        meta = {"date": datetime.now().strftime("%d %b %Y, %H:%M"), "url": URL, "browser": f"Chromium {browser.version} (headless, Playwright)"}

        # 1-2 · template download
        open_batch(pg)
        tpl_path = download(pg, "Download example CSV", downloads / "quickbite_scoring_template.csv")
        check("template", "Template downloaded through the browser", tpl_path is not None and tpl_path.stat().st_size > 0, str(tpl_path))
        tpl = pd.read_csv(tpl_path)
        check("template", "Template has diner_id + the 7 required columns, 11 rows, 2 under-18",
              list(tpl.columns) == ["diner_id"] + CLF_FEATURES and len(tpl) == 11 and int((tpl.age < 18).sum()) == 2,
              {"columns": list(tpl.columns), "rows": len(tpl), "under18": int((tpl.age < 18).sum())})

        # 3 · test files built from the template
        mixed = tpl.copy()
        new = pd.DataFrame([
            {"diner_id": "TEST001", "age": 24, "orders_per_month": 9, "avg_order_value": 62.5, "avg_items_per_order": 2,
             "days_since_last_order": 3, "discount_rate": 0.35, "total_spend": 560.0},
            {"diner_id": "TEST002", "age": 41, "orders_per_month": 4, "avg_order_value": 145.0, "avg_items_per_order": 5,
             "days_since_last_order": 21, "discount_rate": 0.10, "total_spend": 610.0},
            {"diner_id": "TEST003", "age": 33, "orders_per_month": 2, "avg_order_value": 88.0, "avg_items_per_order": 3,
             "days_since_last_order": 30, "discount_rate": 0.55, "total_spend": 180.0}])
        mixed = pd.concat([mixed, new], ignore_index=True).astype({"avg_order_value": object, "discount_rate": object})
        bad1 = dict(new.iloc[0]); bad1.update(diner_id="BAD_NONNUMERIC", avg_order_value="abc")
        bad2 = dict(new.iloc[1]); bad2.update(diner_id="BAD_BLANK", discount_rate="")
        mixed = pd.concat([mixed, pd.DataFrame([bad1, bad2])], ignore_index=True)
        mixed["store_note"] = [f"note-{i}" for i in range(len(mixed))]                    # a user column that must survive
        files = {"mixed_valid_and_invalid": mixed, "missing_required_column": tpl.drop(columns=["discount_rate"]),
                 "under18_only": tpl[tpl.age < 18]}
        for k, df in files.items():
            df.to_csv(inputs / f"{k}.csv", index=False)
        (inputs / "empty_0_bytes.csv").write_bytes(b"")
        (inputs / "header_only.csv").write_text(",".join(["diner_id"] + CLF_FEATURES) + "\n")

        # 4-5 · main case
        case = "mixed_valid_and_invalid"
        open_batch(pg); upload(pg, inputs / f"{case}.csv")
        k = kpis(pg)
        check(case, "No exception shown in the browser", not exceptions(pg), exceptions(pg))
        out_path = download(pg, "Download scored file (CSV)", downloads / f"{case}_scored.csv")
        pg.screenshot(path=str(OUT / f"{case}.png"), full_page=False)
        check(case, "Scored CSV downloaded through the browser", out_path is not None, str(out_path))
        # float_precision="round_trip": parse each number exactly as written (pandas' default fast parser may be 1 ulp off)
        res = pd.read_csv(out_path, float_precision="round_trip") if out_path else pd.DataFrame()
        src = pd.read_csv(inputs / f"{case}.csv", dtype=str, keep_default_na=False)
        exp = expected(src)
        check(case, "Every uploaded row is in the scored file, in the same order (no row lost or added)",
              len(res) == len(src) and list(res.diner_id) == list(src.diner_id), {"uploaded": len(src), "downloaded": len(res)})
        check(case, "Columns: every uploaded column kept with its name and order, then the documented output columns",
              list(res.columns) == list(src.columns) + APPENDED, list(res.columns))
        check(case, "Identifiers and the extra user column are preserved exactly",
              list(res.diner_id.astype(str)) == list(src.diner_id) and list(res.store_note) == list(src.store_note))
        check(case, "Status per row = independent rule (scored / under 18 / missing or non-numeric)",
              list(res.status) == list(exp.status), [(i, a, b) for i, (a, b) in enumerate(zip(res.status, exp.status)) if a != b])
        sc = exp.status == ST_SCORED
        check(case, "Expected mix in the test file: 12 scored, 2 under-18, 2 missing / non-numeric",
              (int(sc.sum()), int((exp.status == ST_U18).sum()), int((exp.status == ST_BAD).sum())) == (12, 2, 2),
              dict(exp.status.value_counts()))
        pr = pd.to_numeric(res.loc[sc, "p_reorder"], errors="coerce")
        check(case, "P(reorder) is numeric and within [0, 1] for every scored row", pr.notna().all() and pr.between(0, 1).all(), list(pr))
        diff = float(np.max(np.abs(pr.values - exp.loc[sc, "p_reorder"].astype(float).values))) if sc.any() else math.nan
        check(case, "P(reorder) equals the independent recomputation from food_models.joblib (exact after the CSV round trip)",
              diff == 0.0, f"max |difference| = {diff}")
        check(case, "Segment names equal the independent recomputation", list(res.loc[sc, "segment"]) == list(exp.loc[sc, "segment"]),
              list(zip(res.loc[sc, "segment"], exp.loc[sc, "segment"])))
        check(case, "Predicted class (Yes / At risk) equals clf.predict", list(res.loc[sc, "will_reorder"]) == list(exp.loc[sc, "will_reorder"]))
        check(case, "Risk tier equals the documented cut-offs (75 / 50 / 25 %) applied to the recomputed probability",
              list(res.loc[sc, "risk_tier"]) == list(exp.loc[sc, "risk_tier"]),
              list(zip(res.loc[sc, "risk_tier"], exp.loc[sc, "risk_tier"])))
        check(case, "Every scored row has an action and as many recommended items as its segment's list",
              res.loc[sc, "action"].notna().all() and [len(str(x).split(", ")) for x in res.loc[sc, "recommended_items"]]
              == [int(n) for n in exp.loc[sc, "n_items"]])
        ns = ~sc
        check(case, "Rows not scored carry no segment, probability or tier (flagged, not guessed)",
              res.loc[ns, ["segment", "p_reorder", "will_reorder", "risk_tier"]].isna().all().all(),
              res.loc[ns, ["diner_id", "status", "segment", "p_reorder", "risk_tier"]].to_dict("records"))
        check(case, "KPI cards match the file (rows uploaded, scored, under 18, predicted at risk)",
              k.get("Rows uploaded") == str(len(src)) and k.get("Scored") == str(int(sc.sum()))
              and k.get("Not scored — under 18") == "2" and k.get("Predicted at risk") == str(int((pr < 0.5).sum())),
              {x: k.get(x) for x in ("Rows uploaded", "Scored", "Not scored — under 18", "Predicted at risk", "Mean P(reorder)")})

        # error handling
        case = "missing_required_column"
        open_batch(pg); upload(pg, inputs / f"{case}.csv")
        al = alerts(pg)
        check(case, "Clear error naming the missing column; nothing scored or offered for download",
              any("Missing required columns: discount_rate" in a for a in al) and not exceptions(pg)
              and not pg.locator("[data-testid=stDownloadButton] button").filter(has_text="Download scored file").count(), al)

        case = "empty_0_bytes"
        open_batch(pg); upload(pg, inputs / "empty_0_bytes.csv")
        al = alerts(pg)
        check(case, "Clear 'could not read the file' message; no crash, nothing scored",
              any("Could not read the file" in a for a in al) and not exceptions(pg)
              and not pg.locator("[data-testid=stDownloadButton] button").filter(has_text="Download scored file").count(), al)

        case = "header_only"
        open_batch(pg); upload(pg, inputs / "header_only.csv")
        k = kpis(pg)
        check(case, "Header-only file: no crash; 0 rows uploaded, 0 scored", not exceptions(pg) and k.get("Rows uploaded") == "0"
              and k.get("Scored") == "0", {"kpis": {x: k.get(x) for x in ("Rows uploaded", "Scored")}, "alerts": alerts(pg), "exceptions": exceptions(pg)})

        case = "under18_only"
        open_batch(pg); upload(pg, inputs / f"{case}.csv")
        k = kpis(pg)
        out_path = download(pg, "Download scored file (CSV)", downloads / f"{case}_scored.csv")
        res = pd.read_csv(out_path, float_precision="round_trip") if out_path else pd.DataFrame()
        check(case, "Under-18 rows flagged 'Not scored — under 18 (18+ policy)', kept in the file, no prediction",
              not exceptions(pg) and len(res) == 2 and (res.status == ST_U18).all() and res.p_reorder.isna().all()
              and k.get("Scored") == "0" and k.get("Not scored — under 18") == "2",
              {"kpis": {x: k.get(x) for x in ("Rows uploaded", "Scored", "Not scored — under 18")},
               "rows": res[["diner_id", "status"]].to_dict("records") if len(res) else []})
        browser.close()

    if REF:
        for got, ref in (("quickbite_scoring_template.csv", "template.csv"),
                         ("mixed_valid_and_invalid_scored.csv", "scored_mixed_valid_and_invalid.csv"),
                         ("under18_only_scored.csv", "scored_under18_only.csv")):
            a, b = downloads / got, REF / ref
            same = a.exists() and b.exists() and a.read_bytes() == b.read_bytes()
            check("reference", f"Browser download {got} byte-identical to the reference ({REF.name}/{ref})", same,
                  {"bytes_now": a.stat().st_size if a.exists() else None, "bytes_reference": b.stat().st_size if b.exists() else None})
        meta["reference"] = str(REF.relative_to(ROOT)) if REF.is_relative_to(ROOT) else str(REF)

    summary = {"PASS": sum(r["result"] == "PASS" for r in results), "FAIL": sum(r["result"] == "FAIL" for r in results)}
    verdict = "PASS" if summary["FAIL"] == 0 and summary["PASS"] > 0 else "FAIL"
    (OUT / "browser_upload_test_results.json").write_text(json.dumps(
        {"verdict": verdict, "summary": summary, **meta,
         "scope": "Automated, browser-level: real 'Browse files' click and browser file chooser (answered by Playwright, as a headless "
                  "browser draws no operating-system dialog), real upload, scoring, rendering and browser download. Not a human, "
                  "on-screen manual test.",
         "observations": ["In the scored file, a cell that could not be read as a number is written back empty (the app converts "
                          "the required columns to numbers before scoring), so the original text (e.g. 'abc') is not echoed; the row "
                          "itself is kept and flagged 'Not scored — missing / non-numeric value'. Existing behaviour, not changed."],
         "checks": results}, indent=1, ensure_ascii=False, default=str))
    print(json.dumps({"verdict": verdict, **summary}))
    return verdict == "PASS"


if __name__ == "__main__":
    sys.exit(0 if main() else 1)
