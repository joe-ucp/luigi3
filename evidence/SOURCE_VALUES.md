# Source values and verification record

Checked 2026-08-30. This record covers only the inputs in the paper's
area-to-stock chain. Page numbers are printed article pages.

| ID | Value or proposition | Primary location | Evidentiary status |
|---|---|---|---|
| O1 | Continental slopes cover `41 million km²` | Boetius & Wenzhöfer (2013), p. 725, opening paragraph; statement carries ref. 6 | Directly observed in coauthor-uploaded full text; bibliographic identity cross-checked against Nature and AWI |
| O2 | Global scaling assumes active seep systems occupy `~0.05%` of continental-slope area | Boetius & Wenzhöfer (2013), p. 731, “Methane emissions from cold seep ecosystems” | Directly observed; no citation marker is attached to the percentage/assumption |
| O3 | Boetius ref. 6 is Levin & Sibuet (2012) | Boetius & Wenzhöfer (2013), reference list, p. 733 | Directly observed |
| O4 | A primary predecessor defines a georeferenced 140–3,500 m deep-margin domain and computes approximately `40 million km²` | Menot et al. (2010), p. 80, Box 5.1 | Verified in the public VLIZ repository copy; supports the scale/domain, not the exact rounding path from 40 to 41 million |
| A1 | `0.05% = 0.0005`; `41,000,000 × 0.0005 = 20,500 km² = 2.05 × 10^4 km²` | Executable audit and tests | Exact arithmetic; fifteen tests pass |
| A2 | To obtain `205,000 km²` while retaining one printed premise requires either `0.5%`, `410,000,000 km²`, or an unreported `×10` | Executable audit and source checks | Exact inverse calculation; none of the required alternatives is present in the inspected sources |
| J1 | Jiang publishes `2.05–3.15 × 10^5 km²` and jointly cites refs. 56–57 | Jiang et al. (2025), p. 4, Results and Discussion | Verified against the published version of record |
| J2 | Jiang ref. 56 is Boetius & Wenzhöfer (2013); ref. 57 is Li et al. (2024) | Jiang et al. (2025), p. 14 reference list | Directly observed |
| J3 | Jiang provides no derivation or data encoding for either area endpoint | Jiang main article, 32-page SI, all 26 Supplementary Data sheets, all 6 Source Data sheets | Exhaustive text/workbook search; bounded negative result |
| L1 | Li uses approximately `350 km²` active Haima area and more than `900` known seeps | Li et al. (2024), p. 6, right column | Verified against the published version of record |
| L2 | `350 × 900 = 315,000 km² = 3.15 × 10^5 km²` | Evaluation of Li's approximate area at a nominal count of 900 | Numerical fingerprint matching Jiang's reported upper endpoint; not an empirical upper bound because Li states approximately `350 km²` and more than `900` seeps |
| Y1 | Mature-seep Fe-OC content is `0.14 ± 0.06%` of sediment dry mass | Ye et al. (2026), section 4.3 | Directly observed in official Wiley full text; distinct from the percentage of TOC associated with iron |
| Y2 | Ye upscales the 0–30 cm mature-seep mean using `2.05–3.15 × 10^5 km²`, cites Jiang and Li, and reports `142–218 Tg C` | Ye et al. (2026), section 4.3 | Directly observed in official Wiley full text |
| Y3 | Current-study mature rows: `n=14`, mean `0.108571...%`, sample SD `0.024133...%` | Ye OSF source data, Table S4 | Independently computed; rounds to the paper's `0.11 ± 0.02%` |
| Y4 | Historical mature rows: `n=8`, mean `0.195%`, sample SD `0.055806...%` | Ye OSF source data, Table S7 | Independently computed |
| Y5 | Combined mature depth rows: `n=22`, exact row-weighted mean `0.14%`, row sample SD `0.056653...%` | Ye OSF Tables S4 and S7 | Numerically matches `0.14 ± 0.06%`; the public files do not disclose the authors' aggregation rule, and this is not a site-level estimate, confidence interval, or global uncertainty |
| Y5b | Equal weighting of the current-study and Hu et al. source-block means gives `0.151786%` | Ye OSF Tables S4 and S7 | Descriptive weighting sensitivity only; source tables do not support a formal site-equal analysis |
| Y5a | All seep rows: `n=43`, mean `0.151860...%`, sample SD `0.050768...%` | Ye OSF Tables S4 and S7 | Independent adjacent cross-check; rounds to Ye's `0.15 ± 0.05%` all-seep summary |
| Y6 | Standard stock identity: `stock_Tg = area_km² × depth_m × dry-bulk-density_g/cm³ × FeOC_percent / 100` | Dimensional mass balance | Unit-derived identity, not a formula printed by Ye |
| Y7 | With the explicit/data-derived inputs and an effective sediment-mass coefficient represented as `1.65 g cm⁻³`, the identity gives `142.065` and `218.295 Tg C` | Executable audit | Both values round to the published endpoints; the coefficient is reverse-engineered, nonunique, and not author-reported |
| Y8 | Changing only the lower area to `20,500 km²` gives `14.2065 Tg C`, or `14.2 Tg C`, under the compatible `1.65` reconstruction | Executable audit | Exact conditional counterfactual calculation |
| Y8a | Every common area-linear coefficient compatible with both printed integer endpoints gives a corrected lower stock in `[14.1548, 14.2198) Tg C` | Endpoint-rounding audit | Density-independent robustness result; the physical decomposition remains unidentified |
| Y9 | The effective `1.65 g cm⁻³` factor was not located in Ye's article, 30-page SI, public OSF DOCX, frozen OSF registration, registration metadata, or hidden DOCX text | Article/SI/OSF inspection | Explicit reporting gap; it is an inferred input compatible with both rounded endpoints, not a parameter attributed to Ye as printed text |
| V1 | No indexed correction/update relation was located for Boetius, Jiang, Li, or Ye | Publisher pages, Crossref records; Jiang additionally checked in PMC/Europe PMC | Bounded negative search as of 2026-08-30 |

## Primary URLs

- Boetius & Wenzhöfer (2013): https://doi.org/10.1038/ngeo1926
- Coauthor-uploaded Boetius full-text page: https://www.researchgate.net/publication/260208770_Boetius_A_Wenzhfer_F_Seafloor_oxygen_consumption_fuelled_by_methane_from_cold_seeps_Nat_Geosci_6_725-734
- Levin & Sibuet (2012): https://doi.org/10.1146/annurev-marine-120709-142714
- Menot et al. (2010): https://doi.org/10.1002/9781444325508.ch5
- Jiang et al. (2025): https://doi.org/10.1038/s41467-025-56774-1
- Li et al. (2024): https://doi.org/10.1038/s43247-024-01484-7
- Ye et al. (2026): https://doi.org/10.1029/2025GB008889
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
