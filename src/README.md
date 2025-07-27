# sources

1. neo 4j project routing with openstreetmap data
- https://neo4j.com/blog/developer/routing-web-app-neo4j-openstreetmap-leafletjs/
- code: https://github.com/johnymontana/openstreetmap-routing-web-app-workshop
- tutorial: https://www.youtube.com/watch?v=Z4XZgsbaD9c

3. geofox
https://gti.geofox.de/html/GTIHandbuch_p.html#methode-liststations
- wurde beantragt

4. gtfs transparenzportal hamburg
- https://suche.transparenz.hamburg.de/dataset/hvv-fahrplandaten-gtfs-maerz-2025-bis-dezember-2025


# Design

Nodes: POI, AOI, Station


POI & AOI
- name, street, housnumber, postcode, 
- description based on (osm: description:de + description)
- tags based on: office, amenity, community_centre, operator, building, sport, dsa:criteria, official_name, operator:type, tourism

## geofox
### import
filter:
- serviceTypes = ZUG, BUS

import pois
    - URL: /gti/public/checkName 
    - darin können auch stations enthalten sein mit zusatz info ob innerCity

## graph rag
### vector index
https://neo4j.com/docs/neo4j-graphrag-python/current/user_guide_rag.html#vector-cypher-retriever



