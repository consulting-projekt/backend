from sentence_transformers import SentenceTransformer
import pandas as pd
from typing import List, Dict, Any
from neo4j import GraphDatabase
from sentence_transformers import SentenceTransformer
from utils_neo4j import get_node_count
import json



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



def get_nodes_batch(driver, label: str, offset: int, batch_size: int) -> List[Dict]:
    """
    Get a batch of nodes with the specified label.
    
    Args:
        driver: Neo4j driver instance
        label: Node label to query
        offset: Starting offset for pagination
        batch_size: Number of nodes to retrieve
        
    Returns:
        List of node dictionaries with their properties
    """
    with driver.session() as session:
        query = f"""
        MATCH (n:{label})
        WHERE NOT EXISTS(n.embeddings_json)
        RETURN elementId(n) AS id, properties(n) AS properties
        SKIP {offset}
        LIMIT {batch_size}
        """
        
        result = session.run(query)
        return [{"id": record["id"], "properties": record["properties"]} for record in result]

def generate_embeddings_for_text(model, text: str) -> List[float]:
    """
    Generate embeddings for a text string.
    
    Args:
        model: SentenceTransformer model
        text: Text to generate embeddings for
        
    Returns:
        List of embedding values
    """
    if text:
        return model.encode(text).tolist()
    return []

def generate_node_embeddings(model, node_properties: Dict) -> List[List[float]]:
    """
    Generate embeddings for node properties (name, description, tags).
    
    Args:
        model: SentenceTransformer model
        node_properties: Dictionary of node properties
        
    Returns:
        List of embedding arrays
    """
    embeddings_dic = {}
    
    # Generate embedding for name if it exists
    if "name" in node_properties and node_properties["name"]:
        name_embedding = generate_embeddings_for_text(model, node_properties["name"])
        embeddings_dic['name'] = name_embedding
    else:
        embeddings_dic['name'] = []
    
    # Generate embedding for description if it exists
    if "description" in node_properties and node_properties["description"]:
        desc_embedding = generate_embeddings_for_text(model, node_properties["description"])
        embeddings_dic['description'] = desc_embedding
    else:
        embeddings_dic['description'] = []
    
    # Generate embeddings for each tag if they exist
    if "tags" in node_properties and isinstance(node_properties["tags"], list):
        tagEmbeddings = []
        for tag in node_properties["tags"]:
            if tag:  # Only process non-empty tags
                tag_embedding = generate_embeddings_for_text(model, tag)
                tagEmbeddings.append(tag_embedding)
        embeddings_dic['tags'] = tagEmbeddings
    else:
        embeddings_dic['tags'] = []
    
    return embeddings_dic

def update_node_embeddings(driver, node_id: int, embeddings_dict) -> None:
    """
    Update a Neo4j node with the generated embeddings list.
    
    Args:
        driver: Neo4j driver instance
        node_id: ID of the node to update
        embeddings_list: List of embedding arrays to store
    """
    with driver.session() as session:
        update_query = """
        MATCH (n)
        WHERE elementId(n) = $node_id
        SET n.embeddings_json = $embeddings_json
        """
        session.run(update_query, {"node_id": node_id, "embeddings_json": json.dumps(embeddings_dict)})

def process_nodes(driver, model, label: str, batch_size: int = 100) -> None:
    """
    Process all nodes with the specified label to generate and store embeddings.
    
    Args:
        driver: Neo4j driver instance
        model: SentenceTransformer model
        label: Node label to process
        batch_size: Number of nodes to process in each batch
    """
    print(f"Processing nodes with label: {label}")
    
    # Get total count
    total_count = get_node_count(driver, label)
    print(f"Found {total_count} {label} nodes")
    
    # Process in batches
    for offset in range(0, total_count, batch_size):
        print(f"Processing batch at offset {offset}")
        
        # Get batch of nodes
        nodes = get_nodes_batch(driver, label, offset, batch_size)
        
        # Process each node
        for node in nodes:
            node_id = node["id"]
            node_properties = node["properties"]
            
            # Generate embeddings
            embeddings_dict = generate_node_embeddings(model, node_properties)
            
            # Update node with embeddings
            update_node_embeddings(driver, node_id, embeddings_dict)
            
        print(f"Completed batch processing (offset: {offset})")

# Initialize the sentence transformer model
model_std = 'paraphrase-multilingual-MiniLM-L12-v2'

def load_embedding_model_std():
    """
    Load a sentence transformer model for generating embeddings.
    
    Args:
        model_name: Name of the sentence-transformers model to use
        
    Returns:
        A SentenceTransformer model
    """
    print(f"Loading embedding model: {model_std}")
    return SentenceTransformer(model_std)