'''
Daniel Kronovet
dbk2123@columbia.edu

Module to parse tweets to aid in analysis.
'''
import argparse
import json

### Command Line Options
parser = argparse.ArgumentParser(description='Parse tweets to aid in analysis.')
parser.add_argument('tweet_file', help='Path to the tweet file to parse')
parser.add_argument('-p', '--profile', dest='remove_profile', action='store_true',
    default=False, help='Remove profile display data from the tweet.')
parser.add_argument('-f', '--flatten', dest='flatten', action='store_true',
    default=False, help='Flatten tweet and remove nesting of objects.')


def parse_tweet(tweet, remove_profile=False, flatten=False):
    for key in tweet:
        if is_tweet(tweet[key]):
            parse_tweet(tweet[key], remove_profile, flatten)

    if remove_profile:
        user_dict = tweet.get('user')
        for key in user_dict.keys():
            if 'profile_' in key:
                del user_dict[key]

    if flatten:
        user_dict = tweet.get('user')
        for key in user_dict:
            new_key = 'user_{}'.format(key)
            tweet[new_key] = user_dict[key]
        del tweet['user']

        entities_dict = tweet.get('entities')
        for _type in entities_dict:
            for i, entity in enumerate(entities_dict[_type]):
                for key in entity:
                    new_key = 'entities_{}_{}_{}'.format(_type, i, key)
                    tweet[new_key] = entity[key]
        del tweet['entities']

def is_tweet(tweet):
    return isinstance(tweet, dict) and ('text' in tweet)


if __name__ == '__main__':
    args = parser.parse_args()

    with open(args.tweet_file, 'r') as tweets:
        for tweet in tweets:
            tweet = json.loads(tweet)
            parse_tweet(tweet, args.remove_profile, args.flatten)
            # print tweet
            print json.dumps(tweet)
