import pandas as pd

assert_types = [
    "startstation_distance_from_location_lt",
    "endstation_is_inner_city",
    "answer_similar",
    "endstation_is_near",
    "aoi_isnear_poi",
]

test_cases = [
        { 
        "anfrage": "Wann kommt der nächste Bus in die Innenstadt?", 
        "user_location": {"lat": 52.5200, "lon": 13.4050},
        "start_location": None,
        "assert": [
            {
                "startstation_distance_from_location_lt": 200,
            },
            {
                "endstation_is_inner_city": True,
            }
        ]
    }, 
    { 
        "anfrage": "Wann kommt der nächste Bus in die Innenstadt?", 
        "user_location": None,
        "start_location": None,
        "assert": [{
            "answer_similar": "Bitte gib zunächst einen Startpunkt oder deinen Standort an.",
        }]
    },
    { 
        "anfrage": "Welche Route muss ich nehmen wenn ich von der Herberstraße schnell zu einem Restaurant am See kommen möchte?", 
        "user_location": None,
        "start_location": {"lat": 52.5200, "lon": 13.4050},
        "assert": [{
            {
                "startstation_distance_from_location_lt": 200,
            },
            {
                "endstation_is_near": ["Restaurant am See", "Stadtparksee"],
            },
            {
                "aoi_isnear_poi": {"poi": "Restaurant am See", "aoi": "Stadtparksee"},
            }
        }]
    },
]


def generate_tests():
    return test_cases