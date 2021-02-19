# Pump Use Case Description:
Consider an industrial water pump used in a cooling tower that has a type of mechanical seal as shown in the following image. Due to some residual stress in the seal (caused by nonuniform cooling during the casting process, for example), an internal crack forms and begins to grow gradually inside the seal. As the crack grows, the pump begins to operate with some unusual noise and mild vibration. However, the pump functions as intended (i.e., pumps water with the nominal pressure of 100 l/s as expected). After a few days, the crack reaches the surface of the seal. At this point, leaking begins and, as a result, the pump is only delivering 40 l/s.  Therefore, the pump is unable to perform its intended function to a desired level of performance. A request for service is initiated and a maintenance technician responds to the request and fixes the pump by replacing the seal and the pump begins to function normally as intended. 

## Failure Process, Event, and Stasis:
In the proposed formalization, failure event is considered to be a process boundary that the begins a failed stasis. An artifact is in a state of failure if it fails to conform with specifications and requirements. A failure event is preceded by a failure process. A failure process is a process that changes an artifcat, or one or more of its parts, in a way that it eventually becomes nonconforming, defective, of disfunctional. In the pump example, the crack in the mechanical seal is formed during some _crack formation process_ with an unknown start time. As the crack grows, it renders the seal defective (because crack is a _defect_ according to the specifications). When the crack grows beyond a certain size, at a certain point in time, the seal fails to perform the _bodyguard function_ of leak prevention. Here is when the functional failure event occurs and the pump enters a fault stasis. Note that the same failure process (change process) that turns the seal into a defective component continues to unfold in time until it causes the pump to become dysfunctional. 

![](https://github.com/InfoneerTXST/IOF-SupplyChain-WG/blob/master/Documentation%20%26%20Resources/images/failure-event.png)

| Term | Semi-formal Natural Language Definition |
|--|--|
| Nonconforming Quality Stasis	| A Stasis in which an Artifact bears some Quality that fails to conform with the specifications of the Artifact|
| Fault (Defunct) Stasis	|A Stasis in which an Artifact no longer maintains some of its intended functions to a desired level of performance|
| Defective Stasis	| A Stasis in which an Artifact fails to meet its intended usage requirements| 
| Nominal Stasis	|A Stasis in which an Artifcat endures and all Qualities born by the Artifcat conform with the specifications and the Artifact meets intended usage requirements and functions as expected to a desired level of performance|
| Failure Process	|A Process that changes some Quality or Disposition born by an Artifact and causes the the Artifcat to become nonconforming, defective, or faulty|
| Failure Event	|A Process Boundary that 1) occurs on a zero-dimensional temporal region that is part of a one-dimensional temporal region on which a Failure Process occures and 2) is the begining of some Nonconfroming Quality Stasis or Fault Stasis or Defective Stasis|
| Functional Failure Event	|A Failure Event that is the begining of and some Fault Stasis|


![](https://github.com/InfoneerTXST/IOF-SupplyChain-WG/blob/master/Documentation%20%26%20Resources/images/pump-stasis.png)

## Disposition Vs. Predesposition
