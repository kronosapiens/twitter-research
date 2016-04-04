# -*- coding: utf-8 -*-
'''
Daniel Kronovet
dbk2123@columbia.edu

Code to convert a tweet JSON to a compact CSV.

Use:
    python to_csv.py <flags> <input_file> <output_file>

Example:
    python to_csv.py -l 1 tweets.03.02.2016.json tweets.03.02.2016.csv

Options:
    -h -- print help text
    -l -- pass a level between 1-3 to set the completeness of the parsing.
        There are three levels of parsing. Level 1 is the simplest, keeping
        only the text, screen_name, id_str, and created_at information from
        the tweet. Levels 2 and 3 correspond to the output from R's parseTweet
        function, with 2 corresponding to simplify=TRUE and 3 corresponding to
        simplify=FALSE.

'''

import argparse
import json
import sys

### Command Line Options
parser = argparse.ArgumentParser(
    description='Convert json file to compact CSV')
parser.add_argument('input_file', type=str, help='JSON file to parse')
parser.add_argument('output_file', type=str, nargs='?',
    help='Name of destination .csv file')
parser.add_argument('-l', '--level', type=int, choices=[1,2,3], default=2,
    help='completeness level for parsing')

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

def to_csv(input_file, output_file, level=2):
    keys = base_keys.keys()
    if level not in [1,2,3]:
        raise ValueError('Level must be between 1-3')
    if level >= 2:
        keys.extend(simple_keys.keys())
    if level == 3:
        keys.extend(advanced_keys.keys())

    with open(output_file, 'w') as output_file:
        def write(string):
            output_file.write(string.encode('utf-8'))

        ### Prepare headers
        write('idx')
        for key in keys:
            write(',')
            write(key)

        ### Process file
        with open(input_file, 'r') as input_file:
            idx = 1
            for tweet in input_file:
                tweet_json = json.loads(tweet, encoding='utf8')
                if not tweet_json.get('id_str'):
                    continue # Null tweet
                write('\n')
                write(str(idx))
                idx += 1
                for key in keys:
                    write(',')
                    value = get_value(tweet_json, key_dict[key])

                    if value is None:
                        continue

                    if key == 'place_lat':
                        value = (value[0][1] + value[1][1]) / 2.

                    if key == 'place_lon':
                        value = (value[0][0] + value[2][0]) / 2.

                    value = unicode(value)
                    value = value.replace('\n', ' ')
                    value = value.replace(u',', ' ')
                    value = value.replace(u'"', u"'") # May help avoid error: "EOF within quoted string"
                    write(value)


if __name__ == '__main__':
    args = parser.parse_args()

    if args.output_file is None:
        args.output_file = args.input_file + '.csv'

    to_csv(args.input_file, args.output_file, keys, args.level)








