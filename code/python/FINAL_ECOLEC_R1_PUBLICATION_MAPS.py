#!/usr/bin/env python3
"""
Publication cartography companion for ECOLEC-D-26-03083 Revision 1.

IMPORTANT
---------
This script performs NO econometric estimation and NO scenario/backcast
calculation. It only redraws four thematic maps from county values frozen by
Stata in the final Stata .dta (preferred) or publication_map_values.csv (fallback).

Maps produced
-------------
Figure 1  corn-ethanol transition exposure, 2022
Figure 3  predicted 2030 transition pressure
Figure 4  county classification against the 20% diagnostic corn-share threshold
Figure 7  residual corn-share gap after differential-channel removal, with exact zero separated

Geometry
--------
Official 2023 Census Cartographic Boundary counties, 1:500,000, supplied in
cb_2023_midwest_counties_500k.zip. County results are merged to geometry by FIPS.

Author: Elvis Kwame Ofori
Revision cartography: 2026-09
"""

from __future__ import annotations

import argparse
import shutil
import sys
import zipfile
from pathlib import Path


def _dependency_error(exc: Exception) -> None:
    msg = f"""
Required Python mapping packages are missing.

Install once with:
    python -m pip install pandas geopandas matplotlib shapely pyogrio

Then rerun this script.

Original import error: {exc}
"""
    raise SystemExit(msg)


try:
    import numpy as np
    import pandas as pd
    import geopandas as gpd
    import matplotlib.pyplot as plt
    from matplotlib.colors import BoundaryNorm, ListedColormap
    from matplotlib.patches import Patch
except Exception as exc:  # pragma: no cover
    _dependency_error(exc)


DEFAULT_ROOT = Path(r"C:\Users\23108811\Documents\EthanolCorn_Data")
# Frozen Stata run used for the revision. Python reads analytical values directly
# from this run's final_county_outputs_for_maps_and_tables.dta.
DEFAULT_RUN_DIR = Path(r"C:\Users\23108811\Documents\EthanolCorn_Data\R1_OHIO_CORRECTED_corn_ethanol__3_Sep_2026_123259")
RUN_PREFIX = "R1_OHIO_CORRECTED_corn_ethanol_"
CB_ZIP = "cb_2023_midwest_counties_500k.zip"

# Final publication palette. Values are intentionally fixed so all four maps
# are visually consistent across reruns. Analytical class definitions remain
# entirely determined by Stata.
MISSING_COLOR = "#9e9e9e"
COUNTY_EDGE = "#ffffff"
STATE_EDGE = "#4d4d4d"

FIG4_COLORS = {
    1: "#f2f2f2",  # already at/below threshold
    2: "#fee8c8",  # crosses under 25%
    3: "#fdbb84",  # crosses under 50%
    4: "#e34a33",  # crosses only under full differential removal
    5: "#990000",  # remains above threshold
}
FIG4_LABELS = {
    1: "Already at or below 20%",
    2: "Crosses under 25% decline",
    3: "Crosses under 50% decline",
    4: "Crosses only under full removal",
    5: "Remains above threshold",
}


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Render publication-quality R1 county maps from frozen Stata outputs.")
    p.add_argument("--root", type=Path, default=DEFAULT_ROOT,
                   help="EthanolCorn_Data project folder.")
    p.add_argument("--run-dir", type=Path, default=DEFAULT_RUN_DIR,
                   help="Specific completed R1 run folder. Default is the frozen 3 Sep 2026 12:32:59 Stata run.")
    p.add_argument("--dpi", type=int, default=600,
                   help="PNG resolution. Default: 600 dpi.")

    # Jupyter/IPython launches the kernel with its own command-line arguments
    # such as: -f <kernel-connection-file.json>. argparse would normally reject
    # those arguments. parse_known_args() safely ignores only arguments that this
    # mapping script does not define, while still honoring --root, --run-dir and
    # --dpi when supplied. This makes the same file runnable from Command Prompt,
    # Anaconda Prompt, Spyder/Jupyter, or via %run.
    args, unknown = p.parse_known_args()
    if unknown and "ipykernel" not in sys.modules:
        print("Note: ignoring unrecognized arguments:", " ".join(unknown), file=sys.stderr)
    return args


