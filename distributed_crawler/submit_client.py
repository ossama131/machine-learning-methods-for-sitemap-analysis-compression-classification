from celery import group
from tqdm import tqdm
import glob
import sys

from proj.tasks import crawl

files = glob.glob('/home/smida/to_be_crawled/*')
urls = []
print(f'Reading {len(files)} files...')
for file in tqdm(files):
    with open(file, 'r') as f:
        l = f.read().split('\n')[:-1]
        urls.extend(l)

size_b = sys.getsizeof(urls)
size_m = size_b / (1024*1024)
print(f'{len(urls)} URLs loaded!')
print('URLs size:')
print('\t+Bytes: ', size_b)
print('\t+Mb: ', size_m)

t = group(crawl.s(url, 1) for url in tqdm(urls))
t.apply_async()