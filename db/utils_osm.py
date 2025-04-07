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


def aoidf2rows(df):
    """
    Convert a GeoDataFrame containing Areas of Interest (with polygon geometries)
    to a format suitable for Neo4j import.
    
    Parameters:
    -----------
    df : GeoDataFrame
        A GeoDataFrame with AOI data (parks, lakes, etc.)
    
    Returns:
    --------
    rows : list
        A list of dictionaries, each representing an AOI
    """
    import pandas as pd
    import shapely.wkt
    from shapely.geometry import Polygon, MultiPolygon
    
    # Extract data from DataFrame and format for Neo4j
    rows = []
    for index, row in df.iterrows():
        # Handle Polygon/MultiPolygon geometry
        try:
            # If geometry is already a shapely object
            if isinstance(row.geometry, (Polygon, MultiPolygon)):
                geometry_wkt = row.geometry.wkt
                # Get the centroid (useful for some operations)
                centroid = row.geometry.centroid
                centroid_lon = centroid.x
                centroid_lat = centroid.y
                # Get the boundary for distance calculations
                boundary_wkt = row.geometry.boundary.wkt
            # If geometry is WKT string
            elif isinstance(row.geometry, str):
                geom = shapely.wkt.loads(row.geometry)
                geometry_wkt = geom.wkt
                centroid = geom.centroid
                centroid_lon = centroid.x
                centroid_lat = centroid.y
                boundary_wkt = geom.boundary.wkt
            else:
                geometry_wkt = None
                centroid_lon = None
                centroid_lat = None
                boundary_wkt = None
        except Exception as e:
            print(f"Error processing geometry for row {index}: {e}")
            geometry_wkt = None
            centroid_lon = None
            centroid_lat = None
            boundary_wkt = None
        
        # Convert tags to a list if it's not already
        if isinstance(row.tags, str):
            # This assumes tags are stored as a string representation of a list
            import ast
            tags = ast.literal_eval(row.tags)
        else:
            tags = row.tags if isinstance(row.tags, list) else []
        
        # Create a dictionary for each row
        aoi_data = {
            "osmid": row.osmid if hasattr(row, 'osmid') else str(index),
            "name": row['name'] if 'name' in row and pd.notna(row['name']) else f"AOI_{index}",
            "description": row.description if hasattr(row, 'description') and pd.notna(row.description) else None,
            "tags": tags,
            "geometry_wkt": geometry_wkt,
            "boundary_wkt": boundary_wkt,
            "centroid_lon": centroid_lon,
            "centroid_lat": centroid_lat
        }
        
            
        rows.append(aoi_data)

    return rows