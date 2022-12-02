
## URLs store architecture
![alt text](https://github.com/ossama131/machine-learning-methods-for-sitemap-analysis-compression-classification/blob/main/resources/urls_store.PNG?raw=true)

## Server Configurations
- `/server/config/config.py`: contains config for :
  - `ElasticSearch` server
  - `FastText` model path
  - Index name in Elasticsearch
  - `USE_DENSE_VECTORS`: a flag to indicate the usage of dense vectors for indexing or not
  - `INIT_INDICES`: a flag to initialize indices at the start or not.

- `/server/document_store/elasticsearch/es_config/`:
  - `mapping.py`: The mapping for the created indices in Elasticsearch
  - `query_templates`: The template to be used when querying for the indexed data

## Running the server
The server is implemented in FastAPI and can be run from `/server` folder using:
  `uvicorn main:app` : https://fastapi.tiangolo.com/tutorial/
  
## Run an indexing or querying action
- The client must be configured first using `/client/config.py` file.
- Run a query or index action from command line as following: `python client.py --config_file config.py {--options}`
