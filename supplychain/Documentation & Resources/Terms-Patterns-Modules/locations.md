


# Locations 

Objects and processes are related to places. Objects are located in places and processes occur at places. Places are represented in two distinct, complementary ways by the BFO classes `Site` (an immaterial entity bound by an object) and `Spatial Region` (a continuant part of space relative to a frame of reference). At any particular time, a site and an independent continuant (excluding spatial regions) must occupy some spatial region. _located in_ is a relation between an independent continuant and a site when the independent continuant is entirely within the site. To be more accurate, independent continuants (ic1) is located in `Site` (s1) when the spatial region that ic1 occupies is a (proper or improper) continuant part of the spatial region that s1 occupies. 
For example, if the `Spatial Region` that a `Grain Cart` (gc) occupies is the continuant part of the `Spatial Region` that a `Field Site` (fs) occupies, then it can be asserted that `Grain Cart` (gc) is located in `Field Site` (fs). A more complete label for occupies relationship is in fact _occupies spatial region_. Since _located in_ and _occupies spatial region_ are both snapshots in time, they participate in temporal relationships and BFO 2020 has introduced temporalized versions of these relationships such that one can assert if a continuant is located in a site at all times or at some time, or in a particular (absolute) spatial region at all times or at some times.

In most agri-food traceability use cases, the sites of interest are at or near the surface of the earth. This type of site is a universal called `Geospatial Site` in the SCT ontology.  As can be seen in Figure 8, a Field Site (a site of a Field with specified boundaries) is a type of `Geospatial Site`. If a particular grain cart is ‘located in’ a particular field site at time t, then it can be inferred that the 2D spatial region occupied by the grain cart at time t must necessarily be part of the 2D spatial region occupied by the field site. Similarly, if it is asserted that a particular Field (i.e., a Piece of Land that is used for agricultural purposes) is located in some `Field Site` at all times, then it can be inferred that the spatial region occupied by the field must necessarily be part of the spatial region occupied by the field site at all times  (Figure 9). A `Farm` is considered to be an `Agricultural Facility` (Artifact) that has Field as its proper or improper part. A Farm Site occupies a larger two-dimensional spatial region compared to a Field Site because it includes more parts such as storage facilities and other buildings besides the field itself. Therefore, a Field Site is continuant part of a Farm Site. It is semantically invalid to assert that a Farm is located in a Field Site because there are some parts of the Farm Site that occupy some spatial region that is not part of the spatial region occupied by the Field Site. 



![A Grain Cart (Object) is located in a Site and the Transfer Event occurs at a site](https://github.com/InfoneerTXST/IOF-SupplyChain-WG/blob/master/Documentation%20%26%20Resources/images/location-3.png)

> Figure 8: A Grain Cart (Object) is located in a Site and the Transfer Event (Process) occurs at a site



![](https://github.com/InfoneerTXST/IOF-SupplyChain-WG/blob/master/Documentation%20%26%20Resources/images/location-4.png)

> Figure 9: A Field is a piece of land located in a Field Site. A Field can have multiple sub-Fields as its parts.

Sometimes the location of a Field or Farm needs to be specified in a more granular and precise manner than just specifying the site of the Field or Farm. For example, in many occasions, the approximate location of a Field or Farm needs to be specified based on some coordinate reference system such as the World Geodetic System (WGS) used by the Global Positioning System (GPS). The GPS position in the proposed ontology is represented by `Ground Spatial Point` (a point on the surface of the earth ) that is a type of Spatial Region (zero-dimensional spatial region). Suppose the idealized fiat point `Geospatial Position` (p) that represents Farm (f) occupies `Ground Spatial Point` (gp) at time t. The coordinates of the `Ground Spatial Point` (gp) are designated by a GPS Identifier (gps ID1) that is a type of `Designative Information Content Entity`. Then it can be inferred that gps ID1 also designates the position of Farm (f). This approach for specifying the position relative to a frame of reference is adopted from Common Core Ontologies (CCO) with some modifications to exclude Spatial Region form the range of located in relationship. The definitions of the main classes used in the location module of the SCT ontology are provided in Table 1.


> Table 1: The semi-formal natural language definition for some of the main classes used for specifying the locations of independent continuants 


| term | Semi-formal Natural Language Definition |
|--|--|
| Geospatial Position	| A zero-dimensional continuant fiat boundary (fiat point) that is at or near the surface of the Earth and fixed according to some Geospatial Coor-dinate Reference System.|
|Object Position Reference Point|A Fiat Point that is on the surface of an object and represents the   ob-ject and specifies the position the object relative to a Geospatial Coordi-nate Reference System.|
|Ground Spatial Point|A Zero-Dimensional Spatial Region that is an idealized point on the sur-face of an Astronomical Body.|
|Object Track Point|A zero-Dimensional Spatial Region that is an idealized point that an Ob-ject Position Reference Point occupies at some time during some mo-tion.|
|Object Track |A One-Dimensional Spatial Region that is the idealized line along which an Object has traversed during some motion.|
|Ground Track Point|A Zero-Dimensional Spatial Region that is an idealized point located on the surface of an Astronomical Body directly below an Object Track Point (subclass of Ground Spatial Point).|


![](https://github.com/InfoneerTXST/IOF-SupplyChain-WG/blob/master/Documentation%20%26%20Resources/images/location-1.png)

 > Figure 10: A Farm is represented by an idealized point (Geospatial Position) that occupies a Ground Spatial Point. The Ground Spatial point is a Zero-Dimensional Spatial Region which is designated by a GPS identifier.    

To specify the GPS location of a moving object, such as a truck, at any given moment in time, `Object Track Point` (a type of zero-dimensional spatial region) is used. The `Object Position Reference Point` (a fiat point that moves with its host) of a moving object occupies different instances of `Object Track Point` at different points in time. An `Object Track` (a type of one-dimensional spatial region) is a line composed of an infinite number of Object Track Points. It is the idealized line (trajectory) along which an Object has traversed during some motion. An `Object Track Point` is projected on the surface of the earth as `Ground Track Point` which is designated by some GPS Identifier (a type of Code Identifier). Through this chain of relationships, it can be inferred that the same instance of GPS Identifier individual also designates the position of the truck at time t (Figure 11). Although no property chain is introduced here, a super-property axiom can be added to the ontology to relate an object to its GPS position.

![](https://github.com/InfoneerTXST/IOF-SupplyChain-WG/blob/master/Documentation%20%26%20Resources/images/location-2.png)

> Figure 11: The location of moving objects is specified through using a sequence of position reference point occupying the object track point which is projected on ground track point at any given time. 

	
	
	
 

