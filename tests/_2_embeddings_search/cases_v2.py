
distance2centroid_small = 1000
distance2centroid_medium = 3500
distance2centroid_big = 6000

test_cases = [
    {
        # target = "Jugendzentrum Heimfeld"
        "vars": {
            # extrahiert aus der Anfrage (start oder dest) -> kann abwandlung von target sein
            "point": "Jugendzentrum Heimfeld",
            # extrahiert aus der Anfrage (dest_aoi), umgebung in der sich dest befinden soll
            "point_cond": None,
            "target_distance2centroid": f'("POINT(9.956510900962325 53.46846007447076)", {distance2centroid_small})',
            "target_name_contains": '["Jugendclub Heimfeld"]'
        }
    },
    {
        # target = "Agentur für Arbeit Eimsbüttel"
        "vars": {
            "point": "Jobhaus Eimsbüttel",
            "point_cond": None,
            "target_distance2centroid": f'("POINT(9.957572 53.5693)", {distance2centroid_small})',
            "target_name_contains": '["Agentur für Arbeit"]'
        }
    },
    {
        # target = "Schulungszentrum Deichverteidigung"
        "vars": {
            "point": "Deichverteidigungs-Schulungszentrum",
            "point_cond": None,
            "target_distance2centroid": f'("POINT(10.026079492966264 53.540246749061104)", {distance2centroid_small})',
            "target_name_contains": '["Schulungszentrum Deichverteidigung"]'
        }
    },
    {
        # target = "Rathaus"
        "vars": {
            "point": "Hamburger Rathaus",
            "point_cond": None,
            "target_distance2centroid": f'("POINT(9.992400088323125 53.55041280989229)", {distance2centroid_small})',
            "target_name_contains": '["Rathaus"]'
        }
    },
    {
        # target = "Bauspielplatz und Spielhaus Eppendorfer Park"
        "vars": {
            "point": "Spielhaus Epndorferpark",  # zusammengezogen
            "point_cond": None,
            "target_distance2centroid": f'("POINT(9.981581819228403 53.59016276572776)", {distance2centroid_small})',
            "target_name_contains": '["Bauspielplatz und Spielhaus Eppendorfer Park", "Eppendorfer Park"]'
        }
    },
    {
        # target = "Gut vernetzt"
        "vars": {
            "point": "Gut Versetzt",
            "point_cond": None,
            "target_distance2centroid": f'("POINT(9.996434428442694 53.54090433330553)", {distance2centroid_small})',
            "target_name_contains": '["Gut vernetzt"]'
        }
    },
    {
        # target = "DLRG Bezirk Wandsbek"
        "vars": {
            "point": "DLRG Wandsbek",
            "point_cond": None,
            "target_distance2centroid": f'("POINT(10.082359380443732 53.57452932441537)", {distance2centroid_small})',
            "target_name_contains": '["DLRG Bezirk Wandsbek"]'
        }
    },
    {
        # target = "Cruise Center Altona"
        "vars": {
            "point": "Kreuzfahrtterminal Altona",
            "point_cond": None,
            "target_distance2centroid": f'("POINT(9.937450892684728 53.5435580737001)", {distance2centroid_small})',
            "target_name_contains": '["Cruise Center Altona", "Kreuzfahrtterminal Altona"]'
        }
    },
    {
        # target = "Trollhaus"
        "vars": {
            "point": "Troll Haus",
            "point_cond": None,
            "target_distance2centroid": f'("POINT(10.15005405831095 53.58454534926207)", {distance2centroid_small})',
            "target_name_contains": '["Trollhaus"]'
        }
    },
    {
        # target = "Amtsgericht Hamburg-Altona"
        "vars": {
            "point": "Amtsgericht Altona",
            "point_cond": None,
            "target_distance2centroid": f'("POINT(9.94306296405268 53.55625350172331)", {distance2centroid_small})',
            "target_name_contains": '["Amtsgericht Hamburg-Altona"]'
        }
    },
    {
        # target = "Hamburg Dammtor Bahnhof"
        "vars": {
            "point": "Dsmmtor Bahnhof",
            "point_cond": None,
            "target_distance2centroid": f'("POINT(9.989592264735405 53.56083428484313)", {distance2centroid_small})',
            "target_name_contains": '["Hamburg Dammtor Bahnhof", "Bf. Dammtor"]'
        }
    },
    {
        # target = "Uni Hamburg - Career Center"
        "vars": {
            "point": "Career Center Uni Hamburg",
            "point_cond": None,
            "target_distance2centroid": f'("POINT(9.97665 53.569927)", {distance2centroid_small})',
            "target_name_contains": '["Uni Hamburg - Career Center"]'
        }
    },
    {
        # target = "Alsterredder - Grundschule mit Vorschulklasse"
        "vars": {
            "point": "Grundschule Alsterredder",
            "point_cond": None,
            "target_distance2centroid": f'("POINT(10.099568 53.658768)", {distance2centroid_small})',
            "target_name_contains": '["Alsterredder - Grundschule mit Vorschulklasse"]'
        }
    },
    {
        # target = "Freizeitzentrum Feuervogel,offene Kinder- und Jugendarbeit"
        "vars": {
            "point": "Kinderzentrum Feuervogel",
            "point_cond": None,
            "target_distance2centroid": f'("POINT(9.980852853928896 53.45366288508031)", {distance2centroid_small})',
            "target_name_contains": '["Freizeitzentrum Feuervogel,offene Kinder- und Jugendarbeit"]'
        }
    },
    {
        # target = "Biozentrum Klein Flottbek - allgemeine Pflanzenberatung"
        "vars": {
            "point": "Zentrum für Pflanzen Klein Flottbek",
            "point_cond": None,
            "target_distance2centroid": f'("POINT(9.859803 53.559665)", {distance2centroid_small})',
            "target_name_contains": '["Biozentrum Klein Flottbek"]'
        }
    },



    # 15 with point_cond
    {
        # target = "Nachtschicht St. Pauli"
        "vars": {
            "point": "Bar Nachtschicht",
            "point_cond": "St. Pauli",
            # st. Pauli als centroid
            "target_distance2centroid": f'("POINT(9.9608543 53.5478483)", {distance2centroid_medium})',
            "target_name_contains": '["Nachtschicht St. Pauli"]'
        }
    },
    {
        # target = ein Fischrestaurant in der Nähe des Tierparks Hagenbeck
        "vars": {
            "point": "Fischrestaurant",
            "point_cond": "Tierpark in Hagenbeck",
            # Hagenbecks Tierpark als centroid
            "target_distance2centroid": f'("POINT(9.941535 53.594856)", {distance2centroid_medium})',
            "target_name_contains": '["FischHütte", "Fischerstube", "Fischrestaurant"]'
        }
    },
    {
        # target = "Hamburgische Staatsoper" (in der Nähe von Innenstadt)
        "vars": {
            "point": "Staatsoper",
            "point_cond": "Innenstadt",
            # Hamburgische Staatsoper als centroid
            "target_distance2centroid": f'("POINT(9.98892444516007 53.55666143940254)", {distance2centroid_medium})',
            "target_name_contains": '["Hamburgische Staatsoper"]'
        }
    },
    {
        # target = "Bäderland Elbgaustraße"
        "vars": {
            "point": "Schwimmbad",
            "point_cond": "Altona Volkspark",  # Altonaer Volkspark
            # Altonaer Volkspark als centroid
            "target_distance2centroid": f'("POINT(9.900253504833403 53.58051197902252)", {distance2centroid_medium})',
            "target_name_contains": '["Bäderland Elbgaustraße", "Altonaer Volkspark"]'
        }
    },
    {
        # target = "Bauspielplatz und Spielhaus Eppendorfer Park"
        "vars": {
            "point": "Spielhaus",
            "point_cond": "Eppendorfer Park",
            # eppendorfer park als centroid
            "target_distance2centroid": f'("POINT(9.979047274237926 53.589320108207936)", {distance2centroid_medium})',
            "target_name_contains": '["Eppendorfer Park"]'
        }
    },
    {
        # target = "Park in der Nähe der Innenstadt"
        "vars": {
            "point": "Waldpark",
            "point_cond": "Innenstadt",
            # Innenstadt als centroid
            "target_distance2centroid": f'("POINT(9.988080668856236 53.55184559306223)", {distance2centroid_big})',
            "target_name_contains": '["Park", "Wald"]'
        }
    },
    {
        # target = "Theater in der Nähe eines Parks mit See"
        "vars": {
            "point": "Theater",
            "point_cond": "Stadtpark",
            # Stadtpark als centroid
            "target_distance2centroid": f'("POINT(10.029177 53.592139)", {distance2centroid_medium})',
            "target_name_contains": '["Theater"]'
        }
    },
    {
        # target = "Theater in der Nähe eines Parks mit See"
        "vars": {
            "point": "Museum",
            "point_cond": "Stadtpark",
            # Stadtpark als centroid
            "target_distance2centroid": f'("POINT(10.029177 53.592139)", {distance2centroid_medium})',
            "target_name_contains": '["Museum"]'
        }
    },
    {
        # target = "Theater in der Nähe eines Parks mit See"
        "vars": {
            "point": "Kino",
            "point_cond": "Innenstadt",
            # Innenstadt als centroid
            "target_distance2centroid": f'("POINT(9.988080668856236 53.55184559306223)", {distance2centroid_medium})',
            "target_name_contains": '["Kino", "Filmtheater", "Kinos"]'
        }
    },
    {
        # target = "Bücherrei in der Nähe einer Liegewiese"
        "vars": {
            "point": "Bücherei",
            "point_cond": "Liegewiese Boberger See",
            # Liegewiese als centroid
            "target_distance2centroid": f'("POINT(10.1377648 53.5153121)", {distance2centroid_medium})',
            "target_name_contains": '["Bücherei", "Bibliothek", "Bücherhalle", "Boberger See"]'
        }
    },
]


def generate_tests():
    return test_cases
