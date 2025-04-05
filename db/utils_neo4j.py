from tqdm import tqdm

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
                
                # Cypher query to create stations and relationship
                query = """
                // Create FROM station if it doesn't exist
                MERGE (from:Station {name: $from_station})
                ON CREATE SET from.geofoxid = $from_station_id
                ON MATCH SET from.geofoxid = $from_station_id
                
                // Create TO station (next_station) if it doesn't exist
                MERGE (to:Station {name: $next_station})
                
                // Create relationship with all the data
                CREATE (from)-[r:CONNECTS_TO {
                    departure_time: $departure_time,
                    arrival_time: $arrival_time,
                    line_id: $line_id,
                    line_name: $line_name,
                    line_info: $line_info,
                    platform: $platform,
                    line_terminal: $line_terminal,
                    line_origin: $line_origin,
                    direction_id: $direction_id
                }]->(to)
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
                    'line_id': record['line_id'],
                    'line_name': record['line_name'],
                    'line_info': record['line_info'],
                    'platform': record['platform'],
                    'line_terminal': record['line_terminal'],
                    'line_origin': record['line_origin'],
                    'direction_id': int(record['direction_id'])  # Ensure this is an integer
                }
                
                # Execute the query
                tx.run(query, params)
    
    print("Creating additional indexes for optimized querying...")
    # Create compound indexes for common query patterns
    session.run("CREATE INDEX IF NOT EXISTS FOR ()-[r:CONNECTS_TO]-() ON (r.line_id, r.direction_id)")
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

