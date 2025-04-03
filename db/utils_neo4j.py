# First, define Cypher queries to create constraints and indexes
constraint_query = "CREATE CONSTRAINT IF NOT EXISTS FOR (i:POI) REQUIRE i.osmid IS UNIQUE"
constraint_query2 = "CREATE CONSTRAINT IF NOT EXISTS FOR (i:AOI) REQUIRE i.osmid IS UNIQUE"
point_index_query = "CREATE POINT INDEX IF NOT EXISTS FOR (i:POI) ON i.location"

rel_index_query = "CREATE INDEX IF NOT EXISTS FOR ()-[r:ROAD_SEGMENT]-() ON r.osmids"

address_constraint_query = "CREATE CONSTRAINT IF NOT EXISTS FOR (a:Address) REQUIRE a.id IS UNIQUE"


# Cypher query to import our road network nodes GeoDataFrame

# Cypher query for importing POIs
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
    try:
        with driver.session() as session:
            session.run(constraint_query)
            session.run(constraint_query2)
            session.run(point_index_query)
    except Exception as e:
        print(f"Error initializing database: {e}")

