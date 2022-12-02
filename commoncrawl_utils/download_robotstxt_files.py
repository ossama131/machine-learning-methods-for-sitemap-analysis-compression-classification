import os
import gc
from concurrent import futures
from itertools import product
import logging
import gzip
import pickle
from tempfile import TemporaryFile

import boto3
from botocore.client import ClientError
from botocore import UNSIGNED
from botocore.config import Config

from tqdm import tqdm


def get_s3client():
    #https://github.com/commoncrawl/cc-mrjob/blob/master/mrcc.py
    #commoncrawl is public and uses no authentication so we use unsigned 
    boto_config = Config(
            signature_version=UNSIGNED,
            read_timeout=180,
            retries={'max_attempts' : 20})
    s3client = boto3.client('s3', config=boto_config)
    return s3client

def get_robotstxt_paths(s3client, bucket, robotstxt_paths):
    temp = TemporaryFile(mode='w+b')
    try:
        logging.info('Downloading ' + bucket + '/' + robotstxt_paths)
        s3client.download_fileobj(bucket, robotstxt_paths, temp)
    except ClientError as exception:
        logging.error('Failed to download %s: %s', robotstxt_paths, exception)
        return[]
    
    temp.seek(0)
    with gzip.open(temp, 'rb') as f:
        try:
            paths = f.read().decode('utf-8', 'strict').strip().split('\n')
        except UnicodeDecodeError:
            logging.error('Failed to decode robotstxt.paths.gz')
            return []
        
    
    if len(paths) != 72000:
        logging.error('Number of rbotstxt paths != 72000')
        return []
    
    return paths


def download_file(bucket, key, download_path):
    file_key_path = '/'.join(key.split('/')[:-1])
    file_dir = f'{download_path}/{file_key_path}'
    if not os.path.exists(file_dir):
        os.makedirs(file_dir, exist_ok=True)
    file = f'{download_path}/{key}' 
    try:
        with open(file, 'wb') as data:
            logging.info('Downloading s3://%s/%s', bucket, key)
            s3client.download_fileobj(bucket, key, data)
        return 0
    except ClientError as exception:
        logging.error('Failed to download %s: %s', key, exception)
        return -1
    

def download_file_wrapper(args):
    return download_file(*args)

if __name__ == '__main__':
    logging.basicConfig(level=logging.ERROR, format="%(asctime)s %(levelname)s %(message)s")
    
    bucket = 'commoncrawl'
    robotstxt_paths = 'crawl-data/CC-MAIN-2021-43/robotstxt.paths.gz'

    home_path = os.path.expanduser('~')
    download_path = home_path + '/commoncrawl'

    s3client = get_s3client()

    paths = get_robotstxt_paths(s3client, bucket, robotstxt_paths)

    all_args_iter = product([bucket], paths, [download_path])

    del paths
    gc.collect()

    success_count = 0
    failed_count = 0
    failed_paths = []
    with futures.ProcessPoolExecutor() as executor:
        future_to_filename = {}
        for item in all_args_iter:
            future = executor.submit(download_file_wrapper, item)
            future_to_filename[future] = item[1]
        

        for future in tqdm(futures.as_completed(future_to_filename), total=len(future_to_filename)):
            if future.result() == 0:
                success_count = success_count + 1
            else:
                failed_count = failed_count + 1
                failed_paths.append(future_to_filename[future])
    
    print('\n')
    print('Total: ' + str(len(future_to_filename)))
    print('Successfull: ' + str(success_count))
    print('Failed: ' + str(failed_count))

    if failed_paths:
        with open(download_path + '/failed.pickle', 'wb') as handle:
            pickle.dump(failed_paths, handle, protocol=pickle.HIGHEST_PROTOCOL)
        print('\n')
        print('Failed paths saved under: ' + download_path + '/failed.pickle')

