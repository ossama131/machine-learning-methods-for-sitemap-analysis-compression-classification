from celery import (
    group,
    Task
)
from minio import Minio

from .celery_config import app

from .utils.response import (
    SucessfulResponse,
)
from .utils.sitemap import (
    SitemapIndex,
    SitemapUrlSet
)
from .utils.utils import (
    fetch_url,
    xml_parser,
    upload_data_to_minio_s3
)
from .utils.exceptions import SitemapMaximumRecursionLevelReached

MAX_RECURSION_LEVEL = 5
BUCKET_NAME='crawled'

class MinioS3Task(Task):
        
    _minio = None

    @property
    def minio(self):
        if self._minio is None:
            self._minio = Minio(
                endpoint="localhost:9000",
                access_key="minioadmin",
                secret_key="minioadmin",
                secure=False
            )
        return self._minio

@app.task(base=MinioS3Task, bind=True, ignore_result=True)
def crawl(self, url:str, recursion_level:int):
    response = fetch_url(url)
    if isinstance(response, SucessfulResponse):
        sitemap = xml_parser(response)
        if isinstance(sitemap, SitemapIndex):
            #max recursion level reached
            if recursion_level >= MAX_RECURSION_LEVEL:
                raise SitemapMaximumRecursionLevelReached()
            subtasks = group(crawl.s(url, recursion_level + 1) for url in sitemap.urls)
            subtasks.apply_async()
        elif isinstance(sitemap, SitemapUrlSet):
            upload_data_to_minio_s3(
                client=self.minio,
                data=sitemap.urls,
                file_name=self.request.id + '.txt',
                bucket=BUCKET_NAME
            )
            return