from pathlib import Path
import sys
sys.path.append(str(Path(__file__).parent.parent.parent))
import os
from langchain_community.chat_models import ChatOllama
from langchain.schema import HumanMessage
from qdrant_client import QdrantClient
from db.utils_embeddings import load_embedding_model_std


COLLECTION_NAME = "aoipoi_embeddings_std"

client = QdrantClient("localhost", port=6333)
emb_modell = load_embedding_model_std()

def call_api(prompt, options, context):
    query_emb = emb_modell.encode(prompt)

    # Direkter Check in Qdrant
    qdrant_results = client.search(
        collection_name=COLLECTION_NAME,
        query_vector=query_emb,
        limit=2
    )
    
    
    # Evaluate response
    
    return {
        "output": qdrant_results,
    }