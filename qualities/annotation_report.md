# IOF Annotation Compliance Report

## Summary

| File | Terms checked | Terms with issues | Ontology-level issues |
|------|:---:|:---:|:---:|
| [Metadataqualities.rdf](#metadataqualitiesrdf) | 0 | 0 | 3 |
| [Qualities-Biological.rdf](#qualities-biologicalrdf) | 209 | 2 | 1 |
| [Qualities-Chemical.rdf](#qualities-chemicalrdf) | 14 | 1 | 1 |
| [Qualities-MeasurementPerformance.rdf](#qualities-measurementperformancerdf) | 7 | 0 | 1 |
| [Qualities-Morphological.rdf](#qualities-morphologicalrdf) | 706 | 11 | 2 |
| [Qualities-Physical.rdf](#qualities-physicalrdf) | 190 | 11 | 2 |
| [Qualities.rdf](#qualitiesrdf) | 7 | 4 | 1 |

**Total terms checked:** 1133  
**Total terms with issues:** 29  
**Total ontology-level issues:** 11

## Violation Breakdown (all files)

Ranked by frequency — use this to prioritise your work.

| # | Violation | Occurrences |
|---|-----------|:-----------:|
| 1 | [MUST] Missing iof-av:naturalLanguageDefinition | 12 |
| 2 | [MUST] Multiple English rdfs:label (2 found); exactly one required | 9 |
| 3 | [MUST] Missing rdfs:label entirely | 4 |
| 4 | [MUST] Multiple English naturalLanguageDefinition (2); exactly one allowed | 3 |
| 5 | [MUST] naturalLanguageDefinition starts with article 'A' | 2 |
| 6 | [MUST] Label case: word 'Type' is capitalised mid-label (use lowercase) | 1 |
| 7 | [MUST] Missing English iof-av:naturalLanguageDefinition | 1 |
| 8 | [MUST NOT] rdfs:comment used; replace with iof-av:explanatoryNote, iof-av:usageNote, or skos:scopeNote | 1 |
| 9 | [MUST] Missing English rdfs:label (lang='en' or 'en-US') | 1 |

---

## Metadataqualities.rdf

**Ontology IRI:** `https://spec.industrialontologies.org/ontology/qualities/Metadataqualities/`  
**Constructs:** 0 classes, 0 object properties, 0 data properties, 0 annotation properties (own namespace)  
**Terms checked:** 0 | **Terms with issues:** 0

### Ontology-level annotations

- **[MUST]** Ontology missing dcterms:title
- **[MUST]** Ontology missing iof-av:maturity
- **[MUST]** Ontology missing owl:versionInfo

_No construct violations found._

---

## Qualities-Biological.rdf

**Ontology IRI:** `https://spec.industrialontologies.org/ontology/qualities/Qualities-Biological/`  
**Constructs:** 209 classes, 0 object properties, 0 data properties, 0 annotation properties (own namespace)  
**Terms checked:** 209 | **Terms with issues:** 2

### Ontology-level annotations

- **[MUST]** Ontology missing owl:versionInfo

### Construct violations

MUST/MUST-NOT violations: **2** | SHOULD violations: **0**

#### `alpha mating Type (yeast)` (class)
IRI: `https://spec.industrialontologies.org/ontology/qualities/Qualities-Biological/AlphaMatingTypeYeast`

- **[MUST]** Label case: word 'Type' is capitalised mid-label (use lowercase)

#### `a mating type (yeast)` (class)
IRI: `https://spec.industrialontologies.org/ontology/qualities/Qualities-Biological/MatingTypeYeast`

- **[MUST]** naturalLanguageDefinition starts with article 'A'

---

## Qualities-Chemical.rdf

**Ontology IRI:** `https://spec.industrialontologies.org/ontology/qualities/Qualities-Chemical/`  
**Constructs:** 14 classes, 0 object properties, 0 data properties, 0 annotation properties (own namespace)  
**Terms checked:** 14 | **Terms with issues:** 1

### Ontology-level annotations

- **[MUST]** Ontology missing owl:versionInfo

### Construct violations

MUST/MUST-NOT violations: **1** | SHOULD violations: **0**

#### `chemical capability` (class)
IRI: `https://spec.industrialontologies.org/ontology/qualities/Qualities-Chemical/ChemicalCapability`

- **[MUST]** Multiple English naturalLanguageDefinition (2); exactly one allowed

---

## Qualities-MeasurementPerformance.rdf

**Ontology IRI:** `https://spec.industrialontologies.org/ontology/qualities/Qualities-MeasurementPerformance/`  
**Constructs:** 7 classes, 0 object properties, 0 data properties, 0 annotation properties (own namespace)  
**Terms checked:** 7 | **Terms with issues:** 0

### Ontology-level annotations

- **[MUST]** Ontology missing owl:versionInfo

_No construct violations found._

---

## Qualities-Morphological.rdf

**Ontology IRI:** `https://spec.industrialontologies.org/ontology/qualities/Qualities-Morphological/`  
**Constructs:** 706 classes, 0 object properties, 0 data properties, 0 annotation properties (own namespace)  
**Terms checked:** 706 | **Terms with issues:** 11

### Ontology-level annotations

- **[MUST]** Ontology missing iof-av:copyright
- **[MUST]** Ontology missing owl:versionInfo

### Construct violations

MUST/MUST-NOT violations: **11** | SHOULD violations: **0**

#### `cavities` (class)
IRI: `https://spec.industrialontologies.org/ontology/qualities/Qualities-Morphological/Cavities`

- **[MUST]** Missing iof-av:naturalLanguageDefinition

#### `coating` (class)
IRI: `https://spec.industrialontologies.org/ontology/qualities/Qualities-Morphological/Coating`

- **[MUST]** Missing iof-av:naturalLanguageDefinition

#### `Looseness` (class)
IRI: `https://spec.industrialontologies.org/ontology/qualities/Qualities-Morphological/Looseness`

- **[MUST]** Multiple English rdfs:label (2 found); exactly one required

#### `Medially Rotated` (class)
IRI: `https://spec.industrialontologies.org/ontology/qualities/Qualities-Morphological/MediallyRotated`

- **[MUST]** Multiple English rdfs:label (2 found); exactly one required

#### `metallic` (class)
IRI: `https://spec.industrialontologies.org/ontology/qualities/Qualities-Morphological/Metallic`

- **[MUST]** Missing iof-av:naturalLanguageDefinition

#### `natural color` (class)
IRI: `https://spec.industrialontologies.org/ontology/qualities/Qualities-Morphological/NaturalColor`

- **[MUST]** Missing iof-av:naturalLanguageDefinition

#### `Necrotic` (class)
IRI: `https://spec.industrialontologies.org/ontology/qualities/Qualities-Morphological/Necrotic`

- **[MUST]** Multiple English rdfs:label (2 found); exactly one required

#### `networked` (class)
IRI: `https://spec.industrialontologies.org/ontology/qualities/Qualities-Morphological/Networked`

- **[MUST]** Missing iof-av:naturalLanguageDefinition

#### `shovel shaped` (class)
IRI: `https://spec.industrialontologies.org/ontology/qualities/Qualities-Morphological/ShovelShaped`

- **[MUST]** Multiple English rdfs:label (2 found); exactly one required

#### `sickle shaped` (class)
IRI: `https://spec.industrialontologies.org/ontology/qualities/Qualities-Morphological/SickleShaped`

- **[MUST]** Multiple English rdfs:label (2 found); exactly one required

#### `wedge shaped` (class)
IRI: `https://spec.industrialontologies.org/ontology/qualities/Qualities-Morphological/WedgeShaped`

- **[MUST]** Multiple English rdfs:label (2 found); exactly one required

---

## Qualities-Physical.rdf

**Ontology IRI:** `https://spec.industrialontologies.org/ontology/qualities/Qualities-Physical/`  
**Constructs:** 188 classes, 0 object properties, 0 data properties, 2 annotation properties (own namespace)  
**Terms checked:** 190 | **Terms with issues:** 11

### Ontology-level annotations

- **[MUST]** Ontology missing iof-av:copyright
- **[MUST]** Ontology missing owl:versionInfo

### Construct violations

MUST/MUST-NOT violations: **15** | SHOULD violations: **0**

#### `pressure measurement capability` (class)
IRI: `https://spec.industrialontologies.org/ontology/materials/Materials/PressureMeasurementCapability`

- **[MUST]** Missing English iof-av:naturalLanguageDefinition

#### `breaking strength` (class)
IRI: `https://spec.industrialontologies.org/ontology/qualities/Qualities-Physical/BreakingStrength`

- **[MUST]** Multiple English naturalLanguageDefinition (2); exactly one allowed
- **[MUST NOT]** rdfs:comment used; replace with iof-av:explanatoryNote, iof-av:usageNote, or skos:scopeNote

#### `elastic strain` (class)
IRI: `https://spec.industrialontologies.org/ontology/qualities/Qualities-Physical/ElasticStrain`

- **[MUST]** Missing iof-av:naturalLanguageDefinition

#### `Voltage` (class)
IRI: `https://spec.industrialontologies.org/ontology/qualities/Qualities-Physical/ElectricPotential`

- **[MUST]** Multiple English rdfs:label (2 found); exactly one required

#### `FluidDynamicQuality` (class)
IRI: `https://spec.industrialontologies.org/ontology/qualities/Qualities-Physical/FluidDynamicQuality`

- **[MUST]** Missing English rdfs:label (lang='en' or 'en-US')

#### `force` (class)
IRI: `https://spec.industrialontologies.org/ontology/qualities/Qualities-Physical/Force`

- **[MUST]** Multiple English naturalLanguageDefinition (2); exactly one allowed

#### `aterial fatigue` (class)
IRI: `https://spec.industrialontologies.org/ontology/qualities/Qualities-Physical/MaterialFatigue`

- **[MUST]** Multiple English rdfs:label (2 found); exactly one required

#### `RadiationEmissonCapability` (class)
IRI: `https://spec.industrialontologies.org/ontology/qualities/Qualities-Physical/RadiationEmissonCapability`

- **[MUST]** Missing rdfs:label entirely
- **[MUST]** Missing iof-av:naturalLanguageDefinition

#### `logarithmic strain` (class)
IRI: `https://spec.industrialontologies.org/ontology/qualities/Qualities-Physical/TrueStrain`

- **[MUST]** Multiple English rdfs:label (2 found); exactly one required

#### `isTriggeredBy` (annotation property)
IRI: `https://spec.industrialontologies.org/ontology/qualities/Qualities-Physical/isTriggeredBy`

- **[MUST]** Missing rdfs:label entirely
- **[MUST]** Missing iof-av:naturalLanguageDefinition

#### `triggers` (annotation property)
IRI: `https://spec.industrialontologies.org/ontology/qualities/Qualities-Physical/triggers`

- **[MUST]** Missing rdfs:label entirely
- **[MUST]** Missing iof-av:naturalLanguageDefinition

---

## Qualities.rdf

**Ontology IRI:** `https://spec.industrialontologies.org/ontology/qualities/Qualities/`  
**Constructs:** 5 classes, 2 object properties, 0 data properties, 0 annotation properties (own namespace)  
**Terms checked:** 7 | **Terms with issues:** 4

### Ontology-level annotations

- **[MUST]** Ontology missing owl:versionInfo

### Construct violations

MUST/MUST-NOT violations: **5** | SHOULD violations: **0**

#### `dimension quality` (class)
IRI: `https://spec.industrialontologies.org/ontology/qualities/Qualities/DimensionQuality`

- **[MUST]** Missing iof-av:naturalLanguageDefinition

#### `spatial relational quality` (class)
IRI: `https://spec.industrialontologies.org/ontology/qualities/Qualities/SpatialRelationalQuality`

- **[MUST]** Missing iof-av:naturalLanguageDefinition

#### `ToBeReviewed` (class)
IRI: `https://spec.industrialontologies.org/ontology/qualities/Qualities/ToBeReviewed`

- **[MUST]** Missing rdfs:label entirely
- **[MUST]** Missing iof-av:naturalLanguageDefinition

#### `triggers` (object property)
IRI: `https://spec.industrialontologies.org/ontology/qualities/Qualities/triggers`

- **[MUST]** naturalLanguageDefinition starts with article 'A'

---
