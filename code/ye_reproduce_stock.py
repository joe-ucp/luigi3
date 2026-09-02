"""Independent reconstruction of Ye et al. (2026)'s Fe-OC stock endpoints.

The script deliberately separates source-stated inputs from the endpoint-
compatible effective sediment-mass coefficient required to recover the
published integer endpoints. The latter is neither labelled as a source-
stated value nor assumed to be dry bulk density.
"""

from __future__ import annotations

import argparse
import csv
import json
import statistics
from decimal import Decimal
from pathlib import Path


AREA_LOW_PUBLISHED_KM2 = Decimal("205000")
AREA_HIGH_KM2 = Decimal("315000")
AREA_LOW_CORRECTED_KM2 = Decimal("20500")
DEPTH_M = Decimal("0.30")
FEOC_PERCENT = Decimal("0.14")
ENDPOINT_COMPATIBLE_EFFECTIVE_SEDIMENT_MASS_COEFFICIENT_G_CM3 = Decimal("1.65")


def read_mature_feoc(current_csv: Path, literature_csv: Path) -> tuple[list[float], list[float]]:
    """Read the two source-data blocks used in the paper's mature-seep summary."""
    with current_csv.open(encoding="utf-8-sig", newline="") as handle:
        rows = list(csv.reader(handle))
    current = [float(row[3]) for row in rows[1:] if row and row[0].startswith("Mature seep")]

    with literature_csv.open(encoding="utf-8-sig", newline="") as handle:
        rows = list(csv.reader(handle))
    literature = [float(row[6]) for row in rows[1:] if row and row[1] == "Mature Cold Seep"]
    return current, literature


def read_mature_profile_groups(
    current_csv: Path, literature_csv: Path
) -> tuple[dict[str, list[float]], dict[str, list[float]]]:
    """Return the profile/location groupings visible in the retained OSF tables.

    The function does not assert that these labels are independent sites or
    statistically exchangeable units.  It only exposes the grouping structure
    printed in the source rows for a descriptive weighting sensitivity.
    """
    current_groups: dict[str, list[float]] = {}
    with current_csv.open(encoding="utf-8-sig", newline="") as handle:
        for row in csv.DictReader(handle):
            if not row["Group"].startswith("Mature seep"):
                continue
            current_groups.setdefault(row["Station"], []).append(float(row["FeOC (%)"]))

    literature_groups: dict[str, list[float]] = {}
    with literature_csv.open(encoding="utf-8-sig", newline="") as handle:
        rows = list(csv.reader(handle))
    for row in rows[1:]:
        if not row or row[1] != "Mature Cold Seep":
            continue
        location = row[0]
        if location.startswith("PC01-"):
            group = "PC01"
        elif location.startswith("ROV5-"):
            group = "ROV5"
        else:
            group = location
        literature_groups.setdefault(group, []).append(float(row[6]))
    return current_groups, literature_groups


def stock_tg(
    area_km2: Decimal, sediment_mass_coefficient_g_cm3: Decimal
) -> Decimal:
    """Return Fe-OC stock in Tg C with every unit conversion explicit.

    area[km2] * 1e6[m2/km2] * depth[m] * coefficient[g/cm3]
    * 1e6[g/m3 per g/cm3] * FeOC[%]/100 * 1e-12[Tg/g]

    For a fully specified dry-mass inventory, the coefficient is dry bulk
    density. Reverse-engineering rounded endpoints recovers only an
    algebraically equivalent effective coefficient, not its physical identity.
    """
    return (
        area_km2
        * Decimal("1e6")
        * DEPTH_M
        * sediment_mass_coefficient_g_cm3
        * Decimal("1e6")
        * FEOC_PERCENT
        / Decimal("100")
        * Decimal("1e-12")
    )


def effective_sediment_mass_coefficient_interval_for_integer(
    area_km2: Decimal, reported_tg: Decimal
) -> tuple[Decimal, Decimal]:
    """Half-open effective-coefficient interval for a rounded stock endpoint."""

    multiplier = stock_tg(area_km2, Decimal("1"))
    return (
        (reported_tg - Decimal("0.5")) / multiplier,
        (reported_tg + Decimal("0.5")) / multiplier,
    )


