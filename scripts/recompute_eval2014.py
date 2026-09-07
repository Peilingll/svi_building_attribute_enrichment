"""Recompute every thesis-referenced result on the 2,014-building evaluation set.

Nothing is retrained or re-inferred. Each step filters the existing hold-out
prediction files to data/processed/evaluation_pand_ids.parquet and writes new
outputs with the suffix `_eval2014`; the published files are left untouched.

Steps (run all, or pick with --steps a,b,...):
  check     reproduce the published Stage 1 headline numbers on the full hold-out
  stage1    T3 model comparison + R^2 + per-model metrics JSON      (tab:upstream_attributes)
  joint     T4 joint cell table via src.stage1.joint_cell_eval       (tab:joint_cell)
  htr       T7 h_tr instrument via src.stage3.htr_instrument         (tab:htr_metrics, tab:wwr_sensitivity)
  stage3    T3 main tables, 7-class and binary, via src.stage3.run_stage3 (tab:binary/sevenclass_conditions)
  m2        direct-image (M2) metrics re-evaluated on the same buildings
  random    analytic uniform-random expectations                     (first row of the Stage 3 tables)
  prf       binary per-class precision/recall/F1 + h_tr R^2          (tab:binary_perclass, tab:htr_metrics R^2)
  figures   F4_2 type confusion, F4_3 cell recall, F4_3 pred-vs-true, period Sankey
  bycity    evaluation-set composition by study area

Run:  .venv/Scripts/python.exe scripts/recompute_eval2014.py [--steps stage1,joint]
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

import numpy as np
import pandas as pd

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO))
sys.path.insert(0, str(REPO / "scripts"))

from src.stage1.evaluate import evaluate_predictions  # noqa: E402
from src.stage2.metrics import evaluate as stage3_evaluate  # noqa: E402
from src.stage3.htr_instrument import MODELS as HTR_MODELS, WWR_MAIN, h_tr, load_geometry  # noqa: E402
from src.tabula_matcher import classify_period  # noqa: E402
from compute_binary_prf_htr_r2 import BINARY_METRICS, macro_prf  # noqa: E402
from compute_random_baseline import binary as rb_binary, merge_epc, seven_class as rb_seven  # noqa: E402
from compute_stage1_r2 import r2 as r2_fn  # noqa: E402

PY = sys.executable
SFX = "_eval2014"
EVAL = REPO / "data/processed/evaluation_pand_ids.parquet"
PROCESSED = REPO / "data/processed"
STAGE1 = {
    "dinov2_frozen": ("DINOv2 frozen", "reports/stage1/dinov2_frozen/holdout_preds.parquet"),
    "resnet50_ft": ("ResNet-50 ft", "reports/stage1/resnet50_ft/holdout_preds.parquet"),
    "vlm_internvl3_v3": ("InternVL3 (ZS)", "reports/stage1/vlm_internvl3/v3_holdout_per_pand_id.parquet"),
}
M2_RUNS = {  # name -> (preds file, task)
    "M2-DINOv2": ("M2-DINOv2_holdout_preds.parquet", "7class"),
    "M2-ResNet50": ("M2-ResNet50_holdout_preds.parquet", "7class"),
    "M2-VLM": ("M2-VLM_holdout_preds.parquet", "7class"),
    "M2-DINOv2_binary": ("M2-DINOv2_binary_holdout_preds.parquet", "binary"),
    "M2-ResNet50_binary": ("M2-ResNet50_binary_holdout_preds.parquet", "binary"),
    "M2-VLM-binprompt_binary": ("M2-VLM-binprompt_binary_holdout_preds.parquet", "binary"),
}


def eval_ids() -> set[str]:
    return set(pd.read_parquet(EVAL)["pand_id"].astype(str).str.zfill(16))


def load_preds(path: str, ids: set[str] | None) -> pd.DataFrame:
    df = pd.read_parquet(REPO / path)
    df["pand_id"] = df["pand_id"].astype(str).str.zfill(16)
    if ids is not None:
        df = df[df["pand_id"].isin(ids)]
    return df.reset_index(drop=True)


def run(cmd: list[str]) -> None:
    print("+", " ".join(cmd))
    subprocess.run(cmd, check=True, cwd=REPO)


# ---------------------------------------------------------------- stage 1
def stage1_metrics(ids: set[str] | None) -> dict:
    rng = np.random.default_rng(42)
    out = {}
    for key, (_, path) in STAGE1.items():
        df = load_preds(path, ids)
        rep = evaluate_predictions(df, with_ci=True)
        for target, (pc, tc) in {"year": ("pred_year", "true_bouwjaar"),
                                 "floors": ("pred_floors", "true_num_floors")}.items():
            sub = df[[pc, tc]].dropna()
            yt, yp = sub[tc].to_numpy(float), sub[pc].to_numpy(float)
            boots = []
            for _ in range(1000):
                idx = rng.integers(0, len(sub), len(sub))
                if np.ptp(yt[idx]) == 0:
                    continue
                boots.append(r2_fn(yt[idx], yp[idx]))
            lo, hi = np.percentile(boots, [2.5, 97.5])
            rep[f"{target}_r2"] = round(r2_fn(yt, yp), 4)
            rep[f"{target}_r2_ci95"] = [round(float(lo), 4), round(float(hi), 4)]
        out[key] = rep
    return out


def step_check() -> None:
    print("== reproduction check on the full hold-out (should match T3_model_comparison.md)")
    for key, rep in stage1_metrics(None).items():
        print(f"{STAGE1[key][0]:>16}  n={rep['n_eval']}  type_acc={rep['type_acc']}  "
              f"f1={rep['type_macro_f1']}  year_mae={rep['year_mae']}  period={rep['period_acc']}  "
              f"floors_mae={rep['floors_mae']}  year_r2={rep['year_r2']}  floors_r2={rep['floors_r2']}")


def step_stage1(ids: set[str]) -> None:
    reps = stage1_metrics(ids)
    lines = ["| model | n | type_acc | type_macro_f1 | year_mae | year_r2 | period_acc | floors_mae | floors_r2 |",
             "| --- | ---: | --- | --- | --- | --- | --- | --- | --- |"]
    r2json = {"n_boot": 1000, "seed": 42, "models": {}}
    for key, rep in reps.items():
        name, path = STAGE1[key]
        (REPO / Path(path).parent / f"holdout_metrics{SFX}.json").write_text(
            json.dumps(rep, indent=2), encoding="utf-8")
        lines.append(f"| {name} | {rep['n_eval']} | {rep['type_acc']:.4f} | {rep['type_macro_f1']:.4f} | "
                     f"{rep['year_mae']:.4f} | {rep['year_r2']:.4f} | {rep['period_acc']:.4f} | "
                     f"{rep['floors_mae']:.4f} | {rep['floors_r2']:.4f} |")
        r2json["models"][key] = {t: {"n_eval": rep["n_eval"], "r2": rep[f"{t}_r2"],
                                     "r2_ci95": rep[f"{t}_r2_ci95"]} for t in ("year", "floors")}
    out = REPO / "reports/tables/stage1" / f"T3_model_comparison{SFX}.md"
    out.write_text("\n".join(lines) + "\n", encoding="utf-8")
    (REPO / "reports/stage1" / f"r2_holdout{SFX}.json").write_text(json.dumps(r2json, indent=2), encoding="utf-8")
    print("\n".join(lines))


# ---------------------------------------------------------------- subprocess steps
def step_joint() -> None:
    run([PY, "-m", "src.stage1.joint_cell_eval", "--restrict", str(EVAL),
         "--out", str(REPO / "reports/tables/stage1" / f"T4_joint_cell{SFX}.md")])


def step_htr() -> None:
    run([PY, "-m", "src.stage3.htr_instrument", "--restrict", str(EVAL),
         "--out", str(REPO / "reports/tables/stage3" / f"T7_htr_instrument{SFX}.md")])


def step_stage3() -> None:
    for task in ("7class", "binary"):
        run([PY, "-m", "src.stage3.run_stage3", "--task", task, "--holdout", str(EVAL),
             "--out-suffix", SFX])


def step_figures() -> None:
    for script in ("fig_ch4_2_type_confusion.py", "fig_ch4_3_cell_recall_heatmap.py",
                   "fig_ch4_4_pred_vs_true_r2.py", "fig_ch4_3_period_sankey.py"):
        run([PY, str(REPO / "scripts" / script), "--restrict", str(EVAL), "--suffix", SFX])


# ---------------------------------------------------------------- M2, random, prf
def step_m2(ids: set[str]) -> None:
    for name, (fname, task) in M2_RUNS.items():
        df = load_preds(f"reports/stage3/{fname}", ids).sort_values("pand_id").reset_index(drop=True)
        proba = df["proba"] if "proba" in df.columns else None
        rep = stage3_evaluate(df, with_ci=True, task=task, proba=proba)
        rep["route"] = name
        rep["n_eval_restricted"] = int(len(df))
        (REPO / "reports/stage3" / f"{name}{SFX}_metrics.json").write_text(
            json.dumps(rep, indent=2, ensure_ascii=False), encoding="utf-8")
        print(f"{name:>26}  n={len(df)}  macro_f1={rep['macro_f1']:.4f}  acc={rep['accuracy']:.4f}")


def step_random(ids: set[str]) -> None:
    pool = pd.read_parquet(PROCESSED / "stage1_gt.parquet")
    pool["pand_id"] = pool["pand_id"].astype(str).str.zfill(16)
    manifest = pd.read_parquet(PROCESSED / "svi_manifest.parquet")
    hold_ids = set(pd.read_parquet(PROCESSED / "holdout_test_pand_ids.parquet")["pand_id"].astype(str))
    sample = pool[pool["pand_id"].isin(set(manifest["pand_id"].astype(str)))].copy()
    sample["epc7"] = sample["Energieklasse"].map(merge_epc)
    sample["epc_bin"] = sample["epc7"].map(lambda c: "A-C" if c in ("A", "B", "C") else "D-G")
    dev = sample[~sample["pand_id"].isin(hold_ids)]
    rate = float((dev["epc_bin"] == "D-G").mean())
    ev = sample[sample["pand_id"].isin(ids)]
    out = {"evaluation_set": {"n": int(len(ev)), "seven_class": rb_seven(ev["epc7"]),
                              "binary": rb_binary(ev["epc_bin"], rate)},
           "rate_from_dev": round(rate, 4)}
    (REPO / "reports/stage2" / f"random_baseline{SFX}.json").write_text(json.dumps(out, indent=2), encoding="utf-8")
    print(json.dumps(out, indent=1))


def step_prf(ids: set[str]) -> None:
    out = {"binary_prf_at_0.5": {}, "htr_r2": {}}
    for route, fname in BINARY_METRICS.items():
        m = json.load(open(REPO / "reports/stage3" / fname.replace("_metrics.json", f"{SFX}_metrics.json")))
        out["binary_prf_at_0.5"][route] = macro_prf(m)
    m1 = json.load(open(REPO / "reports/stage3" / f"M1_binary{SFX}_metrics.json"))
    supp = {k: v["support"] for k, v in m1["per_class"].items()}
    n = sum(supp.values())
    p = {k: v / n for k, v in supp.items()}
    f1 = lambda pr, rc: 0.0 if pr + rc == 0 else 2 * pr * rc / (pr + rc)  # noqa: E731
    out["binary_prf_at_0.5"]["M0-random"] = {
        "macro_precision": round(sum(p.values()) / len(p), 4), "macro_recall": 0.5,
        "macro_f1": round(sum(f1(p[k], 0.5) for k in p) / len(p), 4), "n_eval": n,
        "support": supp}
    tab = pd.read_csv(PROCESSED / "tabula_nl.csv")
    tab["key"] = tab["building_type"] + "|" + tab["period"]
    U = tab.set_index("key")[["u_wall", "u_roof", "u_floor", "u_window"]]
    geo = load_geometry()
    for name, path in HTR_MODELS.items():
        d = load_preds(path, ids).merge(geo, on="pand_id", how="inner")
        d = d.dropna(subset=["true_bouwjaar", "pred_year", "true_type", "pred_type"])
        cg = d["true_type"].astype(str) + "|" + pd.Series([classify_period(int(y)) for y in d["true_bouwjaar"]], index=d.index)
        cp = d["pred_type"].astype(str) + "|" + pd.Series([classify_period(int(round(y))) for y in d["pred_year"]], index=d.index)
        keep = cg.isin(U.index) & cp.isin(U.index)
        d, cg, cp = d[keep], cg[keep], cp[keep]
        hg, hp = h_tr(cg.to_numpy(), d, U, WWR_MAIN), h_tr(cp.to_numpy(), d, U, WWR_MAIN)
        m = np.isfinite(hg) & np.isfinite(hp)
        hg, hp = hg[m], hp[m]
        out["htr_r2"][name] = {"n": int(m.sum()),
                               "r2": round(1 - float(np.sum((hp - hg) ** 2)) / float(np.sum((hg - hg.mean()) ** 2)), 4),
                               "mae_check": round(float(np.abs(hp - hg).mean()), 4)}
    (REPO / "reports/stage3" / f"binary_prf_htr_r2{SFX}.json").write_text(json.dumps(out, indent=2), encoding="utf-8")
    print(json.dumps(out, indent=1))


def step_bycity(ids: set[str]) -> None:
    ev = pd.read_parquet(EVAL)
    man = pd.read_parquet(PROCESSED / "svi_manifest.parquet")
    man = man[man["pand_id"].isin(ids)]
    t = ev.groupby("city").size().rename("buildings").to_frame()
    t["images"] = man.groupby("city").size()
    t.loc["TOTAL"] = t.sum()
    md = ["| city | evaluation_buildings | evaluation_images |", "| --- | ---: | ---: |"]
    md += [f"| {c} | {int(r.buildings)} | {int(r.images)} |" for c, r in t.iterrows()]
    (REPO / "reports/tables/stage1" / f"T1_evaluation_set_by_city{SFX}.md").write_text("\n".join(md) + "\n", encoding="utf-8")
    print("\n".join(md))


STEPS = ["check", "stage1", "joint", "htr", "stage3", "m2", "random", "prf", "figures", "bycity"]


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--steps", default=",".join(STEPS))
    args = ap.parse_args()
    ids = eval_ids()
    print(f"evaluation set: {len(ids)} buildings")
    for s in [x.strip() for x in args.steps.split(",") if x.strip()]:
        print(f"\n##### {s}")
        {"check": step_check, "stage1": lambda: step_stage1(ids), "joint": step_joint, "htr": step_htr,
         "stage3": step_stage3, "m2": lambda: step_m2(ids), "random": lambda: step_random(ids),
         "prf": lambda: step_prf(ids), "figures": step_figures, "bycity": lambda: step_bycity(ids)}[s]()


if __name__ == "__main__":
    main()
