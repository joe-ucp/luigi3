# Global cold-seep area and Fe-OC stock reanalysis

This repository accompanies the paper **[“Incommensurate Global Cold-Seep Area Constructions and Their Consequences for an Iron-Bound Organic-Carbon Stock”](manuscript/rendered/Cold_Seep_Area_Reanalysis.pdf)**.

## Main findings

- Ye et al. (2026) state that cold seeps occupy less than **0.05% of continental-slope area** but later apply **2.05–3.15 × 10⁵ km²**. With the approximately 41-million-km² slope domain in the cited source, the first statement implies less than **2.05 × 10⁴ km²**. No spatial-domain conversion reconciles the two.
- The published area pair is not a scientific interval. Joint citation and numerical fingerprints associate it with a top-down slope-area × occupation assumption and a bottom-up Haima-field-area × discovery-count extrapolation. No disclosed method makes those constructions bounds on a common quantity.
- Independent fluid-expulsion compilations and regional surveys demonstrate incomplete inventories, extreme spatial heterogeneity, and non-equivalence among fields, plumes, points, and habitat patches. They do not validate a global active-sediment area.
- The reported absolute Fe-OC stock requires an undisclosed sediment-mass coefficient. An effective value near **1.65 g cm⁻³** reproduces the published endpoints; interpreted as dry bulk density, it is high relative to available regional and hydrate-margin context but is not physically impossible.
- Mature-versus-active area is a target-domain problem. Holding concentration and sediment mass per area fixed, total active area increases a current mature-only stock only when the mature fraction is below one; the direction remains unresolved for an all-active inventory or Ye et al.’s eventual-mature scenario.
- Holding the published area-linear calculation fixed while changing only **205,000** to the printed-premise product **20,500 km²** changes the corresponding endpoint from approximately **142** to **14.2 Tg C**. This is a controlled sensitivity, not a new global lower bound.

The central conclusion is that neither the original area pair nor an exponent-corrected pairing is a defensible global interval. The true global active cold-seep area and the resulting Fe-OC stock remain unresolved.

## Independent scientific review

[Luigi’s independent review](Luigi%20Feeback/Cold_Seep_Reanalysis_Review02092026.docx) reproduced and confirmed the numerical results in the original manuscript. It also helped recenter the revision on the within-article area inconsistency and the lack of a demonstrated common basis for the reported area span, while motivating the added examinations of sediment density, global seep-area context, and developmental-stage commensurability. Each proposed strengthening was evaluated independently against primary evidence before inclusion; the review informed the inquiry but was not treated as scientific evidence. The linked review addresses the original manuscript, not the present revision.

## Repository guide

| Resource | Contents |
|---|---|
| [Compiled paper](manuscript/rendered/Cold_Seep_Area_Reanalysis.pdf) | Revised scientific manuscript for review and citation. |
| [Canonical TeX source](manuscript/source/Cold_Seep_Area_Reanalysis.tex) | Manuscript source, equations, figure, tables, and references. |
| [Independent scientific review](Luigi%20Feeback/Cold_Seep_Reanalysis_Review02092026.docx) | Independent numerical reproduction and scientific recommendations concerning the original manuscript; not a review of the present revision. |
| [Reproducibility guide](REPRODUCIBILITY.md) | Calculation package and verification commands. |
| [Source-value record](evidence/SOURCE_VALUES.md) | Source locators, extracted values, qualifications, and claim status. |
| [Primary reconstruction](code/audit_error_chain.py) | Area, denominator, density, endpoint-rounding, and stage-domain analyses. |
| [Independent stock reconstruction](code/ye_reproduce_stock.py) | Source-row summaries, weighting sensitivity, and conditional stock calculations. |
| [Source-derived data](data/ye_osf_extracted/) | Public-source CSV extracts used by the calculations. |
| [Verification tests](tests/) | Twenty automated checks. |
| [Machine-readable results](evidence/calculation_outputs.json) | Complete calculation output and interpretation labels. |
| [Portable supplement](manuscript/source/Reproducibility_Supplement.zip) | Self-contained reproducibility materials distributed with the manuscript. |

## Reproduce the calculations

Python 3.9 or newer is required; the scripts use only the standard library. From the repository root:

```text
python -B -m unittest discover -s tests -v
python -B code/audit_error_chain.py --write
python -B code/ye_reproduce_stock.py --output data/ye_stock_reproduction.json
```

The tests cover the area arithmetic, alternative slope denominator, Fe-OC source-row summaries, area occupation equivalents, stock endpoint reconstruction, dry-density sensitivity, porosity and wet-versus-dry diagnostics, and density-independent 14.2-Tg rounding result.

To build the paper, run this command three times from `manuscript/source/`:

```text
pdflatex --interaction=nonstopmode --halt-on-error --file-line-error --output-directory=../rendered Cold_Seep_Area_Reanalysis.tex
```

Third-party full texts are linked rather than redistributed. Primary-source URLs, locators, and qualifications are recorded in the [source-value record](evidence/SOURCE_VALUES.md).

## Attribution

Research candidate by **UCP Technology LLC**  
[ucptechnology.ai](https://ucptechnology.ai)

**Luigi** supplied the original scientific hypothesis and a subsequent scientific/editorial review. Review suggestions were treated as questions to test against primary evidence, not as evidence themselves.
