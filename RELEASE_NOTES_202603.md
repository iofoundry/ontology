# IOF Ontology — Release 202603

**Release date:** 2026-09-03
**Tag:** `Release_202603`
**Version IRI base:** `https://spec.industrialontologies.org/ontology/202603/`

This release has been merged to `master`. The notes below describe the changes relative to the previous release, **202602** (105 files changed, ~48,000 insertions / ~3,200 deletions across 384 commits).

---

## Highlights

- **New Biopharmaceutical Manufacturing suite (`biopharma`).** The NIIMBL-originated biopharma ontologies (transferred to IOF under the MIT license) are now published as a suite of modular ontologies, built on IOF Core and QUDT. Nine new modules were added and the existing modules substantially revised.
- **Maturity promotions.** Several reference ontologies advanced from *Provisional* to *Released*: **Maintenance**, **Supply Chain**, **Production Planning**, and **Certification**.
- **New Product Service System module.** A **Sensor** module was added to the Product Service System (PSS) ontology.
- **Core additions.** Material State terms were introduced into Core, `Container` was migrated from Supply Chain into Core, and temporal-relation / Allen interval algebra support was revised.
- **Unversioned imports throughout.** Import IRIs no longer embed a version; the catalog files resolve versioned IRIs to local files. Ontology prefixes were normalized across the repository.
- **Aggregation files.** Every domain now provides `AboutIOFProd` (imports Released content) and `AboutIOFDev` (imports Released + Provisional content). Load these from the root to bring in all ontologies.

---

## Maturity status changes

| Ontology | 202602 | 202603 |
|---|---|---|
| `maintenance/Maintenance` | Provisional | **Released** |
| `supplychain/SupplyChain` | Provisional | **Released** |
| `productionplanning/ProductionPlanning` | — | **Released** |
| `certification/Certification` | — | **Released** |
| `productservicesystem/ProductServiceSystem` | — | Provisional |
| `productservicesystem/Sensor` | — | Provisional (new) |

The authoritative maturity for each construct is the `iof-av:maturity` annotation asserted within each file; the README summary reflects those assertions for this release.

---

## Biopharmaceutical Manufacturing Ontologies (`biopharma`)

A suite of modular ontologies covering biopharmaceutical manufacturing, using IOF Core as its mid-level ontology and QUDT for unit–value pairs. Modules can be used together or independently.

**New modules added this release:**

- `MolecularEntity` **[Released]** — molecular entity populations and roles, chemical residues and moieties, biological sequences, and proteins.
- `TargetsLimitsRanges` **[Released]** — value-expression constructs for prescribed values, intervals, and thresholds (targets, ranges, setpoints) used in process control, quality control, and material conformance.
- `BiopharmaReferenceOntologyAttributes` **[Released]** — annotation constructs specific to the biopharma suite.
- `BiopharmaMaterialTesting` **[Provisional]** — testing activities linking analytical evidence, specifications, acceptance criteria, and out-of-specification results.
- `BiopharmaManufacturingProcessLifecycle` **[Provisional]** — how manufacturing processes are designed, characterized, qualified, validated, and monitored over time.
- `BiopharmaDeviationManagement` **[Provisional]** — deviations from approved plans, procedures, requirements, limits, and ranges, and how deviation events are documented and handled.
- `BiopharmaRiskManagement` **[Provisional]** — identification, analysis, evaluation, control, communication, and review of risks.
- `Statistics` **[Provisional]** — statistical models and analyses; integrates concepts from STATO within the IOF framework.
- `DesignOfExperiments` **[Provisional]** — extends Statistics with study design objectives, factor-level combinations, and design points.

**Existing modules (revised, now Released):** `BiopharmaAgent`, `BiopharmaEquipment`, `BiopharmaManufacturingExecution`, `BiopharmaMaterial`, `BiopharmaMaterialProcurementAndStorage`, `BiopharmaMonitoringAndControl`, `BiopharmaParameter`, `ManufacturingSystemOrganization`, and `Recipe` (with its procedural- and process-occurrence classification utilities).

A cached copy of **STATO** (`cache/STATO/`) was added to support the Statistics module. See the [biopharma README](biopharma/README.md) for detail.

---

## Core

- Added **Material State** terms to Core; the previous *complex material state* was removed and explanatory notes clarified.
- Migrated **`Container`** from Supply Chain into Core (removed from `SupplyChain.rdf`).
- Revised temporal-relation support: `TemporalRelationChain`, `TemporalRelationsInference` (SWRL), and `PrescribedAllenIntervalAlgebraUtility`.
- Refined `has pre-/post-condition`, `has process profile`, and material-containment capability examples.
- Corrected and polished natural-language and semi-formal definitions, capitalization, punctuation, and language attributes.
- Normalized ontology prefixes and updated `isDefinedBy` annotations across Core and the Annotation Vocabulary.

## Supply Chain (now Released)

- `Container` removed (migrated to Core).
- Fixed `MaterialTradeItem` and its role; added notes for ASN and Packing List.
- Fixed IRIs, language attributes, and `isDefinedBy` on new classes.

## Production Planning (now Released)

- Extensive addenda and worked examples added, including machining mapping files (OntoRefine), reasoning/consistency test A-Boxes, and new plastics examples (`plastics10_10_5`, `plastics10_16_4`) with diagrams.
- `catalog-v001-changes.xml` and a `recreate_catalog_file.py` helper script added under `etc/scripts`.

## Certification (now Released)

- Added `Metadatacertification.rdf`; cleaned up typos and the maturity-level individual prefixes.

## Product Service System

- Added new **`Sensor`** module (Provisional) for basic sensor entities and observations; fixed import issues.

---

## Structural / repository changes

- **Unversioned imports:** version numbers removed from `owl:imports`; catalog files map versioned IRIs to local files.
- **Version IRIs** updated to the `202603` namespace across all modules; copyright statements refreshed.
- **Aggregation files:** `AboutIOFProd` / `AboutIOFDev` provided per domain and at the repository root.
- Catalog files reconstructed to correctly associate ontology IRIs with local files.
- README substantially rewritten: current ontology status, aggregation-file guidance, biopharma suite overview, and updated external links (now under `oagi.org`).
- Removed the `.github/workflows/release.yml` workflow.
- Reasoner note updated: all ontologies verified consistent and satisfiable with HermiT in Protégé.

---

## Loading the ontologies

- **Released content only:** load the root `AboutIOFProd` aggregation file.
- **Released + Provisional content:** load the root `AboutIOFDev` aggregation file.

IOF recommends the desktop version of [Protégé](https://protege.stanford.edu/). The repository includes the catalog files needed to open the ontologies without warnings or errors.
