'''
Daniel Kronovet
dbk2123@columbia.edu

Code to copy tweet JSON to AWS S3

Configure as a cron job to run nightly:

To run daily at 1am, run `crontab -e` and add the following line:
0 1 * * * python ~/twitter_research/research/copy_to_s3.py 1 >> ~/twitter_research/cron.log
'''

import sys
from datetime import datetime, timedelta

import boto3

import config
from utils import logging

offset = int(sys.argv[1]) if len(sys.argv) >= 2 else 1
date_to_copy = (datetime.today() - timedelta(days=offset)).strftime('%m.%d.%Y')

print 'Copying tweets from', date_to_copy, '...'

file_name = 'tweets.{}.json'.format(date_to_copy)

s3 = boto3.resource('s3')

try:
    s3.meta.client.upload_file(config.DATA_DIR + file_name, config.S3_BUCKET, file_name)
    print 'Tweets copied!'
except OSError as ex:
    logging.warning(ex)
    print 'Copy failed for reason:', ex
