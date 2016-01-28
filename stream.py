
# -*- coding: utf-8 -*-

'''
Daniel Kronovet
dbk2123@columbia.edu

Code to consume tweets from the Twitter Streaming API.
'''
import logging

import tweepy

from config import consumer_key, consumer_secret
from config import access_token, access_token_secret
from db import engine, metadata

logging.basicConfig(
    filename='stream.log', format='%(levelname)s:%(asctime)s:%(message)s', level=logging.DEBUG)
logging.info('#' * 50 + 'NEW RUN')

tweets = metadata.tables['tweets']
conn = engine.connect()

# https://github.com/tweepy/tweepy/blob/f76492964869caeda933d559fb51441014396b5f/tweepy/streaming.py#L30
class MyStreamListener(tweepy.StreamListener):
    count = 0

    def on_data(self, raw_data):
        print raw_data

    def to_string(self, status):
        string = u'[{}-{}] {}'.format(
            status.author.screen_name, status.created_at, status.text)
        return string.encode('utf-8')

    def on_status(self, status):
        pass
        # print self.to_string(status)
        # ins = tweets.insert().values(
        #     tweet_id=status.id,
        #     user_id=status.author.id,
        #     user_location=status.author.location,
        #     created_at=status.created_at,
        #     text=status.text
        #     )
        # conn.execute(ins)

        self.count += 1
        if self.count % 100 == 0:
            print 'Saved {} tweets'.format(self.count)

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


auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

myStreamListener = MyStreamListener()
myStream = tweepy.Stream(auth=api.auth, listener=myStreamListener)
myStream.filter(
    follow=[], # User ids
    track=["Hillary Clinton", "Bernie Sanders", "Ted Cruz", "Donald Trump"],
    stall_warnings=True,
    )
