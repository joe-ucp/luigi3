# Source values and verification record

Checked 2026-09-02. This record covers the area constructions, independent
area context, Fe-OC inputs, sediment-mass sensitivity, and developmental-stage
domain examined in the paper. Page numbers are printed article pages.

| ID | Value or proposition | Primary location | Evidentiary status |
|---|---|---|---|
| O1 | Continental slopes cover `41 million km²` | Boetius & Wenzhöfer (2013), p. 725, opening paragraph; statement carries ref. 6 | Directly observed in coauthor-uploaded full text; bibliographic identity cross-checked against Nature and AWI |
| O2 | Global scaling assumes active seep systems occupy `~0.05%` of continental-slope area | Boetius & Wenzhöfer (2013), p. 731, “Methane emissions from cold seep ecosystems” | Directly observed; no citation marker is attached to the percentage/assumption |
| O3 | Boetius ref. 6 is Levin & Sibuet (2012) | Boetius & Wenzhöfer (2013), reference list, p. 733 | Directly observed |
| O4 | A primary predecessor defines a georeferenced 140–3,500 m deep-margin domain and computes approximately `40 million km²` | Menot et al. (2010), p. 80, Box 5.1 | Verified in the public VLIZ repository copy; supports the scale/domain, not the exact rounding path from 40 to 41 million |
| A1 | `0.05% = 0.0005`; `41,000,000 × 0.0005 = 20,500 km² = 2.05 × 10^4 km²` | Executable reconstruction and tests | Exact arithmetic; twenty tests pass |
| A2 | To obtain `205,000 km²` while retaining one printed premise requires either `0.5%`, `410,000,000 km²`, or an unreported `×10` | Executable audit and source checks | Exact inverse calculation; none of the required alternatives is present in the inspected sources |
| A3 | On a `41 million km²` slope domain, `20,500`, `205,000`, and `315,000 km²` correspond to `0.050%`, `0.500%`, and `0.768%` occupation | Executable reconstruction | Exact ratios; the published lower and upper areas encode occupation hypotheses 10.0 and 15.4 times the printed `0.05%` premise |
| A4 | A global geomorphic map assigns `19,606,260 km²` to continental slope; `0.05%` of that mask is `9,803.13 km²` | Harris et al. (2014), global geomorphic area table; executable reconstruction | Denominator-definition sensitivity only, not an empirical seep-area interval |
| J1 | Jiang publishes `2.05–3.15 × 10^5 km²` and jointly cites refs. 56–57 | Jiang et al. (2025), p. 4, Results and Discussion | Verified against the published version of record |
| J2 | Jiang ref. 56 is Boetius & Wenzhöfer (2013); ref. 57 is Li et al. (2024) | Jiang et al. (2025), p. 14 reference list | Directly observed |
| J3 | Jiang provides no derivation or data encoding for either area endpoint | Jiang main article, 32-page SI, all 26 Supplementary Data sheets, all 6 Source Data sheets | Exhaustive text/workbook search; bounded negative result |
| L1 | Li uses approximately `350 km²` active Haima area and more than `900` known seeps | Li et al. (2024), p. 6, right column | Verified against the published version of record |
| L2 | `350 × 900 = 315,000 km² = 3.15 × 10^5 km²` | Evaluation of Li's approximate area at a nominal count of 900 | Numerical fingerprint matching Jiang's reported upper endpoint; not an empirical upper bound because Li states approximately `350 km²` and more than `900` seeps |
| C1 | The slope-occupation and Haima-count constructions use different spatial objects and sampling frames and are not shown to share a common operational estimand, completeness model, or error structure | Comparison of Boetius & Wenzhöfer (2013), Li et al. (2024), Jiang et al. (2025), Yao et al. (2022), and Xu et al. (2020) | Demonstrated lack of a disclosed common interval-generating method; endpoint-to-source assignment remains a supported numerical-provenance inference because Jiang cites the two sources jointly |
| I1 | A global SEAFLEA compilation contains more than `10,000` anomalies but is presence-only, incomplete, biased, and mixes present and recent-past feature types | Phrampus et al. (2020), sections 1–2 | Not a census of cold seeps and not fractional active-sediment area; independent context for occurrence and inventory incompleteness |
| I2 | Regional surveys report approximately `570` plumes in `94,000 km²` on the northern U.S. Atlantic margin and `21,703` flares in `4,892 km²` in a Barents Sea leakage region | Skarke et al. (2014); Serov et al. (2024) | Raw densities differ by more than `700×`, but instruments, objects, and geological settings are not calibrated; evidence of heterogeneity, not a global estimator |
| I3 | Yao et al. repeat a literature descriptor of Haima as a `618 km²` field containing a `350 km²` area reported as active; 17 dives in Xu et al. observed at least six community and/or carbonate-mound patches | Yao et al. (2022); Xu et al. (2020) | Yao did not derive the polygon; Xu framed field-wide activity scale as poorly known before reporting the dive observations; evidence for scale distinction, not a global mean footprint |
| I4 | Ocean-to-atmosphere methane transfer depends strongly on depth, bubble properties, dissolution, and oxidation | Weber et al. (2019) | Methane budgets cannot be inverted to active-sediment area without a representative footprint-specific flux and transfer distribution |
| Y0 | Ye states that cold seeps cover less than `0.05%` of continental-slope area, then later applies `2.05–3.15 × 10^5 km²` to mature-seep Fe-OC | Ye et al. (2026), Introduction and section 4.3 | Directly observed within-article scale/domain inconsistency; no conversion between the two statements is supplied |
| Y1 | Mature-seep Fe-OC content is `0.14 ± 0.06%` of sediment dry mass | Ye et al. (2026), section 4.3 | Directly observed in official Wiley full text; distinct from the percentage of TOC associated with iron |
| Y2 | Ye upscales the 0–30 cm mature-seep mean using `2.05–3.15 × 10^5 km²`, cites Jiang and Li, and reports `142–218 Tg C` | Ye et al. (2026), section 4.3 | Directly observed in official Wiley full text |
| Y3 | Current-study mature rows: `n=14`, mean `0.108571...%`, sample SD `0.024133...%` | Ye OSF source data, Table S4 | Independently computed; rounds to the paper's `0.11 ± 0.02%` |
| Y4 | Historical mature rows: `n=8`, mean `0.195%`, sample SD `0.055806...%` | Ye OSF source data, Table S7 | Independently computed |
| Y5 | Combined mature depth rows: `n=22`, exact row-weighted mean `0.14%`, row sample SD `0.056653...%` | Ye OSF Tables S4 and S7 | Numerically matches `0.14 ± 0.06%`; the public files do not disclose the authors' aggregation rule, and this is not a site-level estimate, confidence interval, or global uncertainty |
| Y5b | Equal weighting of the current-study and Hu et al. source-block means gives `0.151786%` | Ye OSF Tables S4 and S7 | Descriptive weighting sensitivity only; source tables do not support a formal site-equal analysis |
| Y5a | All seep rows: `n=43`, mean `0.151860...%`, sample SD `0.050768...%` | Ye OSF Tables S4 and S7 | Independent adjacent cross-check; rounds to Ye's `0.15 ± 0.05%` all-seep summary |
| Y5c | Current-study early-stage rows: `n=21`, mean `0.164286%`, sample SD `0.041542%` | Ye OSF Table S4 | Reproduces the reported early-stage scale and shows that the current-study early mean exceeds the current-study mature mean; does not establish global stage means |
| Y6 | Standard stock identity: `stock_Tg = area_km² × depth_m × dry-bulk-density_g/cm³ × FeOC_percent / 100` | Dimensional mass balance | Unit-derived identity, not a formula printed by Ye |
| Y7 | With the explicit/data-derived inputs and an effective sediment-mass coefficient represented as `1.65 g cm⁻³`, the identity gives `142.065` and `218.295 Tg C` | Executable audit | Both values round to the published endpoints; the coefficient is reverse-engineered, nonunique, and not author-reported |
| Y8 | Changing only the lower area to `20,500 km²` gives `14.2065 Tg C`, or `14.2 Tg C`, under the compatible `1.65` reconstruction | Executable audit | Exact conditional counterfactual calculation |
| Y8a | Every common area-linear coefficient compatible with both printed integer endpoints gives a corrected lower stock in `[14.1548, 14.2198) Tg C` | Endpoint-rounding audit | Density-independent robustness result; the physical decomposition remains unidentified |
| Y9 | The effective `1.65 g cm⁻³` factor was not located in Ye's article, 30-page SI, public OSF DOCX, frozen OSF registration, registration metadata, or hidden DOCX text | Article/SI/OSF inspection | Explicit reporting gap; it is an inferred input compatible with both rounded endpoints, not a parameter attributed to Ye as printed text |
| D1 | Because Fe-OC is a percentage of dry sediment mass, the commensurate volume-to-mass term is dry bulk density: dry mass divided by original bulk volume | Dimensional mass balance; Chen et al. (2024), Methods and equations 5–6 | Demonstrated dimensional requirement; wet/saturated bulk density is not interchangeable with a dry-mass concentration |
| D2 | Conditional stocks at literature dry-density comparators `ρd = 0.9` and `1.3 g cm⁻³`, and at the endpoint-compatible effective coefficient `ρeff = 1.65 g cm⁻³`, are respectively `77.49–119.07`, `111.93–171.99`, and `142.07–218.30 Tg C` over the two published areas | Chen et al. (2024); Jiang et al. (2025); Li et al. (2024); executable reconstruction | Sensitivity rows, not confidence limits or preferred replacements for Ye's unmeasured mass coefficient |
| D3 | If the effective `1.65 g cm⁻³` coefficient is interpreted as `ρd` and grain density is the `2.70 g cm⁻³` mean measured by Riedel et al., the two-phase relation implies porosity `0.389` | Executable diagnostic; Riedel et al. (2006), Tang et al. (2025), and Huang et al. (2022) for context | The dry-density interpretation is high, and its implied porosity low, relative to available shallow-seep/hydrate-margin context but not physically impossible; does not prove Ye used a dry density of 1.65 |
| D4 | At illustrative porosity `0.65`, grain density `2.70 g cm⁻³`, and porewater density `1.024 g cm⁻³`, dry bulk density is `0.945 g cm⁻³` and saturated bulk density is `1.6106 g cm⁻³` | Executable two-phase diagnostic; Riedel et al. (2006) and Tang et al. (2025) for input context | Demonstrates why wet and dry coefficients can differ materially and why numerical proximity to `1.65` is diagnostically interesting; does not identify Ye's method |
| S1 | Ye's stock is framed as an eventual-mature scenario; a current mature-only, current all-active, and future mature stock require different area-stage mappings | Ye et al. (2026), section 4.3; Bowden et al. (2013) | Holding concentration and sediment mass per area fixed, total-active substitution for a current mature-only target multiplies by `1/fm`, is upward if `0 < fm < 1`, and is unchanged if `fm = 1`; all-active and future-mature directions remain unresolved |
| V1 | No indexed correction/update relation was located for Boetius, Jiang, Li, or Ye | Publisher pages, Crossref records; Jiang additionally checked in PMC/Europe PMC | Bounded negative search as of 2026-08-30 |

