# Qualities Module

## Overview

This module contains a curated subset of quality-related terms harvested from [PATO](https://obofoundry.org/ontology/pato.html). The extracted subclass hierarchy is aligned under [BFO:Quality](http://purl.obolibrary.org/obo/BFO_0000019) and categorizes qualities into major groups such as biological, chemical, physical, and performance qualities. In particular, it emphasizes morphological qualities by including many mechanical quality terms and reusing core PATO concepts such as size, shape, texture, structure, color, odor, and spatial pattern. The module also incorporates organismal and cellular qualities as subclasses of biological quality.

**Translation Information:**
Additionally, this module features German translations for all terms. Initially created using an AI-generated output (text-davinci-003) followed by manual revisions.

## Metrics

Metrics on the ontology modules can be found in the [Metrics Report](./report.md)

## Annotation Compliance

All terms in this module comply with the [IOF Annotation Vocabulary](https://spec.industrialontologies.org/ontology/core/meta/AnnotationVocabulary/) principles defined in `annotation_principles.md`. Compliance is verified by the `annotation_checker.py` script and all known MUST violations have been resolved.

### Tooling

#### `annotation_checker.py`

Checks every term in the module against the IOF annotation principles and generates a Markdown compliance report (`annotation_report.md`).

```bash
# Check all files in the qualities/ directory (MUST violations only)
python annotation_checker.py --directory qualities/ --no-should

# Check all files including SHOULD recommendations
python annotation_checker.py --directory qualities/

# Check a single file
python annotation_checker.py --file qualities/Qualities-Physical.rdf

# Write report to a custom location
python annotation_checker.py --directory qualities/ --output my_report.md
```

Rules checked include:
- Every term has exactly one English `rdfs:label` (lowercase)
- Every term has exactly one English `iof-av:naturalLanguageDefinition` (not starting with an article)
- No `rdfs:comment` annotations (use NLD instead)
- Primitive classes have `iof-av:isPrimitive=true` and `iof-av:primitiveRationale`
- Non-primitive classes have `iof-av:firstOrderLogicDefinition` and `iof-av:semiFormalNaturalLanguageDefinition`
- German label and NLD present (SHOULD)
- Ontology-level annotations present (`iof-av:maturity`, `iof-av:copyright`, `owl:versionInfo`)

#### `fol_fixer.py`

Automatically resolves annotation gaps by analysing each class and applying one of the following actions:

| Condition | Action |
|---|---|
| Has `owl:equivalentClass`, no FOL definition | Generate `firstOrderLogicDefinition` + `semiFormalNaturalLanguageDefinition` from the OWL axiom |
| Has `owl:equivalentClass` but marked `isPrimitive=true` | Clear the primitive flag (formal axiom takes precedence) |
| No `owl:equivalentClass`, no FOL definition | Add `isPrimitive=true` + generated `primitiveRationale` |
| `isPrimitive=true` but no rationale | Add generated `primitiveRationale` |

The script is **re-entrant**: once a formal OWL axiom is added to a previously primitive term, re-running the script automatically promotes it to a formally defined term.

```bash
# Dry run — preview planned changes (default)
python fol_fixer.py --directory qualities/

# Apply to a single file for testing
python fol_fixer.py --file qualities/Qualities-Physical.rdf --apply

# Apply to all files
python fol_fixer.py --directory qualities/ --apply
```

## Source and Provenance

- **Primary Source Ontology:**  
  [PATO (Phenotype And Trait Ontology)](https://obofoundry.org/ontology/pato.html)

- **Alignment:**  
  The harvested qualities are organized as a subclass hierarchy under [BFO:Quality](http://purl.obolibrary.org/obo/BFO_0000019).

- **Imported Annotations:**  
  Quality terms include references marked with [adaptedFrom](https://spec.industrialontologies.org/ontology/core/meta/AnnotationVocabulary/adaptedFrom).

## Usage

This module is designed to be incorporated into ontology projects where quality attributes play a role. It serves as a reference for:
- Assigning quality attributes in biological, chemical, physical, and performance contexts.
- Enriching morphological data with standardized measures (e.g., size, shape, texture).
- Supporting multilingual applications via provided German translations.

## Contributing

Contributions to improve term curation, translation quality, or alignment with source ontologies are welcome. Please submit pull requests or open issues on the repository.

