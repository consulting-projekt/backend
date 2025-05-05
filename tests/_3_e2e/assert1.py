from pathlib import Path  # noqa: E402
import sys  # noqa: E402
sys.path.append(str(Path(__file__).parent.parent.parent))  # noqa: E402
from typing import Dict, Any, Union
from db.utils_embeddings import compute_cosine_similarity
from db.utils_embeddings import load_embedding_model_std
import json

emb_model = load_embedding_model_std()


def get_assert(output: str, options: Dict[str, Any]) -> Union[bool, float, Dict[str, Any]]:
    # test case variablen
    expected_output = options.get('vars', {}).get('answer', {})

    output_textemb = emb_model.encode(output)
    expected_output_textemb = emb_model.encode(expected_output)

    # Compute cosine similarity
    try:
        cosine_similarity = compute_cosine_similarity(
            output_textemb, expected_output_textemb)

        # Decide pass/fail based on similarity threshold (e.g., 0.9)
        threshold = 0.9
        return {
            "pass": cosine_similarity >= threshold,
            "score": cosine_similarity,
            "reason": "Cosine similarity computed"
        }

    except Exception as e:
        print("Error:", e)
        return {"pass": False, "reason": str(e)}


if __name__ == "__main__":
    # Example usage
    output = "Um <TIME> fährt ein Bus von der Station <START> zur Station <DEST>. Wir wünschen Ihnen eine angenehme Fahrt!"
    options = {
        "vars": {
            "anfrage": "Ich brauche ca. 15:00 einen Bus in die Innenstadt. Gib mir die Route dazu.",
            "start": None,  # hiermit kann simuliert werden dass systemseitig standort des nutzers verwendet wird
            "date": None,  # hiermit kann simuliert werden dass systemseitig aktueller Tag verwendet wird
            "time": None,  # hiermit kann simuliert werden dass systemseitig aktuelle Zeit verwendet wird
            "answer": "Um <TIME> fährt ein Bus von der Station <START> zur Station <DEST>. Wir wünschen Ihnen eine angenehme Fahrt!"
        }
    }

    score = get_assert(output, options)
    print("Score:", score)
