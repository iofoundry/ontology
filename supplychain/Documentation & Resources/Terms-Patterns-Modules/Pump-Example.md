# Pump Use Case Description:
Consider an industrial water pump used in a cooling tower that has a type of mechanical seal as shown in the following image. Due to some residual stress in the seal (caused by nonuniform cooling during the casting process, for example), an internal crack forms and begins to grow gradually inside the body of the seal. As the crack grows, the pump begins to operate with some unusual noise and mild vibration. However, the pump functions as intended (i.e., pumps water with the nominal pressure of 100 l/s as expected). After a few days, the crack reaches the surface of the seal. At this point, leaking begins and, as a result, the pump is only delivering 40 l/s.  Therefore, the pump is unable to perform its intended function to a desired level of performance. A request for service is initiated and a maintenance technician responds to the request and fixes the pump by replacing the seal and the pump then resumes to function normally as intended. 

<p align="center">
<img  align="center"  src="https://github.com/InfoneerTXST/IOF-SupplyChain-WG/blob/master/Documentation%20%26%20Resources/images/pump.png"
	title="a pump" height="300">
</p>

<p align="center">
	Figure 1: A typical pump with a mechanical seal
</p>


## Failure Process, Event, and Stasis:
In general, an event can be instantaneous or it can have a duration. In the proposed formalization, `Failure Event` is considered to be an instantaneous event or `process boundary`that initiates a failed stasis as shown in Figure 1. An artifact is in a state of failure (`Failed Stasis`) if it fails to conform with the specifications and requirements of the artifact. A `Failure Event` is preceded by a `Failure Process`. A `Failure Process` is a process that changes an artifcat, or one or more of its parts, in a way that it eventually becomes nonconforming, defective, or dysfunctional. A failure process may continue beyond the failure event. In the pump example, the crack in the mechanical seal is formed during some _crack formation process_ with an unknown start time. As the crack grows, it renders the seal defective (because crack is a _defect_ according to the specifications). When the crack grows beyond a certain size, at some point in time, the seal fails to perform the _bodyguard function_ of leak prevention. Here is when the `Functional Failure Event` occurs and the pump enters a `Fault Stasis`. This approach is consistent with viewing an event as a minimal unit of observable change. In this example, the _observable change_ is leaking and reduction in pumping pressure (a process profile).  Note that the same failure process (crack formation process) that turns the seal into a defective component, continues to unfold in time until it causes the pump to become dysfunctional. 

<p align="center">
<img  align="center"  src="https://github.com/InfoneerTXST/IOF-SupplyChain-WG/blob/master/Documentation%20%26%20Resources/images/failure-event.png">
</p>
<p align="center">
	Figure 2: The relationship between failure process, event, and stasis
</p>


| Term | Semi-formal Natural Language Definition |
|--|--|
| Nonconforming Quality Stasis	| A Stasis in which an Artifact bears some Quality that is outside the specification limits|
| Fault (Defunct) Stasis	|A Stasis in which an Artifact no longer maintains some of its intended functions to a desired level of performance|
| Defective Stasis	| A Stasis in which an Artifact fails to meet its intended usage requirements (or fittness for use requirements )| 
| Nominal Stasis	|A Stasis in which an Artifcat endures and all Qualities born by the Artifcat conform with the specifications and the Artifact meets intended usage requirements and functions as expected to a desired level of performance|
| Failure Process	|A Process that changes some Quality or Disposition born by an Artifact and causes the the Artifcat to become nonconforming, defective, or faulty|
| Failure Event	|A Process Boundary that 1) occurs on a zero-dimensional temporal region that is part of a spatiotemporal region on which a Failure Process occures and 2) is the begining of some Nonconfroming Quality Stasis or Fault Stasis or Defective Stasis|
| Functional Failure Event|A Failure Event that is the begining of and some Fault Stasis|
| Disposition to Fail|A Disposition that inheres in a bearer in virtue of its being susceptible to bearing nonconfroming qualities or failing to meet functional requirements or fittness for use requirements|


![](https://github.com/InfoneerTXST/IOF-SupplyChain-WG/blob/master/Documentation%20%26%20Resources/images/pump-stasis.png)


<p align="center">
<img  align="center"  src="https://github.com/InfoneerTXST/IOF-SupplyChain-WG/blob/master/Documentation%20%26%20Resources/images/FailureModule.png">
</p>
<p align="center">
	Figure 3: The top-level classes of the Failure Module 
</p>

## Disposition Vs. Predisposition
In FMEA process, we try to identify all potential types of failure that might happen in an item (the ways things can go wrong in an item which is referred to as _failure mode_). The failures listed in FMEA table point to the propensity of an item to behave in certain ways or fail to meet the requirements. Therefore, in BFO sense, they are _dispositions_ or, more accurately, `Disposition to Fail`. Dispositions are _internally grounded_ realizable entities meaning that they can be realized when the bearer is in some special _physical_ circumstances or conditions. Dispositions come to existance in virtue of bearer's physical make-up or properties. A pump doesn't have a disposition to leak when it is normal conditions physically. But it can acquire a disposition to leak if certain conditions are present in the pump such as a damaged gasket or a cracked seal. Therefore, we can assert that any pump is _predisposed_ to disposition to leak (i.e., it has a disposition to have a disposition to leak). A pump with a damaged gasket is already disposed to leak becasue there exist a physical disorder (damaged gasket) in the pump. Predispositions are  _risk factors_ that we care about them and would like to have mitigation plans in place to deal with them in case they are ealized. But for example, we don't say a pump is predisposed to explode because it is not possiblility based on the physical make-up and design specifications of a typical pump . Currently we don't have a relationship _has predisposition_ in BFO or IOF but it is sensible to have one. 

## Open Issues
- Do we need to create a _state diagram_ for maintenance to relate 'events' to 'states' in a more granular way?  
- Since failures are connected to _requirements_ in the proposed definitons, it is necessary to have a formalization of functional and nonfunctional requirements and specifications. 
- _Crack_ is a `site` in BFO and it cannot be treated as a Specifically Dependant Continuant. Therefore, we cannot say, for instance, Seal(x) _is bearer of_ Crack(y). The surface of the seal (fiat object part of the seal)is the material boundary for the crack. The question is what should be a relationship for relating a crack to its host, or a pump, for that matter. We would like to classify both crack and bump as types of defects that may render an item defective. 

   - Barry's comments on crack: "a crack is a site, in BFO terms
a break is, first of all, a process (properly called the process of breaking) whose output is an object aggregate whose member parts are objects which correspond in the obvious way [we do not have a name for this but 'transformation-of' might work] to certain fiat object parts of the broken object that had existed immediately before the break". 



