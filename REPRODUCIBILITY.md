# Reproducibility supplement

This supplement reproduces the arithmetic and endpoint calculations reported in the manuscript, “A Factor-of-Ten Inconsistency in a Cited Cold-Seep Area and Its Conditional Effect on a Published Global Fe-OC Stock Endpoint.”

Contents:

- `evidence/`: source values, provenance qualifications, and machine-readable calculation output.
- `code/audit_error_chain.py`: exact decimal audit of the area provenance chain and density-independent endpoint-rounding check.
- `code/ye_reproduce_stock.py`: reconstruction of the mature-seep Fe-OC source rows, source-block weighting sensitivity, and conditional stock calculation.
- `data/`: the two extracted public OSF tables used by the calculations and machine-readable results.
- `tests/`: 15 executable verification tests.

From the extracted supplement root, run:

```text
python -B -m unittest discover -s tests -v
python -B code/audit_error_chain.py --write
python -B code/ye_reproduce_stock.py --output data/ye_stock_reproduction.json
```

The scripts and tests use the Python standard library. Primary publications and publisher supplements are identified by DOI or public repository URL and are not redistributed in this archive.
