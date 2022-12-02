import re
import os
import glob
import time

from urllib.parse import urljoin
from urllib.parse import urlparse

from pyspark import SparkConf, SparkContext

from warcio.archiveiterator import ArchiveIterator


def extractor(f):
    #https://hpcf.umbc.edu/general-productivity/checking-which-cpus-are-used-by-your-program/
    command = "echo $(cat /proc/self/stat) | awk '{print $39}'"
    def new_f(warc_files):
        cpu_id = os.popen(command).read().strip()
        for index, warc_file in enumerate(warc_files):
            print(f"Processing ==> {index+1}/{partition_len} : cpu_id {cpu_id}")
            with open(warc_file, 'rb') as stream:
                for record in ArchiveIterator(stream):
                    yield from f(record)
           
            if os.path.isfile(warc_file):
                try:
                    os.remove(warc_file)
                except:
                    pass

    return new_f

@extractor
def extract_sitemaps_url(record):
    global robotstxt_processed_acc
    global robotstxt_invalid_encoding_acc
    global robotstxt_empty_acc
    global robotstxt_with_invalid_url_acc
    global robotstxt_announcing_a_sitemap_acc
    global robotstxt_with_more_than_50_sitemaps_acc
    global sitemap_urls_found_acc

    if record.rec_type == 'response':
        robotstxt_processed_acc += 1
        try:
            lines = record.raw_stream.read().decode('utf-8', 'strict').splitlines()
        except UnicodeDecodeError:
            robotstxt_invalid_encoding_acc += 1
            return

        if not lines:
            robotstxt_empty_acc += 1
            return

        url = None
        n_sitemaps = 0
        for line in lines:
            match = sitemap_pattern.match(line)
            if match:
                if not url:
                    url = record.rec_headers.get_header('WARC-Target-URI')
                    try:
                        host = urlparse(url).netloc.lower().lstrip('.')
                    except Exception as e:
                        robotstxt_with_invalid_url_acc +=1
                        return

                sitemap_urls_found_acc += 1
                n_sitemaps += 1

                sitemap_url = match.group(1).strip().lower()
                if not sitemap_url.startswith('http'):
                    sitemap_url = urljoin(url, sitemap_url)
                
                yield sitemap_url, [host]

        if n_sitemaps > 0:
            robotstxt_announcing_a_sitemap_acc += 1
        if n_sitemaps > 50:
            robotstxt_with_more_than_50_sitemaps_acc += 1

def reducer(x):
    global invalid_sitemap_urls_found_acc
    global cross_submit_hosts_found_acc

    try:
        sitemap_uri = urlparse(x[0])
    except Exception as e:
        invalid_sitemap_urls_found_acc += 1
        return
    
    sitemap_host = sitemap_uri.netloc.lower().lstrip('.')
    cross_submit_hosts = set()

    for robotstxt_hosts in x[1]:
        for robotstxt_host in robotstxt_hosts:
            if robotstxt_host != sitemap_host:
                cross_submit_hosts.add(robotstxt_host)
    
    cross_submit_hosts_found_acc += len(cross_submit_hosts)

    return x[0], list(cross_submit_hosts)

if __name__ == '__main__':

    cpu_to_be_used = 32

    conf = SparkConf().setAppName('sitemapExtractor').setMaster(f'local[{cpu_to_be_used}]').set("spark.eventLog.enabled", True)\
        .set("spark.eventLog.dir", "/root/logs/spark-events")
    sc = SparkContext(conf=conf)

    codec = "org.apache.hadoop.io.compress.GzipCodec"

    #use regex in main and not in extractor func, as we are running locally, so no need for regex to be inside function
    #and that makes it faster as it is compiled just once
    sitemap_pattern = re.compile(r'^site-?map:\s*(\S+)', re.I)

    robotstxt_processed_acc = sc.accumulator(0)
    robotstxt_invalid_encoding_acc = sc.accumulator(0)
    robotstxt_empty_acc = sc.accumulator(0)
    robotstxt_with_invalid_url_acc = sc.accumulator(0)
    robotstxt_announcing_a_sitemap_acc = sc.accumulator(0)
    robotstxt_with_more_than_50_sitemaps_acc = sc.accumulator(0)
    sitemap_urls_found_acc = sc.accumulator(0)
    invalid_sitemap_urls_found_acc = sc.accumulator(0)
    cross_submit_hosts_found_acc = sc.accumulator(0)

    files = glob.glob("/root/commoncrawl/crawl-data/CC-MAIN-2021-43/**/*.gz", recursive=True)

    
    partition_len = len(files) // cpu_to_be_used

    start_time = time.time()

    rddData = sc.parallelize(files, cpu_to_be_used)
    mapped = rddData.mapPartitions(extract_sitemaps_url)
    reduced = mapped.groupByKey().map(reducer)

    reduced.saveAsTextFile('/root/commoncrawl/data/output-data/sitemap_extractor', codec)
    
    end_time = time.time()

    print('\n')
    print('-'*40)
    print("robotstxt_processed: " + str(robotstxt_processed_acc.value))
    print("robotstxt_invalid_encoding: " + str(robotstxt_invalid_encoding_acc.value))
    print("robotstxt_empty: " + str(robotstxt_empty_acc.value))
    print("robotstxt_with_invalid_url: " + str(robotstxt_with_invalid_url_acc.value))
    print("robotstxt_announcing_a_sitemap: " + str(robotstxt_announcing_a_sitemap_acc.value))
    print("robotstxt_with_more_than_50_sitemaps: " + str(robotstxt_with_more_than_50_sitemaps_acc.value))
    print("sitemap_urls_found: " + str(sitemap_urls_found_acc.value))
    print("invalid_sitemap_urls_found: " + str(invalid_sitemap_urls_found_acc.value))
    print("cross_submit_hosts_found: " + str(cross_submit_hosts_found_acc.value))
    
    print("\n")
    print("Duration: " + str(end_time - start_time))
    sc.stop()

