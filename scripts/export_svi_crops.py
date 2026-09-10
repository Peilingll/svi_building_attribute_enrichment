"""Stage the street-view crops referenced by the manifest under data/svi/<city>/.

Copies every crop listed in data/processed/svi_manifest.parquet into
data/svi/<city>/<file>.png and rewrites the manifest's file_path column to that
repo-relative path. Crops already present are not copied again, so the script
is safe to rerun. Use it once to migrate a manifest that still carries absolute
OpenFACADES paths, or to rebuild data/svi/ from the OpenFACADES output tree.

Run:  uv run python scripts/export_svi_crops.py [--manifest PATH] [--dry-run]
"""
from __future__ import annotations

import argparse
import logging
import sys
from pathlib import Path

import pandas as pd

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO))
from src.config import resolve_path  # noqa: E402
from src.svi_manifest import stage_crops  # noqa: E402


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--manifest", type=Path, default=REPO / "data/processed/svi_manifest.parquet")
    ap.add_argument("--dry-run", action="store_true", help="report only; copy nothing, write nothing")
    args = ap.parse_args()
    logging.basicConfig(level=logging.INFO, format="%(message)s")

    manifest = pd.read_parquet(args.manifest)
    if args.dry_run:
        uniq = manifest.drop_duplicates("file_path")
        print(f"{len(manifest):,} rows, {len(uniq):,} unique files")
        print(uniq.groupby("city")["file_path"].size().to_string())
        return

    staged = stage_crops(manifest)
    missing = [p for p in staged["file_path"].unique() if not resolve_path(p).exists()]
    if missing:
        raise SystemExit(f"{len(missing)} staged paths do not resolve, e.g. {missing[0]}")
    staged.to_parquet(args.manifest, index=False)

    uniq = staged.drop_duplicates("file_path")
    size_mb = sum(resolve_path(p).stat().st_size for p in uniq["file_path"]) / 1e6
    print(f"wrote {args.manifest.relative_to(REPO)}: {len(staged):,} rows, "
          f"{len(uniq):,} unique crops, {size_mb:,.0f} MB under data/svi/")
    print(uniq.groupby("city")["file_path"].size().to_string())


if __name__ == "__main__":
    main()
