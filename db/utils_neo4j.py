from tqdm import tqdm
import pandas as pd

# First, define Cypher queries to create constraints and indexes
## osm specific constraints and indexes
osm_constraint_query = "CREATE CONSTRAINT IF NOT EXISTS FOR (i:POI) REQUIRE i.osmid IS UNIQUE"
osm_constraint_query2 = "CREATE CONSTRAINT IF NOT EXISTS FOR (i:AOI) REQUIRE i.osmid IS UNIQUE"

## Geofox specific constraints and indexes
geofox_constraint_query = "CREATE CONSTRAINT IF NOT EXISTS FOR (i:POI) REQUIRE i.geofoxid IS UNIQUE"
geofox_constraint_query2 = "CREATE CONSTRAINT IF NOT EXISTS FOR (i:Station) REQUIRE i.geofoxid IS UNIQUE"

## etc
point_index_query = "CREATE POINT INDEX IF NOT EXISTS FOR (i:POI) ON i.location"
poi_constraint_query = "CREATE CONSTRAINT IF NOT EXISTS FOR (i:POI) REQUIRE i.name IS UNIQUE"


# Cypher query to import our road network nodes GeoDataFrame

# Cypher query for importing POIs from osm
poi_insert_query = '''
UNWIND $rows AS row
MERGE (p:POI {osmid: row.osmid})
SET p.name = row.name,
    p.addr_street = row.addr_street,
    p.addr_housenumber = row.addr_housenumber,
    p.addr_postcode = row.addr_postcode,
    p.description = row.description,
    p.tags = row.tags
WITH p, row
WHERE row.longitude IS NOT NULL AND row.latitude IS NOT NULL
SET p.location = point({longitude: row.longitude, latitude: row.latitude})
RETURN COUNT(*) as total
'''

# Cypher query for importing AOIs from osm
aoi_insert_query = '''
UNWIND $rows AS row
MERGE (a:AOI {osmid: row.osmid})
SET a.name = row.name,
    a.description = row.description,
    a.tags = row.tags,
    a.geometry_wkt = row.geometry_wkt,
    a.boundary_wkt = row.boundary_wkt
WITH a, row
WHERE row.centroid_lon IS NOT NULL AND row.centroid_lat IS NOT NULL
SET a.centroid = point({longitude: row.centroid_lon, latitude: row.centroid_lat})
RETURN COUNT(*) as total
'''


# Cypher query for importing stations from geofox
station_insert_query = '''
UNWIND $rows AS row
MERGE (p:Station {geofoxid: row.geofoxid})
SET p.name = row.name,
    p.city = row.city,
    p.vehicleTypes = row.vehicleTypes,
    p.aliasses = row.aliasses
WITH p, row
WHERE row.longitude IS NOT NULL AND row.latitude IS NOT NULL
SET p.location = point({longitude: row.longitude, latitude: row.latitude})
RETURN COUNT(*) as total
'''

# Cypher query for setting inner_city prop of stations from geofox
station_ictag_insert_query = '''
UNWIND $rows AS row
Match (p:Station {geofoxid: row.geofoxid})
SET p.tags = ['inner_city']
RETURN COUNT(*) as total
'''

# Cypher query for importing pois from geofox
geofoxpois_insert_query = '''
UNWIND $rows AS row
MERGE (p:POI {geofoxid: row.geofoxid})
SET p.name = row.name,
    p.city = row.city,
    p.address = row.address
WITH p, row
WHERE row.longitude IS NOT NULL AND row.latitude IS NOT NULL
SET p.location = point({longitude: row.longitude, latitude: row.latitude})
RETURN COUNT(*) as total
'''

def del_stations(session):
    """
    Run a Cypher query in a safe manner, handling errors and returning results.
    """
    try:
        result = session.run('''
            MATCH (s:Station)
            DETACH DELETE s''')
        return result
    except Exception as e:
        print(f"Error running query: {e}")
        return None


