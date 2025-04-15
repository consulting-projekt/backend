
from qdrant_client import QdrantClient, models
from db.utils import parse_point_string

def get_startdest(qdrant_client, emb_model, anfrage, coll_name):
    '''
    Get start and destination from a Qdrant client.
    anfrage type: 
        {
            "start": str|None,
            "start_bedingung": str|None,
            "ziel": str|None,
            "ziel_bedingung": str|None
        }

    return type: (start, dest)
    '''
    start, start_cond = anfrage.get("start"), anfrage.get("start_bedingung")
    ziel, ziel_cond = anfrage.get("ziel"), anfrage.get("ziel_bedingung")

    start = get_point_byquery(start, start_cond, qdrant_client, emb_model, coll_name)
    dest = get_point_byquery(ziel, ziel_cond, qdrant_client, emb_model, coll_name)

    return start, dest


def get_point_byquery(point_text, point_condition, client, emb_model, coll_name, limit=1):
    # Process ziel search
    if point_text:
        # Generate embedding for ziel
        point_textemb = emb_model.encode(point_text)
        
        # Create filter for ziel_bedingung if present
        filter_query = None
        if point_condition:
            # First search for ziel_bedingung to get geo location
            bedingung_query_emb = emb_model.encode(point_condition)
            bedingung_results = client.search(
                collection_name=coll_name,
                query_vector=bedingung_query_emb,
                limit=1
            )
            
            # If we found a result for the bedingung
            if bedingung_results:
                # Extract the location from the result (assuming it's in the payload)
                location = None
                found_result = bedingung_results[0].payload
                if "location" in found_result:
                    location = found_result["location"]
                
                # Create geo filter if location was found
                if location:
                    # Parse location string to extract coordinates
                    try:
                        # Assuming location is stored as "POINT(lon lat)" in the payload
                        location_str = location
                        if location_str.startswith("POINT("):
                            coords_str = location_str.replace("POINT(", "").replace(")", "")
                            lon, lat = map(float, coords_str.split())
                            
                            # Create geo filter
                            from qdrant_client.models import Filter, FieldCondition, GeoRadius, GeoPoint
                            filter_query = Filter(
                                must=[
                                    FieldCondition(
                                        key="location",
                                        geo_radius=GeoRadius(
                                            center=GeoPoint(
                                                lon=lon,
                                                lat=lat
                                            ),
                                            radius=5000  # 5km radius, adjust as needed
                                        )
                                    )
                                ]
                            )
                    except:
                        filter_query = None
        
        # Search for ziel with or without geo filter
        ziel_results = client.search(
            collection_name=coll_name,
            query_vector=point_textemb,
            limit=limit,
            query_filter=filter_query
        )
        res = ziel_results[0].payload
        res['score'] = ziel_results[0].score
        return res
    else:
        # If no point_text is provided, return an empty list
        return None


def search_qdrant_with_geo_filter(client, query_emb, coll_name, geo_point=None, limit=5):
    """
    Search in Qdrant with optional geo filtering.
    
    Args:
        search_term (str): The term to search for
        geo_point (str): A string in format "POINT(lon lat)" for geo filtering
        limit (int): Maximum number of results to return
        
    Returns:
        List of search results from Qdrant
    """

    # Create filter if geo_point is provided
    filter_query = None
    if geo_point and geo_point.startswith("POINT("):
        # Extract coordinates from POINT(lon lat) format
        coords = parse_point_string(geo_point)
        if coords:
            try:
                lon, lat = float(coords[0]), float(coords[1])
                # Create geo filter - assuming Qdrant has geo points stored in payload.location
                filter_query = models.Filter(
                    must=[
                        models.FieldCondition(
                            key="location",
                            geo_radius=models.GeoRadius(
                                center=models.GeoPoint(
                                    lon=lon,
                                    lat=lat
                                ),
                                radius=5000  # 5km radius, adjust as needed
                            )
                        )
                    ]
                )
            except (ValueError, IndexError):
                pass
    
    # Search in Qdrant
    results = client.search(
        collection_name=coll_name,
        query_vector=query_emb,
        limit=limit,
        query_filter=filter_query
    )
    
    return results

