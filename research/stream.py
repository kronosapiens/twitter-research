'''
Daniel Kronovet
dbk2123@columbia.edu

Code to consume tweets from the Twitter Streaming API.
'''
import tweepy

import config
import keywords
from utils import logging

from streamlistener import MyStreamListener

auth = tweepy.OAuthHandler(config.consumer_key, config.consumer_secret)
auth.set_access_token(config.access_token, config.access_token_secret)

api = tweepy.API(auth)

if __name__ == '__main__':
    import sys

    storage = sys.argv[1]

    logging.info('#' * 32 + 'NEW RUN')
    myStream = tweepy.Stream(auth=auth, listener=MyStreamListener(storage))
    myStream.filter(
        follow=keywords.users,
        track=keywords.keywords,
        stall_warnings=True
        )