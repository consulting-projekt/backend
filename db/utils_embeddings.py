from pathlib import Path
import sys
# add parent directory to path
sys.path.append(str(Path(__file__).resolve(strict=True).parent.parent))  # noqa: E402
from sentence_transformers import SentenceTransformer
import pandas as pd
from typing import List, Dict, Any
from neo4j import GraphDatabase
from qdrant_client.models import Distance, VectorParams
import uuid
import numpy as np
from openai import OpenAI
import ollama
client = OpenAI()


def load_embedding_model(model_name: str = "all-MiniLM-L6-v2"):
    """
    Load a sentence transformer model for generating embeddings.

    Args:
        model_name: Name of the sentence-transformers model to use

    Returns:
        A SentenceTransformer model
    """
    print(f"Loading embedding model: {model_name}")
    return SentenceTransformer(model_name)


def get_nodes(driver, label: str, batch_size: int, offset: int) -> List[Dict]:
    """
    Get a batch of nodes of a specific type from Neo4j.

    Args:
        driver: Neo4j driver instance
        node_type: Type of nodes to retrieve
        batch_size: Number of nodes to retrieve
        offset: Starting offset for pagination

    Returns:
        List of node dictionaries with their properties
    """
    with driver.session() as session:
        query = f"""
        MATCH (n:{label}) 
        RETURN elementId(n) AS id, properties(n) AS properties
        SKIP $offset
        LIMIT $batch_size
        """

        result = session.run(
            query, {"offset": offset, "batch_size": batch_size})
        return [{"id": record["id"], "properties": record["properties"]} for record in result]


def get_node_count(driver, label: str) -> int:
    """
    Get the count of nodes of a specific type.

    Args:
        driver: Neo4j driver instance
        node_type: Type of nodes to count

    Returns:
        Number of nodes of the specified type
    """
    with driver.session() as session:
        count_query = f"""
        MATCH (n:{label})
        RETURN count(n) AS count
        """
        result = session.run(count_query)
        return result.single()["count"]


def create_text_for_embedding(node_properties: Dict, label) -> str:
    """
    Create a combined text from node properties for embedding.

    Args:
        node_properties: Dictionary of node properties

    Returns:
        Combined text for embedding
    """
    combined_text = ""

    if label == "POI":
        combined_text += "Entität: point of interest\n"
    if label == "AOI":
        combined_text += "Entität: area of interest\n"

    if "name" in node_properties and node_properties["name"]:
        combined_text += f"Name: {node_properties['name']}\n"

    if "description" in node_properties and node_properties["description"]:
        combined_text += f"Beschreibung: {node_properties['description']}\n"

    if "tags" in node_properties and isinstance(node_properties["tags"], list):
        combined_text += f"Schlagwörter: {', '.join(node_properties['tags'])}"

    return combined_text


def initialize_collection(client, model, collection_name: str):
    """
    Initialize Qdrant collection for embeddings.

    Args:
        client: Qdrant client instance
        model: SentenceTransformer model
        collection_name: Name of the collection to create
    """
    # Get embedding dimension from the model
    vector_size = model.get_sentence_embedding_dimension()

    # Create or recreate the collection
    client.recreate_collection(
        collection_name=collection_name,
        vectors_config=VectorParams(
            size=vector_size,
            distance=Distance.COSINE
        ),

    )
    print(f"Qdrant Collection '{collection_name}' created")


