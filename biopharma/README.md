# Biopharmaceutical Manufacturing Ontologies

## About Biopharmaceutical Manufacturing Ontologies

Biopharmaceutical Manufacturing Ontologies contain notions found to be common across biopharmaceutical manufacturing, intially developed as the National Institute for Innovation in Manufacturing Biopharmaceuticals (NIIMBL) Ontology and transfered to IOF under the MIT license. The files provided are an RDF implementation of these notions. All the ontologies are currently in the draft stage and are as such labeled as Provisional.

Biopharmaceutical Manufacturing Ontologies utilize  the  Industrial Ontologies Foundry Core ontology as its mid-level ontology. The purpose of the IOF Core ontology is to serve as a foundation for ensuring consistency and interoperability across the Biopharmaceutical Manufacturing Ontologies. Biopharmaceutical Manufacturing Ontologies also use the Quantities, Units, Dimensions and Types (QUDT) Ontologies to ensure consistent representation of unit-value pairs. The utilization of the QUDT ontology conforms to the guideline published by IOF (LINK). 

The ontology modules include Agent, Equipment, Manufacturing Execution, Material, Material Procurement & Storage, Monitoring & Control, Parameter, Physical, and Recipe.  Below is a diagram depiciting relationships between the modules themselves. The ontology modules are structured such that they can be used together or independently depending on the application purpose. 

Details on the modules are as follow:

### Agent

The Agent module contains terms and relations necessary for representing various types of agents (actors) in biopharmaceutical manufacturing. The actors here correspond to both human actors as well as engineered systems and organizations.

### Equipment

The Equipment module contains terms and relations enabling representation of equipment types, properties (qualities, capabilities, and functions), equipment specifications and validation (e.g., methods, testing, reporting, etc.).

### Manufacturing Execution

The Manufacturing Execution module contains terms and relations necessary for representing the actual occurrences of manufacturing processes with respect to recipes.

### Material

The Material module contains terms and relations enabling representation of material types and their associated properties. Terms for characterizing material usages in internal operation systems are also included (e.g., consumable, process intermediate, final product…).

### Material Procurement & Storage

The Material Procurement & Storage module contains terms and relations for tracking and tracing of materials. The purpose of the module is to provide support for use cases related to connecting process control to raw material procurement as well as for use cases related to regulatory compliance.

### Monitoring & Control

The Monitoring & Control module contains terms and relations necessary for representing the planning and execution of monitoring and/or controlling for both laboratory and manufacturing scale.

### Parameter

The Parameter module contains terms and relations necessary for representing process intermediate and product quality attributes, process indicators and process parameters.

### Physical

The Physical module contains terms and relations to represent the physical spaces where processing and storage occurs. Spaces are specific and bounded geographic locations which can be heirarchical and embedded.

### Recipe

The Recipe module contains terms and relations for describing the hierarchical and temporally sequenced operations and actions which comprise the recipe. Module contents also describes the evolution and maturation of the recipe over time as it is transformed from a general recipe (not specific for a site) to a specific instance recipe associated with a batch.


## Contributing to this ontology

The authors welcome discussion on the future of this Biopharma Ontology. Contributors are requested to post an issue in this GitHub folder and use the label 'biopharma'.


## Current Outstanding Issues

Please refer to the list kept on the IOF Confluence site for potential improvements/ additions for a v2 and the Issues list here on GitHub.
