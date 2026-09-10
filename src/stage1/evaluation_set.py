"""Define the evaluation set used for holdout performance comparisons.

The fixed holdout set (data/processed/holdout_test_pand_ids.parquet, n = 2,018)
is the predefined partition. Four holdout buildings cannot be evaluated under
every condition:

  * buildings without a valid InternVL3-2B building-level record
    (pred_type, pred_year or pred_floors missing), and
  * buildings without valid 3DBAG reconstructed areas as required by the
    h_tr calculation (src/stage3/htr_instrument.load_geometry).

The evaluation set is the holdout set minus the union of these two groups.
Every holdout performance comparison in the thesis reports metrics on this set
so that all configurations are compared on identical buildings. Dataset checks
and development-set analyses retain their own stated denominators.

Outputs
  data/processed/evaluation_pand_ids.parquet        one row per evaluated building
  data/processed/evaluation_pand_ids.checksum.txt   sha256 prefix, counts, excluded ids

Run:  uv run python -m src.stage1.evaluation_set
"""
from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO))
from src.stage1.splits import compute_checksum  # noqa: E402
from src.stage3.htr_instrument import load_geometry  # noqa: E402

PROCESSED = REPO / "data" / "processed"
HOLDOUT = PROCESSED / "holdout_test_pand_ids.parquet"
VLM = REPO / "reports" / "stage1" / "vlm_internvl3" / "v3_holdout_per_pand_id.parquet"
OUT = PROCESSED / "evaluation_pand_ids.parquet"
OUT_CHECKSUM = PROCESSED / "evaluation_pand_ids.checksum.txt"


def main() -> None:
    ho = pd.read_parquet(HOLDOUT)
    ho["pand_id"] = ho["pand_id"].astype(str).str.zfill(16)
    n_holdout = len(ho)

    vlm = pd.read_parquet(VLM)
    vlm["pand_id"] = vlm["pand_id"].astype(str).str.zfill(16)
    vlm = vlm[vlm["pand_id"].isin(ho["pand_id"])]
    bad_vlm = vlm.loc[vlm[["pred_type", "pred_year", "pred_floors"]].isna().any(axis=1), "pand_id"]
    missing_vlm = set(ho["pand_id"]) - set(vlm["pand_id"])
    no_vlm = sorted(set(bad_vlm) | missing_vlm)

    geo_ids = set(load_geometry()["pand_id"])
    no_geo = sorted(set(ho["pand_id"]) - geo_ids)

    overlap = sorted(set(no_vlm) & set(no_geo))
    excluded = sorted(set(no_vlm) | set(no_geo))

    ev = ho[~ho["pand_id"].isin(excluded)].copy()
    ev["split"] = "evaluation"
    ev = ev.sort_values("pand_id").reset_index(drop=True)
    ev.to_parquet(OUT, index=False)

    checksum = compute_checksum(ev["pand_id"].tolist())
    lines = [
        f"sha256_prefix: {checksum}",
        f"n_buildings:   {len(ev)}",
        f"n_holdout:     {n_holdout}",
        f"n_excluded:    {len(excluded)}",
        "derived_from:  data/processed/holdout_test_pand_ids.parquet",
        "created_with:  src/stage1/evaluation_set.py",
        "",
        "excluded_no_valid_internvl3_record:",
        *[f"  {p}" for p in no_vlm],
        "excluded_no_valid_3dbag_areas:",
        *[f"  {p}" for p in no_geo],
        f"excluded_both: {overlap if overlap else 'none'}",
        "",
    ]
    OUT_CHECKSUM.write_text("\n".join(lines), encoding="utf-8")

    print(f"holdout {n_holdout} -> evaluation {len(ev)} (excluded {len(excluded)})")
    print("no valid InternVL3-2B record:", no_vlm)
    print("no valid 3DBAG areas:        ", no_geo)
    print("overlap:", overlap or "none")
    print("sha256 prefix:", checksum)


if __name__ == "__main__":
    main()
