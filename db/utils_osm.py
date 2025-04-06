import pandas as pd
import shapely.wkt

def poidf2rows(df):
    # Extract data from DataFrame and format for Neo4j
    rows = []
    for index, row in df.iterrows():
        # Handle WKT geometry object
        try:
            # If geometry is already a shapely object
            if hasattr(row.geometry, 'x') and hasattr(row.geometry, 'y'):
                longitude = row.geometry.x
                latitude = row.geometry.y
            # If geometry is WKT string
            elif isinstance(row.geometry, str):
                point = shapely.wkt.loads(row.geometry)
                longitude = point.x
                latitude = point.y
            else:
                longitude = None
                latitude = None
        except Exception as e:
            print(f"Error processing geometry for row {index}: {e}")
            longitude = None
            latitude = None
        
        # Convert tags to a list if it's not already
        if isinstance(row.tags, str):
            # This assumes tags are stored as a string representation of a list
            import ast
            tags = ast.literal_eval(row.tags)
        else:
            tags = row.tags if isinstance(row.tags, list) else []
        
        # Create a dictionary for each row
        poi_data = {
            "osmid": row.osmid,
            "name": row['name'],
            "addr_street": row["addr:street"] if pd.notna(row["addr:street"]) else None,
            "addr_housenumber": row["addr:housenumber"] if pd.notna(row["addr:housenumber"]) else None,
            "addr_postcode": row["addr:postcode"] if pd.notna(row["addr:postcode"]) else None,
            "description": row.description if pd.notna(row.description) else None,
            "tags": tags,
            "longitude": longitude,
            "latitude": latitude
        }
        rows.append(poi_data)

    return rows