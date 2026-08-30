#!/usr/bin/env python3
"""Executable numerical audit for the cold-seep area reanalysis.

This script addresses only the numerical lineage described in the manuscript.
It reconstructs the mature-seep Fe-OC summary from Ye et al.'s public
OSF source tables, checks the cold-seep-area arithmetic, recovers the published
stock endpoints under the stock identity, and changes only the disputed lower
area endpoint.

The value 1.65 g cm-3 is labelled *implicit*: it is the simple two-decimal bulk
density that reproduces both rounded stock endpoints when combined with Ye's
explicit area, depth, and independently reconstructed 0.14% Fe-OC mean.  It is
not treated here as a parameter explicitly reported by Ye et al.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
import statistics
from decimal import Decimal, getcontext
from pathlib import Path
from typing import Iterable


getcontext().prec = 28

REPO_ROOT = Path(__file__).resolve().parents[1]
TABLE_S4 = REPO_ROOT / "data" / "ye_osf_extracted" / "ye_osf_table_04.csv"
TABLE_S7 = REPO_ROOT / "data" / "ye_osf_extracted" / "ye_osf_table_06.csv"
DEFAULT_OUTPUT = REPO_ROOT / "evidence" / "calculation_outputs.json"


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def _clean_key(key: str) -> str:
    return " ".join(key.replace("\ufeff", "").split())


def _rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        return [
            {_clean_key(key): value.strip() for key, value in row.items()}
            for row in reader
        ]


def _decimal_values(rows: Iterable[dict[str, str]], column: str) -> list[Decimal]:
    return [Decimal(row[column]) for row in rows]


def _summary(values: list[Decimal]) -> dict[str, object]:
    floats = [float(value) for value in values]
    return {
        "n": len(values),
        "values_percent": [str(value) for value in values],
        "sum_percent": str(sum(values, Decimal("0"))),
        "mean_percent": str(sum(values, Decimal("0")) / Decimal(len(values))),
        "sample_sd_percent": format(statistics.stdev(floats), ".15g"),
    }


def stock_tg(
    area_km2: Decimal,
    depth_m: Decimal,
    dry_bulk_density_g_cm3: Decimal,
    feoc_percent: Decimal,
) -> Decimal:
    """Return carbon stock in Tg using a dimensionally explicit identity.

    area[km2] * 1e10[cm2/km2] * depth[m] * 100[cm/m]
      * density[g/cm3] * FeOC[%]/100 * 1e-12[Tg/g]

    The powers of ten reduce to the compact expression below.
    """

    return area_km2 * depth_m * dry_bulk_density_g_cm3 * feoc_percent / Decimal(
        "100"
    )


def implied_density_g_cm3(
    reported_stock_tg: Decimal,
    area_km2: Decimal,
    depth_m: Decimal,
    feoc_percent: Decimal,
) -> Decimal:
    return (
        reported_stock_tg
        * Decimal("100")
        / (area_km2 * depth_m * feoc_percent)
    )


def density_interval_for_integer_rounding(
    displayed_stock_tg: Decimal,
    area_km2: Decimal,
    depth_m: Decimal,
    feoc_percent: Decimal,
) -> tuple[Decimal, Decimal]:
    """Density interval whose exact stock rounds to the displayed integer.

    The interval is half-open under ordinary nearest-integer rounding.  It is
    used only to test compatibility with the whole-Tg values printed by Ye;
    it does not turn the unstated density into a reported parameter.
    """

    half = Decimal("0.5")
    return (
        implied_density_g_cm3(
            displayed_stock_tg - half, area_km2, depth_m, feoc_percent
        ),
        implied_density_g_cm3(
            displayed_stock_tg + half, area_km2, depth_m, feoc_percent
        ),
    )


def calculate() -> dict[str, object]:
    s4_rows = _rows(TABLE_S4)
    s7_rows = _rows(TABLE_S7)

    current_rows = [row for row in s4_rows if row["Group"].startswith("Mature seep")]
    historical_rows = [row for row in s7_rows if row["Group"] == "Mature Cold Seep"]
    current_values = _decimal_values(current_rows, "FeOC (%)")
    historical_values = _decimal_values(historical_rows, "FeOC (%)")
    combined_values = current_values + historical_values
    all_current_seep_rows = [
        row
        for row in s4_rows
        if row["Group"].startswith(("Early-stage seep", "Mature seep"))
    ]
    all_seep_values = (
        _decimal_values(all_current_seep_rows, "FeOC (%)") + historical_values
    )

    slope_area_km2 = Decimal("41000000")
    occupancy_percent = Decimal("0.05")
    occupancy_fraction = occupancy_percent / Decimal("100")
    arithmetical_area_km2 = slope_area_km2 * occupancy_fraction
    published_lower_area_km2 = Decimal("205000")
    corrected_lower_area_km2 = Decimal("20500")
    upper_area_km2 = Decimal("315000")

    depth_m = Decimal("0.30")
    reconstructed_feoc_percent = sum(combined_values) / Decimal(len(combined_values))
    implicit_density = Decimal("1.65")
    lower_stock = stock_tg(
        published_lower_area_km2,
        depth_m,
        implicit_density,
        reconstructed_feoc_percent,
    )
    upper_stock = stock_tg(
        upper_area_km2,
        depth_m,
        implicit_density,
        reconstructed_feoc_percent,
    )
    corrected_lower_stock = stock_tg(
        corrected_lower_area_km2,
        depth_m,
        implicit_density,
        reconstructed_feoc_percent,
    )
    lower_density_interval = density_interval_for_integer_rounding(
        Decimal("142"),
        published_lower_area_km2,
        depth_m,
        reconstructed_feoc_percent,
    )
    upper_density_interval = density_interval_for_integer_rounding(
        Decimal("218"),
        upper_area_km2,
        depth_m,
        reconstructed_feoc_percent,
    )
    joint_density_interval = (
        max(lower_density_interval[0], upper_density_interval[0]),
        min(lower_density_interval[1], upper_density_interval[1]),
    )
    lower_area_coefficient_interval = (
        (Decimal("142") - Decimal("0.5")) / published_lower_area_km2,
        (Decimal("142") + Decimal("0.5")) / published_lower_area_km2,
    )
    upper_area_coefficient_interval = (
        (Decimal("218") - Decimal("0.5")) / upper_area_km2,
        (Decimal("218") + Decimal("0.5")) / upper_area_km2,
    )
    joint_area_coefficient_interval = (
        max(lower_area_coefficient_interval[0], upper_area_coefficient_interval[0]),
        min(lower_area_coefficient_interval[1], upper_area_coefficient_interval[1]),
    )
    density_free_corrected_lower_interval = (
        corrected_lower_area_km2 * joint_area_coefficient_interval[0],
        corrected_lower_area_km2 * joint_area_coefficient_interval[1],
    )

    return {
        "scope": "One numerical lineage only; no global-area reassessment.",
        "source_files": {
            "ye_table_s4_csv": {
                "path": TABLE_S4.relative_to(REPO_ROOT).as_posix(),
                "sha256": _sha256(TABLE_S4),
            },
            "ye_table_s7_csv": {
                "path": TABLE_S7.relative_to(REPO_ROOT).as_posix(),
                "sha256": _sha256(TABLE_S7),
            },
        },
        "ye_mature_feoc_reconstruction": {
            "current_study_table_s4": _summary(current_values),
            "historical_table_s7": _summary(historical_values),
            "combined": _summary(combined_values),
            "all_seep_cross_check": _summary(all_seep_values),
            "reported_rounding_check": {
                "current_mean_sd_percent_2dp": (
                    f"{statistics.mean(map(float, current_values)):.2f} +/- "
                    f"{statistics.stdev(map(float, current_values)):.2f}"
                ),
                "combined_mean_sd_percent_2dp": (
                    f"{statistics.mean(map(float, combined_values)):.2f} +/- "
                    f"{statistics.stdev(map(float, combined_values)):.2f}"
                ),
                "all_seep_mean_sd_percent_2dp": (
                    f"{statistics.mean(map(float, all_seep_values)):.2f} +/- "
                    f"{statistics.stdev(map(float, all_seep_values)):.2f}"
                ),
            },
        },
        "area_arithmetic": {
            "continental_slope_area_km2": str(slope_area_km2),
            "occupation_percent": str(occupancy_percent),
            "occupation_fraction": str(occupancy_fraction),
            "product_km2": str(arithmetical_area_km2),
            "scientific_notation": "2.05e4 km2",
            "jiang_published_lower_km2": str(published_lower_area_km2),
            "published_to_arithmetic_ratio": str(
                published_lower_area_km2 / arithmetical_area_km2
            ),
            "inputs_required_to_generate_published_lower": {
                "occupation_percent_if_area_stays_41_million_km2": str(
                    published_lower_area_km2 / slope_area_km2 * Decimal("100")
                ),
                "slope_area_km2_if_occupation_stays_0.05_percent": str(
                    published_lower_area_km2 / occupancy_fraction
                ),
                "unreported_multiplier": str(
                    published_lower_area_km2 / arithmetical_area_km2
                ),
            },
            "unit_round_trips_for_correct_product": {
                "square_metres": str(arithmetical_area_km2 * Decimal("1000000")),
                "hectares": str(arithmetical_area_km2 * Decimal("100")),
                "square_nautical_miles": str(
                    arithmetical_area_km2 / (Decimal("1.852") ** 2)
                ),
            },
        },
        "ye_stock_reconstruction": {
            "identity": (
                "stock_Tg = area_km2 * depth_m * dry_bulk_density_g_cm3 "
                "* FeOC_percent / 100"
            ),
            "explicit_or_data_reconstructed_inputs": {
                "published_lower_area_km2": str(published_lower_area_km2),
                "published_upper_area_km2": str(upper_area_km2),
                "depth_m": str(depth_m),
                "combined_mature_FeOC_percent": str(reconstructed_feoc_percent),
            },
            "implicit_input_not_located_in_article_si_or_osf": {
                "dry_bulk_density_g_cm3": str(implicit_density),
                "basis": (
                    "simple two-decimal value that recovers both published "
                    "whole-Tg endpoints from the explicit/data-derived inputs"
                ),
            },
            "computed": {
                "reconstruction_with_implicit_1p65_lower_Tg": str(lower_stock),
                "reconstruction_with_implicit_1p65_lower_rounded_Tg": str(
                    round(lower_stock)
                ),
                "reconstruction_with_implicit_1p65_upper_Tg": str(upper_stock),
                "reconstruction_with_implicit_1p65_upper_rounded_Tg": str(
                    round(upper_stock)
                ),
                "corrected_reconstruction_with_implicit_1p65_lower_Tg": str(
                    corrected_lower_stock
                ),
                "corrected_reconstruction_with_implicit_1p65_lower_1dp_Tg": (
                    f"{float(corrected_lower_stock):.1f}"
                ),
                "lower_stock_ratio_published_to_corrected": str(
                    lower_stock / corrected_lower_stock
                ),
            },
            "density_implied_by_rounded_endpoints_separately": {
                "from_142_Tg": str(
                    implied_density_g_cm3(
                        Decimal("142"),
                        published_lower_area_km2,
                        depth_m,
                        reconstructed_feoc_percent,
                    )
                ),
                "from_218_Tg": str(
                    implied_density_g_cm3(
                        Decimal("218"),
                        upper_area_km2,
                        depth_m,
                        reconstructed_feoc_percent,
                    )
                ),
            },
            "density_intervals_that_round_to_each_endpoint": {
                "from_142_Tg_lower_inclusive_upper_exclusive": [
                    str(lower_density_interval[0]),
                    str(lower_density_interval[1]),
                ],
                "from_218_Tg_lower_inclusive_upper_exclusive": [
                    str(upper_density_interval[0]),
                    str(upper_density_interval[1]),
                ],
                "joint_interval_lower_inclusive_upper_exclusive": [
                    str(joint_density_interval[0]),
                    str(joint_density_interval[1]),
                ],
                "implicit_1.65_is_inside_joint_interval": (
                    joint_density_interval[0]
                    <= implicit_density
                    < joint_density_interval[1]
                ),
            },
            "density_free_area_linear_rounding_audit": {
                "joint_area_coefficient_Tg_per_km2_lower_inclusive_upper_exclusive": [
                    str(joint_area_coefficient_interval[0]),
                    str(joint_area_coefficient_interval[1]),
                ],
                "corrected_lower_Tg_lower_inclusive_upper_exclusive": [
                    str(density_free_corrected_lower_interval[0]),
                    str(density_free_corrected_lower_interval[1]),
                ],
                "interpretation": (
                    "Every common area-linear coefficient consistent with both published "
                    "whole-Tg endpoints gives about 14.2 Tg after changing only the lower "
                    "area to 20,500 km2; this does not identify the hidden physical coefficient."
                ),
            },
        },
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--write",
        action="store_true",
        help=f"write the JSON result to {DEFAULT_OUTPUT}",
    )
    args = parser.parse_args()
    result = calculate()
    rendered = json.dumps(result, indent=2, ensure_ascii=False) + "\n"
    if args.write:
        DEFAULT_OUTPUT.parent.mkdir(parents=True, exist_ok=True)
        DEFAULT_OUTPUT.write_text(rendered, encoding="utf-8")
    print(rendered, end="")


if __name__ == "__main__":
    main()
