# Ontology Modules Metrics Report

## Overview

This report summarizes the metrics computed across all processed ontology modules. Below are the definitions for the counts and metrics:

- **Total Modules Processed:** Number of ontology files analyzed.
- **Total Classes:** Count of ontology concepts (entities typed as owl:Class or rdfs:Class).
- **Total Properties:** Count of properties (entities typed as rdf:Property or owl:AnnotationProperty).
- **Total Labels:** Count of rdfs:label annotations attached to entities.
- **Total Comments:** Count of rdfs:comment annotations attached to entities.
- **Total Imports:** Number of owl:imports statements indicating reuse of external ontologies.

- **Total Modules Processed:** **7**
- **Total Classes:** **1139**
- **Total Properties:** **45**
- **Total Labels:** **2261**
- **Total Comments:** **2**
- **Total Imports:** **9**

### AdaptedFrom Sources (Aggregated by Namespace)
The adaptedFrom property indicates the provenance or source from which parts of the ontology were adapted. To provide a concise overview, these sources have been aggregated by their namespace (the common base URI).

- **http://purl.obolibrary.org/obo/**: 906
- **https://de.wikipedia.org/wiki/**: 6
- **https://en.wikipedia.org/wiki/**: 45
- **https://simple.wikipedia.org/wiki/**: 1
- **https://www.britannica.com/science/**: 6
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
- **Average Hierarchy Depth:** 4.71
- **Maximum Hierarchy Breadth:** 102
- **Average Hierarchy Breadth:** 19.57

### Graph Connectivity Metrics (Overall)
These metrics are derived by modeling each ontology as an undirected graph, where nodes represent entities and edges represent relationships. - **Average Node Degree:** Reflects the average number of connections per entity, indicating overall interconnectedness.
- **Maximum Node Degree:** The maximum number of connections that any single entity has.

- **Average Node Degree:** 2.29
- **Maximum Node Degree:** 707

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
- **Imports Count:** 2

### Hierarchy Metrics
These metrics describe the subclass structure of the ontology:

- **Maximum Depth:** 0 (Longest chain of subclass relationships)
- **Average Depth:** 0.00 (Typical number of levels in the hierarchy)
- **Maximum Breadth:** 0 (Highest number of direct subclasses)
- **Average Breadth:** 0.00 (Average direct subclasses per class)

### Graph Connectivity Metrics
These metrics are derived from modeling the ontology as an undirected graph:

- **Average Node Degree:** 1.87 (Average connections per entity)
- **Maximum Node Degree:** 9 (Highest connections on a single entity)

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

- **Classes Count:** 211
- **Properties Count:** 10
- **Labels Count:** 424
- **Comments Count:** 0
- **Imports Count:** 1

### Hierarchy Metrics
These metrics describe the subclass structure of the ontology:

- **Maximum Depth:** 9 (Longest chain of subclass relationships)
- **Average Depth:** 5.45 (Typical number of levels in the hierarchy)
- **Maximum Breadth:** 19 (Highest number of direct subclasses)
- **Average Breadth:** 0.97 (Average direct subclasses per class)

### Graph Connectivity Metrics
These metrics are derived from modeling the ontology as an undirected graph:

- **Average Node Degree:** 2.40 (Average connections per entity)
- **Maximum Node Degree:** 211 (Highest connections on a single entity)

### Aggregated AdaptedFrom Sources (by Namespace)
This section shows the provenance of adapted content, aggregated by the common base URI.

- **http://purl.obolibrary.org/obo/**: 197
- **https://en.wikipedia.org/wiki/**: 2

---

## Module: Qualities-Chemical.rdf

**Abstract:** The IOF Qualities-Chemical Ontology aims to represent Qualities relevant to chemicals and chemical processes

The following metrics were computed for this ontology module:

- **Classes Count:** Number of defined ontology concepts (owl:Class and rdfs:Class).
- **Properties Count:** Number of properties (rdf:Property and owl:AnnotationProperty).
- **Labels Count:** Number of rdfs:label annotations.
- **Comments Count:** Number of rdfs:comment annotations.
- **Imports Count:** Number of owl:imports (external ontology references).

- **Classes Count:** 16
- **Properties Count:** 9
- **Labels Count:** 35
- **Comments Count:** 0
- **Imports Count:** 1

### Hierarchy Metrics
These metrics describe the subclass structure of the ontology:

- **Maximum Depth:** 3 (Longest chain of subclass relationships)
- **Average Depth:** 2.31 (Typical number of levels in the hierarchy)
- **Maximum Breadth:** 4 (Highest number of direct subclasses)
- **Average Breadth:** 0.44 (Average direct subclasses per class)

### Graph Connectivity Metrics
These metrics are derived from modeling the ontology as an undirected graph:

- **Average Node Degree:** 2.27 (Average connections per entity)
- **Maximum Node Degree:** 16 (Highest connections on a single entity)

### Aggregated AdaptedFrom Sources (by Namespace)
This section shows the provenance of adapted content, aggregated by the common base URI.

