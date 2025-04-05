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


def add_relationships_to_neo4j(processed_data, session):
    """
    Add relationships to Neo4j database based on processed departure data.
    
    Args:
        processed_data: List of processed departure dictionaries
    """

    for record in processed_data:
        # Cypher query to create stations if they don't exist and then create relationship
        query = """
        // Create FROM station if it doesn't exist
        MERGE (from:Station {name: $from_station, id: $from_station_id})
        
        // Create TO station if it doesn't exist
        MERGE (to:Station {name: $to_station})
        
        // Create relationship
        CREATE (from)-[r:CONNECTS_TO {
            departure: $departure_time,
            lineId: $line_id,
            lineInfo: $line_info,
            lineName: $line_name,
            platform: $platform
        }]->(to)
        """
        
        # Parameters for the query
        params = {
            'from_station': record['from_station'],
            'from_station_id': record['from_station_id'],
            'to_station': record['to_station'],
            'departure_time': record['departure_time'],
            'line_id': record['line_id'],
            'line_name': record['line_name'],
            'line_info': record['line_info'],
            'platform': record['platform']
        }
        
        # Execute the query
        session.run(query, params)
    



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

