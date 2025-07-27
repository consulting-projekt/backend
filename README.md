# Backend Repository - Wissenschaftliche Arbeit

Dieses Repository enthält das Backend-System der wissenschaftlichen Arbeit und ist als Anhang der Abschlussarbeit beigefügt.

## Repository-Struktur

### Hauptverzeichnisse

- **`src/`** - Hauptquellcode des Backends
  - Utility-Module für verschiedene Funktionalitäten (Embeddings, Datenverarbeitung, APIs)
  - Jupyter Notebooks für die Erstellung von Embeddings mit verschiedenen Modellen
  - Docker-Konfiguration
  
- **`tests/`** - Testframework und Evaluierung
  - **`_1_params_extract/`** - Tests für Parameter-Extraktion mit verschiedenen LLMs
  - **`_2_embeddings_search/`** - Tests für Embedding-basierte Suche
  - **`_3_e2e/`** - End-to-End Tests des Gesamtsystems
  
- **`imports/`** - Datenimport-Scripts
  - Notebooks für Import von OSM-Daten, Geofox-APIs und benutzerdefinierten Daten
  
- **`exports/`** - Datenexport-Funktionalitäten
  - CSV-Export von verarbeiteten Daten

### Kernkomponenten

#### Utility-Module (`src/`)
- `utils_embeddings.py` - Embedding-Generierung und -Verarbeitung
- `utils_qdrant.py` - Vector-Database Integration
- `utils_geofox.py` - Geofox API Client
- `utils_osm.py` - OpenStreetMap Datenverarbeitung
- `utils_llm.py` - Large Language Model Integration
- `geofox_client.py` - Geofox API Wrapper

#### Embedding-Notebooks
- `create_embeddings_aoipoi_*.ipynb` - Verschiedene Embedding-Modelle:
  - DistilUSE
  - LaBSE
  - Nomic v2
  - OpenAI
  - Standard v2

#### Experimentelle Entwicklung (`src/eperiments/`)
- Prototyping und Experimente mit verschiedenen Ansätzen
- POI-Suche, Routing, Vector-Suche Experimente

### Testsystem

Das Repository implementiert ein umfassendes Testsystem mit drei Evaluierungsebenen:

1. **Parameter-Extraktion** - Evaluation verschiedener LLMs bei der Extraktion von Suchparametern
2. **Embedding-Suche** - Vergleich verschiedener Embedding-Modelle für semantische Suche
3. **End-to-End** - Gesamtsystem-Tests mit realen Szenarien

## Setup

### Voraussetzungen
- Python 3.10
- Docker (für Qdrant Vector Database)

### Installation
```bash
pip install -r requirements.txt
```

### Datenbank
Das System verwendet Qdrant als Vector-Database, konfiguriert über Docker Compose.

## Verwendung im Kontext der Arbeit

Dieses Repository demonstriert die praktische Implementierung der in der wissenschaftlichen Arbeit beschriebenen Konzepte für:
- Multimodale Suche in Point-of-Interest Daten
- Embedding-basierte semantische Suche
- Integration verschiedener Datenquellen (OSM, Geofox)
- Evaluierung und Vergleich verschiedener KI-Modelle