- **http://purl.obolibrary.org/obo/**: 3
- **https://en.wikipedia.org/wiki/**: 1

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

### Graph Connectivity Metrics
These metrics are derived from modeling the ontology as an undirected graph:

- **Average Node Degree:** 2.13 (Average connections per entity)
- **Maximum Node Degree:** 12 (Highest connections on a single entity)

### Aggregated AdaptedFrom Sources (by Namespace)
This section shows the provenance of adapted content, aggregated by the common base URI.

- **https://en.wikipedia.org/wiki/**: 1
- **“Precision.” Merriam-Webster.com Dictionary, Merriam-Webster, https://www.merriam-webster.com/dictionary/**: 1

---

## Module: Qualities-Morphologic.rdf

**Abstract:** The IOF Morphologic Qualities Ontology represents Qualities of material entities that describe the look and feel.

The following metrics were computed for this ontology module:

- **Classes Count:** Number of defined ontology concepts (owl:Class and rdfs:Class).
- **Properties Count:** Number of properties (rdf:Property and owl:AnnotationProperty).
- **Labels Count:** Number of rdfs:label annotations.
- **Comments Count:** Number of rdfs:comment annotations.
- **Imports Count:** Number of owl:imports (external ontology references).

- **Classes Count:** 707
- **Properties Count:** 4
- **Labels Count:** 1388
- **Comments Count:** 0
- **Imports Count:** 1

### Hierarchy Metrics
These metrics describe the subclass structure of the ontology:

- **Maximum Depth:** 8 (Longest chain of subclass relationships)
- **Average Depth:** 5.07 (Typical number of levels in the hierarchy)
- **Maximum Breadth:** 102 (Highest number of direct subclasses)
- **Average Breadth:** 1.05 (Average direct subclasses per class)

### Graph Connectivity Metrics
These metrics are derived from modeling the ontology as an undirected graph:

- **Average Node Degree:** 2.47 (Average connections per entity)
- **Maximum Node Degree:** 707 (Highest connections on a single entity)

### Aggregated AdaptedFrom Sources (by Namespace)
This section shows the provenance of adapted content, aggregated by the common base URI.

- **http://purl.obolibrary.org/obo/**: 690

---

## Module: Qualities-Physical.rdf

**Abstract:** The IOF Physical Qualities Ontology represents Qualities found in material entities (e.g., Mass).

The following metrics were computed for this ontology module:

- **Classes Count:** Number of defined ontology concepts (owl:Class and rdfs:Class).
- **Properties Count:** Number of properties (rdf:Property and owl:AnnotationProperty).
- **Labels Count:** Number of rdfs:label annotations.
- **Comments Count:** Number of rdfs:comment annotations.
- **Imports Count:** Number of owl:imports (external ontology references).

- **Classes Count:** 191
- **Properties Count:** 13
- **Labels Count:** 381
- **Comments Count:** 2
- **Imports Count:** 1

### Hierarchy Metrics
These metrics describe the subclass structure of the ontology:

- **Maximum Depth:** 7 (Longest chain of subclass relationships)
- **Average Depth:** 4.09 (Typical number of levels in the hierarchy)
- **Maximum Breadth:** 10 (Highest number of direct subclasses)
- **Average Breadth:** 0.88 (Average direct subclasses per class)

### Graph Connectivity Metrics
These metrics are derived from modeling the ontology as an undirected graph:

- **Average Node Degree:** 2.54 (Average connections per entity)
- **Maximum Node Degree:** 191 (Highest connections on a single entity)

### Aggregated AdaptedFrom Sources (by Namespace)
This section shows the provenance of adapted content, aggregated by the common base URI.

- **http://purl.obolibrary.org/obo/**: 16
- **https://de.wikipedia.org/wiki/**: 6
- **https://en.wikipedia.org/wiki/**: 41
- **https://simple.wikipedia.org/wiki/**: 1
- **https://www.britannica.com/science/**: 6
- **https://www.britannica.com/technology/**: 1
- **https://www.merriam-webster.com/dictionary/**: 2
- **https://www.nrc.gov/reading-rm/basic-ref/glossary/**: 1
- **https://www.oxfordreference.com/display/10.1093/oi/**: 1

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
- **Labels Count:** 11
- **Comments Count:** 0
- **Imports Count:** 2

### Hierarchy Metrics
These metrics describe the subclass structure of the ontology:

- **Maximum Depth:** 2 (Longest chain of subclass relationships)
- **Average Depth:** 1.57 (Typical number of levels in the hierarchy)
- **Maximum Breadth:** 0 (Highest number of direct subclasses)
- **Average Breadth:** 0.00 (Average direct subclasses per class)

### Graph Connectivity Metrics
These metrics are derived from modeling the ontology as an undirected graph:

- **Average Node Degree:** 2.32 (Average connections per entity)
- **Maximum Node Degree:** 15 (Highest connections on a single entity)

### Aggregated AdaptedFrom Sources (by Namespace)
This section shows the provenance of adapted content, aggregated by the common base URI.

- None found

---
