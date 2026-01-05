<p align="center">
<img src="https://user-images.githubusercontent.com/12449023/166088434-b6761386-9b3f-4881-a891-c8ffdbde0fae.png" height="80">
<img src="https://user-images.githubusercontent.com/12449023/166088435-a9fcc4c7-f51d-443a-b1fd-9fe96a204f77.png" >
</p>

# The ProductionPlanning Ontology

Version  202502, December 2025 maturity provisional

# Introduction

Production Plannig ontology is a domain reference ontology for process and production planning activities within various industries. It include general terms common for different types of manufacturing industries, such as discrete manufacturing, process manufacturing, batch manufacturing, biomanufacturing, and others. Being refernce ontology, it is expacted that users of the production planing ontology will extend its classes is ways compatible with common vocabulary in manufacturing domains, such as aerospace, automotive, food industries, and others. 

The IOF ProductionPlanning is a reference ontology for the domain of manufacturing/production planning that resides under  the IOF Core ontolgy (it imports IOF Core)  As a reference ontology, ProductionPlanning contains terms used by most industries utilizing data interoperability in their production planning activities in relation to various ERP amd MES software.

The IOF ProductionPlanning Ontology is developed and formalized as an ontology using both first-order logic and version 2 of the Web Ontology Language (OWL). The use of logic ensures that each term is defined in a way that is unambiguous to humans and can be processed by computers. The vocabulary in Production Planning is curated by the Production Planning and Schedling Working Group and an attempt is made to validate and ground terms utilizing use cases from industry.

# Release Notes

Version  202502, December 2025 maturity provisional

This ontology includes constructs for upper level terms found in most manufacturing industries (including discrete, continuous, and batch manufacturing) related to planning, in areas such as specifications (ICEs), artifacts, and processes. The information content entities (ICE) include material product specification and several classes for the levels of plan specifications, the artifacts include fundamental resources, namely production machine and tool, and processes include classes for inspection and manufacturing industrial processes from which users may create domain ontologies that extend those classes for specific manufacturing areas or companies. This module is expected to mature in future release based on the user feedback.

# Contents

1.

# Installing / Getting started

