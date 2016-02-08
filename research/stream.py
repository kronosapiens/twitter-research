'''
Daniel Kronovet
dbk2123@columbia.edu

Code to consume tweets from the Twitter Streaming API.
'''
import argparse

import tweepy

import secrets
import keywords
from utils import logging
from streamlistener import MyStreamListener

### Command Line Options
parser = argparse.ArgumentParser(description='Open connection to Twitter Stream')
parser.add_argument('storage', nargs='*', default=['stdout'])

auth = tweepy.OAuthHandler(secrets.consumer_key, secrets.consumer_secret)
auth.set_access_token(secrets.access_token, secrets.access_token_secret)

api = tweepy.API(auth)

if __name__ == '__main__':
    logging.info('NEW RUN ' * 8)
    args = parser.parse_args()

    myStream = tweepy.Stream(auth=auth, listener=MyStreamListener(args.storage))
    myStream.filter(
        follow=keywords.users,
        track=keywords.keywords,
        stall_warnings=True
        )