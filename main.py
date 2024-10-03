from fastapi import FastAPI
from elasticsearch import Elasticsearch
import requests
import os

app = FastAPI()

# Elasticsearch Cloud Connection using environment variables
es = Elasticsearch(
    hosts=[os.getenv("ELASTICSEARCH_HOST")],
    http_auth=(os.getenv("ELASTICSEARCH_USERNAME"), os.getenv("ELASTICSEARCH_PASSWORD"))
)

FOOTBALL_API_URL = "https://api.football-data.org/v4/matches"
API_KEY = "api_key"

# Root route
@app.get("/")
def read_root():
    return {"message": "Welcome to the Football Data Ingestion API"}

# Ingest real-time football data into Elasticsearch
@app.get("/ingest-live-football-data")
def ingest_football_data():
    headers = {"X-Auth-Token": API_KEY}
    response = requests.get(FOOTBALL_API_URL, headers=headers)
    
    # Debugging: Log the status code and response
    print(f"Response Status Code: {response.status_code}")
    print(f"Response Content: {response.text}")

    if response.status_code != 200:
        return {"error": "Failed to fetch data from API"}

    match_data = response.json()

    # Ingest data into Elasticsearch
    for match in match_data['matches']:
        es.index(index="football-data", document=match)

    return {"status": "Data ingested"}

# Search API for football matches
@app.get("/search-matches")
def search_matches(team_name: str):
    query = {
        "query": {
            "match": {"homeTeam.name": team_name}
        }
    }
    result = es.search(index="football-data", body=query)
    return {"matches": result['hits']['hits']}
