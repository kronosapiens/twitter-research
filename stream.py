
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

tweets = metadata.tables['tweets']
conn = engine.connect()

# https://github.com/tweepy/tweepy/blob/f76492964869caeda933d559fb51441014396b5f/tweepy/streaming.py#L30
class MyStreamListener(tweepy.StreamListener):
    def to_string(self, status):
        string = u'[{}-{}] {}'.format(
            status.author.screen_name, status.created_at, status.text)
        return string.encode('utf-8')

    def on_status(self, status):
        # print self.to_string(status)
        ins = tweets.insert().values(
            tweet_id=status.id,
            user_id=status.author.id,
            user_location=status.author.location,
            created_at=status.created_at,
            text=status.text
            )
        conn.execute(ins)

    def on_error(self, status):
        logger.error(status)

    def on_exception(self, exception):
        logger.error(exception)

    def on_warning(self, warning):
        logger.warning(warning)

    def on_disconnect(self, notice):
        logger.warning(notice)

    def on_timeout(self):
        logger.warning('TIMEOUT')


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