The minimal setup you need short of reading raw XML is a suitable ontology viewer or editing tool, installed on your client machine. IOF recommends a desktop version of the open-source tool [Protégé](https://protege.stanford.edu/), but other open source and commercial tools are known to work as well. The repository for this ontology includes the necessary files for opening the ontology in Protégé without warnings and errors. The same is not guaranteed for other tools.  

# Publications related to production planning and scheduling ontologies

F Ameri, D Sormaz, F Psarommatis, D Kiritsis, Industrial ontologies for interoperability in agile and resilient manufacturing, International Journal of Production Research 60 (2), 420-441, 2022

D Šormaz, A Sarkar, SIMPM–Upper-level ontology for manufacturing process plan network generation, Robotics and Computer-Integrated Manufacturing 55, 183-198	9	2019

Saruda Seeharit, Dusan N. Sormaz, Emre Bilgin Sari, A Systematic Review of Ontology-Based Scheduling Approaches in Manufacturing: Enhancing Decision Making and Resilience, 28th International Conference on Production Research, July 12-17, Chia, Colombia

Arkopaul Sarkar. Milos Drobnjakovic, Ana Nikolov, Saruda Seeharit, Adlane Rebaï, Gabriela Henning, Dusan Sormaz, Yan Lu, Evan K. Wallace, Serm Kulvatunyou, Toward a Standardized Manufacturing Operation Management Ontology (MOMO): Findings from the NIST Workshop, 28th International Conference on Production Research, July 12-17, Chia, Colombia

Saruda Seeharit, Dušan Šormaz and Mandvi Fuloria, Interoperability Between ERP and PLM Systems using Ontologies - A Case Study, 12th International Conference on Production Research Americas Region, ICPR Americas 2024, July 21-25, Athens, OH

Dušan Šormaz, Saruda Seeharit, Boonserm Kulvatunyou, Miloš Drobnjaković, A Basic Formal Ontology-Based Ontological Modeling for Plan and Occurrence, a Biomanufacturing Process Verification Use Case, Proceedings of the ASME 2024 International Design Engineering Technical Conferences and Computers and Information in Engineering Conference, IDETC/CIE2023, August 25-28, 2024, Washington, DC

Dušan Šormaz, Boonserm Kulvatunyou, Miloš Drobnjaković, Saruda Seeharit, Comparative Study of Approaches for an Ontology of Digital Artifacts, Proceedings of the ASME 2023 International Design Engineering Technical Conferences and Computers and Information in Engineering Conference, IDETC/CIE2023, August 20-23, 2023, Boston, MA 

Arkopaul Sarkar, Milos Drobnjakovic, Sina Namaki Araghi, Mohamed Hedi Karray and Dusan Sormaz, Ontology Modeling of Plan and their Conformance to Manufacturing Execution, Proceedings of 27th International Conference on Production Research, Cluj-Napoca, Romania, 23-28 July 2023.

Riad Al Hasan Abir, Mandvi Malik Fuloria, Dusan Sormaz, Peter Adjei, Felix Asare, David Koonce and Saruda Seeharit, Ontology Model for Mapping Terms and Relations in Plastic Manufacturing – A Case Study, Proceedings of  27th International Conference on Production Research, Cluj-Napoca, Romania, 23-28 July 2023.

Dusan Sormaz, Arkopaul Sarkar and David Koonce, Application Integration in Smart Manufacturing and Industry 4.0 using Ontologies, ICPR 2022, International Conference on Production Research Americas, November 23-25, 2022, Curitiba, Brazil

Arkopaul Sarkar, Dusan Sormaz and Hedi Karray, Taxonomy of Manufacturing Joining Operations based on Process Characterization, 12th International Workshop on Formal Ontologies meet Industry, September 12-15, 2022, Tarbes, France

Sarkar, Arkopaul, Sormaz, Dusan, Hedi Karray, Mohamed, Taxonomy of Manufacturing Joining Operations based on Process Characterization, in Kyoung-Yun Kim, Leslie Monplaisir, Jeremy Rickli, Ed. Flexible Automation and Intelligent Manufacturing: The Human-Data-Technology Nexus, Proceedings of FAIM 2022, June 19–23, 2022, Detroit, Michigan, USA, Volume 2

A. Sarkar, M. R. Naqvi, L. Elmhadhbi, Dusan Sormaz, Bernard Archimede, M. H. Karray, CHAIKMAT 4.0 - Commonsense Knowledge & Hybrid Artificial Intelligence for Trusted Flexible Manufacturing, in Kyoung-Yun Kim, Leslie Monplaisir, Jeremy Rickli, Ed. Flexible Automation and Intelligent Manufacturing: The Human-Data-Technology Nexus, Proceedings of FAIM 2022, June 19–23, 2022, Detroit, Michigan, USA, Volume 2

Arkopaul Sarkar, Dušan Šormaz, Interoperability between PLM, ERP, and MES Systems Using Formal Ontologies, International Conference of Production Research, July 18-21, 2021, Taiwan - virtual

Arkopaul Sarkar, Dušan Šormaz, David Koonce, and Sharmake Farah, Developing a Resource-based Manufacturing Process Capability Ontology, The International Conference of Production Research, ICPR - Americas 2020, December 2020, Bahía Blanca, Argentina - virtual

Dusan Šormaz, Arkopaul Sarkar, Walter Terkaj, Progress on IOF’s Process and Production Planning Reference Ontology, Proceedings of the 10th International Conference on Interoperability for Enterprise Systems and Applications, November 17-19, 2020, Tarbes, France, (Virtual)

Sarkar, Arkopaul; Sormaz, Dusan, On Semantic Interoperability of Model-based Definition of Product Design, 29th International Conference on Flexible Automation and Intelligent Manufacturing, 24th - 28th June 2019, Limerick, Ireland

A Sarkar, D Šormaz, Ontology Model for Process Level Capabilities of Manufacturing Resources, Procedia Manufacturing 39, 1889-1898, 2019

A Sarkar, D Šormaz, On Semantic Interoperability of Model-based Definition of Product Design, Procedia Manufacturing 38, 513-523, 2019

DN Sormaz, A Sarkar, S Ghosal, A Multiagent System for Distributed Manufacturing Process Planning,  Procedia Manufacturing, 2018




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


