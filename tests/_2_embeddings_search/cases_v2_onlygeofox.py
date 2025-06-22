
distance2centroid_small = 1000
distance2centroid_medium = 3500
distance2centroid_big = 6000

test_cases = [
    {
        # target = "Jugendzentrum Heimfeld"
        "vars": {
            # extrahiert aus der Anfrage (start oder dest) -> kann abwandlung von target sein
            "point": "Arbeitamt Emsbuttel",
            # extrahiert aus der Anfrage (dest_aoi), umgebung in der sich dest befinden soll
            "point_cond": None,
            "target_distance2centroid": f'("POINT(9.957572 53.569363)", {distance2centroid_small})',
            "target_name_contains": '["Agentur für Arbeit Eimsbüttel"]'
        }
    },
    {
        # target = "Agentur für Arbeit Eimsbüttel"
        "vars": {
            "point": "Werkstatt für Jugendliche",
            "point_cond": None,
            "target_distance2centroid": f'("POINT(10.013918 53.549049)", {distance2centroid_small})',
            "target_name_contains": '["Jugendwerkstatt Rosenallee"]'
        }
    },
    {
        # target = "Schulungszentrum Deichverteidigung"
        "vars": {
            "point": "Statue Bismrack",
            "point_cond": None,
            "target_distance2centroid": f'("POINT(9.972206 53.548623)", {distance2centroid_small})',
            "target_name_contains": '["Bismarck-Denkmal"]'
        }
    },
    {
        # target = "Rathaus"
        "vars": {
            "point": "Leichenbrugge",
            "point_cond": None,
            "target_distance2centroid": f'("POINT(9.988779 53.551479)", {distance2centroid_small})',
            "target_name_contains": '["Bleichenbrücke"]'
        }
    },
    {
        # target = "Bauspielplatz und Spielhaus Eppendorfer Park"
        "vars": {
            "point": "Spieothek",  # zusammengezogen
            "point_cond": None,
            "target_distance2centroid": f'("POINT(9.990283 53.558386)", {distance2centroid_small})',
            "target_name_contains": '["Spielbank Hamburg"]'
        }
    },
    {
        # target = "Gut vernetzt"
        "vars": {
            "point": "Sternwarte Universität Hamburg",
            "point_cond": None,
            "target_distance2centroid": f'("POINT(10.239206 53.479713)", {distance2centroid_small})',
            "target_name_contains": '["Sternwarte Bergedorf der Uni Hamburg", "Sternwarte (Universität)"]'
        }
    },
    {
        # target = "DLRG Bezirk Wandsbek"
        "vars": {
            "point": "politische Bildungszentrale",
            "point_cond": None,
            "target_distance2centroid": f'("POINT(9.988608 53.557088)", {distance2centroid_small})',
            "target_name_contains": '["Landeszentrale für politische Bildung"]'
        }
    },
    {
        # target = "Zentrum für Medien"
        "vars": {
            "point": "Medienzentrum",
            "point_cond": None,
            "target_distance2centroid": f'("POINT(9.988525 53.572948)", {distance2centroid_small})',
            "target_name_contains": '["MediaCentre"]'
        }
    },
    {
        # target = "Trollhaus"
        "vars": {
            "point": "Innenstadt",
            "point_cond": None,
            "target_distance2centroid": f'("POINT(9.988080668856236 53.55184559306223)", {distance2centroid_small})',
            "target_name_contains": '["City Center" ,"Innenstadt"]'
        }
    },
    {
        # target = "Amtsgericht Hamburg-Altona"
        "vars": {
            "point": "Hotel Grand Hamburg Mitte",
            "point_cond": None,
            "target_distance2centroid": f'("POINT(10.026981 53.553898)", {distance2centroid_small})',
            "target_name_contains": '["Grand City Hamburg Mitte"]'
        }
    },
    {
        # target = "Hamburg Dammtor Bahnhof"
        "vars": {
            "point": "CarSharing Falkenried",
            "point_cond": None,
            "target_distance2centroid": f'("POINT(9.977068 53.579538)", {distance2centroid_small})',
            "target_name_contains": '["Falkenried - cambio CarSharing Station"]'
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
            "point": "Prkplatz Damtor",
            "point_cond": None,
            "target_distance2centroid": f'("POINT(9.984641 53.556518)", {distance2centroid_small})',
            "target_name_contains": '["Parkhaus Dammtor"]'
        }
    },
    {
        # target = "Freizeitzentrum Feuervogel,offene Kinder- und Jugendarbeit"
        "vars": {
            "point": "Stat archiv",
            "point_cond": None,
            "target_distance2centroid": f'("POINT(10.069079 53.574779)", {distance2centroid_small})',
            "target_name_contains": '["Staatsarchiv"]'
        }
    },
    {
        # target = "Biozentrum Klein Flottbek - allgemeine Pflanzenberatung"
        "vars": {
            "point": "Willkommenszentrum Flughafen",
            "point_cond": None,
            "target_distance2centroid": f'("POINT(10.005884 53.631953)", {distance2centroid_small})',
            "target_name_contains": '["Welcome Center Airport"]'
        }
    },



    # 15 with point_cond
    {
        # target = "Naturbad Stadtparksee"
        "vars": {
            "point": "Bad",
            "point_cond": "Innenstadt",
            # st. Pauli als centroid
            "target_distance2centroid": f'("POINT(10.029177 53.592139)", {distance2centroid_medium})',
            "target_name_contains": '["Naturbad Stadtparksee"]'
        }
    },
    {
        # target = Pyjama Park Reeperbahn
        "vars": {
            "point": "Park",
            "point_cond": "Reeperbahn",
            # Hagenbecks Tierpark als centroid
            "target_distance2centroid": f'("POINT(9.96649 53.550017)", {distance2centroid_medium})',
            "target_name_contains": '["Park", "Reeperbahn", "Garten"]'
        }
    },
    {
        # target = "Botanischer Garten Klein Flottbek"
        "vars": {
            "point": "bodanicher Garten",
            "point_cond": "Flottbek",
            # Hamburgische Staatsoper als centroid
            "target_distance2centroid": f'("POINT(9.862296 53.559045)", {distance2centroid_medium})',
            "target_name_contains": '["Botanischer Garten Klein Flottbek", "Garten"]'
        }
    },
    {
        # target = "Goßlers Park"
        "vars": {
            "point": "Park",
            "point_cond": "Blankenese",  # Altonaer Volkspark
            # Altonaer Volkspark als centroid
            "target_distance2centroid": f'("POINT(9.811899 53.563361)", {distance2centroid_medium})',
            "target_name_contains": '["Park", "Blankenese", "Garten"]'
        }
    },
    {
        # target = "Hirschpark"
        "vars": {
            "point": "Park",
            "point_cond": "Westen",
            # eppendorfer park als centroid
            "target_distance2centroid": f'("POINT(9.825494 53.556241)", {distance2centroid_medium})',
            "target_name_contains": '["Park", "Garten" ]'
        }
    },
    {
        # target = "Shell Drive Station Hauptbahnhof"
        "vars": {
            "point": "Sell station",
            "point_cond": "Hauptbahnhof",
            # Innenstadt als centroid
            "target_distance2centroid": f'("POINT(10.009242 53.555433)", {distance2centroid_big})',
            "target_name_contains": '["Shell"]'
        }
    },
    {
        # target = "Tiefgarage City Hof"
        "vars": {
            "point": "Garage",
            "point_cond": "Innenstadt",
            # Stadtpark als centroid
            "target_distance2centroid": f'("POINT(10.006052 53.549439)", {distance2centroid_medium})',
            "target_name_contains": '["Garage"]'
        }
    },
    {
        # target = "Europa Passage"
        "vars": {
            "point": "großes Einkaufszentrum",
            "point_cond": "Innenstadt",
            # Stadtpark als centroid
            "target_distance2centroid": f'("POINT(9.995709 53.551665)", {distance2centroid_medium})',
            "target_name_contains": '["Europa Passage" ,"Einkaufszentrum"]'
        }
    },
    {
        # target = "Soziales Dienstleistungszentrum Hamburg-Nord - Bezirksamt Hamburg-Nord"
        "vars": {
            "point": "Sozialstation",
            "point_cond": "Norden",
            # Innenstadt als centroid
            "target_distance2centroid": f'("POINT(9.984334 53.590072)", {distance2centroid_medium})',
            "target_name_contains": '["Soziales Dienstleistungszentrum"]'
        }
    },
    {
        # target = "Schwimmhalle Inselpark"
        "vars": {
            "point": "Hallenbad",
            "point_cond": "Wilhelmsburg",
            # Liegewiese als centroid
            "target_distance2centroid": f'("POINT(10.001809 53.495041)", {distance2centroid_medium})',
            "target_name_contains": '["Schwimmhalle"]'
        }
    },
]


def generate_tests():
    return test_cases