def process_node_embeddings(driver, model, client, label: str, collection_name: str, batch_size: int = 100):
    """
    Process nodes to generate embeddings and store them in Qdrant.

    Args:
        driver: Neo4j driver instance
        model: SentenceTransformer model
        client: Qdrant client instance
        node_type: Type of nodes to process
        collection_name: Name of the Qdrant collection to store embeddings
        batch_size: Number of nodes to process in each batch
    """
    print(f"Processing {label} nodes for embeddings")

    # Get total count of nodes
    total_count = get_node_count(driver, label)
    print(f"Found {total_count} {label} nodes")

    if total_count == 0:
        print(f"No {label} nodes found to process")
        return

    # Process in batches
    for offset in range(0, total_count, batch_size):
        print(f"Processing batch at offset {offset}")

        # Get batch of nodes
        nodes = get_nodes(driver, label, batch_size, offset)

        # Process each node
        for node in nodes:
            node_id = node["id"]
            node_properties = node["properties"]

            # Create combined text for embedding
            combined_text = create_text_for_embedding(node_properties, label)

            if combined_text:
                # Generate embedding
                vector = list(model.encode(combined_text))
                # Generate a new UUID for Qdrant
                qdrant_id = str(uuid.uuid4())
                # Prepare payload with common attributes
                payload = {
                    "neo4j_elementId": str(node_id),
                    "name": node_properties.get("name", ""),
                    "description": node_properties.get("description", ""),
                    "tags": node_properties.get("tags", []),
                    "label": label  # Add label as a property
                }

                # Add location based on node type
                if label == "POI" and "location" in node_properties:
                    longitude, latitude = node_properties.get("location")
                    payload["location"] = {"lon": longitude, "lat": latitude}
                elif label == "AOI" and "centroid" in node_properties:
                    longitude, latitude = node_properties.get("centroid")
                    payload["location"] = {"lon": longitude, "lat": latitude}

                # Store in Qdrant
                client.upsert(
                    collection_name=collection_name,
                    points=[{
                        "id": qdrant_id,
                        "vector": vector,
                        "payload": payload
                    }]
                )

        print(f"Completed batch processing (offset: {offset})")

    # Verify storage
    collection_info = client.get_collection(collection_name=collection_name)
    print(
        f"Qdrant Collection '{collection_name}' contains {collection_info.vectors_count} vectors")


def process_node_embeddings2(driver, model, client, label: str, collection_name: str, batch_size: int = 100):
    """
    Process nodes to generate embeddings and store them in Qdrant.

    Args:
        driver: Neo4j driver instance
        model: SentenceTransformer model
        client: Qdrant client instance
        node_type: Type of nodes to process
        collection_name: Name of the Qdrant collection to store embeddings
        batch_size: Number of nodes to process in each batch
    """
    print(f"Processing {label} nodes for embeddings")

    # Get total count of nodes
    total_count = get_node_count(driver, label)
    print(f"Found {total_count} {label} nodes")

    if total_count == 0:
        print(f"No {label} nodes found to process")
        return

    # Process in batches
    for offset in range(0, total_count, batch_size):
        print(f"Processing batch at offset {offset}")

        # Get batch of nodes
        nodes = get_nodes(driver, label, batch_size, offset)
        # Process each node
        combined_texts = []
        for node in nodes:
            node_properties = node["properties"]
            # Create combined text for embedding
            combined_text = create_text_for_embedding(node_properties, label)
            combined_texts.append(combined_text)
        combined_texts_embs = model.encode(combined_texts)

        # Process each node
        for node, emb in zip(nodes, combined_texts_embs):
            node_id = node["id"]
            node_properties = node["properties"]

            if emb:
                # Generate embedding
                vector = list(emb)
                # Generate a new UUID for Qdrant
                qdrant_id = str(uuid.uuid4())
                # Prepare payload with common attributes
                payload = {
                    "neo4j_elementId": str(node_id),
                    "name": node_properties.get("name", ""),
                    "description": node_properties.get("description", ""),
                    "tags": node_properties.get("tags", []),
                    "label": label  # Add label as a property
                }

                # Add location based on node type
                if label == "POI" and "location" in node_properties:
                    longitude, latitude = node_properties.get("location")
                    payload["location"] = {"lon": longitude, "lat": latitude}
                elif label == "AOI" and "centroid" in node_properties:
                    longitude, latitude = node_properties.get("centroid")
                    payload["location"] = {"lon": longitude, "lat": latitude}

                # Store in Qdrant
                client.upsert(
                    collection_name=collection_name,
                    points=[{
                        "id": qdrant_id,
                        "vector": vector,
                        "payload": payload
                    }]
                )

        print(f"Completed batch processing (offset: {offset})")

    # Verify storage
    collection_info = client.get_collection(collection_name=collection_name)
    print(
        f"Qdrant Collection '{collection_name}' contains {collection_info.vectors_count} vectors")


