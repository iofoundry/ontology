


# Locations 

Objects and processes can be related to places. Places are represented in two distinct, complementary ways by the BFO classes `Site`  (an immaterial region bound by an object) and `Spatial Region`  (a continuant part of space relative to a frame of reference). At any particular time, a site will coincide with (occupy) some spatial region. An independent continuant, such as a grain cart or a facility, is  _located in_  a Site  and occupies some Spatial Region.  _located in_  is a relation between an independent continuant and a site in which the independent continuant is entirely within the site. To be more accurate, Independent continuants  (_ic1_) is located in Site  (_s1_) when the spatial region that  _ic1_ occupies is a (proper or improper) continuant part of the spatial region that s1 occupies. Since location is a temporal relationship, BFO 2020 has introduced temporalized versions of this relationship such that one can assert if a continuant is located in a site at all times or at some time.

`Geospatial Region` is a special type of site at or near the surface of the earth. As can be seen in Figure  8, a `Field Site`  (a site of a Field with specified boundaries) is a type of Geospatial Region  and it can be explicitly asserted that a grain cart is  _located in_  some Field Site  when the spatial region occupied by the grain cart is part of the special region occupied by the field site. Similarly, it can be asserted that a Field, which is Piece of Land  (a bfo:fiat object part) that is used for agricultural purposes, is also located in some Field Site (Figure  9).  A Farm, however, is considered to be an Agricultural Facility  (Artifact) that has Field as its proper part. A `Farm Site`  may cover a larger area compared to a `Field Site`  because it includes more parts such as storage facilities and other buildings. Therefore, it is semantically invalid to assert that a `Farm` is located in a `Field Site`.


![A Grain Cart (Object) is located in a Site and the Transfer Event occurs at a site](https://github.com/InfoneerTXST/IOF-SupplyChain-WG/blob/master/Documentation%20%26%20Resources/images/location-3.png)

> Figure 8: A Grain Cart (Object) is located in a Site and the Transfer Event (Process) occurs at a site



![](https://github.com/InfoneerTXST/IOF-SupplyChain-WG/blob/master/Documentation%20%26%20Resources/images/location-4.png)

> Figure 9: A Field is a piece of land located in a Field Site. A Field can have multiple sub-Fields as its parts.

Sometimes the location of a Field or Farm needs to be specified in a more granular and precise manner than just specifying the site of the Field or Farm. For example, in many occasions, the location of a Field or Farm needs to be specified based on some coordinate reference system such as the World Geodetic System (WGS) used by the Global Positioning System (GPS). The GPS location (or position) in the proposed ontology is represented  by Ground Spatial Point (a point on the surface of the earth ) that is a type of `Spatial Region` (zero-dimensional spatial region). Suppose the idealized fiat point `Geospatial Position` (p) that represents Farm (f) occupies `Ground Spatial Point` (gp) at time t. The coordinates of the `Ground Spatial Point` (gp) are designated by a `GPS Identifier` (gps ID1) that is a type of Designative Information Content Entity. Then it can be inferred that _gps ID1_ also designates the position of `Farm` (f). This approach for specifying the location is adopted from Common Core Ontologies (CCO) with some modifications to exclude Spatial Region form the range of -located in- relationship. The definitions of the main classes used in the location module of the SCT ontology are provided in Table 1.

> Table 1: The semi-formal natural language definition for some of the main classes used for specifying the locations of independent continuants 

| term | Semi-formal Natural Language Definition |
|--|--|
| Geospatial Position	| A zero-dimensional continuant fiat boundary that is at or near the surface of the Earth and fixed according to some Geospatial Coordinate Reference System.|
|Object Position Reference Point| A zero-dimensional continuant fiat boundary that is on the surface of an object and represents the spatial location of the object.|
|Ground Spatial Point|A Zero-Dimensional Spatial Region that is an idealized point located on the surface of an Astronomical Body.|
|Object Track Point|A zero-Dimensional Spatial Region that is an idealized point where an Object is or was located during some motion.|
|Object Track |A zero-Dimensional Spatial Region that is an idealized point where an Object is or was located during some motion|
|Ground Track Point|	A Zero-Dimensional Spatial Region that is an idealized point located on the surface of an Astronomical Body directly below an Object Track Point (subclass of Ground Spatial Point)|


![](https://github.com/InfoneerTXST/IOF-SupplyChain-WG/blob/master/Documentation%20%26%20Resources/images/location-1.png)

 > Figure 10: A Farm is represented by an idealized point (Geospatial Position) that occupies a Ground Spatial Point. The Ground Spatial point is a Zero-Dimensional Spatial Region which is designated by a GPS identifier.    

To specify the GPS location of a moving object, such as a truck, at any given moment in time, `Object Track Point` (a type of zero-dimensional spatial region) is used. The `Object Position Reference Point` (a fiat point that moves with its host) of a moving object occupies different instances of `Object Track Point` at different points in time. An `Object Track` (a type of one-dimensional spatial region) is composed of an infinite number of Object Track Points. It is the idealized line (trajectory) along which an Object has traversed during some motion. An object track point is projected on the surface of the earth as Ground Track Point which is designated by some GPS Identifier. Through this chain of relationships, it can be inferred that the same  GPS Identifier individual also designates the position of the truck at time t (Figure 11). 

![](https://github.com/InfoneerTXST/IOF-SupplyChain-WG/blob/master/Documentation%20%26%20Resources/images/location-2.png)

> Figure 11: The location of moving objects is specified through using a sequence of position reference point occupying the object track point which is projected on ground track point at any given time. 

	
	
	
 