def latest_run(root: Path) -> Path:
    candidates = [p for p in root.glob(f"{RUN_PREFIX}*") if p.is_dir()]
    if not candidates:
        raise FileNotFoundError(
            f"No completed run folder matching {RUN_PREFIX}* was found under {root}."
        )
    return max(candidates, key=lambda p: p.stat().st_mtime)


def load_values(run_dir: Path) -> pd.DataFrame:
    """Load frozen Stata map values without recalculating any analytical result.

    The final Stata .dta is authoritative and is preferred because it preserves
    the numeric backcast_class codes. The CSV is only a fallback for portability.
    Older CSV exports may contain Stata value-label text; those labels are mapped
    back to the original numeric codes before the hard QA checks are applied.
    """
    csv_path = run_dir / "publication_map_values.csv"
    dta_path = run_dir / "final_county_outputs_for_maps_and_tables.dta"

    keep = [
        "fips_code", "has_agdb_2022", "backcast_eligible",
        "state_name_shp", "county_name_shp", "risk_index_100",
        "scenario_pressure_2030_100", "backcast_class", "residual_gap_pp",
    ]

    # Prefer the authoritative frozen Stata dataset.
    if dta_path.exists():
        df = pd.read_stata(dta_path, convert_categoricals=False)
        missing_cols = [c for c in keep if c not in df.columns]
        if missing_cols:
            raise KeyError(f"Required frozen map variables missing from {dta_path.name}: {missing_cols}")
        df = df[keep].copy()
        source = dta_path.name
    elif csv_path.exists():
        df = pd.read_csv(csv_path)
        missing_cols = [c for c in keep if c not in df.columns]
        if missing_cols:
            raise KeyError(f"Required frozen map variables missing from {csv_path.name}: {missing_cols}")
        df = df[keep].copy()
        source = csv_path.name
    else:
        raise FileNotFoundError(
            f"Neither {dta_path.name} nor {csv_path.name} exists in {run_dir}. "
            "Run the final Stata master pipeline first."
        )

    # FIPS must remain a unique numeric county key.
    df["fips_code"] = pd.to_numeric(df["fips_code"], errors="coerce").astype("Int64")
    if df["fips_code"].isna().any():
        raise ValueError(f"Missing/non-numeric county FIPS found while reading {source}.")
    if df["fips_code"].duplicated().any():
        dup = df.loc[df["fips_code"].duplicated(), "fips_code"].tolist()[:10]
        raise ValueError(f"Duplicate county FIPS in frozen map values: {dup}")

    # Compatibility with older Stata CSV exports that wrote value labels rather
    # than numeric codes. This does not reclassify counties; it simply restores
    # the original Stata codes attached to those labels.
    if "backcast_class" in df.columns:
        bc_numeric = pd.to_numeric(df["backcast_class"], errors="coerce")
        if bc_numeric.notna().sum() == 0 and df["backcast_class"].notna().any():
            label_to_code = {
                "Already at or below threshold": 1,
                "Crosses under 25% decline": 2,
                "Crosses under 50% decline": 3,
                "Crosses only under full differential-channel removal": 4,
                "Crosses only under full removal": 4,
                "Remains above threshold": 5,
                "Nonpositive sensitivity": 6,
            }
            mapped = df["backcast_class"].astype("string").str.strip().map(label_to_code)
            unresolved = df.loc[df["backcast_class"].notna() & mapped.isna(), "backcast_class"].drop_duplicates().tolist()
            if unresolved:
                raise ValueError(f"Unrecognized backcast_class labels in {source}: {unresolved[:10]}")
            df["backcast_class"] = mapped.astype("Float64")
        else:
            df["backcast_class"] = bc_numeric

    print(f"Loaded frozen map values from: {source}")
    return df


