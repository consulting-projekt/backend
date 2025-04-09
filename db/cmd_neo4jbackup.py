import subprocess
import datetime
from pathlib import Path

snapshot_container_path="snapshots/std_embeddings"
snapshot_path = Path(__file__).parent / "neo4j_container" / snapshot_container_path
snapshot_path.mkdir(parents=True, exist_ok=True)

print("Stopping Neo4j container...")
subprocess.run(["docker", "stop", "neo4j-bus-chatbot-osm"])

print("Creating backup...")
cmd = [
    "docker", "run", "--rm",
    "--volumes-from", "neo4j-bus-chatbot-osm",
    "--name", "neo4j-backup-container",
    "neo4j:2025.03-community",
    "neo4j-admin", "database", "dump", "neo4j", 
    f"--to-path=/{snapshot_container_path}"
]
subprocess.run(cmd)

print("Starting Neo4j container...")
subprocess.run(["docker", "start", "neo4j-bus-chatbot-osm"])

print(f"Backup created at /snapshots")