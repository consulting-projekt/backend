import subprocess
import os
import argparse
import time
import glob

def restore_neo4j_backup(new_container_name, backup_file=None):
    """
    Restore a Neo4j database backup to a specified container
    
    Args:
        new_container_name (str): Name of the target Neo4j container
        backup_file (str, optional): Specific backup file to restore. If None, uses the latest backup.
    """
    print(f"===== Neo4j Database Restore to {new_container_name} =====")
    
    # Check if container exists
    result = subprocess.run(["docker", "ps", "-a", "--format", "{{.Names}}"], 
                           capture_output=True, text=True)
    containers = result.stdout.strip().split('\n')
    
    if new_container_name not in containers:
        print(f"ERROR: Container '{new_container_name}' not found!")
        return
    
    
    # Determine if backup file is local or inside container
    container_backup_path = f"/snapshots"
    
    
    # Stop the container
    print(f"Stopping container {new_container_name}...")
    subprocess.run(["docker", "stop", new_container_name])
    time.sleep(2)  # Give it time to stop properly
    
    # Restore the database
    print(f"Restoring database from backup...")
    restore_cmd = f"docker run --rm --volumes-from {new_container_name} neo4j:2025.03-community neo4j-admin database load {backup_file} --from-path={container_backup_path} --overwrite-destination=true"
    result = subprocess.run(restore_cmd, shell=True, capture_output=True, text=True)
    
    if result.returncode != 0:
        print("ERROR during restore:")
        print(result.stderr)
    else:
        print("Database restored successfully!")
    
    # Start the container again
    print(f"Starting container {new_container_name}...")
    subprocess.run(["docker", "start", new_container_name])
    
    print("===== Restore Complete =====")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Restore Neo4j database from backup")
    parser.add_argument("--container", default="neo4j-bus-chatbot-osm2", help="Target container name to restore the database to")
    parser.add_argument("-f", "--file", default="neo4j", help="Specific backup file to restore (optional, uses latest if not specified)")
    
    args = parser.parse_args()
    restore_neo4j_backup(args.container, args.file)