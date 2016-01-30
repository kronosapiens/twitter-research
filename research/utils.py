import logging

import boto3

FMT = '[%(levelname)s:%(name)s]:(%(asctime)s):%(message)s'
FMT = '%(asctime)s [%(levelname)s] %(name)s : %(message)s'

logging.basicConfig(
    filename='stream.log', format=FMT, level=logging.INFO)

boto3.set_stream_logger(name='boto3', level=logging.WARNING, format_string=FMT)

# Note: if level is set to logging.DEBUG, boto3 prints full text of every putItem.