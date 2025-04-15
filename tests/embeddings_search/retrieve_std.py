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

COLLECTION_NAME = "aoipoi_embeddings_std"

client = QdrantClient("localhost", port=6333)
emb_modell = load_embedding_model_std()

def call_api(prompt, options, context):
    prompt_dict = ast.literal_eval(prompt.strip())  
    start, dest = get_startdest(client, emb_modell, prompt_dict, COLLECTION_NAME)
    
    return {
        "output": {
            "start": start,
            "dest": dest
        },
    }


if __name__ == "__main__":
    # Example usage
    prompt = """
{
"start": None,
"start_bedingung": None,
"ziel": "Kirche",
"ziel_bedingung": "Kirchdorf-Süd"
}
"""
    call_api(prompt, {}, {})