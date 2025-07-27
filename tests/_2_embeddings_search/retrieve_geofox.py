from pathlib import Path  # noqa: E402
import sys  # noqa: E402
sys.path.append(str(Path(__file__).parent.parent.parent))  # noqa: E402
import os
from src.utils_geofox import get_point_byquery
from src.geofox_client import get_geofox_client
import ast
import json

COLLECTION_NAME = "aoipoi_embeddings_std"

client = get_geofox_client()


def call_api(prompt, options, context):
    # Replace the ast.literal_eval line with:
    vars = context.get('vars', {})

    print(f"vars: {vars}, Options: {options}, Context: {context}")
    point = vars.get("point", None)
    point_cond = vars.get("point_cond", None)
    target = get_point_byquery(client, point, point_cond)

    return {
        "output": {
            "target": target
        },
    }


if __name__ == "__main__":
    # Example usage
    context = {
        "vars": {

            "point": "Bar Nachtschicht",
            "point_cond": "St. Pauli",
            "target_distance2centroid": f'("POINT(9.9608543 53.5478483)", {1000})',
            "target_name_contains": '["Nachtschicht St. Pauli"]'
        }
    }
    call_api({}, {}, context)