def load_geometry(root: Path, out_dir: Path) -> gpd.GeoDataFrame:
    zip_path = root / CB_ZIP
    if not zip_path.exists():
        raise FileNotFoundError(f"Required Census cartographic boundary ZIP not found: {zip_path}")

    geom_dir = out_dir / "geometry_cb2023"
    geom_dir.mkdir(parents=True, exist_ok=True)
    shp = geom_dir / "cb_2023_midwest_counties_500k.shp"
    if not shp.exists():
        with zipfile.ZipFile(zip_path) as zf:
            zf.extractall(geom_dir)

    if not shp.exists():
        candidates = list(geom_dir.glob("*.shp"))
        if len(candidates) != 1:
            raise FileNotFoundError(f"Could not uniquely locate shapefile in {geom_dir}")
        shp = candidates[0]

    gdf = gpd.read_file(shp)
    if "GEOID" not in gdf.columns:
        raise KeyError("GEOID is missing from the Census cartographic boundary shapefile.")

    gdf["fips_code"] = pd.to_numeric(gdf["GEOID"], errors="raise").astype("Int64")
    if len(gdf) != 1055:
        raise AssertionError(f"Expected 1,055 counties in Midwest geometry, found {len(gdf)}.")
    if gdf["fips_code"].duplicated().any():
        raise AssertionError("Duplicate GEOID/FIPS values found in cartographic geometry.")

    return gdf


def prepare_map_data(gdf: gpd.GeoDataFrame, values: pd.DataFrame) -> gpd.GeoDataFrame:
    merged = gdf.merge(values, on="fips_code", how="left", validate="one_to_one")

    # Hard integrity checks against the frozen final R1 run.
    n_matched = int(pd.to_numeric(merged.get("has_agdb_2022"), errors="coerce").fillna(0).eq(1).sum())
    n_backcast = int(pd.to_numeric(merged.get("backcast_eligible"), errors="coerce").fillna(0).eq(1).sum())
    if n_matched != 1048:
        raise AssertionError(f"Expected 1,048 matched study counties, found {n_matched}.")
    if n_backcast != 990:
        raise AssertionError(f"Expected 990 backcast-eligible counties, found {n_backcast}.")

    bc = pd.to_numeric(merged["backcast_class"], errors="coerce")
    counts = {k: int((bc == k).sum()) for k in range(1, 6)}
    expected = {1: 439, 2: 14, 3: 17, 4: 37, 5: 483}
    if counts != expected:
        raise AssertionError(f"Backcast class counts changed. Expected {expected}, found {counts}.")

    return merged


def state_boundaries(gdf: gpd.GeoDataFrame) -> gpd.GeoDataFrame:
    state_col = "STATEFP" if "STATEFP" in gdf.columns else None
    if state_col is None:
        raise KeyError("STATEFP missing from cartographic geometry; cannot draw state outlines.")
    return gdf[[state_col, "geometry"]].dissolve(by=state_col)


def crop_limits(ax, gdf: gpd.GeoDataFrame) -> None:
    minx, miny, maxx, maxy = gdf.total_bounds
    padx = (maxx - minx) * 0.015
    pady = (maxy - miny) * 0.015
    ax.set_xlim(minx - padx, maxx + padx)
    ax.set_ylim(miny - pady, maxy + pady)
    ax.set_axis_off()
    ax.set_aspect("equal")


def save_figure(fig, out_base: Path, dpi: int) -> None:
    fig.savefig(out_base.with_suffix(".png"), dpi=dpi, bbox_inches="tight", facecolor="white")
    fig.savefig(out_base.with_suffix(".pdf"), bbox_inches="tight", facecolor="white")
    plt.close(fig)


