# Cold-seep area and Fe-OC endpoint reanalysis

This repository accompanies the paper, **[“A Factor-of-Ten Inconsistency in a Cited Cold-Seep Area and Its Conditional Effect on a Published Global Fe-OC Stock Endpoint”](manuscript/rendered/Cold_Seep_Area_Reanalysis.pdf)**.

The research began with a hypothesis from **Luigi**: overlooked dark marine nitrogen fixation—especially by Archaea—might help explain the apparent imbalance in global marine nitrogen inputs and losses. That hypothesis did not survive the initial scientific constraints. During the investigation, however, a narrower and independently verifiable result emerged: the published lower estimate of global cold-seep area contains a factor-of-ten discrepancy, and that value was subsequently used in a global iron-bound organic-carbon stock calculation.

## Research origin

Luigi supplied the scientific idea that initiated the research:

> *“Are you interested in doing a slightly deeper test? If you provide me with a high quality idea, hypothesis, or even half a thought, I would love to push this through the machinery to see what it comes up with.*
>
> *Sure. This is my idea (and this may be a game-changer). The fact is that global marine nitrogen inputs and losses seem to be imbalanced, and nobody knows why. A possible hypothesis to test is that this is due to the largely underestimated role of (especially) Archaea and (less importantly) marine Fungi. How to test it? My idea is to try to put in the global nitrogen cycle the ‘dark’ archaeal N2 fixation at seeps, vents, and subsurface sediments.*
>
> *Archaeal ‘dark’ N2 fixation at seeps/vents/subsurface sediments. This will involve extensive analysis of many meta-omics datasets, plus some rigorous modeling math.”*

This was the starting position, not the conclusion. The repository reports the numerical provenance issue found during that investigation; it does not resolve the broader marine nitrogen-budget hypothesis.

## What was found

- Boetius & Wenzhöfer (2013) report approximately **41 million km²** of continental-slope area and assume approximately **0.05%** seep occupation.
- Those printed quantities imply **41,000,000 × 0.0005 = 20,500 km² = 2.05 × 10⁴ km²**.
- Jiang et al. (2025) later report **2.05 × 10⁵ km²** as the lower endpoint of a **2.05–3.15 × 10⁵ km²** global cold-seep-area interval.
- Ye et al. (2026) subsequently use that published interval to estimate **142–218 Tg C** of mature-seep Fe-bound organic carbon.
- Holding Ye et al.’s area-linear calculation fixed while changing only the lower area endpoint gives approximately **14.2 Tg C**, rather than **142 Tg C**, for the corresponding lower stock endpoint.

The evidence establishes an incompatibility between the earlier printed premises and the later published lower endpoint, followed by Ye et al.’s documented use of that endpoint. It does **not** establish the private historical path by which the exponent entered the literature, and it does not attribute the original discrepancy to Ye et al. The **14.2 Tg C** value is a controlled arithmetic substitution, not a new estimate of global cold-seep area or a validated lower bound for global Fe-bound organic-carbon storage.

## Why it matters

The issue is more than an isolated multiplication error. A global spatial scaling parameter was used to convert local observations into a global biogeochemical quantity and was then reused in subsequent literature. This candidate reconstructs that numerical provenance and quantifies the downstream consequence while leaving the underlying sediment observations and the upper endpoint unchanged.

## Repository guide

| Resource | What it contains |
|---|---|
| [Compiled paper](manuscript/rendered/Cold_Seep_Area_Reanalysis.pdf) | The complete research paper for reading, review, and citation. |
| [Canonical TeX source](manuscript/source/Cold_Seep_Area_Reanalysis.tex) | The manuscript source used to build the paper, including its tables, equations, and references. |
| [Reproducibility guide](REPRODUCIBILITY.md) | A compact description of the calculation package and verification commands. |
| [Source-value record](evidence/SOURCE_VALUES.md) | The evidence ledger: source locators, extracted values, qualifications, and verification status for the numerical chain. |
| [Primary audit](code/audit_error_chain.py) and [independent stock reconstruction](code/ye_reproduce_stock.py) | Standard-library Python implementations of the area audit, source-data reconstruction, and conditional stock calculation. |
| [Data provenance](data/README.md) and [source-derived tables](data/ye_osf_extracted/) | Provenance and the two public-source CSV extracts required to reproduce the calculations. |
| [Verification tests](tests/) | Fifteen automated checks covering the area arithmetic, source-table summaries, endpoint reconstruction, and rounding robustness. |
| [Machine-readable results](evidence/calculation_outputs.json) | The primary audit output used to inspect the reconstructed values and assumptions. |
| [Portable supplement](manuscript/source/Reproducibility_Supplement.zip) | A self-contained copy of the reproducibility materials distributed with the manuscript. |

## Reproducibility

The calculations and tests require Python 3.9 or newer and use only the standard library. From the repository root, run:

```text
python -B -m unittest discover -s tests -v
python -B code/audit_error_chain.py --write
python -B code/ye_reproduce_stock.py --output data/ye_stock_reproduction.json
```

The test suite verifies the factor-of-ten area discrepancy, reconstructs the retained Fe-OC source-data summaries, reproduces the published **142–218 Tg C** endpoints under the compatible area-linear calculation, and confirms the conditional **14.2 Tg C** lower endpoint.

To compile the manuscript, run the following command three times from `manuscript/source/` so that the table of contents, citations, and cross-references resolve:

```text
pdflatex --interaction=nonstopmode --halt-on-error --file-line-error --output-directory=../rendered Cold_Seep_Area_Reanalysis.tex
```

Third-party full-text files are linked rather than redistributed. Authoritative source links, locators, and checksums are recorded in the [source-value record](evidence/SOURCE_VALUES.md) and [data provenance record](data/README.md).

## Attribution

Research candidate by **UCP Technology LLC**  
[ucptechnology.ai](https://ucptechnology.ai)

**Luigi** supplied the original scientific hypothesis that initiated the research.
