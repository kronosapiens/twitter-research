'''
Daniel Kronovet
dbk2123@columbia.edu

Code to consume tweets from the Twitter Streaming API.
'''
import tweepy

import config
from config import logging
import keywords

from streamlistener import MyStreamListener

auth = tweepy.OAuthHandler(config.consumer_key, config.consumer_secret)
auth.set_access_token(config.access_token, config.access_token_secret)

# api = tweepy.API(auth)

logging.info('#' * 50 + 'NEW RUN')
myStream = tweepy.Stream(auth=auth, listener=MyStreamListener())
myStream.filter(follow=keywords.users, track=keywords.keywords, stall_warnings=True)