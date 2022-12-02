import numpy as np

def query_no_embedding(text:str) -> dict:
  return {
    "query": {
      "match": {
        "tokens": {
          "query": text
        }
      }
    }
  }

def query_only_embedding(vector) -> dict:
  return {
      "field": "embedding",
      "query_vector": vector,
      "k": 10,
      "num_candidates": 50
  }