'''
Daniel Kronovet
dbk2123@columbia.edu

Code to convert a tweet JSON to a compact CSV.

Use:
    python to_csv.py <file_name> <flags>

Options:
    -l -- pass a level between 1-3 to set the completeness of the parsing.
        There are three levels of parsing. Level 1 is the simplest, keeping
        only the text, screen_name, id_str, and created_at information from
        the tweet. Levels 2 and 3 correspond to the output from R's parseTweet
        function, with 2 corresponding to simplify=TRUE and 3 corresponding to
        simplify=FALSE.

The parser will print the output to the screen. This output can be written
to a file of your choice by adding "> <destination>" to the command.
'''

import argparse
import json
import sys

### Command Line Options
parser = argparse.ArgumentParser(description='Filter tweets to find those with location data')
parser.add_argument('file', type=str)
parser.add_argument('-l', '--level', type=int, choices=[1,2,3], default=2)
args = parser.parse_args()

base_keys = {
    'text': 'text',
    'created_at': 'created_at',
    'screen_name': ('user', 'screen_name'),
}

simple_keys = {
    'id_str': 'id_str',
    'retweet_count': 'retweet_count',
    'favorite_count': 'favorite_count',
    'favorited': 'favorited',
    'truncated': 'truncated',
    'in_reply_to_screen_name': 'in_reply_to_screen_name',
    'source': 'source',
    'retweeted': 'retweeted',
    'in_reply_to_status_id_str': 'in_reply_to_status_id_str',
    'in_reply_to_user_id_str': 'in_reply_to_user_id_str',
    'lang': 'lang',
    'listed_count': ('user', 'listed_count'),
    'verified': ('user', 'verified'),
    'location': ('user', 'location'),
    'user_id_str': ('user', 'id_str'),
    'description': ('user', 'description'),
    'geo_enabled': ('user', 'geo_enabled'),
    'user_created_at': ('user', 'created_at'),
    'statuses_count': ('user', 'statuses_count'),
    'followers_count': ('user', 'followers_count'),
    'favourites_count': ('user', 'favourites_count'),
    'protected': ('user', 'protected'),
    'user_url': ('user', 'url'),
    'name': ('user', 'name'),
    'time_zone': ('user', 'time_zone'),
    'user_lang': ('user', 'lang'),
    'utc_offset': ('user', 'utc_offset'),
    'friends_count': ('user', 'friends_count'),
}

advanced_keys = {
    'country_code': ('place', 'country_code'),
    'country': ('place', 'country'),
    'place_type': ('place', 'place_type'),
    'full_name': ('place', 'full_name'),
    'place_name': ('place', 'name'),
    'place_id': ('place', 'id'),
    'place_lat':('place', 'bounding_box', 'coordinates', 0),
    'place_lon':('place', 'bounding_box', 'coordinates', 0),
    'lat': ('geo', 'coordinates', 0),
    'lon': ('geo', 'coordinates', 1),
    'expanded_url': ('entities', 'urls', 0, 'expanded_url'),
    'url': ('entities', 'urls', 0, 'url'),
}

key_dict = {}
key_dict.update(base_keys)
key_dict.update(simple_keys)
key_dict.update(advanced_keys)

keys = base_keys.keys()
if args.level not in [1,2,3]:
    raise ValueError('Level must be between 1-3')
if args.level >= 2:
    keys.extend(simple_keys.keys())
if args.level == 3:
    keys.extend(advanced_keys.keys())

def write(value):
    if value is None:
        pass
    elif isinstance(value, basestring):
        sys.stdout.write(value)
    else:
        sys.stdout.write(repr(value))

def get_value(tweet_json, key_tuple):
    result = tweet_json
    key_tuple = key_tuple if isinstance(key_tuple, tuple) else (key_tuple,)
    for key in key_tuple:
        if isinstance(key, str) and isinstance(result, dict):
            result = result.get(key)
        elif isinstance(key, int) and isinstance(result, list) and len(result) > key:
            result = result[key]
        else:
            return
    return result

### Prepare headers
write('idx')
for key in keys:
    write(',')
    write(key)
write('\n')

### Process file
with open(args.file, 'r') as f:
    idx = 1
    for tweet in f:
        tweet_json = json.loads(tweet)
        if not tweet_json.get('id_str'):
            continue # Null tweet
        write(idx)
        idx += 1
        for key in keys:
            write(',')
            if key in ['place_lat', 'place_lon']:
                coords = get_value(tweet_json, key_dict[key])
                if coords and key == 'place_lat':
                    value = (coords[0][1] + coords[1][1]) / 2.
                elif coords and key == 'place_lon':
                    value = (coords[0][0] + coords[2][0]) / 2.
                write(value)
            else:
                value = get_value(tweet_json, key_dict[key])
                if isinstance(value, basestring):
                    value = value.replace(',', ' ').encode('utf-8')
                    if key in ['text', 'screen_name', 'description', 'location']:
                        value = repr(value) # Escape newlines in the raw data
                write(value)
        write('\n')











