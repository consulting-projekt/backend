kürzester Pfad von einer zur nächsten Station
```cypher
// Find the true shortest path between Herthastraße and Hamburg Hbf
MATCH (bfr:Station {name: 'Herthastraße'}),
      (ndl:Station {name: 'Hamburg Hbf'})
      
// Use shortestPath algorithm for a single shortest path
MATCH p = shortestPath((bfr)-[:CONNECTS_TO*]-(ndl))

// Calculate travel time and get path details
WITH p,
     reduce(acc = 0.0, r in relationships(p) | acc + r.duration) AS travel_minutes,
     length(p) as connections,
     [node in nodes(p) | node.name] as stations,
     [rel in relationships(p) | rel.line_name] as lines,
     [rel in relationships(p) | rel.line_unique] as line_uniques

// Count line changes
WITH travel_minutes, connections, stations, lines, line_uniques,
     CASE WHEN size(line_uniques) <= 1 
          THEN 0 
          ELSE reduce(changes = 0, i IN range(0, size(line_uniques)-2) | 
               CASE WHEN line_uniques[i] <> line_uniques[i+1] 
                    THEN changes + 1 ELSE changes END)
     END AS transfers

// Calculate total time with transfer penalties
RETURN 
    travel_minutes,
    transfers,
    travel_minutes + (transfers * 5.0) AS total_minutes,
    connections,
    stations,
    lines,
    line_uniques as lines_detail
```

pois in nähe einer station
```
// Find Hamburg Hbf station first
MATCH (station:Station {name: 'Hamburg Hbf'})
WHERE station.location IS NOT NULL

// Find nearest POIs using point distance calculation
MATCH (poi:POI)
WHERE poi.location IS NOT NULL

// Calculate distance between station and POIs
WITH station, poi, 
point.distance(station.location, poi.location) AS distance
ORDER BY distance ASC
LIMIT 10

// Return results with distance in meters
RETURN poi.name AS poiName,
       poi.description AS description,
       poi.tags AS tags,
       poi.addr_street AS street,
       poi.addr_housenumber AS housenumber,
       poi.addr_postcode AS postcode,
       toInteger(distance) AS distance_meters
```

pois in nähe eines aoi (Stadtpark)
```
// Find the Stadtparksee AOI
MATCH (aoi:AOI {name: 'Stadtparksee'})
WHERE aoi.boundary_lons IS NOT NULL AND aoi.boundary_lats IS NOT NULL

// Get all POIs
MATCH (poi:POI)
WHERE poi.location IS NOT NULL

// Calculate initial distance to centroid for efficiency
WITH aoi, poi, 
     point.distance(poi.location, aoi.centroid) AS centroid_distance,
     size(aoi.boundary_lons) as num_points

// Filter by proximity to centroid first
ORDER BY centroid_distance
LIMIT 100

// Calculate minimum distance to any boundary point
WITH aoi, poi, centroid_distance,
     range(0, size(aoi.boundary_lons) - 1) AS indices
UNWIND indices AS i
WITH aoi, poi, centroid_distance, i
WHERE aoi.boundary_lons[i] <> -999.0  // Skip separator points
WITH aoi, poi, centroid_distance, i,
     point.distance(
       poi.location, 
       point({longitude: aoi.boundary_lons[i], latitude: aoi.boundary_lats[i]})
     ) AS point_distance

// Get minimum distance for each POI
WITH aoi, poi, min(point_distance) AS min_distance
ORDER BY min_distance ASC
LIMIT 10

// Return the results
RETURN poi.name AS poi_name,
       poi.description AS description,
       poi.tags AS tags,
       poi.addr_street AS street,
       poi.addr_housenumber AS housenumber,
       poi.addr_postcode AS postcode,
       toInteger(min_distance) AS distance_meters
```