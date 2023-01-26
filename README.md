![Industrial Ontologies Foundry](https://i0.wp.com/industrialontologies.org/wp-content/uploads/2020/01/cropped-IOF-LOGO-2-4.png)

# Industrial Ontologies Foundry

The IOF (The Industrial Ontologies Foundry) is a unit of [OAGi](https://OAGi.org) (Open Applications Group), a non-profit organization with the mission to reduce the cost of integration by developing inter-operable, cross-functional, cross-industry, data-model-driven, and extensible standards to meet the challenge of a rapidly-changing global digital economy. 

IOF's mission is to create a suite of ontologies intended to support digital manufacturing by facilitating cross-system data integration within the factory and across an enterprise; in commerce between suppliers, manufacturers, customers, and other trading partners; and throughout the various stages of the product life cycle. The IOF ontologies consist of a common mid-level ontology, "Core," and several domain specific ontologies.

The IOF Core Ontology resides at the top of this suite from an architectural perspective and contains terms found in several operational areas of manufacturing. Additionally, the architectural approach chosen by the IOF is to base all of its ontologies on a single foundational or top-level ontology–for which the IOF chose the [Basic Formal Ontology](https://basic-formal-ontology.org/bfo-2020.html) or BFO. The Core Ontology contains many intermediate-level terms that derive from BFO and from which the IOF ontologies derive domain industry terms. Core intermediate-level terms are often domain independent–meaning one can find them in other industries and fields, such as in the banking, insurance, and healthcare industries, or the sciences, as in the physics, chemistry, and biology domains. 
# Definition of Status
Following is the detail definitions and usage guide of the Maturity Level (excerpt from [IOF Annotation Vocabulary Guide v2.1](https://oagiscore.atlassian.net/wiki/spaces/IOF/pages/4532142081/IOF+Annotation+Property+Guide+V2.1#Maturity). Note that access to the guide may require [IOF membership](https://industrialontologies.org/participation-request/))

* **maturity** – `iof-av:maturity`* 
 
  * Definition: annotation property used to indicate the development status of a resource such as an ontology or a construct

  * Each IOF ontology **MUST** have exactly one maturity annotation with a value of type iof-av:MaturityLevel

  * Each construct within an ontology will default to the (i.e., be assumed to have the same) maturity of the ontology unless an explicit maturity annotation for the construct indicates otherwise

  * Each construct **MAY** have a maturity annotation, indicating the specific construct’s status of development

  * One **MUST** use the following vocabulary when specifying the maturity:

      * iof-av:Released 

        * Will not be removed from the ontology for a reasonable length of time

        * Indicates an ontology or construct that is considered to be stable and mature from a development perspective

        * Release notes will be provided for any changes concerning released content, and any revisions will be backward compatible with the prior version to the degree possible

      * iof-av:Provisional 

        * Indicates an ontology or construct that is considered to be under development

        * Provisional content is subject to change and may change substantially before release. IOF users should be aware that it is not dependable but could be used for reference and as the basis for further work

# Current Ontology Status

## Released and Provisional Ontologies

* `core/Core` **[Released]**
  >  The IOF Core Ontology contains notions found to be common across multiple manufacturing domains. This file is an RDF rendering of these notions expressed in OWL. The ontology utilizes the Basic Formal Ontology or BFO as a top-level ontology but also borrows terms from various domain-independent or mid-level ontologies. The purpose of the ontology is to serve as a foundation for ensuring consistency and interoperability across various domain-specific reference ontologies the IOF publishes.
  * `core/meta/AnnotationVocabulary` **[Released]**
    > The IOF Annotation Vocabularyprovides a set of OWL annotation properties for annotating IOF or other content with metadata to facilitate user and ontology developer understanding.	
  * `commons-to-core-mapping/MappingCommonsToIOF` **[Released]**
    > This ontology maps the OMG Common Ontologies concepts to those of IOF Core.
  * `commons-to-core-mapping/meta/MappingAnnotationVocabularyToCommons.rdf` **[Released]**
    > The IOF Mapping Annotation Vocabulary to Commons maps the AV to the Object Management Group (OMG)&apos;s Annotation Vocabulary provided in the Commons Ontology Library. The Commons Annotation Vocabulary is a subset of what is included in the IOF AV, but is used across a number of OMG and other emerging standards and thus the mapping makes it easier to use other Commons library ontologies in an IOF context.
* `maintenance/Maintenance` **[Provisional]**
  > The purpose of this IOF Maintenance Reference ontology is to support semantic interoperability through the use of modular ontologies in the maintenance domain. This Ontology contains terms identified as common in a number of application ontologies for maintenance management, maintenance procedures, asset failure, and failure modes and effects analysis. The ontology is based on the IOF Core Ontology.
* `supplychain/SupplyChainReferenceOntology` **[Provisional]**
  > Supply Chain Reference Ontology (SCRO) aims to extend the IOF Core with the notions (including classes and properties) related to the domain of supply chain and logistics. The purpose of the ontology is to serve as a foundation for ensuring consistency and interoperability across various supply chain and logistics application ontologies.
## Reasoner

IOF ontologies, provisional and released, have been verified to be logically consistent and satisfiable with Hermit version 1.4.3 reasoner, plugin to Protege 5.5

## In Development

* `productionplanning/mfg-planning`
* `productservicesystems/pss-ontology2`

# Installing / Getting started

The minimal setup you need, short of reading raw XML, is a suitable ontology viewer or editing tool, installed on your client machine. IOF recommends a desktop version of the open-source tool [Protégé](https://protege.stanford.edu/), but other open source and commercial tools are known to work as well. The repository for this ontology includes the necessary files for opening the ontology in Protégé without warnings and errors. The same is not guaranteed for other tools.  

# Getting Involved

## General Discussions

The IOF welcomes those organizations and persons who would like to contribute to this and other IOF ontology projects. To start contributing, or to join the general discussions, please see [Getting Involved](https://oagiscore.atlassian.net/wiki/spaces/IOF/overview). 

Getting involved will also give you access to discussions on issues regarding issues not raised through GitHub, and the status of any issues posted in these release notes at time of release.

# External Links

- [IOF Web Site for the General Public](http://www.industrialontologies.org/) 
- [IOF Member Portal](https://oagiscore.atlassian.net/wiki/spaces/IOF/overview?homepageId=146047039) 
- [IOF Mission, History and Charter](https://www.industrialontologies.org/our-mission/)
- [IOF Technical Principles](https://www.industrialontologies.org/technical-principles/) 
- [IOF Annotation Properties Version 2](https://oagiscore.atlassian.net/wiki/spaces/IOF/pages/4399431681/IOF+Annotation+Properties+Version+2) 
- [Basic Formal Ontology](https://basic-formal-ontology.org/bfo-2020.html) 

