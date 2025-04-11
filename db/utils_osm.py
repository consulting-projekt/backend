import pandas as pd
import shapely.wkt
import uuid

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


def aoidf2rows(df, type="osm"):
    """
    Convert a GeoDataFrame containing Areas of Interest (with polygon geometries)
    to a format suitable for Neo4j import, extracting boundary points as a flat list.
    
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
            # Get geometry as shapely object
            if isinstance(row.geometry, (Polygon, MultiPolygon)):
                geometry = row.geometry
            elif isinstance(row.geometry, str):
                geometry = shapely.wkt.loads(row.geometry)
            else:
                continue  # Skip rows without valid geometry
                
            geometry_wkt = geometry.wkt
            centroid = geometry.centroid
            centroid_lon = centroid.x
            centroid_lat = centroid.y
            
            # Extract boundary points as flat arrays of coordinates
            # Neo4j can store arrays but not nested objects
            boundary_lons = []
            boundary_lats = []
            
            if isinstance(geometry, Polygon):
                # Get boundary coordinates as flat arrays
                for x, y in geometry.exterior.coords:
                    boundary_lons.append(x)
                    boundary_lats.append(y)
                
            elif isinstance(geometry, MultiPolygon):
                # For multipolygon, collect all coordinates in flat arrays
                # and add a separator between polygons (-999 is used as separator)
                for poly in geometry.geoms:
                    for x, y in poly.exterior.coords:
                        boundary_lons.append(x)
                        boundary_lats.append(y)
                    # Add separator between polygons if there are more to come
                    if poly != list(geometry.geoms)[-1]:
                        boundary_lons.append(-999.0)  # Use -999 as separator
                        boundary_lats.append(-999.0)
            
            # Convert boundary to WKT format
            boundary_wkt = geometry.boundary.wkt
                        
        except Exception as e:
            print(f"Error processing geometry for row {index}: {e}")
            geometry_wkt = None
            centroid_lon = None
            centroid_lat = None
            boundary_wkt = None
            boundary_lons = []
            boundary_lats = []
        
        # Convert tags to a list if it's not already
        if isinstance(row.tags, str):
            # This assumes tags are stored as a string representation of a list
            import ast
            try:
                tags = ast.literal_eval(row.tags)
            except:
                tags = [row.tags]  # Fallback if can't parse
        else:
            tags = row.tags if isinstance(row.tags, list) else []
        
        # Create a dictionary for each row
        aoi_data = {
            "name": row['name'] if 'name' in row and pd.notna(row['name']) else f"AOI_{index}",
            "description": row.description if hasattr(row, 'description') and pd.notna(row.description) else None,
            "tags": tags,
            "geometry_wkt": geometry_wkt,
            "boundary_wkt": boundary_wkt,
            "centroid_lon": centroid_lon,
            "centroid_lat": centroid_lat,
            "boundary_lons": boundary_lons,  # Store longitudes as flat array
            "boundary_lats": boundary_lats   # Store latitudes as flat array
        }

        if type == "osm":
            aoi_data["osmid"] = row.osmid if hasattr(row, 'osmid') else str(index)
            
        rows.append(aoi_data)

    return rows

    """
    Convert a GeoDataFrame containing Areas of Interest (with polygon geometries)
    to a format suitable for Neo4j import, extracting boundary points as a flat list.
    
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
            # Get geometry as shapely object
            if isinstance(row.geometry, (Polygon, MultiPolygon)):
                geometry = row.geometry
            elif isinstance(row.geometry, str):
                geometry = shapely.wkt.loads(row.geometry)
            else:
                continue  # Skip rows without valid geometry
                
            geometry_wkt = geometry.wkt
            centroid = geometry.centroid
            centroid_lon = centroid.x
            centroid_lat = centroid.y
            
            # Extract boundary points as flat arrays of coordinates
            # Neo4j can store arrays but not nested objects
            boundary_lons = []
            boundary_lats = []
            
            if isinstance(geometry, Polygon):
                # Get boundary coordinates as flat arrays
                for x, y in geometry.exterior.coords:
                    boundary_lons.append(x)
                    boundary_lats.append(y)
                
            elif isinstance(geometry, MultiPolygon):
                # For multipolygon, collect all coordinates in flat arrays
                # and add a separator between polygons (-999 is used as separator)
                for poly in geometry.geoms:
                    for x, y in poly.exterior.coords:
                        boundary_lons.append(x)
                        boundary_lats.append(y)
                    # Add separator between polygons if there are more to come
                    if poly != list(geometry.geoms)[-1]:
                        boundary_lons.append(-999.0)  # Use -999 as separator
                        boundary_lats.append(-999.0)
            
            # Convert boundary to WKT format
            boundary_wkt = geometry.boundary.wkt
                        
        except Exception as e:
            print(f"Error processing geometry for row {index}: {e}")
            geometry_wkt = None
            centroid_lon = None
            centroid_lat = None
            boundary_wkt = None
            boundary_lons = []
            boundary_lats = []
        
        # Convert tags to a list if it's not already
        if isinstance(row.tags, str):
            # This assumes tags are stored as a string representation of a list
            import ast
            try:
                tags = ast.literal_eval(row.tags)
            except:
                tags = [row.tags]  # Fallback if can't parse
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
            "centroid_lat": centroid_lat,
            "boundary_lons": boundary_lons,  # Store longitudes as flat array
            "boundary_lats": boundary_lats   # Store latitudes as flat array
        }
            
        rows.append(aoi_data)

    return rows