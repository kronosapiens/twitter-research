import logging

logging.basicConfig(
    filename='stream.log', format='%(levelname)s:%(asctime)s:%(message)s', level=logging.INFO)

# Note: if level is set to logging.DEBUG, boto3 prints full text of every putItem.