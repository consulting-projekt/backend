from pathlib import Path
import sys
sys.path.append(str(Path(__file__).parent.parent.parent))
import os
from langchain_community.chat_models import ChatOllama
from langchain.schema import HumanMessage
from qdrant_client import QdrantClient
from db.utils_embeddings import load_embedding_model_std
from db.utils_qdrant import get_startdest
import ast
import json
from pythelpers.logger.logger import start_logging2

COLLECTION_NAME = "aoipoi_embeddings_std"

client = QdrantClient("localhost", port=6333)
emb_modell = load_embedding_model_std()

def call_api(prompt, options, context):
    # Replace the ast.literal_eval line with:
    anfrage = context.get('vars', {}).get('anfrage', {})

    print(f"Prompt: {anfrage}, Options: {options}, Context: {context}")
    start, dest = get_startdest(client, emb_modell, anfrage, COLLECTION_NAME)

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
                "start_aoi": None,
                "dest": "Haus der Familie",
                "dest_aoi": "Elbstrand"
            }
        }
    }
    call_api({}, {}, context)