## Primary URLs

- Boetius & Wenzhöfer (2013): https://doi.org/10.1038/ngeo1926
- Coauthor-uploaded Boetius full-text page: https://www.researchgate.net/publication/260208770_Boetius_A_Wenzhfer_F_Seafloor_oxygen_consumption_fuelled_by_methane_from_cold_seeps_Nat_Geosci_6_725-734
- Levin & Sibuet (2012): https://doi.org/10.1146/annurev-marine-120709-142714
- Menot et al. (2010): https://doi.org/10.1002/9781444325508.ch5
- Harris et al. (2014): https://doi.org/10.1016/j.margeo.2014.01.011
- Jiang et al. (2025): https://doi.org/10.1038/s41467-025-56774-1
- Li et al. (2024): https://doi.org/10.1038/s43247-024-01484-7
- Ye et al. (2026): https://doi.org/10.1029/2025GB008889
- Phrampus et al. (2020): https://doi.org/10.1029/2019GC008747
- Skarke et al. (2014): https://doi.org/10.1038/ngeo2232
- Serov et al. (2024): https://doi.org/10.3389/feart.2024.1404027
- Weber et al. (2019): https://doi.org/10.1038/s41467-019-12541-7
- Yao et al. (2022): https://doi.org/10.3389/fmars.2022.920327
- Xu et al. (2020): https://doi.org/10.1016/j.seares.2020.101957
- Chen et al. (2024): https://doi.org/10.1038/s41467-024-50578-5
- Riedel et al. (2006): https://doi.org/10.2973/odp.proc.sr.204.104.2006
- Tang et al. (2025): https://doi.org/10.3389/fmars.2025.1714180
- Huang et al. (2022): https://doi.org/10.1016/j.egyr.2022.04.011
- Bowden et al. (2013): https://doi.org/10.1371/journal.pone.0076869
- Ye public source data: https://osf.io/6ymra
- Ye frozen OSF registration: https://osf.io/uesfy

