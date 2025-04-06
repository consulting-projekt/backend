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

Nodes: POI, AOI


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



# Optimiertes Neo4j-Modell für ÖPNV-Routing

Sie haben einen wichtigen Punkt angesprochen! Ihr vorgeschlagenes Modell mit direkten zeitgestempelten Relationen zwischen Stationen ist tatsächlich für viele Routing-Szenarien deutlich effizienter und intuitiver. Das vereinfacht die Pfadsuche erheblich und ermöglicht sehr elegante Abfragen.

## Ihr vorgeschlagenes Modell

```
(Station1)-[:TRIP {line: "U1", departure: "14:00", arrival: "14:10"}]->(Station2)
```

Dieses Modell hat mehrere Vorteile:

### Vorteile:
1. **Direkte Pfadsuche**: Neo4j's Algorithmen wie `shortestPath` können direkt eingesetzt werden
2. **Einfache Zeitprüfung**: Filter auf Relationsattributen sind sehr effizient
3. **Intuitive Abfragestruktur**: Die Abfragen werden viel verständlicher
4. **Bessere Performance**: Weniger JOIN-artige Operationen notwendig


## Routensuche mit diesem Modell

```cypher
// Finde alle Routen von Start zu Ziel ab aktueller Zeit
MATCH path = (start:Station {name: 'Hauptbahnhof'})-[:CONNECTS_TO*1..5]->(end:Station {name: 'Barmbek'})
WHERE ALL(r IN relationships(path) WHERE r.departure_time > datetime("2025-04-05T16:09:39"))

// Prüfe, ob die Umsteigezeiten ausreichend sind
WITH path, relationships(path) AS trips
WHERE ALL(
    i IN range(0, size(trips)-2) 
    WHERE trips[i+1].departure_time > trips[i].arrival_time + duration({minutes: 3})  // Minimale Umsteigezeit
)

// Berechne Gesamtreisezeit und weitere Informationen
WITH path, trips,
     trips[0].departure_time AS start_time,
     trips[size(trips)-1].arrival_time AS end_time,
     duration.between(trips[0].departure_time, trips[size(trips)-1].arrival_time) AS total_travel_time,
     [t IN trips | t.line_id] AS lines,
     [idx IN range(0, size(trips)-1) | 
         CASE WHEN idx = 0 OR trips[idx].line_id <> trips[idx-1].line_id
              THEN idx ELSE NULL END
     ] AS transfers

// Formatiere die Ausgabe
RETURN 
     start_time AS departure,
     end_time AS arrival,
     total_travel_time AS duration,
     size([t IN transfers WHERE t IS NOT NULL])-1 AS transfers,
     [n IN nodes(path) | n.name] AS stations,
     [r IN relationships(path) | r.line_name] AS lines
ORDER BY 
     // Primär nach Ankunftszeit sortieren
     end_time,
     // Sekundär nach Anzahl der Umstiege
     size([t IN transfers WHERE t IS NOT NULL])-1
LIMIT 5
```
