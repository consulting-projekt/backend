from pathlib import Path  # noqa: E402
import sys  # noqa: E402
sys.path.append(str(Path(__file__).parent.parent.parent))  # noqa: E402
from qdrant_client import QdrantClient
from db.utils_qdrant import get_startdest_std

client = QdrantClient("localhost", port=6333)


def call_api(prompt, options, context):
    # Replace the ast.literal_eval line with:
    anfrage = context.get('vars', {}).get('anfrage', {})

    print(f"Prompt: {anfrage}, Options: {options}, Context: {context}")
    start, dest = get_startdest_std(client, anfrage)

    return {
        "output": {
            "start": start,
            "dest": dest
        },
    }


if __name__ == "__main__":
    # Example usage
    context = {
        "vars": {
            "anfrage": {
                "start": "Davidwache",

                "dest": "Haus der Familie",
                        "dest_aoi": "Elbstrand"
            }
        }
    }
    call_api({}, {}, context)
