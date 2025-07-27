# Repository-Struktur

## Hauptverzeichnisse

- **`src/`** - Hauptquellcode des Backends
  - Utility-Module für verschiedene Funktionalitäten (Embeddings, Datenverarbeitung, APIs)
  - Jupyter Notebooks für die Erstellung von Embeddings mit verschiedenen Modellen
  - Docker-Konfiguration
  
  - **`imports/`**
      - Datenimport-Scripts
      - Notebooks für Import von OSM-Daten, Geofox-APIs und benutzerdefinierten Daten
  
  - **`exports/`**
      - Datenexport-Funktionalitäten
      - CSV-Export von verarbeiteten Daten
  
  - **`experiments/`**
      - Prototyping und Experimente mit verschiedenen Ansätzen
      - POI-Suche, Routing, Vector-Suche Experimente

- **`tests/`** - Testframework und Evaluierung
  - **`_1_params_extract/`**
    - Tests für Parameter-Extraktion mit verschiedenen LLMs
  - **`_2_embeddings_search/`**
    - Tests für Embedding-basierte Suche
  - **`_3_e2e/`**
    - End-to-End Tests des Gesamtsystems

## Testsystem

Das Repository implementiert ein umfassendes Testsystem mit drei Evaluierungsebenen:

1. **Parameter-Extraktion** - Evaluation verschiedener LLMs bei der Extraktion von Parametern
2. **Embedding-Suche** - Vergleich verschiedener Embedding-Modelle für semantische Suche
3. **End-to-End** - Gesamtsystem-Tests mit realen Szenarien

# Setup

## Voraussetzungen
- Python 3.10
- Docker (für Qdrant Vector Database)

## Installation
```bash
pip install -r requirements.txt
```

## Datenbank
Das System verwendet Qdrant als Vector-Database, konfiguriert über Docker Compose.

# Verwendung im Kontext der Arbeit

Dieses Repository demonstriert die praktische Implementierung der in der wissenschaftlichen Arbeit beschriebenen Konzepte für:
- Intention-Detection und Slot-Filling
- Embedding-basierte semantische Suche
- Integration verschiedener Datenquellen (OSM, Geofox)
- Evaluierung und Vergleich verschiedener KI-Modelle

