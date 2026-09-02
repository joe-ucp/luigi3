#!/usr/bin/env python3
"""Executable numerical audit for the cold-seep area reanalysis.

This script addresses only the numerical lineage described in the manuscript.
It reconstructs the mature-seep Fe-OC summary from Ye et al.'s public
OSF source tables, checks the cold-seep-area arithmetic, recovers the published
stock endpoints under the stock identity, and changes only the disputed lower
area endpoint.

The value 1.65 g cm-3 is labelled an *endpoint-compatible effective sediment-
mass coefficient*: it is the simple two-decimal coefficient that reproduces
both rounded stock endpoints when combined with Ye's explicit area, depth, and
independently reconstructed 0.14% Fe-OC mean.  It is not treated here as a
parameter explicitly reported by Ye et al. or as an established dry bulk
density.
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
    sediment_mass_coefficient_g_cm3: Decimal,
    feoc_percent: Decimal,
) -> Decimal:
    """Return carbon stock in Tg using a dimensionally explicit identity.

    area[km2] * 1e10[cm2/km2] * depth[m] * 100[cm/m]
      * sediment mass coefficient[g/cm3] * FeOC[%]/100 * 1e-12[Tg/g]

    The powers of ten reduce to the compact expression below.

    In a fully specified dry-mass inventory, the coefficient is dry bulk
    density.  A coefficient inferred only by reversing rounded endpoints is
    algebraically equivalent but does not by itself establish that physical
    interpretation.
    """

    return (
        area_km2
        * depth_m
        * sediment_mass_coefficient_g_cm3
        * feoc_percent
        / Decimal("100")
    )


def implied_effective_sediment_mass_coefficient_g_cm3(
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


def implied_porosity_from_dry_bulk_density(
    dry_bulk_density_g_cm3: Decimal,
    grain_density_g_cm3: Decimal,
) -> Decimal:
    """Return porosity implied by a two-phase dry-density relation.

    This diagnostic assumes negligible dry pore mass and uses
    rho_d = rho_grain * (1 - porosity).  It is not a sediment model and does
    not establish that a density was actually used by the source authors.
    """

    return Decimal("1") - dry_bulk_density_g_cm3 / grain_density_g_cm3


def dry_bulk_density_from_porosity(
    grain_density_g_cm3: Decimal,
    porosity: Decimal,
) -> Decimal:
    """Return dry bulk density under the two-phase solid-volume relation."""

    return grain_density_g_cm3 * (Decimal("1") - porosity)


def saturated_bulk_density_from_porosity(
    grain_density_g_cm3: Decimal,
    porewater_density_g_cm3: Decimal,
    porosity: Decimal,
) -> Decimal:
    """Return saturated bulk density for solid and porewater volume fractions."""

    return dry_bulk_density_from_porosity(
        grain_density_g_cm3, porosity
    ) + porewater_density_g_cm3 * porosity


def effective_sediment_mass_coefficient_interval_for_integer_rounding(
    displayed_stock_tg: Decimal,
    area_km2: Decimal,
    depth_m: Decimal,
    feoc_percent: Decimal,
) -> tuple[Decimal, Decimal]:
    """Effective-coefficient interval whose stock rounds to the shown integer.

    The interval is half-open under ordinary nearest-integer rounding.  It is
    used only to test compatibility with the whole-Tg values printed by Ye;
    it does not turn the unstated coefficient into a reported parameter or
    establish that it is dry bulk density.
    """

    half = Decimal("0.5")
    return (
        implied_effective_sediment_mass_coefficient_g_cm3(
            displayed_stock_tg - half, area_km2, depth_m, feoc_percent
        ),
        implied_effective_sediment_mass_coefficient_g_cm3(
            displayed_stock_tg + half, area_km2, depth_m, feoc_percent
        ),
    )


def calculate() -> dict[str, object]:
    s4_rows = _rows(TABLE_S4)
    s7_rows = _rows(TABLE_S7)

    current_rows = [row for row in s4_rows if row["Group"].startswith("Mature seep")]
    early_rows = [row for row in s4_rows if row["Group"].startswith("Early-stage seep")]
    historical_rows = [row for row in s7_rows if row["Group"] == "Mature Cold Seep"]
    current_values = _decimal_values(current_rows, "FeOC (%)")
    early_values = _decimal_values(early_rows, "FeOC (%)")
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
    harris_geomorphic_slope_area_km2 = Decimal("19606260")

    depth_m = Decimal("0.30")
    reconstructed_feoc_percent = sum(combined_values) / Decimal(len(combined_values))
    endpoint_compatible_effective_coefficient = Decimal("1.65")
    lower_stock = stock_tg(
        published_lower_area_km2,
        depth_m,
        endpoint_compatible_effective_coefficient,
        reconstructed_feoc_percent,
    )
    upper_stock = stock_tg(
        upper_area_km2,
        depth_m,
        endpoint_compatible_effective_coefficient,
        reconstructed_feoc_percent,
    )
    corrected_lower_stock = stock_tg(
        corrected_lower_area_km2,
        depth_m,
        endpoint_compatible_effective_coefficient,
        reconstructed_feoc_percent,
    )
    lower_effective_coefficient_interval = (
        effective_sediment_mass_coefficient_interval_for_integer_rounding(
            Decimal("142"),
            published_lower_area_km2,
            depth_m,
            reconstructed_feoc_percent,
        )
    )
    upper_effective_coefficient_interval = (
        effective_sediment_mass_coefficient_interval_for_integer_rounding(
            Decimal("218"),
            upper_area_km2,
            depth_m,
            reconstructed_feoc_percent,
        )
    )
    joint_effective_coefficient_interval = (
        max(
            lower_effective_coefficient_interval[0],
            upper_effective_coefficient_interval[0],
        ),
        min(
            lower_effective_coefficient_interval[1],
            upper_effective_coefficient_interval[1],
        ),
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
    sediment_mass_coefficient_scenarios = {
        "same_region_measured_average_chen_2024": {
            "coefficient_g_cm3": Decimal("0.9"),
            "coefficient_role": "literature_dry_bulk_density_comparator",
        },
        "jiang_and_li_assumption": {
            "coefficient_g_cm3": Decimal("1.3"),
            "coefficient_role": "literature_dry_bulk_density_assumption",
        },
        "endpoint_compatible_effective_value": {
            "coefficient_g_cm3": endpoint_compatible_effective_coefficient,
            "coefficient_role": (
                "reverse_engineered_effective_coefficient_not_author_reported"
            ),
        },
    }
    sediment_mass_coefficient_sensitivity = {
        label: {
            "coefficient_g_cm3": str(scenario["coefficient_g_cm3"]),
            "coefficient_role": scenario["coefficient_role"],
            "nominal_20500_km2_tg": str(
                stock_tg(
                    corrected_lower_area_km2,
                    depth_m,
                    scenario["coefficient_g_cm3"],
                    reconstructed_feoc_percent,
                )
            ),
            "published_205000_km2_tg": str(
                stock_tg(
                    published_lower_area_km2,
                    depth_m,
                    scenario["coefficient_g_cm3"],
                    reconstructed_feoc_percent,
                )
            ),
            "published_315000_km2_tg": str(
                stock_tg(
                    upper_area_km2,
                    depth_m,
                    scenario["coefficient_g_cm3"],
                    reconstructed_feoc_percent,
                )
            ),
        }
        for label, scenario in sediment_mass_coefficient_scenarios.items()
    }

    wet_dry_diagnostic_porosity = Decimal("0.65")
    wet_dry_diagnostic_grain_density = Decimal("2.70")
    wet_dry_diagnostic_porewater_density = Decimal("1.024")
    wet_dry_diagnostic_dry_bulk_density = dry_bulk_density_from_porosity(
        wet_dry_diagnostic_grain_density,
        wet_dry_diagnostic_porosity,
    )
    wet_dry_diagnostic_saturated_bulk_density = (
        saturated_bulk_density_from_porosity(
            wet_dry_diagnostic_grain_density,
            wet_dry_diagnostic_porewater_density,
            wet_dry_diagnostic_porosity,
        )
    )

    return {
        "scope": (
            "Area provenance, construction comparability, density sensitivity, and "
            "stage-domain consistency; no new global-area or global-stock estimate."
        ),
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
            "current_study_early_stage_table_s4": _summary(early_values),
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
            "occupation_equivalents_on_41_million_km2_percent": {
                "nominal_20500_km2": str(
                    corrected_lower_area_km2 / slope_area_km2 * Decimal("100")
                ),
                "published_205000_km2": str(
                    published_lower_area_km2 / slope_area_km2 * Decimal("100")
                ),
                "published_315000_km2": str(
                    upper_area_km2 / slope_area_km2 * Decimal("100")
                ),
            },
            "slope_mask_sensitivity": {
                "harris_2014_geomorphic_slope_area_km2": str(
                    harris_geomorphic_slope_area_km2
                ),
                "area_at_0_05_percent_km2": str(
                    harris_geomorphic_slope_area_km2 * occupancy_fraction
                ),
                "interpretation": (
                    "A denominator-definition sensitivity, not an empirical "
                    "confidence interval for seep area."
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
                "endpoint_compatible_effective_sediment_mass_coefficient_g_cm3": str(
                    endpoint_compatible_effective_coefficient
                ),
                "basis": (
                    "simple two-decimal value that recovers both published "
                    "whole-Tg endpoints from the explicit/data-derived inputs; "
                    "this algebraic reconstruction neither identifies the "
                    "coefficient as dry bulk density nor attributes it to Ye et al."
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
            "effective_sediment_mass_coefficient_implied_by_rounded_endpoints_separately": {
                "from_142_Tg": str(
                    implied_effective_sediment_mass_coefficient_g_cm3(
                        Decimal("142"),
                        published_lower_area_km2,
                        depth_m,
                        reconstructed_feoc_percent,
                    )
                ),
                "from_218_Tg": str(
                    implied_effective_sediment_mass_coefficient_g_cm3(
                        Decimal("218"),
                        upper_area_km2,
                        depth_m,
                        reconstructed_feoc_percent,
                    )
                ),
            },
            "effective_sediment_mass_coefficient_intervals_that_round_to_each_endpoint": {
                "from_142_Tg_lower_inclusive_upper_exclusive": [
                    str(lower_effective_coefficient_interval[0]),
                    str(lower_effective_coefficient_interval[1]),
                ],
                "from_218_Tg_lower_inclusive_upper_exclusive": [
                    str(upper_effective_coefficient_interval[0]),
                    str(upper_effective_coefficient_interval[1]),
                ],
                "joint_interval_lower_inclusive_upper_exclusive": [
                    str(joint_effective_coefficient_interval[0]),
                    str(joint_effective_coefficient_interval[1]),
                ],
                "endpoint_compatible_1.65_is_inside_joint_interval": (
                    joint_effective_coefficient_interval[0]
                    <= endpoint_compatible_effective_coefficient
                    < joint_effective_coefficient_interval[1]
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
            "sediment_mass_coefficient_sensitivity": {
                "values": sediment_mass_coefficient_sensitivity,
                "interpretation": (
                    "Conditional stocks with fixed area, depth, and Fe-OC content. "
                    "The 0.9 and 1.3 g cm-3 values are literature dry-bulk-density "
                    "comparators, not a probability distribution or replacements "
                    "established for Ye's samples. The 1.65 g cm-3 value is an "
                    "endpoint-compatible effective coefficient, not a reported density."
                ),
            },
            "porosity_diagnostic": {
                "analog_measured_grain_density_g_cm3": "2.70",
                "porosity_if_1_65_effective_coefficient_is_dry_bulk_density": str(
                    implied_porosity_from_dry_bulk_density(
                        endpoint_compatible_effective_coefficient, Decimal("2.70")
                    )
                ),
                "wet_vs_dry_density_diagnostic": {
                    "porosity": str(wet_dry_diagnostic_porosity),
                    "grain_density_g_cm3": str(
                        wet_dry_diagnostic_grain_density
                    ),
                    "porewater_density_g_cm3": str(
                        wet_dry_diagnostic_porewater_density
                    ),
                    "dry_bulk_density_formula": "rho_d = rho_g * (1 - porosity)",
                    "dry_bulk_density_g_cm3": str(
                        wet_dry_diagnostic_dry_bulk_density
                    ),
                    "saturated_bulk_density_formula": (
                        "rho_sat = rho_d + rho_w * porosity"
                    ),
                    "saturated_bulk_density_g_cm3": str(
                        wet_dry_diagnostic_saturated_bulk_density
                    ),
                    "interpretation": (
                        "The numerical proximity of the illustrative saturated "
                        "bulk density to 1.65 g cm-3 makes a wet-versus-dry mismatch "
                        "a diagnostic possibility, not evidence of Ye et al.'s method."
                    ),
                },
                "interpretation": (
                    "Two-phase diagnostic using the mean grain density measured "
                    "at a hydrate-margin analog. If the effective 1.65 g cm-3 "
                    "coefficient is interpreted as dry bulk density, it is high "
                    "relative to local comparators; this conditional diagnostic "
                    "does not make the value physically impossible or prove its use."
                ),
            },
            "stage_domain_test": {
                "current_mature_only": (
                    "With Fe-OC concentration and the sediment-mass coefficient "
                    "held fixed, if A_mature = f_m * A_active and 0 < f_m <= 1, "
                    "substituting total active area for current mature area "
                    "multiplies current-mature-only stock by 1/f_m: upward for "
                    "0 < f_m < 1 and unchanged at f_m = 1."
                ),
                "all_active_stages": (
                    "If a common sediment-mass factor K is fixed across stages, "
                    "the sign depends on c_mature minus the area-weighted Fe-OC "
                    "concentration across active stages. If stage-specific mass "
                    "coefficients K_i vary, it instead depends on K_mature * "
                    "c_mature minus the area-weighted K_i * c_i products."
                ),
                "eventual_mature_scenario": (
                    "Even with Fe-OC concentration and the sediment-mass coefficient "
                    "held fixed, this scenario requires the untested equality "
                    "A_future_mature = A_current_active; its bias direction is unresolved."
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
