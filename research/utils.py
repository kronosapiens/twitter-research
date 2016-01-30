import logging

import boto3

FMT = '[%(name)s:%(levelname)s]:%(asctime)s:%(message)s'

logging.basicConfig(
    filename='stream.log', format=FMT, level=logging.INFO)

boto3.set_stream_logger(name='boto3', level=logging.WARNING, format_string=FMT)

# Note: if level is set to logging.DEBUG, boto3 prints full text of every putItem.