## Qualification on the `41 million km²` ancestry

Boetius is the primary source in which the two load-bearing premises first
co-occur in this chain. It attributes `41 million km²` to Levin & Sibuet.
Levin & Sibuet's version of record is closed access and no lawful open copy was
located, so the exact inline route by which its cited 40–45-million-km² source
literature became `41 million` remains unverified. The complete Menot chapter
provides the closest primary georeferenced calculation (`~40 million km²`).
This bibliographic rounding gap does not affect the factor-of-ten test: every
inspected 30–45-million-km² slope/margin definition yields order `10^4 km²` at
`0.05%`, not `10^5 km²`.

## Qualification on Ye's unstated density factor

The secondary endpoint-compatibility check uses the mature-seep mean that Ye
prints and that a row-weighted calculation from its public rows numerically
reproduces; the authors' aggregation rule is undisclosed. An
effective coefficient represented as `1.65 g cm⁻³` returns values that round to
both stock endpoints. The joint coefficient interval that
would round to both printed endpoints is approximately
`[1.643991, 1.651550) g cm⁻³`, which includes `1.65`. Because Ye does not print
that coefficient or a stock equation, it must be described as a reverse-engineered,
nonunique effective factor, not as a reported method. This gap does not change
the controlled substitution:
holding Ye's calculation fixed and replacing only its lower area with a value
one-tenth as large makes its lower stock one-tenth as large.