def load_embedding_model_std():
    """
    Load a sentence transformer model for generating embeddings.

    Args:
        model_name: Name of the sentence-transformers model to use

    Returns:
        A SentenceTransformer model
    """
    # Initialize the sentence transformer model
    model_std = 'paraphrase-multilingual-MiniLM-L12-v2'
    print(f"Loading embedding model: {model_std}")
    return SentenceTransformer(model_std)


def compute_cosine_similarity(embedding1, embedding2):
    # Convert embeddings to numpy arrays
    emb1 = np.array(embedding1)
    emb2 = np.array(embedding2)

    # Compute dot product and norms
    dot_product = np.dot(emb1, emb2)
    norm_emb1 = np.linalg.norm(emb1)
    norm_emb2 = np.linalg.norm(emb2)

    # Compute cosine similarity
    cosine_similarity = dot_product / (norm_emb1 * norm_emb2)
    return cosine_similarity


class OpenAIEmbeddingModel:
    def __init__(self, model_name='text-embedding-3-small'):
        self.model_name = model_name
        # You can set this statically or fetch it from OpenAI documentation
        self.embedding_dimensions = {
            'text-embedding-3-small': 1536,
            'text-embedding-3-large': 3072,
        }

    def get_sentence_embedding_dimension(self):
        return self.embedding_dimensions.get(self.model_name, None)

    def encode(self, texts):
        input_was_string = False
        if isinstance(texts, str):
            texts = [texts]
            input_was_string = True
        texts = [text.replace("\n", " ").strip() for text in texts]
        res_data = client.embeddings.create(
            input=texts,
            model=self.model_name
        ).data
        all_embeddings = [res.embedding for res in res_data]
        if input_was_string:
            all_embeddings = all_embeddings[0]

        return all_embeddings


def load_embedding_model_openai():
    """
    Load an OpenAI embedding model wrapped in a SentenceTransformer-like interface.

    Returns:
        An object with get_sentence_embedding_dimension() and encode() methods.
    """
    model_name = 'text-embedding-3-small'
    print(f"Loading OpenAI embedding model: {model_name}")
    return OpenAIEmbeddingModel(model_name)


class NomicEmbeddingModel:
    def __init__(self, model_name='nomic-embed-text'):
        self.model_name = model_name
        # You can adjust this based on the actual model spec
        self.embedding_dimensions = {
            'nomic-embed-text': 768,  # You can verify this value based on the model docs
        }

    def get_sentence_embedding_dimension(self):
        return self.embedding_dimensions.get(self.model_name, None)

    def encode(self, texts):
        input_was_string = False
        if isinstance(texts, str):
            texts = [texts]
            input_was_string = True

        texts = [text.replace("\n", " ").strip() for text in texts]
        all_embeddings = []
        for text in texts:
            response = ollama.embeddings(model=self.model_name, prompt=text)
            all_embeddings.append(response['embedding'])

        if input_was_string:
            return all_embeddings[0]

        return all_embeddings


def load_embedding_model_nomic():
    """
    Load a Nomic embedding model via Ollama, wrapped in a SentenceTransformer-like interface.

    Returns:
        An object with get_sentence_embedding_dimension() and encode() methods.
    """
    model_name = 'nomic-embed-text'
    print(f"Loading Nomic embedding model via Ollama: {model_name}")
    return NomicEmbeddingModel(model_name)
