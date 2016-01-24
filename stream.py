'''
Daniel Kronovet
dbk2123@columbia.edu

Code to consume tweets from the Twitter Streaming API.
'''

import tweepy

from config import consumer_key, consumer_secret
from config import access_token, access_token_secret

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)


class MyStreamListener(tweepy.StreamListener):

    def on_status(self, status):
        print(status.text)


api = tweepy.API(auth)

myStreamListener = MyStreamListener()
myStream = tweepy.Stream(auth = api.auth, listener=myStreamListener)
myStream.filter(track=['primaries'])