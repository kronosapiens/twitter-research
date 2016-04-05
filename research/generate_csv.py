'''
Daniel Kronovet
dbk2123@columbia.edu

One-off script to create summaries / CSV files from raw JSON files.
'''

from datetime import datetime, timedelta
import os
import subprocess
import re

import boto3

import config
from utils import logging
from to_csv import to_csv


FILE_TEMPLATE = 'tweets.{}.json'
CSV_TEMPLATE = 'tweets.{}.csv'
SUMMARY_TEMPLATE = 'tweets.{}.summary.json'
SUMMARY_CSV_TEMPLATE = 'tweets.{}.summary.csv'

def upload_file(file_name, path, bucket):
    full_path = '{}/{}'.format(path, file_name)
    s3.meta.client.upload_file(
        full_path, bucket, file_name, ExtraArgs={'ACL': 'public-read'})

path_root = os.path.dirname(os.path.abspath(__file__))
path = path_root + '/../' + config.DATA_DIR

s3 = boto3.resource('s3')

# matcher = re.compile('tweets[\d.]+json') # Skip summary files
# raw_json_filenames = [
#     obj.key for obj in s3.Bucket(config.JSON_BUCKET).objects.all()
#     if matcher.match(obj.key)
# ]


for obj in s3.Bucket(config.SUMMARY_BUCKET).objects.all():
    file_name = obj.key
    date_to_copy = file_name.split('tweets.')[1].split('.summary.json')[0]

    print 'Downloading', file_name
    s3.Bucket(config.SUMMARY_BUCKET).download_file(file_name, '{}/{}'.format(path, file_name))

    print 'Generating CSV of', file_name, '...'
    csv_name = SUMMARY_CSV_TEMPLATE.format(date_to_copy)
    try:
        to_csv('{}/{}'.format(path, file_name), '{}/{}'.format(path, csv_name), level=3)
        print 'CSV created!'
    except Exception as ex:
        logging.warning(ex)
        print 'CSV creation failed for reason:', ex

    try:
        upload_file(csv_name, path, config.SUMMARY_CSV_BUCKET)
        print 'CSV copied!'
    except OSError as ex:
        logging.warning(ex)
        print 'Copy failed for reason:', ex
    else:
        os.remove('{}/{}'.format(path, csv_name))
        print 'CSV deleted!'


    print 'Deleting {}...'.format(file_name)
    os.remove('{}/{}'.format(path, file_name))
    print 'File deleted!'



