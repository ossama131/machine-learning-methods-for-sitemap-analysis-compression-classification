
## Crawler architecture
![alt text](https://github.com/ossama131/machine-learning-methods-for-sitemap-analysis-compression-classification/blob/main/resources/distributed_crawler.PNG?raw=true)

## Running the crawler
#### Configurations
- `celery_config.py`: provide broker location
- `tasks.py`: configure MinIO location

#### Running
- Run the celery worker using: `celery -A tasks worker --loglevel=INFO`
- Submit tasks using `submit_client.py` by providing the path for text files containig one URL per line.

For more about configurations of Celery: https://docs.celeryq.dev/en/stable/getting-started/first-steps-with-celery.html