def discrete_map(
    gdf: gpd.GeoDataFrame,
    states: gpd.GeoDataFrame,
    var: str,
    breaks: list[float],
    colors: list[str],
    labels: list[str],
    title: str,
    subtitle: str | None,
    legend_title: str,
    out_base: Path,
    dpi: int,
) -> None:
    vals = pd.to_numeric(gdf[var], errors="coerce")
    cmap = ListedColormap(colors)
    norm = BoundaryNorm(breaks, cmap.N, clip=True)

    fig, ax = plt.subplots(figsize=(11.5, 7.4))
    # Missing first, then observed counties, then state outlines.
    gdf.loc[vals.isna()].plot(ax=ax, color=MISSING_COLOR, edgecolor=COUNTY_EDGE, linewidth=0.18)
    gdf.loc[vals.notna()].assign(_v=vals[vals.notna()]).plot(
        ax=ax, column="_v", cmap=cmap, norm=norm, edgecolor=COUNTY_EDGE, linewidth=0.18
    )
    states.boundary.plot(ax=ax, color=STATE_EDGE, linewidth=0.72)

    crop_limits(ax, gdf)
    fig.suptitle(title, fontsize=18, y=0.965)
    if subtitle:
        ax.set_title(subtitle, fontsize=11.5, pad=6)

    handles = [Patch(facecolor=c, edgecolor="none", label=l) for c, l in zip(colors, labels)]
    handles.append(Patch(facecolor=MISSING_COLOR, edgecolor="none", label="No data"))
    leg = ax.legend(
        handles=handles,
        title=legend_title,
        loc="lower left",
        bbox_to_anchor=(0.01, 0.015),
        frameon=True,
        framealpha=0.96,
        facecolor="white",
        edgecolor="#d9d9d9",
        fontsize=9.5,
        title_fontsize=10.5,
        handlelength=1.3,
        handleheight=1.0,
        borderpad=0.7,
        labelspacing=0.35,
    )
    leg._legend_box.align = "left"
    fig.subplots_adjust(left=0.01, right=0.995, bottom=0.01, top=0.90)
    save_figure(fig, out_base, dpi)


def categorical_map(
    gdf: gpd.GeoDataFrame,
    states: gpd.GeoDataFrame,
    out_base: Path,
    dpi: int,
) -> None:
    cls = pd.to_numeric(gdf["backcast_class"], errors="coerce")
    fig, ax = plt.subplots(figsize=(11.5, 7.4))

    # No-data/ineligible first so it is visually distinct from class 1.
    gdf.loc[cls.isna()].plot(ax=ax, color=MISSING_COLOR, edgecolor=COUNTY_EDGE, linewidth=0.18)
    for k in [1, 2, 3, 4, 5]:
        gdf.loc[cls == k].plot(
            ax=ax, color=FIG4_COLORS[k], edgecolor=COUNTY_EDGE, linewidth=0.18
        )
    states.boundary.plot(ax=ax, color=STATE_EDGE, linewidth=0.72)

    crop_limits(ax, gdf)
    fig.suptitle("County classification under differential-channel removal", fontsize=17.5, y=0.965)
    ax.set_title("Diagnostic threshold: corn share at or below 20% of agricultural land", fontsize=11.5, pad=6)

    order = [5, 4, 3, 2, 1]
    handles = [Patch(facecolor=FIG4_COLORS[k], edgecolor="none", label=FIG4_LABELS[k]) for k in order]
    handles.append(Patch(facecolor=MISSING_COLOR, edgecolor="none", label="No data / not eligible"))
    leg = ax.legend(
        handles=handles,
        title="Classification",
        loc="lower left",
        bbox_to_anchor=(0.01, 0.015),
        frameon=True,
        framealpha=0.97,
        facecolor="white",
        edgecolor="#d9d9d9",
        fontsize=9.3,
        title_fontsize=10.5,
        handlelength=1.3,
        handleheight=1.0,
        borderpad=0.7,
        labelspacing=0.36,
    )
    leg._legend_box.align = "left"
    fig.subplots_adjust(left=0.01, right=0.995, bottom=0.01, top=0.90)
    save_figure(fig, out_base, dpi)


