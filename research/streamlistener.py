# -*- coding: utf-8 -*-
'''
https://github.com/tweepy/tweepy/blob/f76492964869caeda933d559fb51441014396b5f/tweepy/streaming.py#L30
'''
import json
import decimal

from tweepy import StreamListener
import boto3
from botocore.exceptions import ClientError

import db
from utils import logging

class MyStreamListener(StreamListener):
    def __init__(self, storage='stdout'):
        if storage == 'nosql':
            dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
            self.tweets = dynamodb.Table('tweets')
        elif storage == 'sql':
            self.conn = db.engine.connect()
            self.tweets = db.metadata.tables['tweets']
        elif storage == 'stdout':
            pass
        else:
            raise ValueError('Must specify storage (sql, nosql, stdout)')

        self.storage = storage
        super(MyStreamListener, self).__init__()

    ##################
    ### EVENT HANDLERS

    def on_data(self, raw_data):
        if self.storage == 'nosql':
            tweet_dict = self.to_json(raw_data)
            self.to_nosql(tweet_dict)
        super(MyStreamListener, self).on_data(raw_data)

    def on_status(self, status):
        if self.storage == 'stdout':
            print self.to_string(status)
        elif self.storage == 'sql':
            try:
                self.to_sql(status)
            except db.DataError as ex:
                logging.error(ex)
                raise ex

    def on_error(self, status):
        logging.error(status)

    def on_exception(self, exception):
        logging.error(exception)

    def on_warning(self, warning):
        logging.warning(warning)

    def on_disconnect(self, notice):
        logging.warning(notice)

    def on_timeout(self):
        logging.warning('TIMEOUT')

    ####################
    ### OUTPUT FUNCTIONS

    def to_string(self, status):
        string = u'[{}-{}] {}'.format(
            status.author.screen_name, status.created_at, status.text)
        return string.encode('utf-8')

    def to_json(self, raw_data):
        tweet_json = json.loads(raw_data, parse_float=decimal.Decimal)

        sub_tweets = [
            tweet_json,
            tweet_json.get('retweeted_status', {}),
            tweet_json.get('retweeted_status', {}).get('quoted_status', {}),
            tweet_json.get('quoted_status', {}),
            tweet_json.get('quoted_status', {}).get('retweeted_status', {}),
        ]

        sub_tweets = [st for st in sub_tweets if st] # Skip empty dicts

        keys = [
            'profile_background_image_url',
            'profile_background_image_url_https'
        ]

        for sub_tweet in sub_tweets:
            for key in keys:
                if sub_tweet.get('user', {}).get(key, None) == '':
                    del sub_tweet['user'][key]

        return tweet_json

    def to_sql(self, status):
        ins = self.tweets.insert().values(
            tweet_id=status.id,
            user_id=status.author.id,
            user_location=status.author.location,
            created_at=status.created_at,
            text=status.text
            )
        self.conn.execute(ins)

    def to_nosql(self, tweet_dict):
        try:
            self.tweets.put_item(Item=tweet_dict)
            print tweet_dict['text']
        except ClientError as ex:
            print tweet_dict
            raise ex
            # print ex
            # logging.error(ex)
