## sources

1. neo 4j project routing with openstreetmap data
- https://neo4j.com/blog/developer/routing-web-app-neo4j-openstreetmap-leafletjs/
- code: https://github.com/johnymontana/openstreetmap-routing-web-app-workshop
- tutorial: https://www.youtube.com/watch?v=Z4XZgsbaD9c

2. osm for neo4j
- https://github.com/neo4j-contrib/osm

3. geofox
https://gti.geofox.de/html/GTIHandbuch_p.html#methode-liststations
- wurde beantragt

4. gtfs transparenzportal hamburg
- https://suche.transparenz.hamburg.de/dataset/hvv-fahrplandaten-gtfs-maerz-2025-bis-dezember-2025

### haltestellen
- nachteil osm 
    - tags nicht konsistent
- mögliche alternative: openaddresses.io
    - https://www.youtube.com/watch?v=Z4XZgsbaD9c 1:30


# Design

Nodes: POI, AOI, Station


POI
- geometry in WKT format mit shape: (Längengrad Breitengrad) z.b. (9.97694 53.55304)


AOI
- geometry in WKT format mit shape: ((Längengrad Breitengrad), (Längengrad Breitengrad), (Längengrad Breitengrad), ...)

POI & AOI
- name, street, housnumber, postcode, 
- description based on (osm: description:de + description)
- tags based on: office, amenity, community_centre, operator, building, sport, dsa:criteria, official_name, operator:type, tourism

## geofox
### import
filter:
- serviceTypes = ZUG, BUS


import von stationen
    - listStations

import von abfahrten zu jeder station
    - URL: /gti/public/departureList 
    - direction -> combinedName
    - dierctionId Hin- (1) und Rückrichtung (6) 
    bsp. resp:
    "departures": [{'line': {'name': 'U2',
    'direction': 'Jungfernstieg',
    'origin': 'Hammer Kirche',
    'type': {'simpleType': 'TRAIN',
     'shortInfo': 'U',
     'longInfo': 'U-Bahn',
     'model': 'U-Bahn'},
    'id': 'HHA-U:U2_HHA-U'},
   'directionId': 6,
   'timeOffset': 1,
   'serviceId': 27552,
   'station': {'combinedName': 'Berliner Tor', 'id': 'Master:10952'},
   'platform': 'Gleis 3',
   'realtimePlatform': 'Gleis 3'},
   ...

import pois
    - URL: /gti/public/checkName 
    - darin können auch stations enthalten sein mit zusatz info ob innerCity


## graph rag
### vector index
https://neo4j.com/docs/neo4j-graphrag-python/current/user_guide_rag.html#vector-cypher-retriever



