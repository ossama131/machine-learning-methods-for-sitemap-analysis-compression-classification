mapping_no_embedding = {
  "settings": {
    "index": {
      "number_of_shards": "2",
      "number_of_replicas": "1"
    }
  },
  "mappings": {
    "properties": {
      "id": {
        "type": "keyword"
      },
      "url": {
        "type": "keyword"
      },
      "tokens": {
        "type": "text",
        "analyzer": "whitespace"
      }
    }
  },
  "aliases": {}
}

mapping_embedding = {
  "settings": {
    "index": {
      "number_of_shards": "2",
      "number_of_replicas": "1",
    }
  },
  "mappings": {
    "properties": {
      "id": {
        "type": "keyword"
      },
      "tokens": {
        "type": "text",
        "analyzer": "whitespace"
      },
      "url": {
        "type": "keyword"
      },
      "embedding": {
          "type": "dense_vector",
          "dims": 300,
          "index": True,
          "similarity": "cosine",
          "index_options": {
            "type": "hnsw",
            "m": 16,
            "ef_construction": 100
          }
      }
    }
  },
  "aliases": {}
}