def residual_gap_map(
    gdf: gpd.GeoDataFrame,
    states: gpd.GeoDataFrame,
    out_base: Path,
    dpi: int,
) -> None:
    """Render Figure 7 with exact zero separated from positive residual gaps."""
    gap = pd.to_numeric(gdf["residual_gap_pp"], errors="coerce")

    # Publication classes. Exact zero is substantively distinct because it means
    # the county reaches the diagnostic threshold under the simulated removal.
    # Positive classes show the additional corn-share reduction still required.
    class_colors = {
        0: "#f7fbff",
        1: "#deebf7",
        2: "#9ecae1",
        3: "#6baed6",
        4: "#3182bd",
        5: "#08519c",
    }
    class_labels = {
        0: "No residual gap",
        1: ">0–5",
        2: ">5–10",
        3: ">10–15",
        4: ">15–25",
        5: ">25–45",
    }

    cls = pd.Series(pd.NA, index=gdf.index, dtype="Int64")
    cls.loc[gap.eq(0)] = 0
    cls.loc[gap.gt(0) & gap.le(5)] = 1
    cls.loc[gap.gt(5) & gap.le(10)] = 2
    cls.loc[gap.gt(10) & gap.le(15)] = 3
    cls.loc[gap.gt(15) & gap.le(25)] = 4
    cls.loc[gap.gt(25)] = 5

    fig, ax = plt.subplots(figsize=(11.5, 7.4))
    gdf.loc[gap.isna()].plot(
        ax=ax, color=MISSING_COLOR, edgecolor=COUNTY_EDGE, linewidth=0.18
    )
    for k in range(6):
        subset = gdf.loc[cls.eq(k).fillna(False)]
        if not subset.empty:
            subset.plot(
                ax=ax, color=class_colors[k], edgecolor=COUNTY_EDGE, linewidth=0.18
            )
    states.boundary.plot(ax=ax, color=STATE_EDGE, linewidth=0.72)

    crop_limits(ax, gdf)
    fig.suptitle(
        "Residual corn-share gap after differential-channel removal",
        fontsize=18,
        y=0.965,
    )
    ax.set_title(
        "Additional corn-share reduction beyond the estimated differential demand component",
        fontsize=11.5,
        pad=6,
    )

    handles = [
        Patch(facecolor=class_colors[k], edgecolor="none", label=class_labels[k])
        for k in range(6)
    ]
    handles.append(Patch(facecolor=MISSING_COLOR, edgecolor="none", label="No data / not eligible"))
    leg = ax.legend(
        handles=handles,
        title="Residual gap, pp",
        loc="lower left",
        bbox_to_anchor=(0.01, 0.015),
        frameon=True,
        framealpha=0.97,
        facecolor="white",
        edgecolor="#d9d9d9",
        fontsize=9.3,
        title_fontsize=10.5,
        handlelength=1.3,
        handleheight=1.0,
        borderpad=0.7,
        labelspacing=0.36,
    )
    leg._legend_box.align = "left"
    fig.subplots_adjust(left=0.01, right=0.995, bottom=0.01, top=0.90)
    save_figure(fig, out_base, dpi)


def copy_submission(publication_dir: Path, submission_dir: Path) -> None:
    submission_dir.mkdir(parents=True, exist_ok=True)
    stems = [
        "figure_01_exposure_index_2022",
        "figure_03_scenario_pressure_2030",
        "figure_04_threshold_classification_2035",
        "figure_07_residual_corn_share_gap",
    ]
    for stem in stems:
        for ext in [".png", ".pdf"]:
            src = publication_dir / f"{stem}{ext}"
            if src.exists():
                shutil.copy2(src, submission_dir / src.name)


