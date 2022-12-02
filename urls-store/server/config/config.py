import os

INIT_INDICES = os.environ.get('INIT_INDICES', 'True').lower() in ('true', '1', 't')
USE_DENSE_VECTORS = os.environ.get('USE_DENSE_VECTORS', 'False').lower() in ('true', '1', 't')
INDEX_NAME = os.environ.get('INDEX_NAME', 'urls-index-default')
ELASTICSEARCH_URI = os.environ.get('ELASTICSEARCH_URI', 'http://localhost:9200')
FASTTEXT_MODEL_PATH = os.environ.get('FASTTEXT_MODEL_PATH', 'embedding/models/fasttext/gpt2_bpe_fasttext_model.bin')
