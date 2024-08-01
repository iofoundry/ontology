<p align="center">
<img src="https://user-images.githubusercontent.com/12449023/166088434-b6761386-9b3f-4881-a891-c8ffdbde0fae.png" height="80">
<img src="https://user-images.githubusercontent.com/12449023/166088435-a9fcc4c7-f51d-443a-b1fd-9fe96a204f77.png" >
</p>

# Supply Chain Reference Ontology (SCRO)

Version 1 Beta, 2022-11-18

*The IOF is an international standards group that operates under the auspices of the Open Applications Group.*

# Introduction

Supply Chain Reference Ontology (SCRO) aims to represent the generic constructs (including classes and properties) related to the domain of supply chain and logistics. SCRO uses BFO as the top-level ontology and IOF Core as the mid-level ontology. The purpose of the ontology is to serve as a foundation for ensuring consistency and interoperability across various supply chain and logistics ontologies that use IOF reference ontolgies. The Supply Chain Reference Ontology can be extended to create application ontologies addressing the needs of specific use cases. The development of SCRO was initially motivated by use cases related to supplier discovery (i.e., supplier capability matching with manufacturing requirements), shipment request and fulfillment,  and agri-food supply chain traceability. While the ontology is driven by specific use cases, the definitions of terms are intended to be applicable beyond these use cases and are extracted from widely accepted industry standards such as GS1 and APICS.



SCRO.owl imports IOF Core directly. BFO-2020.owl and IOF-AnnotationVocabulary.rdf are imported through IOF Core.  

### Taxonomy of SCRO Continuants
> click the image to view the enlarged image in a new tab
![Taxonomy of SCRO Continuants](images/SCRO-continuants.png)

### Taxonomy of SCRO Occurrents
> click the image to view the enlarged image in a new tab
![Taxonomy of SCRO Continuants](images/SCRO-Occurrents.png)

## Glossary of Terms
[The glossary](https://htmlpreview.github.io/?https://github.com/InfoneerTXST/Glossary/blob/master/index.html) provides the natural language definitions of SCRO classes and properties

## Example RDF Dataset
This dataset represents a hypothetical supply chain as depicted in [this image](https://github.com/iofoundry/ontology/blob/master/supplychain/Documentation%20&%20Resources/Terms-Patterns-Modules/Ford%20Supply%20Chain.md). The RDF dataset demonstrates how the class "Supply Chain Relationship' is used to represent the strucrue of a supply chain.
- [RDF Dataset](https://github.com/iofoundry/ontology/blob/master/supplychain/data/SCRO_Ford.tt)
=======
Additional class diagrams can be found [here](https://oagiscore.atlassian.net/wiki/spaces/IOF/pages/4554031140/SCRO+Class+Diagrams). 

## Glossary of Terms
[The glossary](https://htmlpreview.github.io/?https://github.com/InfoneerTXST/Glossary/blob/master/index.html) provides the natural language definitions of SCRO classes and properties

## Example Data in RDF
This dataset represents a hypothetical supply chain as depicted in [this image](https://github.com/iofoundry/ontology/blob/SCRO-pre-vote-branch/supplychain/Documentation%20%26%20Resources/images/FORD-SupplyChain.png). The RDF dataset demonstrates how the class "Supply Chain Relationship' is used to represent the strucrue of a supply chain.
- [RDF Dataset](https://github.com/iofoundry/ontology/tree/SCRO-pre-vote-branch/supplychain/data)


## Current Outstanding Issues
- Classifers are excluded from the first release. The plan is to reuse the identifer/classifers patterns provided by Commons Ontologies. However, since their adoption requires some architectural decisions at the core level, this release only includes a few classes related to identifiers.
- Representation of various states of a shipment (delayed, delivered, etc) requires some temporal interval properties (based Allen's Inverval Algebra) which are currently missing.
- The base ontology is large and can be split into several smaller ontologies. Once the geeral approach for using 'sub-topics' in IOF is further formalized, the based ontology will be re-architectured.


## Related Publications
- Farhad Ameri, Evan Wallace, Reid Yoder, Frank Riddick (2022) Enabling Traceability in Agri-Food Supply Chains Using an Ontological Approach, ASME Journal of Computing and Information Systems in Engineering (JCISE), October 2022; 22(5): 051002. https://doi.org/10.1115/1.4054092
- Ameri, F., Sormaz, D., Psarommatis, F., & Kiritsis, D. (2021). Industrial ontologies for interoperability in agile and resilient manufacturing. International Journal of Production Research, 1-22. https://doi.org/10.1080/00207543.2021.1987553
- Farhad Ameri, Evan Wallace, Boonserm Kulvatanyou, and Chris Will, Towards a Reference Ontology for Supply Chain Management, Proceedings of International Conference on Interoperability for Enterprise Systems and Applications (I-ESA), IOF Workshop, November 2020, France, Tarbes.
- Farhad Ameri, Evan Wallace, Reid Yoder, Enabling Traceability in Agri-Food Supply Chains Using an Ontological Approach, ASME International Design Engineering Technical Conferences and Computers and Information in Engineering Conference,  ASME IDETC2020-19995, August 2020, St. Louis, MO.
- Farhad Ameri and Boonserm Kulvatanyou, Modeling a Supply Chain Ontology Based on a Top-Level Ontology, International Design Engineering Technical Conferences and Computers and Information in Engineering Conference, Volume 1B: 38th Computers and Information in Engineering Conference, ASME IDETC2019-98278, Anaheim, CA,  August 2019.
