# -*- coding: utf-8 -*-
'''
https://github.com/tweepy/tweepy/blob/f76492964869caeda933d559fb51441014396b5f/tweepy/streaming.py#L30
'''

from tweepy import StreamListener

from db import engine, metadata

tweets = metadata.tables['tweets']
conn = engine.connect()


class MyStreamListener(StreamListener):
    count = 0

    def to_string(self, status):
        string = u'[{}-{}] {}'.format(
            status.author.screen_name, status.created_at, status.text)
        return string.encode('utf-8')

    # def on_data(self, raw_data):
    #     print raw_data

    def on_status(self, status):
        print self.to_string(status)
        ins = tweets.insert().values(
            tweet_id=status.id,
            user_id=status.author.id,
            user_location=status.author.location,
            created_at=status.created_at,
            text=status.text
            )
        conn.execute(ins)

        self.count += 1
        if self.count % 100 == 0:
            print 'Saved {} tweets'.format(self.count)

    # def on_error(self, status):
    #     logging.error(status)

    # def on_exception(self, exception):
    #     logging.error(exception)

    # def on_warning(self, warning):
    #     logging.warning(warning)

    # def on_disconnect(self, notice):
    #     logging.warning(notice)

    # def on_timeout(self):
    #     logging.warning('TIMEOUT')