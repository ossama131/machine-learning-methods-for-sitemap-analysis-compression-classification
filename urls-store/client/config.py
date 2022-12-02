
import os 

SERVER_URI = os.environ.get('SERVER_URI', 'http://localhost:8000').strip('/')
INDEX_ENDPOINT = os.environ.get('INDEX_ENDPOINT', 'index').strip('/')
QUERY_ENDPOINT = os.environ.get('QUERY_ENDPOINT', 'query_one_item').strip('/')
TOKENIZER_ID = os.environ.get('TOKENIZER_ID', '0')
EMBEDDER_ID = os.environ.get('EMBEDDER_ID', '0')
BATCH_SIZE = int(os.environ.get('BATCH_SIZE', '10000'))

indexer_config = {
    "server_uri": SERVER_URI,
    "index_endpoint": INDEX_ENDPOINT,
    "tokeniezer_id": TOKENIZER_ID,
    "embedder_id": EMBEDDER_ID,
    "indexer_uri": "/".join([SERVER_URI, INDEX_ENDPOINT, TOKENIZER_ID, EMBEDDER_ID]),
    "batch_size": BATCH_SIZE
}


query_config = {
    "server_uri": SERVER_URI,
    "query_endpoint": QUERY_ENDPOINT,
    "tokeniezer_id": TOKENIZER_ID,
    "embedder_id": EMBEDDER_ID,
    "query_uri": "/".join([SERVER_URI, QUERY_ENDPOINT, TOKENIZER_ID, EMBEDDER_ID]),
}