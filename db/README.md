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

## Optimiertes Relationenmodell

```cypher
// Definiere die TRIP-Relation mit relevanten Zeitattributen
MATCH (s1:Station {name: 'Hauptbahnhof'})
MATCH (s2:Station {name: 'Jungfernstieg'})
CREATE (s1)-[:TRIP {
    line: "U1",
    line_name: "U-Bahn Linie 1",
    departure: datetime("2025-04-05T14:00:00"),
    arrival: datetime("2025-04-05T14:10:00"),
    day_type: "WEEKDAY"  // z.B. WEEKDAY, SATURDAY, SUNDAY
}]->(s2)
```

## Routensuche mit diesem Modell

```cypher
// Finde alle Routen von Start zu Ziel ab aktueller Zeit
MATCH path = (start:Station {name: 'Hauptbahnhof'})-[:TRIP*1..5]->(end:Station {name: 'Barmbek'})
WHERE ALL(r IN relationships(path) WHERE r.departure > datetime("2025-04-05T09:37:08"))

// Prüfe, ob die Umsteigezeiten ausreichend sind
WITH path, relationships(path) AS trips
WHERE ALL(
    i IN range(0, size(trips)-2) 
    WHERE trips[i+1].departure > trips[i].arrival + duration({minutes: 3})  // Minimale Umsteigezeit
)

// Berechne Gesamtreisezeit und weitere Informationen
WITH path, trips,
     trips[0].departure AS start_time,
     trips[size(trips)-1].arrival AS end_time,
     duration.between(trips[0].departure, trips[size(trips)-1].arrival) AS total_travel_time,
     [t IN trips | t.line] AS lines,
     [idx IN range(0, size(trips)-1) | 
         CASE WHEN idx = 0 OR trips[idx].line <> trips[idx-1].line
              THEN idx ELSE NULL END
     ] AS transfers

// Formatiere die Ausgabe
RETURN 
     start_time AS departure,
     end_time AS arrival,
     total_travel_time AS duration,
     size([t IN transfers WHERE t IS NOT NULL])-1 AS transfers,
     [n IN nodes(path) | n.name] AS stations,
     [r IN relationships(path) | r.line] AS lines
ORDER BY 
     // Primär nach Ankunftszeit sortieren
     end_time,
     // Sekundär nach Anzahl der Umstiege
     size([t IN transfers WHERE t IS NOT NULL])-1
LIMIT 5
```

## Verbessertes Datenmodell für die Implementierung

```cypher
// Stations-Knoten
CREATE (:Station {id: "Master:10017", name: "Großmannstraße", city: "Hamburg", 
                 location: point({longitude: 10.048892, latitude: 53.541155})})
CREATE (:Station {id: "Master:10018", name: "S Rothenburgsort", city: "Hamburg", 
                 location: point({longitude: 10.042595, latitude: 53.539027})})

// Trip-Relationen für einen Wochentag
MATCH (s1:Station {id: "Master:10017"})
MATCH (s2:Station {id: "Master:10018"})
CREATE (s1)-[:TRIP {
    trip_id: "T1001",
    line: "U1",
    departure: datetime("2025-04-05T09:40:00"),
    arrival: datetime("2025-04-05T09:45:00"),
    day_mask: [true, true, true, true, true, false, false]  // Mo-Fr
}]->(s2)

// Trip-Relationen für Wochenende
MATCH (s1:Station {id: "Master:10017"})
MATCH (s2:Station {id: "Master:10018"})
CREATE (s1)-[:TRIP {
    trip_id: "T1002",
    line: "U1",
    departure: datetime("2025-04-05T09:55:00"),
    arrival: datetime("2025-04-05T10:00:00"),
    day_mask: [false, false, false, false, false, true, true]  // Sa-So
}]->(s2)
```

## Import-Funktion für API-Daten

Hier ist eine Funktion, die hilft, Daten aus Ihrer API in dieses Modell zu importieren:

```python
def convert_departure_data_to_neo4j_trips(api_data):
    """
    Konvertiert Abfahrtsdaten aus der API in Neo4j-Trip-Relationen
    
    Erwartet API-Daten in diesem Format:
    {
        "departures": [
            {
                "line": "U1",
                "direction": "Norderstedt Mitte",
                "station": "Master:10017",
                "time": "2025-04-05T09:40:00",
                "nextStops": [
                    {"station": "Master:10018", "time": "2025-04-05T09:45:00"},
                    {"station": "Master:10019", "time": "2025-04-05T09:50:00"}
                ]
            }
        ]
    }
    """
    neo4j_trips = []
    
    for departure in api_data.get("departures", []):
        line_id = departure.get("line")
        direction = departure.get("direction")
        start_station = departure.get("station")
        start_time = departure.get("time")
        day_type = get_day_type(start_time)  # Funktion zur Bestimmung des Wochentags
        
        # Erstelle eine Relation für jede Haltestelle auf der Route
        for i, stop in enumerate(departure.get("nextStops", [])):
            # Bestimme Startstation (vorherige Station oder Abfahrtsstation)
            from_station = departure.get("nextStops", [])[i-1]["station"] if i > 0 else start_station
            from_time = departure.get("nextStops", [])[i-1]["time"] if i > 0 else start_time
            
            # Zielstation für dieses Segment
            to_station = stop["station"]
            to_time = stop["time"]
            
            trip = {
                "from_station": from_station,
                "to_station": to_station,
                "line": line_id,
                "direction": direction,
                "departure": from_time,
                "arrival": to_time,
                "trip_id": f"{line_id}_{start_time}_{start_station}_{i}",
                "day_type": day_type
            }
            
            neo4j_trips.append(trip)
    
    return neo4j_trips

def get_day_type(datetime_str):
    """Bestimmt den Wochentagstyp aus einem Datumsstring"""
    import datetime
    dt = datetime.datetime.fromisoformat(datetime_str.replace('Z', '+00:00'))
    weekday = dt.weekday()
    
    if weekday < 5:  # Montag-Freitag (0-4)
        return "WEEKDAY"
    elif weekday == 5:  # Samstag
        return "SATURDAY"
    else:  # Sonntag
        return "SUNDAY"
```

## Neo4j-Import-Query

```cypher
// Import der Trip-Daten
UNWIND $trips AS trip
MATCH (from:Station {id: trip.from_station})
MATCH (to:Station {id: trip.to_station})
MERGE (from)-[r:TRIP {
    trip_id: trip.trip_id
}]->(to)
SET r.line = trip.line,
    r.direction = trip.direction,
    r.departure = datetime(trip.departure),
    r.arrival = datetime(trip.arrival),
    r.day_type = trip.day_type
RETURN count(*) AS imported_trips
```

## Fazit

Ihr vorgeschlagener Ansatz mit direkten zeitgestempelten Relationen zwischen Stationen ist tatsächlich eleganter und effizienter für die meisten ÖPNV-Routing-Szenarien. Die Abfragen werden intuitiver, und Neo4j's Graph-Algorithmen können direkt angewendet werden.

Besonders nützlich ist dieses Modell für:
1. Zeitabhängige kürzeste Pfade
2. Berücksichtigung von Umsteigezeiten
3. Minimierung der Anzahl von Umstiegen
4. Dynamische Routenplanung mit aktuellen Zeiten
