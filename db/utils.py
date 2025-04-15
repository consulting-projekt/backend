from typing import Dict, List, Any, Optional

# Funktion, um zu entscheiden, ob ein Polygon durch seinen Centroid ersetzt werden soll
def simplify_to_centroid_if_small(geometry, max_area_threshold=0.0000006791):  # Schwellenwert anpassen
    """
    Ersetzt ein Polygon durch seinen Centroid, wenn die Fläche unter dem Schwellenwert liegt.
    Der Schwellenwert ist in Quadratgrad (für WGS84). 
    0.0001 entspricht ungefähr 1 km² in Hamburg.
    0.0000679123 entspricht ungefähr 0,5 km² in Hamburg.
    0.0000006791 entspricht ungefähr 5.000 m² in Hamburg.
    """
    if geometry.geom_type in ['Polygon', 'MultiPolygon']:
        area = geometry.area
        if area < max_area_threshold:
            return geometry.centroid
    return geometry


def parse_point_string(point_str: str) -> Optional[tuple]:
    """Parse a POINT string and return lon, lat tuple."""
    if not point_str or not point_str.startswith("POINT("):
        return None
    
    try:
        # Extract coordinates from POINT(lon lat) format
        coords_str = point_str.replace("POINT(", "").replace(")", "").strip()
        coords = coords_str.split()
        if len(coords) == 2:
            return float(coords[0]), float(coords[1])
    except (ValueError, IndexError):
        pass
    
    return None