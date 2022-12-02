import io

import requests
from minio import S3Error

from .response import (
    Response,
    SucessfulResponse,
)
from .gz import (
    is_gzipped,
    gunzip
)
from .sitemap import (
    Sitemap,
    SitemapIndex,
    SitemapUrlSet,
    iter_sitemap_entries
)

from .celery_logger import logger
from .exceptions import *

connect_timeout, read_timeout = 10.0, 60.0

def fetch_url(url:str):
    try:
        r = requests.get(
            url=url,
            allow_redirects=False,
            timeout=(connect_timeout, read_timeout)
        )
        r.raise_for_status()
        logger.info('SuccessfulResponse')
        return SucessfulResponse(r.content)
    except requests.exceptions.RequestException:
        logger.info('SitemapRequestError')
        raise SitemapRequestError()

def xml_parser(response: Response):
    try:
        assert isinstance(response, SucessfulResponse)
    except AssertionError:
        raise SitemapRequestError()
    
    if is_gzipped(response.content):
        try:
            content = gunzip(response.content)
        except Exception as e:
            logger.info('SitemapGunzipError')
            raise SitemapGunzipError()
    else:
        content = response.content
        
    encoding = None
    for enc in ('utf-8', 'cp1252', 'utf-8-sig'):
        try:
            content.decode(enc)
            encoding = enc
            content = content.decode(enc)
            break
        except UnicodeError:
            logger.info('SitemapUnicodeError')
            raise SitemapUnicodeError()
    
    if not encoding:
        logger.info('SitemapUnicodeError')
        raise SitemapUnicodeError()

    try:
        s = Sitemap(content.encode('utf-8'))
    except Exception as e:
        logger.info('SitemapParsingError')
        raise SitemapParsingError()        

    try:
        assert s.type in ['sitemapindex', 'urlset']
    except AssertionError:
        logger.info('SitemapTypeNotHandledError')
        raise SitemapTypeNotHandledError()

    try:
        urls = []
        for d in iter_sitemap_entries(s):
            if 'loc' in d.keys():
                urls.append(d['loc'])
        assert len(urls) > 0
    except AssertionError:
        logger.info('SitemapEmptyError')
        raise SitemapEmptyError()

    if s.type == 'sitemapindex':
        logger.info(f'SitemapIndex: {len(urls)} url')
        return SitemapIndex(urls)
    elif s.type == 'urlset':
        logger.info(f'SitemapUrlSet: {len(urls)} url')
        return SitemapUrlSet(urls)
        
    
def upload_data_to_minio_s3(client, data:list, file_name:str, bucket:str):
    try:
        found = client.bucket_exists(bucket)
        if not found:
            #Bucket not found, creating one
            client.make_bucket(bucket)
        data_len = len(data)
        data = '\n'.join(data)
        result = client.put_object(
            bucket,
            file_name,
            io.BytesIO(data.encode()),
            len(data)
        )
        logger.info(f'UploadedSuccessfully: {data_len} url')
        return
    except S3Error as exc:
        logger.info('MinioS3Error')
        raise MinioS3Error()
    except UnicodeError:
        logger.info('MinioS3UnicodeError')
        raise MinioS3UnicodeError()

