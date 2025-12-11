<p align="center">
<img src="https://user-images.githubusercontent.com/12449023/166088434-b6761386-9b3f-4881-a891-c8ffdbde0fae.png" height="80">
<img src="https://user-images.githubusercontent.com/12449023/166088435-a9fcc4c7-f51d-443a-b1fd-9fe96a204f77.png" >
</p>

# The ProductionPlanning Ontology

Version  202502, December 2025 maturity provisional

# Introduction

Production Plannig ontology is a domain reference ontology for process and production planning activities within various industries. It include general terms common for different types of manufacturing industries, such as discrete manufacturing, process manufacturing, batch manufacturing, biomanufacturing, and others. Being refernce ontology, i is expacted that users of the production planign ontology will extend its classes is ways compatible with common vocabulary in manufacturing domains, such as aerospace, automotive, food industries, and others. 

The IOF ProductionPlanning is a reference ontology for the domain of manufacturing/production planning that resides under  the IOF COre ontolgy (it imports IOF Core)  As a mid-level ontology, Core contains terms used by, or anticipated to be used by, a plurality of ontologies in the suite. . 

The IOF ProductionPlanning Ontology is developed and formalized as an ontology using both first-order logic and version 2 of the Web Ontology Language (OWL). The use of logic ensures that each term is defined in a way that is unambiguous to humans and can be processed by computers. The vocabulary in Core is curated by the Core Working Group and an attempt is made to validate and ground terms utilizing use cases from industry.

# Release Notes

Version  202502, December 2025 maturity provisional

This ontology includes constructs for upper level terms found in most manufacturing industries (including discrete, continuous, and batch manufacturing) related to planning, in areas such as specifications (ICEs), artifacts, and processes. The information content entities (ICE) include material product specification and several classes for the levels of plan specifications, the artifacts include fundamental resources, namely production machine and tool, and processes include classes for inspection and manufacturing industrial processes from which users may create domain ontologies that extend those classes for specific manufacturing areas or companies. This module is expected to mature in future release based on the user feedback.

# Contents

1.

# Installing / Getting started

The minimal setup you need short of reading raw XML is a suitable ontology viewer or editing tool, installed on your client machine. IOF recommends a desktop version of the open-source tool [Protégé](https://protege.stanford.edu/), but other open source and commercial tools are known to work as well. The repository for this ontology includes the necessary files for opening the ontology in Protégé without warnings and errors. The same is not guaranteed for other tools.  

To use IOF Core without the need to interoperate with the OMG Commons Ontologies mentioned earlier, simply import Core.rdf into your ontology. To use both IOF Core and the OMG Commons Ontologies mentioned, only import MappingCommonsToIOF.rdf into your ontology. Doing so indirectly imports IOF Core and the applicable OMG Common Ontologies.

# Publications related to production planning and scheduling ontologies

# Reporting Issues for the ProductionPlanning Ontology and Joining the Discussions

The source for ProductionPLanning ontology and its development is managed on GitHub. Please log change requests and bugs for the ontology using the "issues tab" of the GitHub repository for this project. However, if you are a member person or organization of the IOF, we ask that you follow the normal process for reporting change requests and issues via the IOF member portal for the Core Working Group.

Requests and reported bugs are monitored at least bi-weekly during which time you can expect to see a response as to next steps. 

# External Links

- [IOF Web Site for the General Public](http://www.industrialontologies.org/) 
- [IOF Member Portal](https://oagiscore.atlassian.net/wiki/spaces/IOF/overview?homepageId=146047039) 
- [IOF Mission, History and Charter](https://www.industrialontologies.org/our-mission/)
- [IOF Technical Principles](https://www.industrialontologies.org/technical-principles/) 
- [IOF Annotation Properties Version 2](https://oagiscore.atlassian.net/wiki/spaces/IOF/pages/4399431681/IOF+Annotation+Properties+Version+2) 
- [Basic Formal Ontology](https://basic-formal-ontology.org/bfo-2020.html) 


