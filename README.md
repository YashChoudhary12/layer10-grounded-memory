# Layer10 Grounded Memory System

This project implements a grounded long-term memory system that converts
unstructured communication (emails) into a structured memory graph.

## Dataset
Enron Email Dataset

## Pipeline

1. Ingest emails
2. Extract structured entities and claims
3. Deduplicate artifacts/entities/claims
4. Build memory graph
5. Retrieve grounded answers
6. Visualize the graph

## Run

1. Download dataset
2. Run ingestion pipeline
3. Run extraction
4. Build memory graph

Steps- 
## Setup

1. Clone the repo

git clone <https://github.com/YashChoudhary12/layer10-grounded-memory.git>
cd layer10-grounded-memory


2. Install dependencies

pip install -r requirements.txt


3. Download the dataset

bash scripts/download_dataset.sh


4. Run ingestion

python ingestion/ingest_enron.py


5. Run extraction pipeline

python -m extraction.pipeline


6. Run semantic search

python retrieval/semantic_search.py


7. Generate visualization

python -m visualization.graph_view
