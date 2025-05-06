from pathlib import Path  # noqa: E402
import sys  # noqa: E402
sys.path.append(str(Path(__file__).parent.parent.parent))  # noqa: E402
from typing import Dict, Any, Union
from db.utils_embeddings import compute_cosine_similarity
from db.utils_embeddings import load_embedding_model_std
import json

emb_model = load_embedding_model_std()


def get_assert(output: dict, options: Dict[str, Any]) -> Union[bool, float, Dict[str, Any]]:
    # test case variablen

    print(
        f"Output: {output}, Options: {options}")
    expected_answer = options.get('vars', {}).get('answer', '')
    answer = output.get('answer', '')
    answer_vars = output.get('vars', {})

    # Define the placeholders and their corresponding keys in answer_vars
    placeholders = {
        "<START>": "start",
        "<DEST>": "dest",
        "<DATE>": "date",
        "<TIME>": "time"
    }

    # Replace actual values in the answer with placeholders (masks)
    for placeholder, key in placeholders.items():
        if key in answer_vars and answer_vars[key]:
            expected_answer = expected_answer.replace(
                placeholder, answer_vars[key])

    output_textemb = emb_model.encode(answer)
    expected_output_textemb = emb_model.encode(expected_answer)

    # Compute cosine similarity
    try:
        cosine_similarity = compute_cosine_similarity(
            output_textemb, expected_output_textemb)

        # Decide pass/fail based on similarity threshold (e.g., 0.9)
        threshold = 0.9

        return {
            "pass": bool(cosine_similarity >= threshold),
            "score": float(cosine_similarity),
            "reason": "Cosine similarity computed"
        }

    except Exception as e:
        print("Error:", e)
        return {"pass": False, "score": 0.0, "reason": str(e)}


if __name__ == "__main__":
    # Example usage
    output = {"answer": "Gerne, hier ist die Route: Ab Oberschleems 13 fahren Sie mit dem Bus um 15:00 Uhr zur Böckmannstraße 1 an, die Fahrt dauert etwa 33 Minuten.",
              "vars": {"start": "Oberschleems 13", "dest": "Böckmannstraße 1", "date": "05.05.2025", "time": "15:00"}}
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
