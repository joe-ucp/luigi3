from __future__ import annotations

import importlib.util
import statistics
import unittest
from decimal import Decimal
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    "ye_reproduce_stock", REPO_ROOT / "code" / "ye_reproduce_stock.py"
)
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(MODULE)


class YeReproductionTests(unittest.TestCase):
    def setUp(self) -> None:
        self.current_csv = REPO_ROOT / "data" / "ye_osf_extracted" / "ye_osf_table_04.csv"
        self.literature_csv = REPO_ROOT / "data" / "ye_osf_extracted" / "ye_osf_table_06.csv"

    def test_source_data_reproduce_mature_summary(self) -> None:
        current, literature = MODULE.read_mature_feoc(self.current_csv, self.literature_csv)
        self.assertEqual((len(current), len(literature)), (14, 8))
        combined = current + literature
        self.assertAlmostEqual(statistics.mean(combined), 0.14, places=14)
        self.assertEqual(round(statistics.stdev(combined), 2), 0.06)

    def test_published_endpoints_and_corrected_lower(self) -> None:
        density = Decimal("1.65")
        self.assertEqual(MODULE.stock_tg(Decimal("205000"), density), Decimal("142.065"))
        self.assertEqual(MODULE.stock_tg(Decimal("315000"), density), Decimal("218.295"))
        self.assertEqual(MODULE.stock_tg(Decimal("20500"), density), Decimal("14.2065"))

    def test_1_65_density_is_compatible_with_both_rounded_endpoints(self) -> None:
        result = MODULE.build_result(self.current_csv, self.literature_csv)
        audit = result["rounding_audit_density_g_cm3"]
        self.assertTrue(audit["1_65_is_in_joint_interval"])

    def test_profile_structure_and_weighting_sensitivity(self) -> None:
        result = MODULE.build_result(self.current_csv, self.literature_csv)
        sensitivity = result["source_data_weighting_sensitivity"]
        self.assertEqual(
            {key: value["n"] for key, value in sensitivity["current_station_profiles"].items()},
            {"QDN-S18": 7, "HM-S4": 7},
        )
        self.assertEqual(
            {
                key: value["n"]
                for key, value in sensitivity["historical_profile_or_location_labels"].items()
            },
            {"PC01": 1, "ROV5": 7},
        )
        self.assertAlmostEqual(sensitivity["observation_weighted_mean_percent"], 0.14, places=14)
        self.assertAlmostEqual(sensitivity["study_equal_mean_percent"], 0.15178571428571427)
        self.assertAlmostEqual(sensitivity["profile_label_equal_mean_percent"], 0.16142857142857142)


if __name__ == "__main__":
    unittest.main()