The endpoint-rounding audit makes the approximate consequence independent of
selecting `1.65`: a single area-linear coefficient that rounds to both of Ye's
printed endpoints must put the corrected lower result between `14.1548` and
`14.2198 Tg C`. What remains unavailable is the authors' physical decomposition
of that coefficient.

If the endpoint-compatible coefficient is interpreted as dry bulk density,
`1.65 g cm⁻³` implies porosity `~0.39` for the `2.70 g cm⁻³` mean grain
density measured at a hydrate-margin analog. Available context includes a
`0.9 g cm⁻³` regional mean dry
bulk density, a Haima-model porosity of `0.65`, and approximately `0.55–0.75`
near-surface porosities at methane-seep/hydrate-margin analogs. These values
make `1.65` atypically high for unconsolidated shallow sediment, but they do
not establish a physical impossibility or a sample-specific replacement.
A separate Haima reservoir study reports an undepth-resolved porosity near
`0.40`. The paper therefore treats density as an unresolved and consequential
methodological term, not as a demonstrated author error.

## Qualification on developmental stage

The current mature sites in Ye are actively seeping, so current mature active
area can be modeled conditionally as a subset of total active area. Under a
current mature-only estimand, and holding concentration and sediment mass per
area fixed, replacing mature area with total active area multiplies stock by
`1/fm`, where `fm` is the unknown mature fraction. This is upward if
`0 < fm < 1` and unchanged if `fm = 1`. For an all-active-stage inventory the
sign depends on the area-weighted stage concentrations only if sediment mass
per area is common across stages; otherwise it also depends on stage-specific
mass coefficients. For Ye's eventual-mature scenario it depends on unmeasured
footprint persistence, stage duration, and successional dynamics.