def add_station_relationships(processed_data, session):
    """
    Add consolidated relationships to Neo4j database based on processed departure data.
    Each relationship contains lists of departure_times and arrival_times for the same line between stations.

    Args:
        processed_data: List of processed relationship dictionaries
        session: Neo4j database session
    """
    print(f"Adding {len(processed_data)} consolidated relationships to Neo4j...")

    # Create indexes for better performance if they don't exist
    session.run("CREATE INDEX IF NOT EXISTS FOR (s:Station) ON (s.name)")

    # Use batching to improve performance
    batch_size = 100  # Smaller batch size due to larger data per relationship
    total_batches = (len(processed_data) + batch_size - 1) // batch_size

    # Track skipped relationships
    skipped_not_found = 0
    skipped_multiple_found = 0

    for batch_idx in tqdm(range(total_batches), desc="Adding relationships to Neo4j"):
        start_idx = batch_idx * batch_size
        end_idx = min((batch_idx + 1) * batch_size, len(processed_data))
        batch = processed_data[start_idx:end_idx]
        
        # Execute in a transaction for better performance
        with session.begin_transaction() as tx:
            for rel in batch:
                # Skip records where to_station is None
                if not rel['to_station']:
                    continue
                
                # Check if the destination station exists and count how many there are
                check_query = """
                MATCH (to:Station {name: $to_station, city: "Hamburg"})
                RETURN count(to) AS count
                """
                
                # Run the check query
                result = tx.run(check_query, {'to_station': rel['to_station']}).single()
                
                # If station doesn't exist, log and skip
                if not result or result['count'] == 0:
                    skipped_not_found += 1
                    print(f"Skipping relationship from '{rel['from_station']}' to '{rel['to_station']}' - Destination station does not exist")
                    continue
                
                # If multiple stations exist with the same name, log details and skip
                if result['count'] > 1:
                    # Query to get details of all matching stations
                    details_query = """
                    MATCH (to:Station {name: $to_station, city: "Hamburg"})
                    RETURN to.name, to.geofoxid
                    """
                    
                    details_result = tx.run(details_query, {'to_station': rel['to_station']}).data()
                    
                    # Format the details for logging
                    stations_details = "\n  ".join([
                        f"Station: {station['to.name']}, ID: {station.get('to.geofoxid', 'N/A')}"
                        for station in details_result
                    ])
                    
                    print(f"Skipping relationship from '{rel['from_station']}' to '{rel['to_station']}' - Multiple destination stations found:\n  {stations_details}")
                    
                    skipped_multiple_found += 1
                    continue
                    
                # Cypher query to create/update the relationship with consolidated lists
                query = """
                // Match FROM station
                MATCH (from:Station {geofoxid: $from_station_id})
                
                // Need to use WITH to pass variables between MATCH statements
                WITH from

                // Match the TO station that we've confirmed exists uniquely
                MATCH (to:Station {name: $to_station, city: "Hamburg"})
                
                // Create or merge the relationship with the unique line identifier
                MERGE (from)-[r:CONNECTS_TO {line_unique: $line_unique}]->(to)
                
                // Set or update the properties
                SET 
                    r.line_name = $line_name,
                    r.line_info = $line_info,
                    r.departure_times = $departure_times,
                    r.arrival_times = $arrival_times,
                    r.duration = $duration,
                    r.last_updated = $current_time
                """
                
                # Ensure all lists are valid for Neo4j
                # Filter out any None/NaT values in arrival_times and departure_times
                departure_times = [dt for dt in rel['departure_times'] if dt is not None and not pd.isna(dt)]
                arrival_times = [at for at in rel['arrival_times'] if at is not None and not pd.isna(at)]
                
                # Parameters for the query
                params = {
                    'from_station_id': rel['from_station_id'],
                    'to_station': rel['to_station'],
                    'line_unique': rel['line_unique'],
                    'line_name': rel['line_name'],
                    'line_info': rel['line_info'],
                    'departure_times': departure_times,
                    'arrival_times': arrival_times,
                    'duration': rel['duration'],
                    'current_time': "2025-04-06 10:08:11"  # Current timestamp from your context
                }
                
                # Execute the query
                tx.run(query, params)

    # Log summary of skipped relationships
    total_skipped = skipped_not_found + skipped_multiple_found
    if total_skipped > 0:
        print(f"WARNING: Skipped {total_skipped} relationships:")
        if skipped_not_found > 0:
            print(f"  - {skipped_not_found} due to missing destination stations")
        if skipped_multiple_found > 0:
            print(f"  - {skipped_multiple_found} due to multiple matching destination stations")

    print("Creating additional indexes for optimized querying...")
    # Create compound indexes for common query patterns
    session.run("CREATE INDEX IF NOT EXISTS FOR ()-[r:CONNECTS_TO]-() ON (r.line_unique)")
    
    # Create full-text index for searching departure times
    # This can help with finding the next available departure
    session.run("CREATE INDEX IF NOT EXISTS FOR ()-[r:CONNECTS_TO]-() ON (r.departure_times)")

    print("Relationship creation complete!")
        



# Cypher query to import our road network relationships GeoDataFrame

rels_query = '''
    UNWIND $rows AS road
    MATCH (u:Intersection {osmid: road.u})
    MATCH (v:Intersection {osmid: road.v})
    MERGE (u)-[r:ROAD_SEGMENT {osmid: road.osmid}]->(v)
        SET r.oneway = road.oneway,
            r.lanes = road.lanes,
            r.ref = road.ref,
            r.name = road.name,
            r.highway = road.highway,
            r.max_speed = road.maxspeed,
            r.length = toFloat(road.length)
    RETURN COUNT(*) AS total
    '''


def init(driver):
    """
    Initialize the Neo4j database by creating constraints and indexes.
    """
    with driver.session() as session:
        # osm specific constraints and indexes
        run_safe(osm_constraint_query, session)
        run_safe(osm_constraint_query2, session)
        # Geofox specific constraints and indexes
        run_safe(geofox_constraint_query, session)
        run_safe(geofox_constraint_query2, session)
        # etc
        run_safe(point_index_query, session)


def run_safe(query, session):
    """
    Run a Cypher query in a safe manner, handling errors and returning results.
    """
    try:
        result = session.run(query)
        return result
    except Exception as e:
        print(f"Error running query: {e}")
        return None

