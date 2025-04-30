known_points = {
    'Lutterothstraße': [9.952101, 53.580449], # adresse
    'Haus der Familie': [9.96242186569669, 53.557507857835716], # Verein für stadtteilbezogene milieunahe Erziehungshilfen
    'Else-Rauch-Platz': [9.952101, 53.580449], # poi park
}

unknown_points = [
    'Else Rauch Park' # ähnlich wie Else-Rauch-Platz
]


def find_point(point_name):
    """
    Find a point in the known_points dictionary or return None if not found.
    """
    coordinates = known_points.get(point_name, None)
    return {'location': {'lon': coordinates[0], 'lat': coordinates[1]}} if coordinates else None