def build_result(current_csv: Path, literature_csv: Path) -> dict:
    current, literature = read_mature_feoc(current_csv, literature_csv)
    combined = current + literature
    current_groups, literature_groups = read_mature_profile_groups(current_csv, literature_csv)
    profile_groups = current_groups | literature_groups
    study_equal_mean = statistics.mean((statistics.mean(current), statistics.mean(literature)))
    profile_label_equal_mean = statistics.mean(
        statistics.mean(values) for values in profile_groups.values()
    )

    low_effective_coefficient_interval = (
        effective_sediment_mass_coefficient_interval_for_integer(
            AREA_LOW_PUBLISHED_KM2, Decimal("142")
        )
    )
    high_effective_coefficient_interval = (
        effective_sediment_mass_coefficient_interval_for_integer(
            AREA_HIGH_KM2, Decimal("218")
        )
    )
    joint_effective_coefficient_interval = (
        max(
            low_effective_coefficient_interval[0],
            high_effective_coefficient_interval[0],
        ),
        min(
            low_effective_coefficient_interval[1],
            high_effective_coefficient_interval[1],
        ),
    )
    low_coefficient_interval = (
        (Decimal("142") - Decimal("0.5")) / AREA_LOW_PUBLISHED_KM2,
        (Decimal("142") + Decimal("0.5")) / AREA_LOW_PUBLISHED_KM2,
    )
    high_coefficient_interval = (
        (Decimal("218") - Decimal("0.5")) / AREA_HIGH_KM2,
        (Decimal("218") + Decimal("0.5")) / AREA_HIGH_KM2,
    )
    joint_coefficient_interval = (
        max(low_coefficient_interval[0], high_coefficient_interval[0]),
        min(low_coefficient_interval[1], high_coefficient_interval[1]),
    )

    result = {
        "source_data_reconstruction": {
            "current_mature_rows_n": len(current),
            "current_mature_feoc_percent": current,
            "current_mean_percent": statistics.mean(current),
            "current_sample_sd_percent": statistics.stdev(current),
            "historical_mature_rows_n": len(literature),
            "historical_mature_feoc_percent": literature,
            "historical_mean_percent": statistics.mean(literature),
            "historical_sample_sd_percent": statistics.stdev(literature),
            "combined_rows_n": len(combined),
            "combined_mean_percent": statistics.mean(combined),
            "combined_sample_sd_percent": statistics.stdev(combined),
            "published_rounded_summary_percent": "0.14 +/- 0.06",
        },
        "source_data_weighting_sensitivity": {
            "current_station_profiles": {
                label: {"n": len(values), "mean_feoc_percent": statistics.mean(values)}
                for label, values in current_groups.items()
            },
            "historical_profile_or_location_labels": {
                label: {"n": len(values), "mean_feoc_percent": statistics.mean(values)}
                for label, values in literature_groups.items()
            },
            "observation_weighted_mean_percent": statistics.mean(combined),
            "study_equal_mean_percent": study_equal_mean,
            "profile_label_equal_mean_percent": profile_label_equal_mean,
            "historical_mean_percent_above_current_percent": (
                statistics.mean(literature) / statistics.mean(current) - 1
            ) * 100,
            "interpretation": (
                "Descriptive sensitivity only. The source tables expose depth-resolved rows and "
                "profile/location labels, but do not establish row independence, analytical "
                "exchangeability, or globally representative weighting units."
            ),
        },
        "source_stated_stock_inputs": {
            "published_lower_area_km2": int(AREA_LOW_PUBLISHED_KM2),
            "upper_area_km2": int(AREA_HIGH_KM2),
            "depth_m": str(DEPTH_M),
            "mature_feoc_percent": str(FEOC_PERCENT),
        },
        "implicit_coefficient": {
            "endpoint_compatible_effective_sediment_mass_coefficient_g_cm3": str(
                ENDPOINT_COMPATIBLE_EFFECTIVE_SEDIMENT_MASS_COEFFICIENT_G_CM3
            ),
            "status": "reverse-engineered; not stated in the Ye article, SI, or OSF source-data file",
            "caution": (
                "The 1.65 g cm-3 value is an algebraically endpoint-compatible "
                "effective sediment-mass coefficient. Interpreting it as dry bulk "
                "density is conditional; endpoint matching neither establishes its "
                "physical identity nor proves that Ye et al. selected it."
            ),
        },
        "unit_identity": (
            "Tg C = area_km2 * 1e6 m2/km2 * depth_m * "
            "sediment_mass_coefficient_g_cm3 * "
            "1e6 g/m3/(g/cm3) * FeOC_percent/100 * 1e-12 Tg/g"
        ),
        "stock_results_tg": {
            "reconstruction_with_implicit_1p65_lower_tg": str(
                stock_tg(
                    AREA_LOW_PUBLISHED_KM2,
                    ENDPOINT_COMPATIBLE_EFFECTIVE_SEDIMENT_MASS_COEFFICIENT_G_CM3,
                )
            ),
            "reconstruction_with_implicit_1p65_upper_tg": str(
                stock_tg(
                    AREA_HIGH_KM2,
                    ENDPOINT_COMPATIBLE_EFFECTIVE_SEDIMENT_MASS_COEFFICIENT_G_CM3,
                )
            ),
            "reconstruction_with_implicit_1p65_lower_round_1_tg": round(
                float(
                    stock_tg(
                        AREA_LOW_PUBLISHED_KM2,
                        ENDPOINT_COMPATIBLE_EFFECTIVE_SEDIMENT_MASS_COEFFICIENT_G_CM3,
                    )
                )
            ),
            "reconstruction_with_implicit_1p65_upper_round_1_tg": round(
                float(
                    stock_tg(
                        AREA_HIGH_KM2,
                        ENDPOINT_COMPATIBLE_EFFECTIVE_SEDIMENT_MASS_COEFFICIENT_G_CM3,
                    )
                )
            ),
            "corrected_reconstruction_with_implicit_1p65_lower_tg": str(
                stock_tg(
                    AREA_LOW_CORRECTED_KM2,
                    ENDPOINT_COMPATIBLE_EFFECTIVE_SEDIMENT_MASS_COEFFICIENT_G_CM3,
                )
            ),
            "corrected_reconstruction_with_implicit_1p65_lower_3_sigfig": "14.2",
            "upper_unchanged_reconstruction_with_implicit_1p65_tg": str(
                stock_tg(
                    AREA_HIGH_KM2,
                    ENDPOINT_COMPATIBLE_EFFECTIVE_SEDIMENT_MASS_COEFFICIENT_G_CM3,
                )
            ),
        },
        "rounding_audit_effective_sediment_mass_coefficient_g_cm3": {
            "lower_endpoint_142_interval_half_open": [
                str(x) for x in low_effective_coefficient_interval
            ],
            "upper_endpoint_218_interval_half_open": [
                str(x) for x in high_effective_coefficient_interval
            ],
            "joint_interval_half_open": [
                str(x) for x in joint_effective_coefficient_interval
            ],
            "1_65_is_in_joint_interval": (
                joint_effective_coefficient_interval[0]
                <= ENDPOINT_COMPATIBLE_EFFECTIVE_SEDIMENT_MASS_COEFFICIENT_G_CM3
                < joint_effective_coefficient_interval[1]
            ),
            "effective_coefficient_implied_by_exact_142": str(
                Decimal("142")
                / stock_tg(AREA_LOW_PUBLISHED_KM2, Decimal("1"))
            ),
            "effective_coefficient_implied_by_exact_218": str(
                Decimal("218") / stock_tg(AREA_HIGH_KM2, Decimal("1"))
            ),
        },
        "rounding_audit_area_coefficient_tg_per_km2": {
            "coefficient_from_0_14pct_0_30m_and_1_65_effective_g_cm3": "0.000693",
            "joint_interval_that_rounds_to_both_published_endpoints": [
                str(x) for x in joint_coefficient_interval
            ],
            "interpretation": (
                "The reported integer endpoints admit a single common linear area coefficient, but "
                "the reports do not uniquely identify its physical decomposition."
            ),
            "corrected_lower_tg_interval_half_open": [
                str(AREA_LOW_CORRECTED_KM2 * joint_coefficient_interval[0]),
                str(AREA_LOW_CORRECTED_KM2 * joint_coefficient_interval[1]),
            ],
            "corrected_lower_interval_interpretation": (
                "Every common area-linear coefficient compatible with both published integer "
                "endpoints yields about 14.2 Tg after changing only the lower area."
            ),
        },
    }

    assert len(current) == 14
    assert len(literature) == 8
    assert {label: len(values) for label, values in current_groups.items()} == {
        "QDN-S18": 7,
        "HM-S4": 7,
    }
    assert {label: len(values) for label, values in literature_groups.items()} == {
        "PC01": 1,
        "ROV5": 7,
    }
    assert abs(statistics.mean(combined) - 0.14) < 1e-15
    assert abs(study_equal_mean - 0.15178571428571427) < 1e-15
    assert abs(profile_label_equal_mean - 0.16142857142857142) < 1e-15
    assert round(statistics.stdev(combined), 2) == 0.06
    assert stock_tg(
        AREA_LOW_PUBLISHED_KM2,
        ENDPOINT_COMPATIBLE_EFFECTIVE_SEDIMENT_MASS_COEFFICIENT_G_CM3,
    ) == Decimal("142.065")
    assert stock_tg(
        AREA_HIGH_KM2,
        ENDPOINT_COMPATIBLE_EFFECTIVE_SEDIMENT_MASS_COEFFICIENT_G_CM3,
    ) == Decimal("218.295")
    assert stock_tg(
        AREA_LOW_CORRECTED_KM2,
        ENDPOINT_COMPATIBLE_EFFECTIVE_SEDIMENT_MASS_COEFFICIENT_G_CM3,
    ) == Decimal("14.2065")
    assert result[
        "rounding_audit_effective_sediment_mass_coefficient_g_cm3"
    ]["1_65_is_in_joint_interval"]
    return result


def main() -> None:
    repo_root = Path(__file__).resolve().parents[1]
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--current-csv",
        type=Path,
        default=repo_root / "data" / "ye_osf_extracted" / "ye_osf_table_04.csv",
    )
    parser.add_argument(
        "--literature-csv",
        type=Path,
        default=repo_root / "data" / "ye_osf_extracted" / "ye_osf_table_06.csv",
    )
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    result = build_result(args.current_csv, args.literature_csv)
    rendered = json.dumps(result, indent=2, ensure_ascii=False) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(rendered, encoding="utf-8")
    print(rendered, end="")


if __name__ == "__main__":
    main()
