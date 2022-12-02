import time
from uuid import uuid4

from minio import Minio

from utils.utils import (
    fetch_url,
    xml_parser,
    upload_data_to_minio_s3
)

minio = Minio(
    endpoint='localhost:9000',
    access_key='minioadmin',
    secret_key='minioadmin',
    secure=False
    
)



url = 'https://www.bbc.com/sitemaps/https-sitemap-com-news-1.xml'
index_url = 'https://www.bbc.com/sitemaps/https-index-com-news.xml'

ts = time.time()
res = fetch_url(index_url)
te = time.time()

print(f'fetch duration: {te-ts}')

print(res)

ts = time.time()
parsed = xml_parser(res)
te = time.time()


print(f'parsing duration: {te-ts}')

ts = time.time()
upload_data_to_minio_s3(
    client=minio,
    data=parsed.urls,
    file_name='inde_some_file' + '.txt',
    bucket='testbucket'
)
te = time.time()
print(f'uploading duration: {te-ts}')