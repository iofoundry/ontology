# Terms proposed for use in the IOF Maintenance Management Reference ontology

This is now the Master Working document for all terms needed by the Maintenance WG including those terms relating to maintenance management, failure events, and stasis.

## However as of June 9 2022 it is currentlu OUT OF SYNC with the Maintenance terms OWL file and needs to be updated.




__Maintenance WG terms submitted to IOF Technical Oversight Board for consideration for IOF core terms (29/10/21)__

See https://oagiscore.atlassian.net/wiki/spaces/IOF/pages/4229758977/Maintenance+WG+Top-Level+Terms+and+Relations

__Classes from Maintenance WG proposed in IOF Core 2022__
- Maintainable Item Role - checked and it is NOT in IOF Core as proposed.

__Classes used in Application ontologies developed by maintenance WG members:__

- BFO-aligned: 
  - maintenance activity ontology
  - maintenance state ontology
  - maintenance procedure ontology
- ISO15926-14 aligned: 
  - FMEA ontology

__For consideration in the Maintenance Ontology__

> NOTE: not all of the cross-refs in this index work as many do not have definitions at the end of the document.
> When adding new terms use '`### <term>`' so that cross-refs are auto generated.

- - [Component function](#component-function) [Used in FMEA ontology]  
- [Downtime](#downtime)
- - [Failure](#failure) [used in Stasis ontology] 
- - [Failure effect (and Final failure effect)](#failure-effect) [Used in FMEA ontology] 
- [Failure event](#failure-event) [Used in FMEA ontology]
- - [Failure process](#failure-process) [Used in Stasis Ontology  MH 29/6/21] (imported)
- - [Function (asset function)](#function-asset-function) - [Required function used in stasis ontology] 
- - [Function (Primary function)](#function-primary-function) [Used in FMEA ontology] - [used in Stasis ontology] 
- - [Function (Secondary function)](#function-secondary-function) [Used in Stasis ontology] 
- [Failure mode observation (code)](#failure-mode-observation-code) [Used in FMEA ontology]
- - [Functional failure (state)](#functional-failure-state) [Used in FMEA ontology] 
- - [Maintenance](#maintenance) [used in Stasis ontology] 
- [Maintainable Item](#maintainable-item) - [Used in Stasis ontology]
- [Maintenance Activity](#maintenance-activity) - [Used in Maintenance Activity ontology] 
- [Supporting Activity](#supporting-activity) - [Used in Maintenance Activity ontology] 
- [Unspecified Activity](#unspecified-activity) - [Used in Maintenance Activity ontology] 
- - [Maintenance Procedure Document](#maintenance-procedure-document) [used in Procedure ontology] 
- - [Maintenance Process](#maintenance-process) [used in Procedure ontology] 
- - [Maintenance Procedure Process](#maintenance-procedure-process) [used in Procedure ontology] 
- - [Maintenance State](#maintenance-state) [used in Stasis ontology] 
- [Maintenance Task](#maintenance-task)  [Used in Procedure ontology] 
- [Malfunction](#malfunction) [Used in FMEA ontology] (compare definition with non-conformity)
- - [Object in fault state](#object-in-fault-state) [Used in FMEA ontology] 
- - [Physical Asset](#physical-asset) [Used in Stasis ontology] 
- [Maintenance Work Order Record](#maintenance-work-order-record)
- [Non-conformity](#non-conformity) (cross check with malfunction)
- [Stasis (CCO definition)](#stasis-cco)
- [Stasis (nominal)](#stasis-nominal) [equivalent to 'Operating State' used in the Stasis Ontology]
- [Stasis (down state) and up (up state)](#stasis-of-down-down-state) [Used in Stasis ontology] 
- [Stasis (failure/ fault / defunct) also Object in fault state (statis of failure)](#stasis-fault-object-in-fault-state) also Object in fault state (statis of failure)
- [Stasis (degraded/ degradation)](#stasis-degraded) - State of degradation* [used in Stasis ontology]

__Existing Object properties__

- [functional continuant part of at some time](#functional-continuant-part-of-at-some-time) [used in FMEA ontology]
- [as functional continuant part at some time](#as-functional-continuant-part-at-some-time) [used in FMEA ontology]
- [has malfunction](#has-malfunction) [used in FMEA ontology]
- [disabled by / disables](#disabled-by-disables) [used in Stasis ontology]
- [has state / state of](#has-state-state-of) [used in Stasis ontology]
- [functionally depended on by/ functionally depends on](#functionally-depended-on-by-functionally-depends-on) [used in Stasis ontology]
- [failure to participate](#failure-to-participate) [used in Stasis ontology]
- [has incapable participant](#has-incapable-participant) [used in Stasis ontology]
- [kind of](#kind-of) [used in Stasis ontology]
- [type disabled by](#type-disabled-by) [used in Stasis ontology]
- [type has realization](#type-has-realization) [used in Stasis ontology]
- [unable to participate](#unable-to-participate) [used in Stasis ontology]


__Under-consideration classes from previous interations of Maintenance WG maintenance OWL files__

- [Act of modality change](#act-of-modality-change)
- [Asset role](#asset-role) (moved out of V2 core to under consideration)
- [Asset role](#asset-role)
- [Bodyguard capability](#bodyguard-capability)
- [Function descriptor](#function-descriptor)
- [Disposition to fail](#disposition-to-fail)
- [Failure cause](#failure-cause)
- [Failure mode](#failure-mode) (moved out of V2 core to under consideration)
- [Function descriptor](#function-descriptor) (not found in V2 core)
- [Functional location](#functional-location) (moved out of V2 core to under consideration)
- [Failure mechanism](#failure-mechanism) (moved out of V2 core to under consideration)
- [Inspection Action](#inspection-action)
- [Machine (asset) identifier](#machine-asset-identifier) (moved out of V2 core to under consideration)
- [Maintenance Non-standard Work Specification](#maintenance-non-standard-work-specification)
- [Maintenance Notification](#maintenance-notification) (moved out of V2 core to under consideration)
- [Maintenance Plan Specification](#maintenance-plan-specification) (moved out of V2 core to under consideration)
- [Maintenance Schedule List](#maintenance-schedule-list) (moved out of V2 core to under consideration)
- [Maintenance Strategy Specification](#maintenance-stategy-specification) (Type) [consider strategy as a requirements for a process - use requirements ontology aibel as guide] (moved out of V2 core to under consideration)
- [Maintenance Strategy Development Process](#maintenance-stategy-development-process) (moved out of V2 core to under consideration)
- [Maintenance Structured Maintenance Task Specification](#maintenance-structured-maintenance-task-specification) (moved out of V2 core to under consideration)
- [Process of degradation](#process-of-degradation) (MH 29/6/21 - may not be necessary) (moved out of V2 core to under consideration)
- [Stasis (defective)](#stasis-defective)
- [Stasis (functional failure)](#stasis-functional-failure) - see also Stasis (non-conforming quality) - State of Failure Component* - State of Failure Machine
- [Stasis (non-conforming quality)](#stasis-non-conforming-quality)
- [Switched/ powered on](#switched-powered-on)
- [Triggering event (Maintenance)](#triggering-event-maintenance) (MH 29/6/21 - may not be necessary - considering object property instead) (moved out of V2 core to under consideration)
- [Triggering event (Inspection)](#triggering-event-inspection)
- [Triggering event (Maintenance Notification)](#triggering-event-maintenance-notification)
- [Triggering event (Structured maintenance)](#triggering-event-structured-maintenance)
- [Triggering event, operating](#triggering-event-operating)
- [Unchanging (stable)](#unchanging-stable)
************************************************************************************************************************************************
__Object properties__

under consideration
- enables 
- hasFunction 

************************************************************************************************************************************************

Items proposed to remove from March 2021 version of maintenance ontology as being unnecessary and at too detailed a level. They also become redundant once we establish that maintenance occurs due to a maintenance strategy

- Maintenance Standard Work Procedures Specification
- Maintenance Standard Work Specification 

Not necessary at the reference ontology level
- Failure modes and effects analysis specification

************************************************************************************************************************************************
## IOF required Annotations

The following is a transcription from the IOF_AnnotationsVocabulary_11Dec2020.rdf file

Current rules and expectations are at [Confluence](https://oagiscore.atlassian.net/wiki/spaces/IOF/pages/4384686095/Simplified+Annotations+Rules)

rdfs:label - The de facto use of rdfs:label is to exactly reflect (but not necessarily be exactly the same as) the local name of an element in an ontology. Example: If the IRI of a class was www.industrialontologies.org/core#ManufacturedProduct, the rdfs:label might be ‘Manufactured Product’. 

definition - A statement or formal explanation of the meaning of a concept

example - Use of this annotation is optional, but recommended if it will help a user understand the intended interpretation(s).

abbreviation - alternate short label for the resource

acronym - Use this annotation when there is a commonly accepted acronym

adaptedFrom - The source of the resource that was modified to create the subject resource

directSource - The definitive source of the subject resource.

source - The source can be a URL to a standard, common dictionary (e.g. Oxford), or similar reference. Or it can be a short description of where the entity being annotated was derived from.

Natural Language Definition - This annotation is Required for each class and relation of an IOF (OWL or Common Logic) ontology. There should be at most one. This natural language definition should be subject matter expert friendly and consistent with any formal definition or elucidation. Natural language definitions should use class and relation names with following caveats:  Relations – For those relations whose label (i.e. local identifier) consist of multiple terms use a space to separate the terms of the label and apostrophe marks to delineate them: e.g. ‘hasPlan’ would be written as ‘has Plan’.  Classes – For classes whose label has multiple distinct terms, e.g, ManufacturingOperationSpecification, separate the terms with a space but delineate them with apostrophe marks: ‘Manufacturing Operation Specification’.

First Order Logic Definition - The First Order Logic Definition annotation is comprised of the (complete) necessary and sufficient conditions. This annotation is Required for each non-primitive (aka non-axiomatic) class (i.e. unary relation) of a published IOF OWL ontology. This is the most authoritative and comprehensive definition of an IOF element.  There should be at most one First Order Logic definition.

Semi-Formal Natural Language Definition - this annotation is required if an element in an IOF OWL ontology has a First Order Logic definition or in a IOF Common Logic (where the element is defined using Common Logic).The intent of this annotation to provide a transition or bridge from the First Order Logic definition of a notion to the natural language definition. This definition is intended to help a user understand the intended interpretation of the notion. As example using the First Order Logic definition of ‘Product’ above, a semi-formal translation of that might be: Product =def. Continuant that is not a Person and not an Organization and not a Specifically Dependent Continuant and there is a Product Role that the thing has or bears.

elucidation - This annotation is Required for primitive (aka axiomatic) classes and relations.  It is intended to provide guidance or explain (in a natural language style) how to interpret the notion.
There should be at most one. It is used for terms without formal logical definitions of Necessary and Sufficient conditions. The annotation should be used in cases where the complete necessary and sufficient conditions have yet to be determined.

Note - A general note, for any purpose.

explanatoryNote - a note that provides additional explanatory information about a given notion or resource

comment - This annotation is optional. It use is not recommended. But if used, use it only once. This is a catch-all annotation to account for extra information or other bits of useful data to help a user understand the intent of an element.

__Acronym list summary__

Note:

rdfs:label:

definition:

example: 

abbreviation:

acronym:

adaptedFrom:

directSource:

source:

Natural Language Definition:

First Order Logic Definition:

Semi-Formal Natural Language Definition:

elucidation:

explanatoryNote:

comment:


We have added a biblography at the bottom for references used in the 'adaptedFrom' and 'directSource'. We are using last name and date for in-text citation e.g. (Karray2019), (IEC 60300-3.12, 2016)

*****************************************************************************************************************************************
__Useful Figures__

Please see figure at https://github.com/InfoneerTXST/IOF-SupplyChain-WG/blob/master/Documentation%20&%20Resources/Terms-Patterns-Modules/Pump-Example.md


******************************************************************************************************************************************
Note these terms are in alphabetical order

### Act of modality change

Note: This is believed to be important in the ontology to capture the state change - to be confirmed

rdfs:label: 

definition: 
acronym:MWO

example:

adaptedFrom:

directSource:

source:

Natural Language Definition: 

First Order Logic Definition: 

Semi-Formal Natural Language Definition:  

elucidation:

explanatoryNote:

comment:

******************************************************************************************************************************************************************


### Asset role 

Note - work in progress, definition uses undefined concept of ValueAddingProcess

rdfs:label - asset role

definition - the role played by an item when it has actual or potential value to an organisation

example: 

adapted from: N/A

source - ISO 55001:2014 Asset management — Overview, principles and terminology

Natural Language Definition - AssetRole = def. A role that inheres in some IOF:EngineeredSystem that has the capability to serve as the output of some UNK:ValueAddingProcess

First Order Logic Definition - $instanceOf(x, AssetRole, t) \equiv instanceOf(x, Role, t) \land \newline \exists y,w,z(instanceOf(y, EngineeredSystem, t) \land \newline bearerOf(y, x, t) \land hasCapability(y, w) \land \forall z(realises(z, w) \rightarrow \newline (instanceOf(z, ValueAddingProcess) \land has-specified-output(z, y))))$

Semi-Formal Natural Language Definition - An asset role x is equivalent to a role x such that there exists a component  y that is a bearer of the asset role x and has capability w. Any value adding process z that realises w has specified output y.

Explanatory Note - an asset is defined in the ISO 55001 (Asset Management Standard) as "item, thing or entity that has potential or actual value to an organization" with notes to entry: 
Note 1 Value can be tangible or intangible, financial or non-financial, and includes consideration of risks and liabilities. It can be positive or negative at different stages of the asset life.
Note 2 Physical assets usually refer to equipment, inventory and properties owned by the organization. Physical assets are the opposite of intangible assets, which are non-physical assets such as leases, brands, digital assets, use rights, licences, intellectual property rights, reputation or agreements
Note 3 A grouping of assets referred to as an asset system could also be considered as an asset
******************************************************************************************************************************************************************

### Bodyguard capability

Note: this has been proposed as a means to capture properties that prevent undesireable events or processes from occuring

rdfs:label: 

definition: 

acronym:MWO

example:

adaptedFrom:

directSource:

source:

Natural Language Definition:

First Order Logic Definition: 

Semi-Formal Natural Language Definition: 

elucidation:

explanatoryNote:

comment:
******************************************************************************************************************************************************************
### Disposition to fail

Note: this 

rdfs:label: potential to fail

definition: the susceptibility of an asset to a failure mechanism

acronym:MWO

example:

adaptedFrom:

directSource:

source:  https://github.com/InfoneerTXST/IOF-SupplyChain-WG/blob/master/Documentation%20&%20Resources/Terms-Patterns-Modules/Pump-Example.md

Natural Language Definition: def. A Disposition that inheres in a bearer in virtue of its being susceptible to bearing nonconfroming qualities or failing to meet functional requirements or fitness for use requirements

First Order Logic Definition:  

Semi-Formal Natural Language Definition: 

elucidation:

explanatoryNote:

comment:

******************************************************************************************************************************************************************
### Failure 

Note: see either failure event or failure process

******************************************************************************************************************************************************************



### Failure cause 
Note - not a high priority
******************************************************************************************************************************************************************
### Failure effect 
Note - not a high priority.
see discussion  https://github.com/uwasystemhealth/IOF_Maintenance_Working_Group_Private/issues/13

rdfs:label: failure effect

definition: Failure effect is the consequence of  failure, within or beyond the boundary of the failed item. 

acronym:MWO

example:

adaptedFrom:

directSource: IEC 60812:2020 \cite{IEC60812-2020}

source:

Natural Language Definition:

First Order Logic Definition: 

Semi-Formal Natural Language Definition: 

elucidation:

explanatoryNote: Explanatory Note from IEC 60812:2020
Note 1: for some analyses, it may be necessary to consider individual failure modes and their effects.
Note 2: Failure effect also covers the consequence of a failure, within or beyond the boundary of the failed process.

comment:
******************************************************************************************************************************************************************
******************************************************************************************************************************************************************
### Failure event

rdfs:label: Failure Event

definition: The loss of ability of an item to perform a required function 

acronym:

example:

adaptedFrom:

directSource: EN13306, 2017

source:

Natural Language Definition: The loss of ability of an item to perform a required function 

First Order Logic Definition: 

Semi-Formal Natural Language Definition: A BFO: process boundary where some process which realizes the required function of a material artifact ceases. (MH - 29/6/21 needs to be checked)


elucidation:

explanatoryNote:
MH-there may be a disconnect between the engineering standards definition and what the IOF have proposed with their FOL definition. A failure event on a bridge does not impact a production plan process.

NL definition above discussed at Source: https://github.com/InfoneerTXST/IOF-SupplyChain-WG/blob/master/Documentation%20&%20Resources/Terms-Patterns-Modules/Pump-Example.md

The term failure event is NOT defined in any of the main reliability and maintenance Standards.

Earlier definitions:

Semi-Formal Natural Language Definition: A BFO: process boundary where some process which realizes the initial phase of a material product production process plan ceases.

FOR MANUFACTURING PROCESSES ONLY: First Order Logic Definition: $instanceOf(z, FailureEvent, t) \equiv \newline \exists x,y,z,p(instanceOf(x, process, t) \land instanceOf(p, MaterialProductProductionProcessPlan, t) \land realizesInitialPhaseOfPlan(x, y, p) \land terminalProcessBoundary(z, x))$

A failure event z is equivalent to the terminal process boundary z of some process x where x realizes the initial phase y of a material product production process plan p.

1. def  An FSO: process which is the result of an FMO: failure event and results in an FMO: failure effect. Equivalent to (representedBy some FailureModeObservation) and (resultsIn some FailureEffect. It is represented by some FMO: failure mode observation. (MH - not a good definition as some failures are hidden and therefore not observed until we want to use the asset, e.g. failed faire alarms)

2. SME def :  Natural language definition: loss of ability to perform a required function (EN13306, 2017). 
	Note 1 to entry:  After failure the item has a fault, which may be complete or partial.  
	Note 2:  ”Failure” is an event, as distinguished from fault, which is a state.
	Note 3 to entry:  The concept as defined does not apply to items consisting of software only

3. A process or activity which results in functional failure of an item. Equivalent to (hasParticipant some Component) and (resultsIn some FunctionalFailure). (FMEA paper, forthcoming, 2021)

4. def. A Process Boundary that 1) occurs on a zero-dimensional temporal region that is part of a spatiotemporal region on which a Failure Process occures and 2) is the begining of some Nonconfroming Quality Stasis or Fault Stasis or Defective Stasis
Source: https://github.com/InfoneerTXST/IOF-SupplyChain-WG/blob/master/Documentation%20&%20Resources/Terms-Patterns-Modules/Pump-Example.md

5.  A BFO: terminal process boundary where some process which realizes the initial phase of a material product production process plan ceases.
Source: Maintenance WG Slack

6.  An FSO: process that results in an FMO: functional failure. 

7. def: A Process Boundary that 1) occurs on a zero-dimensional temporal region that is part of a spatiotemporal region on which a Failure Process occures and 2) is the begining of some Nonconfroming Quality Stasis or Fault Stasis or Defective Stasis

8. FOL English translation: A failure event z is equivalent to the terminal process boundary z of some process x where x realizes the initial phase y of a material product production process plan p

9. A BFO:process that precedes the ROM:State of Failure.

10. A process or activity which results in functional failure of an item. Equivalent to (hasParticipant some Component) and (resultsIn some FunctionalFailure)

comment:
******************************************************************************************************************************************************************


### Failure mechanism 
Note - may be an equivalent class to Failure Process

Explanatory Note: Previous work  - FailureMechanism =  A XXX:ProcessOfDegradation that results in a XXX:FailureEvent
IEC 60812:2020 \cite{IEC60812-2020} defines failure mechanism as a  process that leads to failure.
Note 1:the process can be physical, chemical, logical, or a combination thereof.
******************************************************************************************************************************************************************
### Failure mode 
Note - needs review, was written before the Maintenance WG discussions on stasis started.

rdfs:label: failure mode

definition: manner in which the inability of an item to perform a required function occurs

example:

adaptedFrom: 

directSource: EN13306:2017 defines failure mode as the "manner in which the inability of an item to perform a required function occurs"
source:

Natural Language Definition: FailureMode = def. A BFO:RealizableEntity that is the result of a XXX:FailureMechanism through which the XXX:StateOfFailure occurs.

First Order Logic Definition: $instanceOf(x, FailureMode, t) \equiv instanceOf(x, RealizableEntity, t) \land \newline ((\exists y,w(instanceOf(y, FailureMechanism, t) \land \newline (instanceOf(w, StateOfFailureComponent, t) \land precedes(y,w,t)) \lor \newline
(Ǝp,z(instanceOf(p, FailureMechanism, t) \land \newline (instanceOf(z, StateOfFailureMachine, t) \land precedes(p,z,t)))$

Semi-Formal Natural Language Definition: A failure mode x is equivalent to a realizable entity x such that either, there exists a failure mechanism y, a state of failure component w and y precedes w, or, there exists a failure mechanism p, a state of failure machine z and p precedes z.

elucidation:

explanatoryNote:
Other definition: 
IEC 60812: 2020 \cite{IEC60812-2020} defines as failure mode as the "manner in which failure occurs"

Earlier attempts to define: 
Note 1 to entry: A failure mode may be determined by the function lost or other state transition that occurred.
Note 2 to entry: Examples of hardware failure modes might be for a valve, "does not open", or for an engine, "does not start".
Note 3 to entry: A human failure mode is determined by the function lost as a result of human action, whether committed or omitted.

BFO:RealizableEntity that is the result of a MNT:FailureMechanism through which the MNT:StateOfFailure occurs.

comment:

******************************************************************************************************************************************************************

### Failure mode code
Note - this is an information artifact for the failure mode defined above. Needs defined.
******************************************************************************************************************************************************************
### Failure Process
Note: See if this is an equivalent class to failure mechanism

rdfs:label: 

definition: 

acronym:MWO

example:

adaptedFrom:

directSource:

source:https://github.com/InfoneerTXST/IOF-SupplyChain-WG/blob/master/Documentation%20&%20Resources/Terms-Patterns-Modules/Pump-Example.md

Natural Language Definition: A Process that changes some quality born by an Artifact and causes the the Artifact to become degraded or failed

First Order Logic Definition: 

Semi-Formal Natural Language Definition: 

elucidation:

explanatoryNote:

comment:
a process that causes the material artifact to fail to perform its desired function
******************************************************************************************************************************************************************
### Function (asset function)
Note: this is a BFO defined term but do we need an engineering version? BFOs definition of Function does not conform to BFO's definition of function. Based on BFO, a function is a disposition that a continuant (e.g., an asset) bears by design. The functions of an asset are independant of the owner's or user's needs or wants. I may want to use a screwdriver to open a can of paint but it is not the "intended" function of a screwdriver.  

rdfs:label: engineering function

definition: hat the owner or user of a physical asset or system wants it to do 

acronym:

example:

adaptedFrom:

directSource: SAE JA1011 & JA1012

source:

Natural Language Definition:

First Order Logic Definition: 

Semi-Formal Natural Language Definition: 

elucidation:

explanatoryNote:
BFO Formal def: f is a function means:
f is a disposition
& f exists in virtue of its bearer’s physical make-up
& this physical make-up is something that this bearer possesses because it came into being, either through evolution (in the case of natural biological entities) or through intentional design (in the case of artifacts), in order to realize processes of a certain sort. 
Source: https://www.researchgate.net/publication/304340796_Functions_in_Basic_Formal_Ontology

comment:



******************************************************************************************************************************************************************
### Functional failure (state)
Note: see potential confusion with functional failure state below. this term is not currently in the OWL file as on 16/4/21. See extensive earlier work on this in the explanatory note section.

rdfs:label: Stasis of functional failure

definition: A state in which a physical asset or system is unable to perform a specific function to a desired level of performance 

example:

adaptedFrom:

directSource: SAE JA1011 defines functional falure as "a state in which a physical asset or system is unable to perform a specific function to a desired level of performance" 

source:

Natural Language Definition:  = def. A IOF:State in which some IOF:component endures and does not meet a requirement

First Order Logic Definition: $instanceOf(x, StateOfFailureComponent, t) \equiv instanceOf(x, State, t) \land \newline \exists y,w(instanceOf(y, component, t) \land instanceOf(w, Requirement, t) \land \newline \neg(meets(y, w))$

Semi-Formal Natural Language Definition: A state of failure component x is equivalent to an IOF state x where for some component y and requirement w, y does not meet the requirement w.

elucidation:

explanatoryNote: Note the concept of functional failure is NOT defined in the most recent revisions of a) IEC 60812:2020 FMEA Standard \cite{IEC60812-2020} and b) ISO 14424:2016 Standard \cite{ISO14224-2016}. IEC 60300.3.11 (2011) \cite{ASIEC60300.3.11} defines functional failure as the  "reduction in function performance below desired level." 

The ROMAIN ontology defines it as "a ROM:state during which a CCO:artifact is unable to perform its BFO:function."

Hodkiewicz, Woods, Kluwer et al in their FMEA paper define functional failure as: the termination of ability of an item to perform a required function. Equivalent to (representedBy some FailureModeObservation) and (resultsIn some FailureEffect) and `object in fault state' is defined as: the state of an item resulting from a malfunction.

Other definitions discussed in this group include: 

A X:Stasis in which some MNT:MaintainableItem endures and is developing one or more failure modes. 
$instanceOf(x, StasisOfFailureMaintainableItem, t) \equiv instanceOf(x, Stasis, t) \land  \exists y,w(instanceOf(y, MaintainableItem, t) \land instanceOf(w, Requirement, t) \land \newline \neg(meets(y, w))$
A stasis of failure maintainable item x is equivalent to an stasis x where for some maintainable item y and requirement w, y does not meet the requirement.
and
def. A IOF:State in which some IOF:machine endures and does not meet a requirement
$instanceOf(x, StateOfFailureComponent, t) \equiv instanceOf(x, State, t) \land \newline \exists y,w(instanceOf(y, Machine, t) \land instanceOf(w, Requirement, t) \land  \neg(meets(y, w))$
A state of failure machine x is equivalent to an IOF state x where for some machine y and requirement w, y does not meet the requirement w.

comment:
******************************************************************************************************************************************************************
### Functional location
Note: not defined yet but important. FLOC is a key field in maintenance data. All maintenance work orders are issued against a functional location. A functional location is a code that uniquely identifies an item that performs a function in a specific location. At that functional location, the individual asset with a unique serial number can be changed out but the functional location stays when a replacement asset with a different serial number is installed. 
******************************************************************************************************************************************************************


### Inspection Action
Note: note defined yet
******************************************************************************************************************************************************************

### Maintainable Item
Note: 

rdfs:label: Maintainable Item

definition: 

example:

abbreviation:

acronym: 

adaptedFrom:

directSource:

source:

Natural Language Definition: A component or grouping of components on which maintenance is actioned according to a maintenance strategy.

First Order Logic Definition: Customer(​x​) ≡ ​Material Artifact(x) ∧ ∃​y(​ MaintainableItemRole(​y)​ ∧ has-role(​x,​ ​y)​ )

Semi-Formal Natural Language Definition: A maintainable item x is equivalent to a material artifact x and there exists some maintainable item role r such that x is a bearerof r.

elucidation:

explanatoryNote: See notes on earlier discussions

Issue#22: One earlier version of maintainable_item had 'Maintainable Item participates in at some time Failure Event' but this is not valid as maintainable items may not be involved in failure events.
Is 'Maintainable Item' something the needs maintenance performed on it, or something the may need to have maintenance performed on it? I think it also comes down to what inferences we want to apply to it. Is Maintainable Item something that an entity needs to be 'tagged' with to identify it as an item of interest for maintenance purposes (which I think I recall seeing somewhere) and have the reasoning tell whether all the information for such purposes is provided; or should the reasoning be able to infer that an entity is a Maintainable Item once it "breaks"? If the former, then I don't think you can apply either axiom. 
Sometimes maintenance is performed on a maintainable item without a failure event actually having occurred. For example, for a car, its maintenance strategy could be to check the oil at a certain time interval. This type of condition monitoring task still comes under the banner of "maintenance" even though the car has not "failed"

The above discussion seems to focus more on a definition of 'items that may fail' rather than 'items that may be maintained'. Which is it that we are trying to capture?

Agreed. Maybe a 'Maintainable Item' is one which is associated with some 'Maintenance Strategy'. I don't think the current scope of the maintenance ontology covers that yet does it?

I agree. The association between the 'item' and the 'maintenance activity' can be captured through the participation of the item in the maintenance activity that realizes the Maintainable Item Role.

Issue#2:  Maintainable item [included in IESA paper and current version of Terms] SME Def.A component or grouping of components on which maintenance is actioned. See also related conversation on maintainable item role...

comment:
******************************************************************************************************************************************************************
### Maintainable Item Role

Note: see maintainable item above

rdfs:label:Maintainable Item Role

definition: 

example:

abbreviation:

acronym:

adaptedFrom:

directSource:

source:

Natural Language Definition: A maintainable item role is a role a material artifact bears when participating in the maintenance management process

First Order Logic Definition: 

Semi-Formal Natural Language Definition: Maintainable Item Role = def. Role a Material Artifact has when participating in the maintenance management process

elucidation:

explanatoryNote:

comment: Previous work 
An IOF:MaterialArtifact that has a MNT:MaintainableItemRole.FOL Axiom.instanceOf(x, M aterialArtif act, t)≡instanceOf(x, Component, t)∧∃r(M aintainableItemRole(r)∧bearerOf(x, r))FOL English translation.

\paragraph{}
$instanceOf(x, MaintainableItemRole, t) \equiv instanceOf(x, Role, t) \land \newline \exists y,w,z(instanceOf(y, Component, t) \land bearerOf(y, x, t) \land hasCapability(y, w) \land$ \newline $\forall z(realises(z, w) \rightarrow (instanceOf(z, MaintenanceProcess) \land \newline  hasSpecifiedOutput(z, y))))$

\paragraph{FOL English translation:}
A maintainable item role x is equivalent to a role x such that there exists a component y that is a bearer of the maintainable item role x and has capability w. Any maintenance process z that realises w has specified output y. 

Issue#2: Formal Def.An IOF:MaterialArtifact that has a MNT:MaintainableItemRole.FOL Axiom.instanceOf(x, M aterialArtif act, t)≡instanceOf(x, Component, t)∧∃r(M aintainableItemRole(r)∧bearerOf(x, r))FOL English translation.

A maintainable item x is equivalent to a material artifact x and there exists some maintainable item role r such that x is a bearerof r.

def. A role that inheres in some IOF:Component that has the capability to serve as  the output of some MNT:MaintenanceProcess
******************************************************************************************************************************************************************
### Maintenance Action
Note: 

rdfs:label: maintenance action

definition: the execution of work authorised by a maintenance work order

example:

adaptedFrom:

directSource:

source:

Natural Language Definition: = def. A BFO:Process to perform work on an IOF:Component according to a MaintenanceWorkOrderSpecification. 

First Order Logic Definition: $instanceOf(x, MaintenanceAction, t) \equiv instanceOf(x, Process, t) \land \newline \exists y(instanceOf(y, MaintenanceWorkOrderSpecification, t) \land inputOf(y,x))$

Semi-Formal Natural Language Definition: A maintenance action x  is equivalent to a process x such that there exists a maintenance work order specification y and y in an input to x.

elucidation:

explanatoryNote:

comment:
******************************************************************************************************************************************************************
### Maintenance Notification 
Note: Need to resolve confusion between MWO record and notification (MWO's are approved). Note the current definition uses the notion of non-conformity which needs to be clearly defined

rdfs:label: maintenance notification

definition: 
acronym:MWO

example:

adaptedFrom:

directSource:

source:

Natural Language Definition: def. An IAO:InformationContentEntity describing a XXX:Non-conformity

First Order Logic Definition:  $instanceOf(x, MaintenanceNotification, t) \equiv \newline instanceOf(x, InformationContentEntity, t) \land  \newline \exists y(instanceOf(y, NonConformity, t) \land denotes(x, y, t))$

Semi-Formal Natural Language Definition: A maintenance notification x is equivalent to an information content entity x and it is the case that there exists a non-conformity y and x denotes y.

elucidation:

explanatoryNote:

comment:
******************************************************************************************************************************************************************

### Maintenance Plan Specification
Note: an important concept that needs work. Tentative definition - an information content entity describing the output of a planning process conducted by a maintenance planner

rdfs:label: maintenance plan

definition: 

acronym:MWO

example:

adaptedFrom:

directSource:

source:

Natural Language Definition: 

First Order Logic Definition:  

Semi-Formal Natural Language Definition: 

elucidation:

explanatoryNote: 
Def. An IAO:Plan_Specification containing MNT:Maintenance_Strategies and MNT:Maintenance_Standard_Work_Procedures for a MNT:Maintainable_Item over its UNK:Lifecycle.

The documentation of a plan for the maintenance of an asset over its life cycle

comment:
******************************************************************************************************************************************************************
### Maintenance Schedule List

Note: needs more work

rdfs:label: maintenance schedule

definition: a list of maintenance work orders to be executed in a defined period

acronym:MWO

example:

adaptedFrom:

directSource:

source:

Natural Language Definition: def. An IAO:InformationContentEntity describing a list of MNT:MaintenanceWorkOrderSpecification to be UNK:Executed in a defined period.

First Order Logic Definition:  $instanceOf(x, MaintenanceScheduleList, t) \equiv \newline instanceOf(x, InformationContentEntity, y) \land \newline \exists x1 , x2 , …, x n, \forall i (instanceOf(xi, MaintenanceWorkOrderSpecification, t) \land partOf(x i , x))$

Semi-Formal Natural Language Definition: A maintenance schedule list x is equivalent to an information content entity such that there exists a set of maintenance work order specification xi (for x1 to xn) where all xi are parts of x.

elucidation:

explanatoryNote:

comment:
******************************************************************************************************************************************************************


### Maintenance Stategy Development Process
Note: 

rdfs:label: maintenance strategy development process

definition: the process to identify a maintenance strategy for a functional failure on an asset or component

acronym:

example:

adaptedFrom:

directSource:

source: 

Natural Language Definition: A BFO:Process to identify an MNT:MaintenanceStrategySpecification for a XXX:FailureMode

First Order Logic Definition:  %$instanceOf(x, MaintenanceStategyDevelopmentProcess) \equiv instanceOf(x, Process) \land \exists y(instanceOf(y, MaintenanceStrategyType, t) \land isSpecifiedOutput(y, x, t))$

Semi-Formal Natural Language Definition: A maintenance strategy process x is equivalent to a process x and there exists some maintenance strategy specification y and y is the specified output of x.

elucidation:

explanatoryNote:

comment:
******************************************************************************************************************************************************************
### Maintenance Stategy Specification

Note: Vital concept, needs work, needs to be done in conjunction with the class above

rdfs:label: maintenance strategy specification

definition: 

example:

adaptedFrom:

directSource:

source: 

Natural Language Definition: def. An IAO:InformationContentEntity resulting from a maintenance strategy development process for a MNT:MaintainableItem

First Order Logic Definition:  $instanceOf(x, MaintenanceStrategyType, t) \equiv \newline instanceOf(x, InformationContentEntity, t) \land \newline
\exists w,z(instanceOf(w, specifiedOutput) \land hasCapability(x, w) \land \newline \forall z(realises(z, w) \rightarrow (instanceOf(z, MaintenanceStrategyDevelopmentProcess) \land hasSpecifiedOutput(z, x))))$

Semi-Formal Natural Language Definition: A maintenance strategy type x is equivalent to an information content entity x and it is the case that w is some specified output and x has capability w. If z realises w then z is maintenance strategy development process with specified output x. 

elucidation:

explanatoryNote:

comment:
******************************************************************************************************************************************************************
### Maintenance Work Order Record
Note: Need to resolve confusion between MWO record and notification (MWO's are approved)

rdfs:label: maintenance work order record

definition: the execution of work authorised by a maintenance work order

acronym:MWO

example:

adaptedFrom:

directSource:

source:

Natural Language Definition: def. An IAO:InformationContentEntity describing a desired MNT:MaintenanceAction 

First Order Logic Definition:  $instanceOf(x, MaintenanceWorkOrderSpecification, t) \equiv  \newline instanceOf(x, InformationContentEntity, t) \land \newline \exists y(instanceOf(y, MaintenanceAction, t) \land denotes(x, y, t))$

Semi-Formal Natural Language Definition: A maintenance work order specification x is equivalent to an information content entity x and it is the case that there exists a maintenance action y and x denotes y.

elucidation:

explanatoryNote:

comment:
******************************************************************************************************************************************************************


### Malfunction 
Note: May be aquivalent to a Functional Failure Event

rdfs:label: 

definition: 

acronym:MWO

example:

adaptedFrom:

directSource:

source:

Natural Language Definition:

First Order Logic Definition: 

Semi-Formal Natural Language Definition: 

elucidation:

explanatoryNote: malfunction is a process not a dispositon. https://github.com/uwasystemhealth/IOF_Maintenance_Working_Group_Private/issues/16
Malfunction is the inability of a continuent to not properly realize a function or function correctly. 

comment:
******************************************************************************************************************************************************************
### Mode
Note: A notion introduced by Chris Will that sits alongside Disposition as a sub-class of Function.
Failure Mode is realised by process called failure event. Source: Maintenance WG

rdfs:label: 

definition: 

acronym:MWO

example:

adaptedFrom:

directSource:

source:

Natural Language Definition:

First Order Logic Definition: 

Semi-Formal Natural Language Definition: 

elucidation:

explanatoryNote:

comment:
******************************************************************************************************************************************************************
### Non-conformity


rdfs:label: 

definition: 

acronym:MWO

example:

adaptedFrom:

directSource:

source:

Natural Language Definition: def. a BFO:disposition to a loss of quality, function or capability for a BFO:material entity or BFO:process

First Order Logic Definition: 

Semi-Formal Natural Language Definition: 

elucidation:

explanatoryNote:

comment:
******************************************************************************************************************************************************************

__Process of degradation__

Note: 

rdfs:label: degradation process

definition: a detrimental change in physical condition, with time, use or due to external cause

acronym:

example:

adaptedFrom:

directSource: EN13306 \cite{IEN13306}

source:

Natural Language Definition: 

First Order Logic Definition: 

Semi-Formal Natural Language Definition:

elucidation:
13306 definition: detrimental change in physical condition, with time, use or due to external cause
Note 1 to entry: Degradation may lead to a failure.
Note 2 to entry: In a system context, degradation may also be caused by failures within the system (see “degraded state”, 6.5).

IEC 60500-192 definition: detrimental change in ability to meet requirements
Note 1 to entry: Degradation may occur with storage or use, brought about by internal processes or effects of the environment.
Note 2 to entry: Degradation beyond specified limits may constitute a degraded state or failure.
Note 3 to entry: In a system context, degradation may also be caused by failures within the system.

explanatoryNote: 
EN

comment:
******************************************************************************************************************************************************************

### Stasis (CCO)
Note: 

rdfs:label: state

definition: a BFO:process in which some independent continuant endures  and  one  or  more  of  the  dependent  entities  it  bears  does  not  change  (in  kind  or intensity)

acronym:

example:

adaptedFrom:

directSource: CCO

source:

Natural Language Definition:

First Order Logic Definition: 

Semi-Formal Natural Language Definition: 

elucidation:

explanatoryNote:
- The stasis does not realise the quality. The stasis maintains some quality at some measured tolerance.
- Stasis has an unchanging quality

Source: Maintenance WG meeting

comment:
******************************************************************************************************************************************************************
### Stasis (fault/ object in fault state)
Note: 

rdfs:label: fault state

definition:  The state of an item characterized by inability to perform a required function,excluding the inability during preventive maintenance or other planned actions, 
or due to lack of external resources

acronym:MWO

example:

adaptedFrom:

directSource:

source:

Natural Language Definition:

First Order Logic Definition: 

Semi-Formal Natural Language Definition: 

elucidation:
SME def 1: 
Note  1  to  entry:  A  fault  usually  results  from  a  failure,  but  in  some  circumstances,  such  as specification, design, manufacture or maintenance, it may be a preexisting fault.
Source: EN 13306:2017

SME def 2: The state of an item resulting from a malfunction
Source: FMEA paper, forthcoming, 2021

SME def 3: A Stasis in which an Artifact no longer maintains some of its intended functions to a desired level of performance
Source: https://github.com/InfoneerTXST/IOF-SupplyChain-WG/blob/master/Documentation%20&%20Resources/Terms-Patterns-Modules/Pump-Example.md

explanatoryNote:

comment:
******************************************************************************************************************************************************************
### Stasis (defective)
Note: Not sure we need this right now

rdfs:label: 

definition: 

acronym:MWO

example:

adaptedFrom:

directSource:

source:

Natural Language Definition:

First Order Logic Definition: 

Semi-Formal Natural Language Definition: 

elucidation:

explanatoryNote:
SME def: A Stasis in which an Artifact fails to meet its intended usage requirements (or fittness for use requirements 
Source: https://github.com/InfoneerTXST/IOF-SupplyChain-WG/blob/master/Documentation%20&%20Resources/Terms-Patterns-Modules/Pump-Example.md

comment:
******************************************************************************************************************************************************************
### Stasis (degraded)
Note: A couple of definitions have been proposed.

rdfs:label: degraded state

definition: 

acronym:

example:

adaptedFrom:

directSource:

source:

Natural Language Definition: def. A stasis in which some MNT:maintainableItem endures and is developing one or more failure modes

First Order Logic Definition: 

Semi-Formal Natural Language Definition: A stasis of degradation maintainable item x is equivalent to an IOF stasis x such that for some component y: such that there is no failure mode at t, there is a failure mode, and t precedes t’.

elucidation:

explanatoryNote:
Other ideas

def.: A IOF:State in which some IOF:component endures and is moving towards non-conformity.
A state of degradation x is equivalent to an IOF state x such that for some component y: there is no non-conformity at t, there is a non-conformity, and t precedes t’
$instanceOf(x, StateOfDegradation, t) \equiv instanceOf(x, State, t) \land \newline \exists y,w,z(instanceOf(y, Component, t) \land \neg(instanceOf(w, nonConformity, t) \land instanceOf(w, nonConformity, t’) \land precedes(t, t’))$
English Translation: A state of degradation x is equivalent to an IOF state x such that for some component y:there is no non-conformity at t, there is a non-conformity, t precedes t’

comment:
******************************************************************************************************************************************************************
### Stasis (functional failure) 
see also Stasis (non-conforming quality) and functional failure event
Note: see dilemma over component, maintainable item, artifact

rdfs:label: 

definition: A state in which a physical asset or system is unable to perform a specific function to a desired level of performance 

acronym:

example:

adaptedFrom:

directSource: SAE JA1011

source:

Natural Language Definition: A IOF:State in which some IOF:component endures and does not meet a requirement 

First Order Logic Definition: 

Semi-Formal Natural Language Definition:  A state of failure component x is equivalent to an IOF state x where for some component y and requirement w, y does not meet the requirement w.

elucidation:

explanatoryNote:
a. When the system is in stasis on not correctly realizing functions or not functioning correctly
Source: Maintenance WG meeting
b. a IOF:state during which a CCO:artifact is unable to perform its BFO:function.
c. A stasis of failure maintainable item x is equivalent to an stasis x where for some maintainable item y and requirement w, y does not meet the requirement.

comment:
******************************************************************************************************************************************************************
### Stasis (nominal)

> Note: Not sure if we need this

> MSe: this is equivalent to the 'Operating State' of the Stasis Ontology

rdfs:label: 

definition: A Stasis in which an Artifcat endures and all Qualities born by the Artifact conform with the specifications and the Artifact meets intended usage requirements and functions as expected to a desired level of performance

acronym:MWO

example:

adaptedFrom:

directSource:

source:  https://github.com/InfoneerTXST/IOF-SupplyChain-WG/blob/master/Documentation%20&%20Resources/Terms-Patterns-Modules/Pump-Example.md

Natural Language Definition: 

First Order Logic Definition: 

Semi-Formal Natural Language Definition: 

elucidation:

explanatoryNote:

comment:
******************************************************************************************************************************************************************
### Stasis of down (down state)
 Note: this is in here for the MTConnect use case

rdfs:label: 

definition: state of an item being unable to perform a required function due to preventive maintenance or a fault (EN13306)
acronym:

example:

adaptedFrom:

directSource: EN13306 

source: 

Natural Language Definition:

First Order Logic Definition: 

Semi-Formal Natural Language Definition: 

elucidation:

explanatoryNote:

EN13306 \cite{EN13306}:  state of an item being unable to perform a required function due to preventive maintenance or a fault

Note 1 to entry: Down state relates to unavailability of the item.
Note 2 to entry: A down state is sometimes referred to as an internal disabled state.


IEC 60050-192: state of being unable to perform as required, due to internal fault, or preventive maintenance

Note 1 to entry: Down state relates to unavailability of the item.
Note 2 to entry: The adjectives “down” or “unavailable” designate an item in a down state.

ISO14224: internal disabled state of an item characterized either by a fault or by a possible inability to perform a required function during preventive maintenance

comment:
******************************************************************************************************************************************************************
### Stasis of up (up state)
 Note: this is in here for the MTConnect use case

rdfs:label: 

definition: state of an item being able to perform a required function (assuming that the external resources, if required, are provided) 

acronym:

example:

adaptedFrom:

directSource: EN13306 

source: 

Natural Language Definition:

First Order Logic Definition: 

Semi-Formal Natural Language Definition: 

elucidation:

explanatoryNote:
IEC 60050-192: state of being able to perform as required

ISO14224: state of an item characterized by the fact it can perform a required function, assuming that the external resources, if required, are provided

comment:
******************************************************************************************************************************************************************
### Stasis (Non conforming quality)
Note: 

rdfs:label: 

definition: A Stasis in which an Artifact bears some Quality that is outside the specification limits

acronym:MWO

example:

adaptedFrom:

directSource:

source: https://github.com/InfoneerTXST/IOF-SupplyChain-WG/blob/master/Documentation%20&%20Resources/Terms-Patterns-Modules/Pump-Example.md

Natural Language Definition:

First Order Logic Definition: 

Semi-Formal Natural Language Definition: 

elucidation:

explanatoryNote:

comment:
******************************************************************************************************************************************************************
### Switched/ powered on
 Note: 

rdfs:label: 

definition: 

acronym:MWO

example:

adaptedFrom:

directSource:

source:

Natural Language Definition:

First Order Logic Definition: 

Semi-Formal Natural Language Definition: 

elucidation:

explanatoryNote:

comment:
******************************************************************************************************************************************************************
### Triggering event
 Note: 

rdfs:label: 

definition: 

acronym:MWO

example:

adaptedFrom:

directSource:

source:

Natural Language Definition:

First Order Logic Definition: 

Semi-Formal Natural Language Definition: 

elucidation:

explanatoryNote: A BFO:process resulting in an action (or is it a process boundary?)

comment:
******************************************************************************************************************************************************************

### Triggering event (Maintenance)

Note: this is necessary in the ontology to define the moment in time when we know a maintenance action is required. this can come from a casual observation by an operator, an inspection, a structured maintenance task (such as fixed interval replacement), from condition monitoring, or in response to a failure. 
An event resulting in the generation of a maintenance notification or generation of a task with structured maintenance task specification (needs more thought. For the latter the triggering event is a state or date for which there is a task specification in place that is then initiated when the trigger occurs)

rdfs:label: 

definition: 
acronym:MWO

example:

adaptedFrom:

directSource:

source:

Natural Language Definition: def. A BFO:Process that initiates a MNT:MaintenanceAction  (this is too circular given the maintenance action definition) or  def. A BFO:Process resulting in a MNT:MaintenanceNotification or a MNT:StructuredMaintenanceTaskSpecification.

First Order Logic Definition: %$instanceOf(x, MaintenanceTriggeringEvent, t) \equiv instanceOf(x,BFO:Process, t) \land \exists y,z(instanceOf(y, MaintenanceProcess, t) \land instanceOf(z,MaintenanceAction, t) \land precedes(x, y) \land precedes(z, x))$ 

Semi-Formal Natural Language Definition: A maintenance triggering event x is equivalent to a process boundary x such that for some process y and some maintenance action z, and x precedes y and z precedes x. 

elucidation:

explanatoryNote:

comment:
******************************************************************************************************************************************************************
### Triggering event, operating
Note: 

rdfs:label: 

definition: 

acronym:MWO

example:

adaptedFrom:

directSource:

source:

Natural Language Definition: A BFO:ProcessBoundary in the operation of a IOF:ManufacturingProcess that begins a MNT:MaintenanceProcess

First Order Logic Definition: 

Semi-Formal Natural Language Definition: An operating triggering event x is equivalent to a process boundary x such that for some maintenance process y and some manufacturing process z, and x precedes y and z precedes x

elucidation:

explanatoryNote:

comment:
******************************************************************************************************************************************************************
******************************************************************************************************************************************************************
__Object Properties__

### Enables
 
Note: there should be some relationship like this defined between a stasis and a process. See ongoing discussion in https://github.com/uwasystemhealth/IOF_Maintenance_Working_Group_Private/issues/18

rdfs:label: enables

definition: To give some thing the  means to do something. (Or optionally, "to make operational") 

acronym:MWO

example: The person enables the lamp's function by flipping on the switch. A sufficient amount of activation energy enables some chain reaction in a mixture of hydrogen and oxygen. 

adaptedFrom:

directSource:

source: [Oxford Languages]

Natural Language Definition:

First Order Logic Definition: 

Semi-Formal Natural Language Definition: 

elucidation:

explanatoryNote:

comment:
******************************************************************************************************************************************************************

### hasFunction

SME def: x hasFunction y is a relation between an independent continuant (the bearer) and a function in which the function specifically depends on the bearer for its existence. -- sub-relation of BFO 'bearer of'.
Note: 

rdfs:label: 

definition: 

acronym:MWO

example:

adaptedFrom:

directSource:

source:

Natural Language Definition:

First Order Logic Definition: 

Semi-Formal Natural Language Definition: 

elucidation:

explanatoryNote:

comment:
******************************************************************************************************************************************************************



__Deprecated classes__ 
- removed from IOF Maintenance WG ontology vXXX

- Maintenance Non-standard Work Specification
- Maintenance Process
- Maintenance Standard Work Procedures Specification
- Maintenance Standard Work Specification
- Maintenance Strategy Specification
- Maintenanace Structured Maintenance Task Specification
- Machine identifier
- Failure modes and effects analysis specification
- Triggering event, operating
- Triggering event (Inspection)
- Triggering event (Maintenance notification)
- Triggering event (Structured maintenance)

*****************************************************************************************************************************
## Bibliography (in no particular order)

```bibtex
@book{EN13306,
  author = {{CEN}},
  title = {EN13306 Maintenance - Maintenance terminology},
  year = {2017},
  institution = {European Committee for Standardization},
  address     = {Brussels}
}

@techreport{IEC,
  type = {Standard},
  key = {AS IEC 60300.3.14},
  year = {2016},
  title = {{Dependability management Application guide - Maintenance and maintenance support}},
  volume = {2016},
  address = {Geneva, Switzerland}
}

@book{IEC60300.3.14,
	author = {{IEC}},
  title = {AS IEC 60300.3.14 Dependability management Application guide - Maintenance and maintenance support},
  year = {2016},
  institution = {International Electrochemical Commission},
  address     = {Geneva Switzerland}
} 

@book{IEC60300.3.11,
  author = {{IEC}},
  title = {AS IEC 60300.3.11 Dependability management Application guide - Reliability-centred Maintenance},
  year = {2011},
  institution = {International Electrochemical Commission},
  address     = {Geneva Switzerland}
} 

@book{IEC60812,
	author = {{IEC}},
  title = {IEC 60812 Failure modes and effects analysis (FMEA and FMECA)},
  year = {2020},
  institution = {International Electrochemical Commission},
  address     = {Geneva, Switzerland}
}

@book{ISO15926,
  author      = {{ISO}},
  title       = {ISO 15926 Industrial automation systems and integration -- Integration of life-cycle data for process plants including oil and gas production facilities -- Part 2: Data model},
  institution = {International Standards Organisation},
  address     = {Geneva Switzerland},
  year        = {2003}
}

@book{SAEJA1012,
	author = {{SAE}},
  title = {SAE JA1012 A guide to the  Reliability-centered maintenance (RCM) Standard},
  year = {2011},
  institution = {SAE International},
  address     = {London}
} 

@book{ISO13372,
	author = {{ISO}},
  title = {ISO 13372 Condition monitoring and diagnostics of machines - Vocabulary},
  year = {2012},
  institution = {International Standards Organization},
  address     = {Geneva, Switzerland}
 }

@book{SMRP,
	author = {SMRP},
  title = {SMRP Best Practice - Maintenance |\& Reliability Body of Knowledge},
  year = {2009},
  edition={5th.},
  publisher = {Society of Maintenance and Reliability Professionals},
  address     = {Atlanta, GA}
}

@article{Rajpathak2013,
  author={Rajpathak, Dnyanesh G},
  journal = {Computers in Industry},
  number = {5},
  pages = {565--580},
  publisher = {Elsevier B.V.},
  title = {{An ontology based text mining system for knowledge discovery from the diagnosis data in the automotive domain}},
  volume = {64},
  year = {2013}
}

@online{CUBRC2000,
  author = {CUBRC},
  title = {Common Core Ontologies for Data Integration},
  year= 2014,
  url = {https://www.cubrc.org/index.php/data-science-and-information-fusion/ontology},
  urldate = {2019-01-10}
}
```
