

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