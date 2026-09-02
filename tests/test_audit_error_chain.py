from __future__ import annotations

import importlib.util
import math
import unittest
from decimal import Decimal
from pathlib import Path


SCRIPT = Path(__file__).resolve().parents[1] / "code" / "audit_error_chain.py"
SPEC = importlib.util.spec_from_file_location("audit_error_chain", SCRIPT)
assert SPEC and SPEC.loader
AUDIT = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(AUDIT)


class ErrorChainAuditTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.result = AUDIT.calculate()

    def test_origin_arithmetic(self) -> None:
        area = self.result["area_arithmetic"]
        self.assertEqual(area["occupation_fraction"], "0.0005")
        self.assertEqual(area["product_km2"], "20500.0000")
        self.assertEqual(area["published_to_arithmetic_ratio"], "1E+1")

    def test_routes_to_published_lower_require_factor_ten_change(self) -> None:
        required = self.result["area_arithmetic"][
            "inputs_required_to_generate_published_lower"
        ]
        self.assertEqual(required["occupation_percent_if_area_stays_41_million_km2"], "0.500")
        self.assertEqual(
            Decimal(required["slope_area_km2_if_occupation_stays_0.05_percent"]),
            Decimal("410000000"),
        )
        self.assertEqual(required["unreported_multiplier"], "1E+1")

    def test_ye_current_study_mature_summary(self) -> None:
        current = self.result["ye_mature_feoc_reconstruction"][
            "current_study_table_s4"
        ]
        self.assertEqual(current["n"], 14)
        self.assertEqual(current["sum_percent"], "1.52")
        self.assertEqual(current["mean_percent"], "0.1085714285714285714285714286")
        self.assertTrue(
            math.isclose(float(current["sample_sd_percent"]), 0.0241333292858151)
        )

    def test_ye_current_study_early_stage_summary(self) -> None:
        early = self.result["ye_mature_feoc_reconstruction"][
            "current_study_early_stage_table_s4"
        ]
        self.assertEqual(early["n"], 21)
        self.assertEqual(early["sum_percent"], "3.45")
        self.assertTrue(math.isclose(float(early["mean_percent"]), 0.1642857142857143))

    def test_ye_historical_mature_summary(self) -> None:
        historical = self.result["ye_mature_feoc_reconstruction"][
            "historical_table_s7"
        ]
        self.assertEqual(historical["n"], 8)
        self.assertEqual(historical["sum_percent"], "1.56")
        self.assertEqual(historical["mean_percent"], "0.195")
        self.assertTrue(
            math.isclose(float(historical["sample_sd_percent"]), 0.0558057856703569)
        )

    def test_ye_combined_mature_summary_reproduces_report(self) -> None:
        combined = self.result["ye_mature_feoc_reconstruction"]["combined"]
        rounding = self.result["ye_mature_feoc_reconstruction"][
            "reported_rounding_check"
        ]
        self.assertEqual(combined["n"], 22)
        self.assertEqual(combined["sum_percent"], "3.08")
        self.assertEqual(combined["mean_percent"], "0.14")
        self.assertTrue(
            math.isclose(float(combined["sample_sd_percent"]), 0.0566526593332017)
        )
        self.assertEqual(rounding["current_mean_sd_percent_2dp"], "0.11 +/- 0.02")
        self.assertEqual(rounding["combined_mean_sd_percent_2dp"], "0.14 +/- 0.06")

    def test_all_seep_cross_check_reproduces_adjacent_report(self) -> None:
        all_seep = self.result["ye_mature_feoc_reconstruction"][
            "all_seep_cross_check"
        ]
        rounding = self.result["ye_mature_feoc_reconstruction"][
            "reported_rounding_check"
        ]
        self.assertEqual(all_seep["n"], 43)
        self.assertEqual(all_seep["sum_percent"], "6.53")
        self.assertTrue(
            math.isclose(float(all_seep["mean_percent"]), 0.151860465116279)
        )
        self.assertTrue(
            math.isclose(float(all_seep["sample_sd_percent"]), 0.050768185288008)
        )
        self.assertEqual(rounding["all_seep_mean_sd_percent_2dp"], "0.15 +/- 0.05")

    def test_stock_identity_and_published_endpoints(self) -> None:
        computed = self.result["ye_stock_reconstruction"]["computed"]
        self.assertEqual(
            Decimal(computed["reconstruction_with_implicit_1p65_lower_Tg"]),
            Decimal("142.065"),
        )
        self.assertEqual(
            computed["reconstruction_with_implicit_1p65_lower_rounded_Tg"], "142"
        )
        self.assertEqual(
            Decimal(computed["reconstruction_with_implicit_1p65_upper_Tg"]),
            Decimal("218.295"),
        )
        self.assertEqual(
            computed["reconstruction_with_implicit_1p65_upper_rounded_Tg"], "218"
        )

    def test_only_correcting_lower_area_gives_14_point_2_Tg(self) -> None:
        computed = self.result["ye_stock_reconstruction"]["computed"]
        self.assertEqual(
            computed["corrected_reconstruction_with_implicit_1p65_lower_Tg"],
            "14.206500",
        )
        self.assertEqual(
            computed["corrected_reconstruction_with_implicit_1p65_lower_1dp_Tg"],
            "14.2",
        )
        self.assertEqual(Decimal(computed["lower_stock_ratio_published_to_corrected"]), Decimal("10"))

    def test_density_free_rounding_bounds_still_give_about_14_point_2(self) -> None:
        audit = self.result["ye_stock_reconstruction"][
            "density_free_area_linear_rounding_audit"
        ]
        lower, upper = map(
            Decimal,
            audit["corrected_lower_Tg_lower_inclusive_upper_exclusive"],
        )
        self.assertEqual(lower.quantize(Decimal("0.1")), Decimal("14.2"))
        self.assertEqual(upper.quantize(Decimal("0.1")), Decimal("14.2"))

    def test_dimensionally_explicit_stock_function(self) -> None:
        value = AUDIT.stock_tg(
            Decimal("205000"),
            Decimal("0.30"),
            Decimal("1.65"),
            Decimal("0.14"),
        )
        self.assertEqual(value, Decimal("142.06500"))

    def test_sediment_mass_coefficient_sensitivity_values_and_roles(self) -> None:
        values = self.result["ye_stock_reconstruction"][
            "sediment_mass_coefficient_sensitivity"
        ]["values"]
        self.assertEqual(
            Decimal(values["same_region_measured_average_chen_2024"]["published_205000_km2_tg"]),
            Decimal("77.49000"),
        )
        self.assertEqual(
            Decimal(values["jiang_and_li_assumption"]["published_315000_km2_tg"]),
            Decimal("171.99000"),
        )
        self.assertEqual(
            Decimal(values["endpoint_compatible_effective_value"]["nominal_20500_km2_tg"]),
            Decimal("14.206500"),
        )
        self.assertEqual(
            values["same_region_measured_average_chen_2024"]["coefficient_role"],
            "literature_dry_bulk_density_comparator",
        )
        self.assertEqual(
            values["jiang_and_li_assumption"]["coefficient_role"],
            "literature_dry_bulk_density_assumption",
        )
        self.assertEqual(
            values["endpoint_compatible_effective_value"]["coefficient_role"],
            "reverse_engineered_effective_coefficient_not_author_reported",
        )
        self.assertEqual(
            values["endpoint_compatible_effective_value"]["coefficient_g_cm3"],
            "1.65",
        )

    def test_area_denominator_and_porosity_diagnostics(self) -> None:
        area = self.result["area_arithmetic"]
        self.assertEqual(
            area["occupation_equivalents_on_41_million_km2_percent"],
            {
                "nominal_20500_km2": "0.0500",
                "published_205000_km2": "0.500",
                "published_315000_km2": "0.7682926829268292682926829268",
            },
        )
        self.assertEqual(
            Decimal(area["slope_mask_sensitivity"]["area_at_0_05_percent_km2"]),
            Decimal("9803.1300"),
        )
        porosity = self.result["ye_stock_reconstruction"]["porosity_diagnostic"]
        self.assertTrue(
            math.isclose(
                float(
                    porosity[
                        "porosity_if_1_65_effective_coefficient_is_dry_bulk_density"
                    ]
                ),
                0.3888888888888889,
            )
        )

    def test_wet_vs_dry_density_diagnostic(self) -> None:
        diagnostic = self.result["ye_stock_reconstruction"][
            "porosity_diagnostic"
        ]["wet_vs_dry_density_diagnostic"]
        self.assertEqual(Decimal(diagnostic["porosity"]), Decimal("0.65"))
        self.assertEqual(
            Decimal(diagnostic["dry_bulk_density_g_cm3"]), Decimal("0.945")
        )
        self.assertEqual(
            Decimal(diagnostic["saturated_bulk_density_g_cm3"]),
            Decimal("1.6106"),
        )
        self.assertEqual(
            AUDIT.dry_bulk_density_from_porosity(
                Decimal("2.70"), Decimal("0.65")
            ),
            Decimal("0.945"),
        )
        self.assertEqual(
            AUDIT.saturated_bulk_density_from_porosity(
                Decimal("2.70"), Decimal("1.024"), Decimal("0.65")
            ),
            Decimal("1.6106"),
        )

    def test_effective_coefficient_is_compatible_with_both_printed_roundings(self) -> None:
        intervals = self.result["ye_stock_reconstruction"][
            "effective_sediment_mass_coefficient_intervals_that_round_to_each_endpoint"
        ]
        lower, upper = map(
            Decimal, intervals["joint_interval_lower_inclusive_upper_exclusive"]
        )
        self.assertLessEqual(lower, Decimal("1.65"))
        self.assertLess(Decimal("1.65"), upper)
        self.assertTrue(
            intervals["endpoint_compatible_1.65_is_inside_joint_interval"]
        )

    def test_stage_domain_diagnostics_state_parameter_conditions(self) -> None:
        stage = self.result["ye_stock_reconstruction"]["stage_domain_test"]
        self.assertIn("held fixed", stage["current_mature_only"])
        self.assertIn("upward for 0 < f_m < 1", stage["current_mature_only"])
        self.assertIn("unchanged at f_m = 1", stage["current_mature_only"])
        self.assertIn("common sediment-mass factor K", stage["all_active_stages"])
        self.assertIn("stage-specific mass coefficients K_i", stage["all_active_stages"])


if __name__ == "__main__":
    unittest.main()
