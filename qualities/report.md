# Ontology Modules Metrics Report

## Overview

This report summarizes the metrics computed across all processed ontology modules. Below are the definitions for the counts and metrics:

- **Total Modules Processed:** Number of ontology files analyzed.
- **Total Classes:** Count of ontology concepts (entities typed as owl:Class or rdfs:Class).
- **Total Properties:** Count of properties (entities typed as rdf:Property or owl:AnnotationProperty).
- **Total Labels:** Count of rdfs:label annotations attached to entities.
- **Total Comments:** Count of rdfs:comment annotations attached to entities.
- **Total Imports:** Number of owl:imports statements indicating reuse of external ontologies.

- **Total Modules Processed:** **8**
- **Total Classes:** **1192**
- **Total Properties:** **45**
- **Total Labels:** **2367**
- **Total Comments:** **0**
- **Total Imports:** **15**

### AdaptedFrom Sources (Aggregated by Namespace)
The adaptedFrom property indicates the provenance or source from which parts of the ontology were adapted. To provide a concise overview, these sources have been aggregated by their namespace (the common base URI).

- **http://purl.obolibrary.org/obo/**: 906
- **https://de.wikipedia.org/wiki/**: 6
- **https://en.wikipedia.org/wiki/**: 45
- **https://simple.wikipedia.org/wiki/**: 1
- **https://w3id.org/pmd/co/**: 57
- **https://www.britannica.com/science/**: 7
- **https://www.britannica.com/technology/**: 1
- **https://www.merriam-webster.com/dictionary/**: 2
- **https://www.nrc.gov/reading-rm/basic-ref/glossary/**: 1
- **https://www.oxfordreference.com/display/10.1093/oi/**: 1
- **“Precision.” Merriam-Webster.com Dictionary, Merriam-Webster, https://www.merriam-webster.com/dictionary/**: 1

### Hierarchy Metrics (Overall)
These metrics describe the structure of the ontologies based on subclass relationships:
- **Maximum Hierarchy Depth:** The longest chain of subclass relationships from a root to a leaf class.
- **Average Hierarchy Depth:** The typical number of levels in the class hierarchy.
- **Maximum Hierarchy Breadth:** The highest number of direct subclasses any class has.
- **Average Hierarchy Breadth:** The average number of direct subclasses per class.

- **Maximum Hierarchy Depth:** 9
- **Average Hierarchy Depth:** 4.75
- **Maximum Hierarchy Breadth:** 102
- **Average Hierarchy Breadth:** 18.62

---

## Module: Qualities.rdf

**Abstract:** The IOF (common) Quality Ontology is an architectural construct allowing separate Quality ontologies for different domains e.g., Physical, Chemical, Biological, etc.
        This ontology also contains those qualities that may be considered 'common'.

The following metrics were computed for this ontology module:

- **Classes Count:** Number of defined ontology concepts (owl:Class and rdfs:Class).
- **Properties Count:** Number of properties (rdf:Property and owl:AnnotationProperty).
- **Labels Count:** Number of rdfs:label annotations.
- **Comments Count:** Number of rdfs:comment annotations.
- **Imports Count:** Number of owl:imports (external ontology references).

- **Classes Count:** 7
- **Properties Count:** 0
- **Labels Count:** 12
- **Comments Count:** 0
- **Imports Count:** 2

### Hierarchy Metrics
These metrics describe the subclass structure of the ontology:

- **Maximum Depth:** 2 (Longest chain of subclass relationships)
- **Average Depth:** 1.57 (Typical number of levels in the hierarchy)
- **Maximum Breadth:** 0 (Highest number of direct subclasses)
- **Average Breadth:** 0.00 (Average direct subclasses per class)

### Aggregated AdaptedFrom Sources (by Namespace)
This section shows the provenance of adapted content, aggregated by the common base URI.

- None found

---

## Module: Qualities-Biological.rdf

**Abstract:** The IOF Biological Qualities Ontology aims to represent the generic constructs (including classes and properties) related to biological qualities.

The following metrics were computed for this ontology module:

- **Classes Count:** Number of defined ontology concepts (owl:Class and rdfs:Class).
- **Properties Count:** Number of properties (rdf:Property and owl:AnnotationProperty).
- **Labels Count:** Number of rdfs:label annotations.
- **Comments Count:** Number of rdfs:comment annotations.
- **Imports Count:** Number of owl:imports (external ontology references).

- **Classes Count:** 216
- **Properties Count:** 10
- **Labels Count:** 434
- **Comments Count:** 0
- **Imports Count:** 1

