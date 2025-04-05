from tqdm import tqdm
import pandas as pd

# First, define Cypher queries to create constraints and indexes
## osm specific constraints and indexes
constraint_query = "CREATE CONSTRAINT IF NOT EXISTS FOR (i:POI) REQUIRE i.osmid IS UNIQUE"
point_index_query = "CREATE POINT INDEX IF NOT EXISTS FOR (i:POI) ON i.location"

constraint_query2 = "CREATE CONSTRAINT IF NOT EXISTS FOR (i:AOI) REQUIRE i.osmid IS UNIQUE"

## Geofox specific constraints and indexes
constraint_query3 = "CREATE CONSTRAINT IF NOT EXISTS FOR (i:Station) REQUIRE i.geofoxid IS UNIQUE"

## etc
rel_index_query = "CREATE INDEX IF NOT EXISTS FOR ()-[r:ROAD_SEGMENT]-() ON r.osmids"

address_constraint_query = "CREATE CONSTRAINT IF NOT EXISTS FOR (a:Address) REQUIRE a.id IS UNIQUE"


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
    Add relationships to Neo4j database based on processed departure data.
    Includes arrival times, origin, directionId and terminal information.

    Args:
        processed_data: List of processed departure dictionaries
        session: Neo4j database session
    """
    print(f"Adding {len(processed_data)} relationships to Neo4j...")

    # Create indexes for better performance if they don't exist
    session.run("CREATE INDEX IF NOT EXISTS FOR (s:Station) ON (s.name)")
    session.run("CREATE INDEX IF NOT EXISTS FOR (s:Station) ON (s.id)")

    # Use batching to improve performance
    batch_size = 1000
    total_batches = (len(processed_data) + batch_size - 1) // batch_size

    # Track skipped departures
    skipped_not_found = 0
    skipped_multiple_found = 0

    for batch_idx in tqdm(range(total_batches), desc="Adding relationships to Neo4j"):
        start_idx = batch_idx * batch_size
        end_idx = min((batch_idx + 1) * batch_size, len(processed_data))
        batch = processed_data[start_idx:end_idx]
        
        # Execute in a transaction for better performance
        with session.begin_transaction() as tx:
            for record in batch:
                # Skip records where next_station is None
                if not record['next_station']:
                    continue
                
                # Check if the destination station exists and count how many there are
                check_query = """
                MATCH (to:Station {name: $next_station, city: "Hamburg"})
                RETURN count(to) AS count
                """
                
                # Run the check query
                result = tx.run(check_query, {'next_station': record['next_station']}).single()
                
                # If station doesn't exist, log and skip
                if not result or result['count'] == 0:
                    skipped_not_found += 1
                    print(f"Skipping departure from '{record['from_station']}' to '{record['next_station']}' - Destination station does not exist")
                    continue
                
                # If multiple stations exist with the same name, log details and skip
                if result['count'] > 1:
                    # Query to get details of all matching stations
                    details_query = """
                    MATCH (to:Station {name: $next_station, city: "Hamburg"})
                    RETURN to.name, to.geofoxid
                    """
                    
                    details_result = tx.run(details_query, {'next_station': record['next_station']}).data()
                    
                    # Format the details for logging
                    stations_details = "\n  ".join([
                        f"Station: {station['to.name']}, ID: {station.get('to.geofoxid', 'N/A')}"
                        for station in details_result
                    ])
                    
                    print(f"Skipping departure from '{record['from_station']}' to '{record['next_station']}' - Multiple destination stations found:\n  {stations_details}")
                    
                    skipped_multiple_found += 1
                    continue
                    
                # Cypher query to create source station and relationship with destination
                query = """
                // Create FROM station if it doesn't exist
                MATCH (from:Station {geofoxid: $from_station_id})
                
                // Need to use WITH to pass variables between MERGE and MATCH
                WITH from

                // Match the TO station that we've confirmed exists uniquely
                MATCH (to:Station {name: $next_station, city: "Hamburg"})
                
                // Check if relationship exists and create only if it doesn't
                MERGE (from)-[r:CONNECTS_TO {
                    departure_time: $departure_time,
                    line_id: $line_id
                }]->(to)
                // Set other properties only on creation
                ON CREATE SET 
                    r.arrival_time = $arrival_time,
                    r.line_name = $line_name,
                    r.line_info = $line_info,
                    r.departure_platform = $platform
                """
                
                # Handle None/NaT values for arrival_time
                arrival_time = record['arrival_time']
                if pd.isna(arrival_time) or arrival_time is None:
                    arrival_time = None
                
                # Parameters for the query
                params = {
                    'from_station': record['from_station'],
                    'from_station_id': record['from_station_id'],
                    'next_station': record['next_station'],
                    'departure_time': record['departure_time'],
                    'arrival_time': arrival_time,
                    'line_id': f"{record['line_id']}#{record['line_origin']}#{record['line_terminal']}", # damit eindeutig identifizierbar
                    'line_name': record['line_name'],
                    'line_info': record['line_info'],
                    'platform': record['platform'],
                }
                
                # Execute the query
                tx.run(query, params)

    # Log summary of skipped departures
    total_skipped = skipped_not_found + skipped_multiple_found
    if total_skipped > 0:
        print(f"WARNING: Skipped {total_skipped} departures:")
        if skipped_not_found > 0:
            print(f"  - {skipped_not_found} due to missing destination stations")
        if skipped_multiple_found > 0:
            print(f"  - {skipped_multiple_found} due to multiple matching destination stations")

    print("Creating additional indexes for optimized querying...")
    # Create compound indexes for common query patterns
    session.run("CREATE INDEX IF NOT EXISTS FOR ()-[r:CONNECTS_TO]-() ON (r.line_id)")
    session.run("CREATE INDEX IF NOT EXISTS FOR ()-[r:CONNECTS_TO]-() ON (r.departure_time)")

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
        run_safe(constraint_query, session)
        run_safe(point_index_query, session)
        run_safe(constraint_query2, session)
        # Geofox specific constraints and indexes
        run_safe(constraint_query3, session)


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

