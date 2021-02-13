


# Locations 

Objects and processes can be related to places. Places are represented in two distinct, complementary ways by the BFO classes Site  (an immaterial region bound by an object) and Spatial Region  (a continuant part of space relative to a frame of reference). At any particular time, a site will coincide with (occupy) some spatial region. An independent continuant, such as a grain cart or a facility, is  _located in_  a Site  and occupies some Spatial Region.  _located in_  is a relation between an independent continuant and a site in which the independent continuant is entirely within the site. To be more accurate, Independent continuants  (_ic1_) is located in Site  (_s1_) when the spatial region that  _ic1_occupies is a (proper or improper) continuant part of the spatial region that s1 occupies. Since location is a temporal relationship, BFO 2020 has introduced temporalized versions of this relationship such that one can assert if a continuant is located in a site at all times or at some time.

Geospatial Region  is a special type of site at or near the surface of the earth. As can be seen in Figure  8, a Field Site  (a site of a Field with specified boundaries) is a type of Geospatial Region  and it can be explicitly asserted that a grain cart is  _located in_  some Field Site  when the spatial region occupied by the grain cart is part of the special region occupied by the field site. Similarly, it can be asserted that a Field, which is Piece of Land  (a bfo:fiat object part) that is used for agricultural purposes, is also located in some Field Site (Figure  9).  A Farm, however, is considered to be an Agricultural Facility  (Artifact) that has Field as its proper part. A Farm Site  may cover a larger area compared to a Field Site  because it includes more parts such as storage facilities and other buildings. Therefore, it is semantically invalid to assert that a Farm is located in a Field Site.


![A Grain Cart (Object) is located in a Site and the Transfer Event (Process) occurs at a site](https://github.com/InfoneerTXST/IOF-SupplyChain-WG/blob/master/Documentation%20%26%20Resources/images/location-1.png)

