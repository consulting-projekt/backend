from pathlib import Path  # noqa: E402
import sys  # noqa: E402
sys.path.append(str(Path(__file__).parent.parent.parent))  # noqa: E402
from qdrant_client import QdrantClient
from db.utils_qdrant import get_point_distiluse

client = QdrantClient("localhost", port=6333)


def call_api(_, options, context):
    # Replace the ast.literal_eval line with:
    vars = context.get('vars', {})

    print(f"vars: {vars}, Options: {options}, Context: {context}")
    point = vars.get("point", None)
    poin_cond = vars.get("point_cond", None)
    target = get_point_distiluse(client, point, poin_cond)

    return {
        "output": {
            "target": target,
        },
    }


if __name__ == "__main__":
    # Example usage
    context = {
        "vars": {
            # extrahiert aus der Anfrage (start oder dest) -> kann abwandlung von target sein
            "point": "Jugendzentrum Heimfeld",
            # extrahiert aus der Anfrage (dest_aoi), umgebung in der sich dest befinden soll
            "point_cond": None,
            "target_distance2centroid": None,
            "target_name_contains": ["Jugendclub Heimfeld"]
        }
    }
    call_api({}, {}, context)
