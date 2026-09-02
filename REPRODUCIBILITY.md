# Reproducibility supplement

This supplement reproduces the calculations in “Incommensurate Global Cold-Seep Area Constructions and Their Consequences for an Iron-Bound Organic-Carbon Stock.”

## Contents

- `evidence/SOURCE_VALUES.md` records source values, locators, qualifications, and the status of each scientific claim.
- `evidence/calculation_outputs.json` contains the machine-readable calculation results.
- `code/audit_error_chain.py` reconstructs the area premises, occupation equivalents, slope-denominator sensitivity, Fe-OC source rows, density sensitivity, porosity and wet-versus-dry diagnostics, and density-independent endpoint-rounding result.
- `code/ye_reproduce_stock.py` independently reconstructs the mature-seep Fe-OC rows, weighting sensitivity, and stock endpoints.
- `data/` contains the two public OSF table extracts and machine-readable stock reconstruction.
- `tests/` contains 20 executable verification tests.

## Run

From the repository or extracted supplement root:

```text
python -B -m unittest discover -s tests -v
python -B code/audit_error_chain.py --write
python -B code/ye_reproduce_stock.py --output data/ye_stock_reproduction.json
```

The scripts use only the Python standard library.

## Interpretation boundaries

The package distinguishes exact arithmetic from scientific estimation:

- `20,500 km²` is the exact product of the printed `41 million km²` and `0.05%` premises; it is not a measured global lower bound.
- `315,000 km²` is the nominal `350 × 900` numerical fingerprint; because the source count is “more than 900” and the spatial unit is not transferable, it is not an upper bound.
- `14.2 Tg C` is the result of changing one area term by a factor of ten while retaining the published area-linear mapping; it is not a corrected global stock estimate.
- Density rows are conditional sensitivity calculations, not a probability distribution or sample-specific replacements.
- The developmental-stage formulas state the conditions under which a directional bias follows; they do not estimate a global mature fraction.

Primary publications and publisher supplements are identified by DOI or public repository URL and are not redistributed.
