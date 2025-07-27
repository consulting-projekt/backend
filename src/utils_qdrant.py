from pathlib import Path
import sys
# add parent directory to path
sys.path.append(str(Path(__file__).resolve(strict=True).parent.parent))  # noqa: E402
from qdrant_client import QdrantClient, models
from src.utils import parse_point_string
from src.utils_embeddings import load_embedding_model_std, load_embedding_model_nomic, load_embedding_model_openai, load_embedding_model_LaBSE, load_embedding_model_distiluse

COLLECTION_NAME_STD = "aoipoi_embeddings_std"
COLLECTION_NAME_LABSE = "aoipoi_embeddings_labse"
COLLECTION_NAME_DISTILUSE = "aoipoi_embeddings_distiluse"
COLLECTION_NAME_OPENAI = "aoipoi_embeddings_openai"
COLLECTION_NAME_NOMIC = "aoipoi_embeddings_nomic"


def get_point_std(qdrant_client, point, point_cond, point_condition_location=None):
    emb_model = load_embedding_model_std()

    return get_point_byquery(point, point_cond, qdrant_client, emb_model, COLLECTION_NAME_STD, point_condition_location=point_condition_location)


def get_point_nomic(qdrant_client, point, point_cond, point_condition_location=None):
    emb_model = load_embedding_model_nomic()

    return get_point_byquery(point, point_cond, qdrant_client, emb_model, COLLECTION_NAME_NOMIC, point_condition_location=point_condition_location)

def get_point_labse(qdrant_client, point, point_cond, point_condition_location=None):
    emb_model = load_embedding_model_LaBSE()

    return get_point_byquery(point, point_cond, qdrant_client, emb_model, COLLECTION_NAME_LABSE, point_condition_location=point_condition_location)

def get_point_distiluse(qdrant_client, point, point_cond, point_condition_location=None):
    emb_model = load_embedding_model_distiluse()

    return get_point_byquery(point, point_cond, qdrant_client, emb_model, COLLECTION_NAME_DISTILUSE, point_condition_location=point_condition_location)


def get_point_openai(qdrant_client, point, point_cond, point_condition_location=None):
    emb_model = load_embedding_model_openai()

    return get_point_byquery(point, point_cond, qdrant_client, emb_model, COLLECTION_NAME_OPENAI, point_condition_location=point_condition_location)


def get_startdest_std(qdrant_client, anfrage):
    emb_modell = load_embedding_model_std()

    return get_startdest(qdrant_client, emb_modell, anfrage, COLLECTION_NAME_STD)


def get_startdest(qdrant_client, emb_model, anfrage, coll_name):
    '''
    Get start and destination from a Qdrant client.
    anfrage type: 
        {
            "start": str|None,
            "dest": str|None,
            "dest_aoi": str|None
        }

    return type: (start, dest)
    '''
    start = anfrage.get("start")
    ziel, ziel_cond = anfrage.get("dest"), anfrage.get("dest_aoi")

    start = get_point_byquery(start, None, qdrant_client, emb_model, coll_name)
    dest = get_point_byquery(
        ziel, ziel_cond, qdrant_client, emb_model, coll_name)

    return start, dest


def get_point_byquery(point_text, point_condition, client, emb_model, coll_name, limit=1, point_condition_location=None):
    """
    Search for points in vector database based on text query and optional geographic condition.

    Args:
        point_text: Main search text
        point_condition: Optional geographic condition
        client: Qdrant client
        emb_model: Embedding model
        coll_name: Collection name
        limit: Maximum number of results to return

    Returns:
        Dictionary with result payload and score, or None if no results
    """
    if not point_text:
        return None

    # Try geo search first if condition is provided
    location = None
    combined_text = f"Name: {point_text}\n"
    if point_condition:
        combined_text += f"in Nähe von: {point_condition}"
        point_textemb = emb_model.encode(combined_text)
        if point_condition_location:
            # If location is provided, use it directly
            location = point_condition_location
        else:
            location = _get_location_from_condition(
                point_condition, client, emb_model, coll_name)

        if location:
            # Try searching with increasingly larger radii
            result = _search_with_increasing_radius(
                point_textemb, location, client, coll_name, limit
            )
            if result:
                return result
    else:
        point_textemb = emb_model.encode(combined_text)

    # Fallback to regular search without geo filter
    return _perform_regular_search(point_textemb, client, coll_name, limit)


def _get_location_from_condition(condition_text, client, emb_model, coll_name):
    """Helper function to get location from condition text"""
    bedingung_query_emb = emb_model.encode(condition_text)
    bedingung_results = client.search(
        collection_name=coll_name,
        query_vector=bedingung_query_emb,
        limit=1
    )

    # Extract location if found
    if bedingung_results and "location" in bedingung_results[0].payload:
        return bedingung_results[0].payload["location"]
    return None


def _create_geo_filter(location, radius):
    """Helper function to create a geo filter with given location and radius"""
    try:
        from qdrant_client.models import Filter, FieldCondition, GeoRadius, GeoPoint
        lon, lat = location['lon'], location['lat']
        return Filter(
            must=[
                FieldCondition(
                    key="location",
                    geo_radius=GeoRadius(
                        center=GeoPoint(lon=lon, lat=lat),
                        radius=radius
                    )
                )
            ]
        )
    except Exception as e:
        print(f"Error creating geo filter: {e}")
        return None


def _search_with_increasing_radius(query_vector, location, client, coll_name, limit):
    """Search with incrementally increasing radius until results found or max radius reached"""
    radius_steps = [5000]  # in meters

    for radius in radius_steps:
        filter_query = _create_geo_filter(location, radius)
        if not filter_query:
            return None

        results = client.search(
            collection_name=coll_name,
            query_vector=query_vector,
            limit=limit,
            query_filter=filter_query
        )

        if len(results) > 0:
            result = results[0].payload.copy()
            result['score'] = results[0].score
            result['found_radius_m'] = radius
            return result

    return None


def _perform_regular_search(query_vector, client, coll_name, limit):
    """Perform search without geo filtering"""
    results = client.search(
        collection_name=coll_name,
        query_vector=query_vector,
        limit=limit
    )

    if results:
        result = results[0].payload.copy()
        result['score'] = results[0].score
        return result
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