def write_qa(run_dir: Path, out_dir: Path, merged: gpd.GeoDataFrame) -> None:
    bc = pd.to_numeric(merged["backcast_class"], errors="coerce")
    risk = pd.to_numeric(merged["risk_index_100"], errors="coerce")
    pressure = pd.to_numeric(merged["scenario_pressure_2030_100"], errors="coerce")
    gap = pd.to_numeric(merged["residual_gap_pp"], errors="coerce")

    lines = [
        "R1 publication map QA",
        "======================",
        f"Run directory: {run_dir}",
        f"Geometry counties: {len(merged)}",
        f"Matched study counties: {int(pd.to_numeric(merged['has_agdb_2022'], errors='coerce').fillna(0).eq(1).sum())}",
        f"Backcast eligible: {int(pd.to_numeric(merged['backcast_eligible'], errors='coerce').fillna(0).eq(1).sum())}",
        "Backcast classes:",
        f"  1 Already at/below threshold: {int((bc == 1).sum())}",
        f"  2 Crosses under 25% decline: {int((bc == 2).sum())}",
        f"  3 Crosses under 50% decline: {int((bc == 3).sum())}",
        f"  4 Crosses only under full removal: {int((bc == 4).sum())}",
        f"  5 Remains above threshold: {int((bc == 5).sum())}",
        f"Figure 1 observed values: {int(risk.notna().sum())}",
        f"Figure 3 observed values: {int(pressure.notna().sum())}",
        f"Figure 7 observed values: {int(gap.notna().sum())}",
        f"Figure 7 exact-zero residual gaps: {int(gap.eq(0).sum())}",
        f"Figure 7 positive residual gaps: {int(gap.gt(0).sum())}",
        "",
        "Python redraws frozen Stata values only. No analytical quantity is recalculated.",
        "Census 2023 Cartographic Boundary geometry is merged by county FIPS.",
    ]
    (out_dir / "publication_maps_QA.txt").write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    args = parse_args()
    root = args.root.expanduser().resolve()
    run_dir = args.run_dir.expanduser().resolve() if args.run_dir else DEFAULT_RUN_DIR.expanduser().resolve()

    if not run_dir.exists():
        raise FileNotFoundError(f"Run directory does not exist: {run_dir}")

    print(f"Using frozen Stata run: {run_dir}")
    print(f"Reading analytical map values from: {run_dir / 'final_county_outputs_for_maps_and_tables.dta'}")

    out_dir = run_dir / "publication_maps"
    out_dir.mkdir(parents=True, exist_ok=True)

    values = load_values(run_dir)
    geometry = load_geometry(root, out_dir)
    merged = prepare_map_data(geometry, values)
    states = state_boundaries(merged)

    reds = ["#fee5d9", "#fcae91", "#fb6a4a", "#de2d26", "#a50f15"]
    discrete_map(
        merged, states,
        var="risk_index_100",
        breaks=[0, 20, 40, 60, 80, 100.000001],
        colors=reds,
        labels=["0–20", "20–40", "40–60", "60–80", "80–100"],
        title="Corn-ethanol transition exposure, 2022",
        subtitle=None,
        legend_title="Exposure index",
        out_base=out_dir / "figure_01_exposure_index_2022",
        dpi=args.dpi,
    )

    discrete_map(
        merged, states,
        var="scenario_pressure_2030_100",
        breaks=[0, 20, 40, 60, 80, 100.000001],
        colors=reds,
        labels=["0–20", "20–40", "40–60", "60–80", "80–100"],
        title="Predicted 2030 transition pressure",
        subtitle="Managed decline: 25% reduction from the 2022 ethanol share",
        legend_title="Pressure index",
        out_base=out_dir / "figure_03_scenario_pressure_2030",
        dpi=args.dpi,
    )

    categorical_map(
        merged, states,
        out_base=out_dir / "figure_04_threshold_classification_2035",
        dpi=args.dpi,
    )

    residual_gap_map(
        merged, states,
        out_base=out_dir / "figure_07_residual_corn_share_gap",
        dpi=args.dpi,
    )

    copy_submission(out_dir, run_dir / "submission_ready")
    write_qa(run_dir, out_dir, merged)

    print("Publication maps complete")
    print(f"Run directory: {run_dir}")
    print(f"Publication maps: {out_dir}")
    print(f"Submission-ready copies: {run_dir / 'submission_ready'}")
    print("Frozen class counts verified: 439 / 14 / 17 / 37 / 483 (N=990)")


if __name__ == "__main__":
    main()
