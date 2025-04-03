# First, define Cypher queries to create constraints and indexes
constraint_query = "CREATE CONSTRAINT IF NOT EXISTS FOR (i:POI) REQUIRE i.osmid IS UNIQUE"
constraint_query2 = "CREATE CONSTRAINT IF NOT EXISTS FOR (i:AOI) REQUIRE i.osmid IS UNIQUE"
point_index_query = "CREATE POINT INDEX IF NOT EXISTS FOR (i:POI) ON i.location"

rel_index_query = "CREATE INDEX IF NOT EXISTS FOR ()-[r:ROAD_SEGMENT]-() ON r.osmids"

address_constraint_query = "CREATE CONSTRAINT IF NOT EXISTS FOR (a:Address) REQUIRE a.id IS UNIQUE"


# Cypher query to import our road network nodes GeoDataFrame

poiinsert_query = '''
    UNWIND $rows AS row
    WITH row WHERE row.osmid IS NOT NULL
    MERGE (i:POI {osmid: row.osmid})
        SET i.geometry = 
         point({latitude: row.y, longitude: row.x }),
            i.ref = row.ref,
            i.highway = row.highway,
            i.street_count = toInteger(row.street_count)
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


# Function to execute our constraint / index queries

def create_constraints(tx):
    tx.run(constraint_query)
    tx.run(constraint_query2)
    tx.run(point_index_query)