### Hierarchy Metrics
These metrics describe the subclass structure of the ontology:

- **Maximum Depth:** 9 (Longest chain of subclass relationships)
- **Average Depth:** 5.41 (Typical number of levels in the hierarchy)
- **Maximum Breadth:** 19 (Highest number of direct subclasses)
- **Average Breadth:** 0.97 (Average direct subclasses per class)

### Aggregated AdaptedFrom Sources (by Namespace)
This section shows the provenance of adapted content, aggregated by the common base URI.

- **http://purl.obolibrary.org/obo/**: 197
- **https://en.wikipedia.org/wiki/**: 2
- **https://w3id.org/pmd/co/**: 5

---

## Module: Qualities-Physical.rdf

**Abstract:** The IOF Physical Qualities Ontology represents Qualities found in material entities (e.g., Mass).

The following metrics were computed for this ontology module:

- **Classes Count:** Number of defined ontology concepts (owl:Class and rdfs:Class).
- **Properties Count:** Number of properties (rdf:Property and owl:AnnotationProperty).
- **Labels Count:** Number of rdfs:label annotations.
- **Comments Count:** Number of rdfs:comment annotations.
- **Imports Count:** Number of owl:imports (external ontology references).

- **Classes Count:** 218
- **Properties Count:** 13
- **Labels Count:** 437
- **Comments Count:** 0
- **Imports Count:** 1

### Hierarchy Metrics
These metrics describe the subclass structure of the ontology:

- **Maximum Depth:** 7 (Longest chain of subclass relationships)
- **Average Depth:** 4.12 (Typical number of levels in the hierarchy)
- **Maximum Breadth:** 13 (Highest number of direct subclasses)
- **Average Breadth:** 0.90 (Average direct subclasses per class)

### Aggregated AdaptedFrom Sources (by Namespace)
This section shows the provenance of adapted content, aggregated by the common base URI.

- **http://purl.obolibrary.org/obo/**: 16
- **https://de.wikipedia.org/wiki/**: 6
- **https://en.wikipedia.org/wiki/**: 41
- **https://simple.wikipedia.org/wiki/**: 1
- **https://w3id.org/pmd/co/**: 33
- **https://www.britannica.com/science/**: 7
- **https://www.britannica.com/technology/**: 1
- **https://www.merriam-webster.com/dictionary/**: 2
- **https://www.nrc.gov/reading-rm/basic-ref/glossary/**: 1
- **https://www.oxfordreference.com/display/10.1093/oi/**: 1

---

## Module: Qualities-MaterialStructure.rdf

The following metrics were computed for this ontology module:

- **Classes Count:** Number of defined ontology concepts (owl:Class and rdfs:Class).
- **Properties Count:** Number of properties (rdf:Property and owl:AnnotationProperty).
- **Labels Count:** Number of rdfs:label annotations.
- **Comments Count:** Number of rdfs:comment annotations.
- **Imports Count:** Number of owl:imports (external ontology references).

- **Classes Count:** 15
- **Properties Count:** 0
- **Labels Count:** 30
- **Comments Count:** 0
- **Imports Count:** 0

### Hierarchy Metrics
These metrics describe the subclass structure of the ontology:

- **Maximum Depth:** 4 (Longest chain of subclass relationships)
- **Average Depth:** 3.00 (Typical number of levels in the hierarchy)
- **Maximum Breadth:** 9 (Highest number of direct subclasses)
- **Average Breadth:** 0.87 (Average direct subclasses per class)

### Aggregated AdaptedFrom Sources (by Namespace)
This section shows the provenance of adapted content, aggregated by the common base URI.

- **https://w3id.org/pmd/co/**: 13

---

## Module: Metadataqualities.rdf

**Abstract:** The IOF (common) Quality Ontology is an architectural construct allowing separate Quality ontologies for different domains e.g., Physical, Chemical, Biological, etc.
        This ontology also contains those qualities that may be considered 'common'

The following metrics were computed for this ontology module:

- **Classes Count:** Number of defined ontology concepts (owl:Class and rdfs:Class).
- **Properties Count:** Number of properties (rdf:Property and owl:AnnotationProperty).
- **Labels Count:** Number of rdfs:label annotations.
- **Comments Count:** Number of rdfs:comment annotations.
- **Imports Count:** Number of owl:imports (external ontology references).

- **Classes Count:** 0
- **Properties Count:** 0
- **Labels Count:** 2
- **Comments Count:** 0
- **Imports Count:** 8

### Hierarchy Metrics
These metrics describe the subclass structure of the ontology:

- **Maximum Depth:** 0 (Longest chain of subclass relationships)
- **Average Depth:** 0.00 (Typical number of levels in the hierarchy)
- **Maximum Breadth:** 0 (Highest number of direct subclasses)
- **Average Breadth:** 0.00 (Average direct subclasses per class)

### Aggregated AdaptedFrom Sources (by Namespace)
This section shows the provenance of adapted content, aggregated by the common base URI.

- None found

---

## Module: Qualities-MeasurementPerformance.rdf

**Abstract:** This Submodule, Measurement Performance Qualities, of the IOF Qualities Ontology aims to represent the generic constructs (including classes and properties) related bfo qualities covering Measurement Performance.

The following metrics were computed for this ontology module:

- **Classes Count:** Number of defined ontology concepts (owl:Class and rdfs:Class).
- **Properties Count:** Number of properties (rdf:Property and owl:AnnotationProperty).
- **Labels Count:** Number of rdfs:label annotations.
- **Comments Count:** Number of rdfs:comment annotations.
- **Imports Count:** Number of owl:imports (external ontology references).

- **Classes Count:** 7
- **Properties Count:** 9
- **Labels Count:** 20
- **Comments Count:** 0
- **Imports Count:** 1

### Hierarchy Metrics
These metrics describe the subclass structure of the ontology:

- **Maximum Depth:** 4 (Longest chain of subclass relationships)
- **Average Depth:** 2.86 (Typical number of levels in the hierarchy)
- **Maximum Breadth:** 2 (Highest number of direct subclasses)
- **Average Breadth:** 0.57 (Average direct subclasses per class)

### Aggregated AdaptedFrom Sources (by Namespace)
This section shows the provenance of adapted content, aggregated by the common base URI.

- **https://en.wikipedia.org/wiki/**: 1
- **“Precision.” Merriam-Webster.com Dictionary, Merriam-Webster, https://www.merriam-webster.com/dictionary/**: 1

---

## Module: Qualities-Chemical.rdf

**Abstract:** The IOF Qualities-Chemical Ontology aims to represent Qualities relevant to chemicals and chemical processes

The following metrics were computed for this ontology module:

- **Classes Count:** Number of defined ontology concepts (owl:Class and rdfs:Class).
- **Properties Count:** Number of properties (rdf:Property and owl:AnnotationProperty).
- **Labels Count:** Number of rdfs:label annotations.
- **Comments Count:** Number of rdfs:comment annotations.
- **Imports Count:** Number of owl:imports (external ontology references).

- **Classes Count:** 22
- **Properties Count:** 9
- **Labels Count:** 47
- **Comments Count:** 0
- **Imports Count:** 1

### Hierarchy Metrics
These metrics describe the subclass structure of the ontology:

- **Maximum Depth:** 4 (Longest chain of subclass relationships)
- **Average Depth:** 2.68 (Typical number of levels in the hierarchy)
- **Maximum Breadth:** 4 (Highest number of direct subclasses)
- **Average Breadth:** 0.59 (Average direct subclasses per class)

### Aggregated AdaptedFrom Sources (by Namespace)
This section shows the provenance of adapted content, aggregated by the common base URI.

- **http://purl.obolibrary.org/obo/**: 3
- **https://en.wikipedia.org/wiki/**: 1
- **https://w3id.org/pmd/co/**: 6

---

## Module: Qualities-Morphological.rdf

**Abstract:** The IOF Morphological Qualities Ontology represents Qualities of material entities that describe the look and feel.

The following metrics were computed for this ontology module:

- **Classes Count:** Number of defined ontology concepts (owl:Class and rdfs:Class).
- **Properties Count:** Number of properties (rdf:Property and owl:AnnotationProperty).
- **Labels Count:** Number of rdfs:label annotations.
- **Comments Count:** Number of rdfs:comment annotations.
- **Imports Count:** Number of owl:imports (external ontology references).

- **Classes Count:** 707
- **Properties Count:** 4
- **Labels Count:** 1385
- **Comments Count:** 0
- **Imports Count:** 1

### Hierarchy Metrics
These metrics describe the subclass structure of the ontology:

- **Maximum Depth:** 8 (Longest chain of subclass relationships)
- **Average Depth:** 5.07 (Typical number of levels in the hierarchy)
- **Maximum Breadth:** 102 (Highest number of direct subclasses)
- **Average Breadth:** 1.05 (Average direct subclasses per class)

### Aggregated AdaptedFrom Sources (by Namespace)
This section shows the provenance of adapted content, aggregated by the common base URI.

- **http://purl.obolibrary.org/obo/**: 690

---
