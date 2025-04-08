# Ontology Modules Metrics Report

## Overview

This report summarizes the metrics computed across all processed ontology modules. Below are the definitions for the counts and metrics:

- **Total Modules Processed:** Number of ontology files analyzed.
- **Total Classes:** Count of ontology concepts (entities typed as owl:Class or rdfs:Class).
- **Total Properties:** Count of properties (entities typed as rdf:Property or owl:AnnotationProperty).
- **Total Labels:** Count of rdfs:label annotations attached to entities.
- **Total Comments:** Count of rdfs:comment annotations attached to entities.
- **Total Imports:** Number of owl:imports statements indicating reuse of external ontologies.

- **Total Modules Processed:** **2**
- **Total Classes:** **47**
- **Total Properties:** **6**
- **Total Labels:** **62**
- **Total Comments:** **1**
- **Total Imports:** **5**

### AdaptedFrom Sources (Aggregated by Namespace)
The adaptedFrom property indicates the provenance or source from which parts of the ontology were adapted. To provide a concise overview, these sources have been aggregated by their namespace (the common base URI).

- None found

### Hierarchy Metrics (Overall)
These metrics describe the structure of the ontologies based on subclass relationships:
- **Maximum Hierarchy Depth:** The longest chain of subclass relationships from a root to a leaf class.
- **Average Hierarchy Depth:** The typical number of levels in the class hierarchy.
- **Maximum Hierarchy Breadth:** The highest number of direct subclasses any class has.
- **Average Hierarchy Breadth:** The average number of direct subclasses per class.

- **Maximum Hierarchy Depth:** 3
- **Average Hierarchy Depth:** 1.50
- **Maximum Hierarchy Breadth:** 4
- **Average Hierarchy Breadth:** 2.00

### Graph Connectivity Metrics (Overall)
These metrics are derived by modeling each ontology as an undirected graph, where nodes represent entities and edges represent relationships. - **Average Node Degree:** Reflects the average number of connections per entity, indicating overall interconnectedness.
- **Maximum Node Degree:** The maximum number of connections that any single entity has.

- **Average Node Degree:** 2.11
- **Maximum Node Degree:** 47

---

## Module: Materials.rdf

**Abstract:** The IOF Materials Ontology aims to represent the generic constructs (including classes and properties) related to the domain of material science and engineering. The Materials Ontology uses BFO as the top-level ontology and IOF Core as the mid-level ontology. The purpose of the ontology is to serve as a foundation for ensuring consistency and interoperability across various material science and engineering ontologies that use IOF reference ontologies.

The following metrics were computed for this ontology module:

- **Classes Count:** Number of defined ontology concepts (owl:Class and rdfs:Class).
- **Properties Count:** Number of properties (rdf:Property and owl:AnnotationProperty).
- **Labels Count:** Number of rdfs:label annotations.
- **Comments Count:** Number of rdfs:comment annotations.
- **Imports Count:** Number of owl:imports (external ontology references).

- **Classes Count:** 47
- **Properties Count:** 6
- **Labels Count:** 60
- **Comments Count:** 1
- **Imports Count:** 3

### Hierarchy Metrics
These metrics describe the subclass structure of the ontology:

- **Maximum Depth:** 3 (Longest chain of subclass relationships)
- **Average Depth:** 1.96 (Typical number of levels in the hierarchy)
- **Maximum Breadth:** 4 (Highest number of direct subclasses)
- **Average Breadth:** 0.51 (Average direct subclasses per class)

### Graph Connectivity Metrics
These metrics are derived from modeling the ontology as an undirected graph:

- **Average Node Degree:** 2.22 (Average connections per entity)
- **Maximum Node Degree:** 47 (Highest connections on a single entity)

### Aggregated AdaptedFrom Sources (by Namespace)
This section shows the provenance of adapted content, aggregated by the common base URI.

- None found

---

## Module: Metadatamaterials.rdf

**Abstract:** The IOF Materials Meta Ontology specifies the metada for the IOF Materials Ontology Library

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

- **Average Node Degree:** 2.00 (Average connections per entity)
- **Maximum Node Degree:** 9 (Highest connections on a single entity)

### Aggregated AdaptedFrom Sources (by Namespace)
This section shows the provenance of adapted content, aggregated by the common base URI.

- None found

---
