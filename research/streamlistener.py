# -*- coding: utf-8 -*-
'''
https://github.com/tweepy/tweepy/blob/f76492964869caeda933d559fb51441014396b5f/tweepy/streaming.py#L30
'''
import calendar
import decimal
import json
import time

from tweepy import StreamListener
import boto3
from botocore.exceptions import ClientError

import db
from utils import logging

class MyStreamListener(StreamListener):
    def __init__(self, storage=['stdout']):
        if 'nosql' in storage:
            dynamodb = boto3.resource('dynamodb')
            self.tweets = dynamodb.Table('tweets')

        if 'sql' in storage:
            self.conn = db.engine.connect()
            self.tweets = db.metadata.tables['tweets']

        if 'datefile' in storage:
            self.cur_date = time.strftime('%m.%d.%Y')
            self.datefile = self.open_datefile(self.cur_date)

        self.storage = storage
        super(MyStreamListener, self).__init__()

    ##################
    ### EVENT HANDLERS

    def on_data(self, raw_data):
        if 'nosql' in self.storage:
            tweet_dict = self.to_json(raw_data)
            if self.is_tweet(tweet_dict):
                self.to_nosql(tweet_dict)
            else:
                logging.info(tweet_dict)

        if 'datefile' in self.storage:
            self.update_datefile()
            self.datefile.write(raw_data)

        super(MyStreamListener, self).on_data(raw_data)

    def on_status(self, status):
        if 'stdout' in self.storage:
            print self.status_to_string(status)

        if 'sql' in self.storage:
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

    def status_to_string(self, status):
        return self.to_string(
            status.author.screen_name,
            status.created_at,
            status.text
        )

    def to_string(self, screen_name, created_at, text):
        string = u'{} [ {} ] {}'.format(created_at, screen_name, text)
        return string.encode('utf-8')

    def to_json(self, raw_data):
        tweet_dict = json.loads(raw_data, parse_float=decimal.Decimal)
        self.remove_empty_strings(tweet_dict)
        self.add_created_date(tweet_dict)
        return tweet_dict

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
            print self.to_string(
                tweet_dict['user']['screen_name'],
                tweet_dict['created_at'],
                tweet_dict['text'],
            )

        except ClientError as ex:
            print tweet_dict
            raise ex

    #####################
    ### UTILITY FUNCTIONS

    def remove_empty_strings(self, tweet_dict):
        for key in tweet_dict.keys():
            if tweet_dict[key] == '':
                del tweet_dict[key]
            elif isinstance(tweet_dict[key], list):
                for element in tweet_dict[key]:
                    if isinstance(element, dict):
                        self.remove_empty_strings(element)
            elif isinstance(tweet_dict[key], dict):
                self.remove_empty_strings(tweet_dict[key])

    @staticmethod
    def add_created_date(tweet_dict):
        created_at = tweet_dict['created_at'].split()
        created_at = [created_at[i] for i in [1,2,5]]
        created_date = '-'.join(created_at)
        tweet_dict[u'created_date'] = created_date

    @staticmethod
    def add_created_at_unix(tweet_dict):
        created_at = tweet_dict['created_at']
        created_ts = time.strptime(created_at, '%a %b %d %H:%M:%S +0000 %Y')
        tweet_dict[u'created_at_unix'] = calendar.timegm(created_ts)

    def is_tweet(self, tweet_dict):
        return 'id_str' in tweet_dict

    def open_datefile(self, cur_date):
        return open('data/tweets.{}.json'.format(cur_date), 'a')

    def update_datefile(self):
        if self.cur_date != time.strftime('%m.%d.%Y'):
            self.datefile.close()
            self.datefile = self.open_datefile(time.strftime('%m.%d.%Y'))
