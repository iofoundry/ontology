<p align="center">
<img src="https://user-images.githubusercontent.com/12449023/166088434-b6761386-9b3f-4881-a891-c8ffdbde0fae.png" height="80">
<img src="https://user-images.githubusercontent.com/12449023/166088435-a9fcc4c7-f51d-443a-b1fd-9fe96a204f77.png" >
</p>

# The IOF Core Ontology

Version  1, Release 2022-02

*The IOF is an international standards group that operates under the auspices of the Open Applications Group.*

# Introduction

The IOF Core Ontology (Core) is a formal ontology that provides a common vocabulary for the industrial domains. Core is a "mid-level" ontology in that it resides at the top of the suite of ontologies the IOF seeks to introduce to fulfill its mission of supporting digital manufacturing by standardizing industrial terminology and improving consistency and interoperability across many operational areas of manufacturing and the product life cycle. As a mid-level ontology, Core contains terms used by, or anticipated to be used by, a plurality of ontologies in the suite. Additionally, as the IOF bases all of its ontologies on a single foundational or top-level ontology – for which the IOF has chosen the Basic Formal Ontology or BFO. Additionally, Core contains generic terms found in domains beyond industry that build upon BFO and provide a consistent foundation for introducing industry-specific terminology. 

The IOF Core Ontology is developed and formalized as an ontology using both first-order logic and version 2 of the Web Ontology Language (OWL). The use of logic ensures that each term is defined in a way that is unambiguous to humans and can be processed by computers. The vocabulary in Core is curated by the Core Working Group and an attempt is made to validate and ground terms utilizing use cases from industry.

# Contents

1. core.rdf – an OWL implementation of the IOF Core Ontology, inclusive of natural language definitions, formalizations in first-order logic, examplyes, and comments, serialized in rdf/xml.
1. meta – folder containing IOF-specific annotation properties used to define and formalize ontology terms, also serialized in rdf/xml, and imported by the core ontology. 

    * AnnotationVocabulary.rdf -- this is the released version of the IOF Annotation Vocabulary, dated 2022-09-29
1. commons-to-core-mapping – folder containing selected mid-level ontologies from the OMG Commons Library of Ontologies, addressing IOF needs in the topic area of identifiers and designators, as well as mapping files to map imported terms to IOF/BFO and align annotation property usage between IOF and OMG.  

	* Commons Folder -- The various OMG Commons Ontology files adopted by Core in this release, including Collections.rdf, Designators.rdf, TextDatatype.rdf and Identifiers.rdf
	* meta folder
	    * MappingAnnotationVocabularyToCommons.rdf -- Maps the somewhat different OMG annotation vocabulary to the IOF annotation vocabulary
	* MappingCommonsToIOF.rdf -- maps terms from the adopted OMG Commons ontologies to BFO and/or to IOF
1. Catalog-v001.xml – a tooling file for rapid loading of the ontology's files in the Protégé ontology development tool.

# Installing / Getting started

The minimal setup you need short of reading raw XML is a suitable ontology viewer or editing tool, installed on your client machine. IOF recommends a desktop version of the open-source tool [Protégé](https://protege.stanford.edu/), but other open source and commercial tools are known to work as well. The repository for this ontology includes the necessary files for opening the ontology in Protégé without warnings and errors. The same is not guaranteed for other tools. 

# Getting Involved

## Reporting Issues for the Core Ontology and Joining the Discussions

The source for Core and its evolution is managed on GitHub. Please log change requests and bugs for the ontology using the "issues tab" of the GitHub repository for this project. However, if you are a member person or organization of the IOF, we ask that you follow the normal process for reporting change requests and issues via the IOF member portal for the Core Working Group.

Requests and reported bugs are monitored at least bi-weekly during which time you can expect to see a response as to next steps. 

## General Discussions

The IOF welcomes those organizations and persons who would like to contribute to this and other IOF ontology projects. To start contributing, or to join the general discussions, please [click here](https://oagiscore.atlassian.net/wiki/spaces/IOF/overview). 

Getting involved will also give you access to discussions on issues regarding issues not raised through GitHub, and the status of any issues posted in these release notes at time of release.

# External Links

- [IOF Web Site for the General Public](http://www.industrialontologies.org/) 
- [IOF Member Portal](https://oagiscore.atlassian.net/wiki/spaces/IOF/overview?homepageId=146047039) 
- [IOF Mission, History and Charter](https://www.industrialontologies.org/our-mission/)
- [IOF Technical Principles](https://www.industrialontologies.org/technical-principles/) 
- [IOF Annotation Properties Version 2](https://oagiscore.atlassian.net/wiki/spaces/IOF/pages/4399431681/IOF+Annotation+Properties+Version+2) 
- [Basic Formal Ontology](https://basic-formal-ontology.org/bfo-2020.html) 


