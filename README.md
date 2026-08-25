![Industrial Ontologies Foundry](https://cdn.shopify.com/s/files/1/0715/9303/4025/files/IOF_480x480.png?v=1678423553)

# Industrial Ontologies Foundry

The IOF (The Industrial Ontologies Foundry) is a unit of [OAGi](https://OAGi.org) (Open Applications Group), a non-profit organization with the mission to reduce the cost of integration by developing inter-operable, cross-functional, cross-industry, data-model-driven, and extensible standards to meet the challenge of a rapidly-changing global digital economy. 

IOF's mission is to create a suite of ontologies intended to support digital manufacturing by facilitating cross-system data integration within the factory and across an enterprise; in commerce between suppliers, manufacturers, customers, and other trading partners; and throughout the various stages of the product life cycle. The IOF ontologies consist of a common mid-level ontology, "Core," and several domain specific ontologies.

The IOF Core Ontology resides at  the top of this suite from an architectural perspective and contains terms found in several operational areas of manufacturing. Additionally, the architectural approach chosen by the IOF is to base all of its ontologies on a single foundational or top-level ontology–for which the IOF chose the [Basic Formal Ontology](https://basic-formal-ontology.org/bfo-2020.html) or BFO. The Core Ontology contains many intermediate-level terms that derive from BFO and from which the IOF ontologies derive domain industry terms. Core intermediate-level terms are often domain independent–meaning one can find them in other industries and fields, such as in the banking, insurance, and healthcare industries, or the sciences, as in the physics, chemistry, and biology domains. 

# How Status is Specified for IOF Ontologies and Constructs

IOF uses Maturity Level to describe the status of its ontological content. The following are the definitions and usage guide for the Maturity Level (excerpt from [IOF Annotation Vocabulary Guide v2.1](https://oagiscore.atlassian.net/wiki/spaces/IOF/pages/4532142081/IOF+Annotation+Property+Guide+V2.1#Maturity). Note that access to the guide may require [IOF membership](https://industrialontologies.org/participation-request/)):
 
> Note: the term _construct_ is inclusive of both classes and properties. 

* **maturity** – `iof-av:maturity`
 
  * The annotation property used to indicate the development status of a resource such as an ontology or a construct

  * IOf uses the following values when specifying the maturity:

      * `iof-av:Released`

        * Will not be removed from the ontology for a reasonable length of time

        * Indicates an ontology or construct that is considered to be stable and mature from a development perspective

        * Release notes will be provided for any changes concerning released content, and any revisions will be backward compatible with the prior version to the degree possible

      * `iof-av:Provisional`

        * Indicates an ontology or construct that is considered to be under development

        * Provisional content is subject to change and may change substantially before release. IOF users should be aware that it is not dependable but could be used for reference and as the basis for further work

## Aggregation Files

All IOF domains provide an `AboutIOFDev` and `AboutIOFProd` aggregation files, which import the modules whose maturity is (respectively) Provisional and Released or Released only. 

# Current Ontology Status

The status of each ontology and construct is declared within the ontology files themselves via the `iof-av:maturity` annotation property (see [How Status is Specified](#how-status-is-specified-for-iof-ontologies-and-constructs) above). The maturity asserted in each file is the authoritative source; the summary below reflects those assertions for this release.

## Released Ontologies

* `core/Core` **[Released]**
  >  The IOF Core Ontology contains notions found to be common across multiple manufacturing domains. The ontology utilizes the Basic Formal Ontology or BFO as a top-level ontology but also borrows terms from various domain-independent or mid-level ontologies. The purpose of the ontology is to serve as a foundation for ensuring consistency and interoperability across various domain-specific reference ontologies the IOF publishes.
  * `core/meta/AnnotationVocabulary` **[Released]**
    > The IOF Annotation Vocabulary provides a set of OWL annotation properties for annotating IOF or other content with metadata to facilitate user and ontology developer understanding.	
  * `commonstocoremapping/MappingCommonsToIOF` **[Released]**
    > This ontology maps the OMG Common Ontologies concepts related to the notion of Identifier to those of IOF Core. Specifically, the OMG ontologies Collections, Designators and Identifiers are mapped to the IOF Core.

    > The purpose of this ontology is to ensure interoperability with the listed OMG Ontologies and to enable users of IOF Core to utilize OMG constructs around identifiers that are currently lacking within the IOF Core.
  * `commonstocoremapping/meta/MappingAnnotationVocabularyToCommons.rdf` **[Released]**
    > The IOF Mapping Annotation Vocabulary to Commons maps the AV to the Object Management Group (OMG)&apos;s Annotation Vocabulary provided in the Commons Ontology Library. The Commons Annotation Vocabulary is a subset of what is included in the IOF AV, but is used across a number of OMG and other emerging standards and thus the mapping makes it easier to use other Commons library ontologies in an IOF context.
* `maintenance/Maintenance` **[Released]**
  > The purpose of this IOF Maintenance Reference ontology is to support semantic interoperability through the use of modular ontologies in the maintenance domain. This Ontology contains terms identified as common in a number of application ontologies for maintenance management, maintenance procedures, asset failure, and failure modes and effects analysis. The ontology is based on the IOF Core Ontology.
* `supplychain/SupplyChain` **[Released]**
  > Supply Chain Reference Ontology (SCRO) aims to extend the IOF Core with the constructs (classes and properties) related to the domain of supply chain and logistics. The purpose of the ontology is to serve as a foundation for ensuring consistency and interoperability across various supply chain and logistics application ontologies.
* `productionplanning/ProductionPlanning` **[Released]**
  > The IOF Production Planning Ontology is a domain reference ontology for process and production planning activities across manufacturing industries, including discrete, process, batch, and biomanufacturing. It provides upper-level terms related to planning — specifications, artifacts (e.g., production machines and tools), and processes — from which users may derive domain- or company-specific application ontologies.
* `certification/Certification` **[Released]**
  > The IOF Certification Ontology extends IOF Core with constructs for representing certification — certificates, the entities they attest to, and the parties and processes involved in issuing them.

## Biopharmaceutical Manufacturing Ontologies (`biopharma`)

The biopharma suite is a set of modular ontologies covering biopharmaceutical manufacturing (described in more detail [below](#biopharmaceutical-manufacturing-ontologies)). Individual modules carry their own maturity assertion:

* **[Released]** modules: `BiopharmaAgent`, `BiopharmaEquipment`, `BiopharmaManufacturingExecution`, `BiopharmaMaterial`, `BiopharmaMaterialProcurementAndStorage`, `BiopharmaMonitoringAndControl`, `BiopharmaParameter`, `BiopharmaReferenceOntologyAttributes`, `MolecularEntity`, `ManufacturingSystemOrganization`, `Recipe` (with `RecipeProceduralOccurrenceClassificationUtility` and `RecipeProcessOccurrenceClassificationUtility`), and `TargetsLimitsRanges`.
* **[Provisional]** modules: `BiopharmaDeviationManagement`, `BiopharmaRiskManagement`, `BiopharmaMaterialTesting`, `BiopharmaManufacturingProcessLifecycle`, `DesignOfExperiments`, and `Statistics`.

## Provisional Ontologies

* `productservicesystem/ProductServiceSystem` **[Provisional]**
  > A reference ontology for enhancing the engineering of Product Service Systems (PSS) in manufacturing by modelling the aspects that affect a PSS across its life cycle — product, service, involved agents and organizations, resources, requirements, design and plan specifications, and PSS business processes. The current module focuses on the manufacturing industry, with extension to other sectors planned.
  * `productservicesystem/Sensor` **[Provisional]**
    > This module contains terms and relations necessary for representing basic sensor entities and observations made by the sensors. The ontology is based on the IOF Core Ontology.

## Reasoner

IOF ontologies, provisional and released, have been verified to be logically consistent and satisfiable with the HermiT reasoner in Protégé.

# Biopharmaceutical Manufacturing Ontologies

The Biopharmaceutical Manufacturing Ontologies (`biopharma`) are a suite of modular ontologies containing notions found to be common across biopharmaceutical manufacturing. They were initially developed as the National Institute for Innovation in Manufacturing Biopharmaceuticals (NIIMBL) Ontology and transferred to the IOF under the MIT license.

The suite uses the IOF Core Ontology as its mid-level ontology and the Quantities, Units, Dimensions and Types (QUDT) ontologies for consistent representation of unit–value pairs. The modules are designed to be used together or independently depending on the application. Their maturity is a mix of Released and Provisional (see [Current Ontology Status](#current-ontology-status)); the suite as a whole remains under active development.

The suite includes the following modules:

* **Agent**  **[Released]** — types of agents (actors) in biopharmaceutical manufacturing, including human actors, engineered systems, and organizations.
* **Equipment**  **[Released]**— equipment types, their properties (qualities, capabilities, and functions), and equipment specification and validation (methods, testing, reporting).
* **Manufacturing Execution**  **[Released]** — the actual occurrences of manufacturing processes with respect to recipes.
* **Material**  **[Released]** — material types and their associated properties, including usages in operations (e.g., consumable, process intermediate, final product).
* **Material Procurement & Storage**  **[Released]** — tracking and tracing of materials, connecting process control to raw material procurement and supporting regulatory compliance.
* **Material Testing** **[Provisional]** — testing activities that determine whether a material is acceptable for its intended use, linking testing processes, analytical evidence, specifications, acceptance criteria, and out-of-specification results.
* **Monitoring & Control**  **[Released]** — planning and execution of monitoring and/or control at both laboratory and manufacturing scale.
* **Parameter**  **[Released]** — process intermediate and product quality attributes, process indicators, and process parameters.
* **Targets, Limits & Ranges**  **[Released]** — value-expression constructs for prescribed values, intervals, and thresholds (target values and ranges, setpoints) used in process control, quality control, and material conformance.
* **Recipe**  **[Released]** — the hierarchical and temporally sequenced operations and actions that comprise a recipe, and its maturation from a general recipe to a batch-specific instance recipe (with procedural- and process-occurrence classification utilities).
* **Manufacturing System Organization**  **[Released]** — the physical spaces where processing and storage occur, represented as bounded, potentially hierarchical locations.
* **Molecular Entity**  **[Released]** — selected molecular entities, including molecular entity populations and roles, chemical residues and moieties, biological sequences, and proteins.
* **Manufacturing Process Lifecycle**  **[Provisional]** — how manufacturing processes are designed, characterized, qualified, validated, and monitored over time.
* **Deviation Management**  **[Provisional]** — deviations from approved plans, procedures, requirements, limits, and ranges, and how deviation events are documented and handled.
* **Risk Management**  **[Provisional]** — how risks are identified, analyzed, evaluated, controlled, communicated, and reviewed.
* **Statistics**  **[Provisional]** — statistical models and analyses that quantify variation, effects, and quality; integrates concepts from STATO within the IOF framework.
* **Design of Experiments**  **[Provisional]** — extends the Statistics module with constructs for design of experiments, including study design objectives, factor-level combinations, and design points.
* **Reference Ontology Attributes**  **[Released]** — annotation constructs specific to the biopharma reference ontology suite.

See the [biopharma README](biopharma/README.md) for further detail.

# Installing / Getting started

The minimal setup you need, short of reading raw XML, is a suitable ontology viewer or editing tool, installed on your client machine. IOF recommends a desktop version of the open-source tool [Protégé](https://protege.stanford.edu/), but other open source and commercial tools are known to work as well. The repository for this ontology includes the necessary files for opening the ontology in Protégé without warnings and errors. The same is not guaranteed for other tools.

To load all the ontologies, load the `AboutIOFProd` aggregation file for released ontologies, or the `AboutIOFDev` aggregation file for both provisional and released ontologies. The aggregation files are located in the root directory.

# Getting Involved

## General Discussions

The IOF welcomes those organizations and persons who would like to contribute to this and other IOF ontology projects. To start contributing, or to join the general discussions, please see [Getting Involved](https://oagiscore.atlassian.net/wiki/spaces/IOF/overview). 

Getting involved will also give you access to discussions on issues regarding issues not raised through GitHub, and the status of any issues posted in these release notes at time of release.

# External Links

- [IOF Web Site for the General Public](https://oagi.org/pages/industrial-ontologies/) 
- [IOF Member Portal](https://oagiscore.atlassian.net/wiki/spaces/IOF/overview?homepageId=146047039) 
- [IOF Mission, History and Charter](https://oagi.org/pages/history-of-the-iof)
- [IOF Technical Principles](https://oagi.org/pages/technical-principles) 
- [Resources and Papers](https://oagi.org/pages/resources-about-from-iof-project) 
- [Basic Formal Ontology](https://basic-formal-ontology.org/bfo-2020.html) 

