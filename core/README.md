![logo of IOF](https://user-images.githubusercontent.com/12449023/166088435-a9fcc4c7-f51d-443a-b1fd-9fe96a204f77.png)
![logo of OAGi](https://user-images.githubusercontent.com/12449023/166088434-b6761386-9b3f-4881-a891-c8ffdbde0fae.png)

# Industrial Ontologies Foundry Core Ontology
Version 1 Beta, 6-May-2022 

The Industrial Ontologies Foundry, or IOF, is an international standards group that operates under the auspices of the Open Applications Group (OAGi).
# Introduction
The IOF’s mission is to create a suite of ontologies intended to support digital manufacturing by facilitating cross-system integration both within the factory, across the enterprise, in commerce between suppliers, manufacturers, customers and other trading partners, and throughout the various stages of the product life cycle. The IOF Core Ontology resides at the top of this suite from an architectural perspective and contains terms found in a number of operational areas of manufacturing. These common terms appear, or anticipated to appear, in two or more of the ontologies of the suite. Additionally, as the architectural approach chosen by the IOF is to base all of its ontologies on a single foundational or top-level ontology – for which the IOF chose the Basic Formal Ontology or BFO – the Core Ontology contains a number of intermediate-level terms that derive from BFO and from which common industry terms are in turn derived. Such intermediate-level terms are most often domain independent – meaning they are found in other industries and domains, such as in the banking, insurance, and healthcare industries, or in the sciences, as in the physics, chemistry and biology domains. 

The IOF Core Ontology is developed and formalized as an ontology using both first-order logic and version 2 of the Web Ontology Language (OWL). The use of logic ensures that each term is defined in a way that is unambiguous to humans, and can be processed by computers. All terms appearing in the ontology are reviewed and curated by a working group and consensus is reached by validating usage in the context of manufacturing domain use cases.

WARNING: This is a repository contains a version 1, “beta release” of the IOF Core Ontology. As such, the contents may undergo some change as we resolve outstanding issues and drive to a first stable release. 
# Contents of this Repository
1. An owl implementation of the IOF Core Ontology, inclusive of natural language definitions, formalizations in first-order logic, examples, and comments, serialized in rdf/xml.
1. A directory containing IOF-specific annotation properties used to define and formalize ontology terms, also serialized in rdf/xml.
1. A license file, containing details of the OAGi copyright statement, licensing and permissions granted for this ontology.
1. A catalog file for rapid loading in the recommended ontology viewing/editing software (see Getting Started next).
# Installing / Getting started
The minimal setup you need short of reading raw XML is a suitable ontology viewer or editing tool, installed on your client machine. IOF recommends a desktop version of the open source tool [Protégé](https://protege.stanford.edu/), but other open source and commercial tools are known to work as well. The repository for this ontology includes the necessary files for opening the ontology in Protégé without warnings and errors. The same is not guaranteed for other tools. 

**<<For the final release, we might insert instructions here for how to create domain-specific or sub ontologies, or application ontologies, that import the core ontology.>>**
# Getting Involved
## Reporting Issues for the Core Ontology and Joining the Discussions
All IOF ontology sources are maintained on GitHub. Any change requests or bugs related to this IOF Core Ontology may be proposed or reported using the issues tab of this GitHub project in the main branch, or against one of the forked branches when they become applicable. For organizations and persons that are members of IOF, we ask that you follow the normal process for reporting issues as described in the IOF member portal.

Requests and reported issues reported through this site are monitored at least weekly during which time you can expect to see a response and what to expect as next steps. To join the extended discussions that occur within the IOF concerning your or any other proposed change or reported bug, you will need to become a member of the organization as discussed in the next section. 

**Please note that you do need a GitHub user name to participate in the development process**. 
## General Discussions
The IOF welcome those organizations and souls who would like to contribute to this and other IOF ontology projects. To start contributing, or to join general discussions about this IOF ontology, including our processes and approach to developing ontologies, please [click here](https://oagiscore.atlassian.net/wiki/spaces/IOF/overview) to take the next steps. 

Getting involved will also give you access to discussions on issues and changes for this and other ontologies not raised through GitHub, and the status of any issues posted in these release notes at time of release.
## Code of conduct
***<<In looking at how FIBO has done their release notes and readme files, we might want to consider including a code-of-conduct file in this repository, and inserting a paragraph in here. TBD>>***
# License
The IOF Core Ontology is licensed under the [**MIT License](http://opensource.org/licenses/MIT)**.** For additional details on licensing, copyrights, and the permissions granted, read the LICENSE file contained in this repository. 
# Links
- [IOF Web Site for the General Public](http://www.industrialontologies.org/) 
- [IOF Member Portal](https://oagiscore.atlassian.net/wiki/spaces/IOF/overview?homepageId=146047039) 
- [IOF Mission, History and Charter](https://www.industrialontologies.org/our-mission/)
- [IOF Technical Principles](https://www.industrialontologies.org/technical-principles/) 
- [IOF Annotation Properties & Usage Rules](https://oagiscore.atlassian.net/wiki/spaces/IOF/pages/3884777496/IOF+Annotation+Properties) 
- [Basic Formal Ontology](https://basic-formal-ontology.org/bfo-2020.html) 
# List of “Important” Outstanding Issues
The following are outstanding issues in this beta release which the IOF considers “important enough” to resolve before publishing a final stable release: 

- [CW-62](https://oagiscore.atlassian.net/browse/CW-62) & [ARCH-33](https://oagiscore.atlassian.net/browse/ARCH-33)  – Natural Language Definitions Missing for a number of the terms, in particular, most object properties (relations). This violates the IOF annotation property usage rules.
- [ARCH-34](https://oagiscore.atlassian.net/browse/ARCH-34) – Details of the annotation usage rules for natural language, semi-formal and first-order logic definitions need to be further “harmonized” and once agreed to, will either drive updates to the annotation rules, or updates to a number of the terms.
