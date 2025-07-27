known_points = {
    'Lutterothstraße': [9.952101, 53.580449],  # adresse
    # Verein für stadtteilbezogene milieunahe Erziehungshilfen
    'Haus der Familie': [9.96242186569669, 53.557507857835716],
    'Else-Rauch-Platz': [9.952101, 53.580449],  # poi park
    'Else-Rauch-Platz': [9.952101, 53.580449],  # poi park
    'Windmühlenweg': [9.868989, 53.571208],  # poi park
}

unknown_points = [
    'Else Rauch Park'  # ähnlich wie Else-Rauch-Platz
]


def find_point(point_name):
    """
    Find a point in the known_points dictionary or return None if not found.
    """
    coordinates = known_points.get(point_name, None)
    return {'location': {'lon': coordinates[0], 'lat': coordinates[1]}} if coordinates else None
