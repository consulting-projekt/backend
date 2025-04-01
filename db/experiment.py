import os
from datetime import datetime, timedelta
import pytz
import numpy as np
from neo4j import GraphDatabase
from sentence_transformers import SentenceTransformer
import pandas as pd


# Initialize the sentence transformer model
model = SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')  # Good for German

class BusTicketChatbot:
    def __init__(self, uri="bolt://localhost:7688", user="neo4j", password="busticket123"):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))
        self.model = model
        
    def close(self):
        self.driver.close()
        
    def create_vector_index(self):
        with self.driver.session() as session:
            # Create vector index for locations
            session.run("""
            CALL db.index.vector.createNodeIndex(
              'location_embeddings',
              'Location',
              'embedding',
              384,
              'cosine'
            )
            """)
    
    def clear_database(self):
        with self.driver.session() as session:
            session.run("MATCH (n) DETACH DELETE n")
    
    def load_sample_german_data(self):
        """Load sample German bus data for a fictional city"""
        self.clear_database()
        
        # Generate current timestamps based on the current time
        now = datetime.now(pytz.timezone('Europe/Berlin'))
        current_time = now.strftime("%H:%M")
        
        # Calculate upcoming bus departure times (every 10-15 minutes)
        upcoming_times = []
        for i in range(1, 8):
            upcoming_times.append((now + timedelta(minutes=i*10 + np.random.randint(0, 5))).strftime("%H:%M"))
        
        with self.driver.session() as session:
            # Create locations (bus stops)
            locations = [
                ("Hauptbahnhof", ["Hauptbahnhof", "HBF", "Zentralbahnhof", "Zentrum", "Bahnhof"], 
                 [48.1402, 11.5584]),  # Munich coordinates
                ("Marienplatz", ["Marienplatz", "Stadtmitte", "Innenstadt", "Altstadt", "Zentrum", "City Center"], 
                 [48.1375, 11.5754]),
                ("Sendlinger Tor", ["Sendlinger Tor", "Innenstadt", "Altstadt"], 
                 [48.1336, 11.5677]),
                ("Universität", ["Universität", "Uni", "Maxvorstadt"], 
                 [48.1507, 11.5801]),
                ("Ostbahnhof", ["Ostbahnhof", "Haidhausen"], 
                 [48.1271, 11.6036]),
                ("Rotkreuzplatz", ["Rotkreuzplatz", "Neuhausen"], 
                 [48.1511, 11.5341]),
                ("Münchner Freiheit", ["Münchner Freiheit", "Schwabing"], 
                 [48.1619, 11.5867])
            ]
            
            # Create bus lines
            bus_lines = [
                ("U3", "U-Bahn 3", "blue"),
                ("U6", "U-Bahn 6", "blue"),
                ("Bus 100", "MetroBus 100", "red"),
                ("Bus 58", "StadtBus 58", "green"),
                ("Tram 19", "Straßenbahn 19", "yellow")
            ]
            
            # Create locations with vector embeddings
            for name, synonyms, coords in locations:
                # Create embedding from name and synonyms
                combined_text = " ".join([name] + synonyms)
                embedding = self.model.encode(combined_text).tolist()
                
                # Create location node with embedding
                session.run("""
                CREATE (l:Location {name: $name, synonyms: $synonyms, latitude: $lat, longitude: $lng, embedding: $embedding})
                """, name=name, synonyms=synonyms, lat=coords[0], lng=coords[1], embedding=embedding)
            
            # Create transportation lines
            for line_id, line_name, color in bus_lines:
                session.run("""
                CREATE (l:Line {id: $id, name: $name, color: $color})
                """, id=line_id, name=line_name, color=color)
            
            # Create connections between stops with schedules
            connections = [
                ("Hauptbahnhof", "Marienplatz", "U3", upcoming_times[0:5]),
                ("Hauptbahnhof", "Sendlinger Tor", "U6", upcoming_times[1:6]),
                ("Marienplatz", "Sendlinger Tor", "U3", upcoming_times[0:5]),
                ("Marienplatz", "Universität", "U6", upcoming_times[2:7]),
                ("Sendlinger Tor", "Ostbahnhof", "U3", upcoming_times[1:6]),
                ("Rotkreuzplatz", "Hauptbahnhof", "Bus 100", upcoming_times[0:5]),
                ("Münchner Freiheit", "Universität", "Tram 19", upcoming_times[1:6]),
                ("Ostbahnhof", "Hauptbahnhof", "Bus 58", upcoming_times[2:7])
            ]
            
            for from_stop, to_stop, line, times in connections:
                session.run("""
                MATCH (from:Location {name: $from_loc})
                MATCH (to:Location {name: $to})
                MATCH (line:Line {id: $line})
                CREATE (from)-[r:CONNECTED_TO {
                    via: $line,
                    travel_time_minutes: $travel_time,
                    upcoming_departures: $times
                }]->(to)
                """, from_loc=from_stop, to=to_stop, line=line, travel_time=10, times=times)
            
            # Create tag for inner city locations
            session.run("""
            MATCH (l:Location)
            WHERE l.name IN ['Marienplatz', 'Sendlinger Tor']
            SET l:InnerCity, l.is_inner_city = true
            """)
            
    def create_vector_embedding(self, text):
        """Create embedding for a query text"""
        return self.model.encode(text).tolist()
    
    def find_next_bus(self, current_location, destination_query, current_time=None):
        """Find the next bus from current location to destination query"""
        if current_time is None:
            current_time = datetime.now(pytz.timezone('Europe/Berlin')).strftime("%H:%M")
        
        # Create embedding for destination query
        query_embedding = self.create_vector_embedding(destination_query)
        
        with self.driver.session() as session:
            # First find the current location
            current_stop = session.run("""
            MATCH (l:Location)
            WHERE l.name = $location
            RETURN l
            """, location=current_location).single()
            
            if not current_stop:
                return {"error": f"Current location '{current_location}' not found"}
                
            # Use vector search to find matching destinations
            result = session.run("""
            // Find potential destinations using vector similarity
            CALL db.index.vector.queryNodes('location_embeddings', $k, $query_embedding)
            YIELD node, score
            WHERE score > 0.7
            
            // Now find paths from current location to these destinations
            WITH node as destination
            MATCH (current:Location {name: $current_location})
            MATCH path = shortestPath((current)-[:CONNECTED_TO*1..3]->(destination))
            
            // Extract connections along path
            WITH path, destination,
                 [rel in relationships(path) | {
                     from: startNode(rel).name,
                     to: endNode(rel).name,
                     line: rel.via,
                     departures: rel.upcoming_departures
                 }] as connections
            
            // Return detailed route information
            RETURN 
                destination.name as destination_name,
                destination.synonyms as destination_synonyms,
                connections
            """, query_embedding=query_embedding, k=5, current_location=current_location)
            
            routes = []
            for record in result:
                destination = record["destination_name"]
                connections = record["connections"]
                synonyms = record["destination_synonyms"]
                
                route_info = {
                    "destination": destination,
                    "synonyms": synonyms,
                    "connections": connections
                }
                
                routes.append(route_info)
            
            return routes

    def format_results(self, routes, query):
        """Format routes into a user-friendly response"""
        if not routes:
            return f"Leider konnte ich keine Verbindung zur '{query}' finden. Bitte überprüfen Sie den Namen des Ziels."
        
        response = f"Hier sind die nächsten Verbindungen zur '{query}':\n\n"
        
        for i, route in enumerate(routes, 1):
            destination = route["destination"]
            response += f"Route {i} nach {destination}:\n"
            
            for j, connection in enumerate(route["connections"], 1):
                from_stop = connection["from"]
                to_stop = connection["to"]
                line = connection["line"]
                departures = connection["departures"]
                
                response += f"  Teilstrecke {j}: Von {from_stop} nach {to_stop} mit {line}\n"
                response += f"    Nächste Abfahrten: {', '.join(departures[:3])}\n"
            
            response += "\n"
            
        return response

    def process_query(self, query, current_location):
        """Process a natural language query about buses"""
        routes = self.find_next_bus(current_location, query)
        return self.format_results(routes, query)


# Example usage
if __name__ == "__main__":
    chatbot = BusTicketChatbot()
    
    # Setup database
    chatbot.load_sample_german_data()
    chatbot.create_vector_index()
    
    # Test query - "When's the next bus to inner city?"
    query = "Wann kommt der nächste Bus in die Innenstadt?"
    current_location = "Hauptbahnhof"  # User's current location
    
    result = chatbot.process_query(query, current_location)
    print(result)
    
    # Try different queries
    queries = [
        "Wie komme ich zum Marienplatz?",
        "Nächster Bus zum Zentrum?",
        "Verbindung zur Universität"
    ]
    
    for q in queries:
        print("\n" + "="*50)
        print(f"Query: {q}")
        result = chatbot.process_query(q, current_location)
        print(result)
        
    chatbot.close()