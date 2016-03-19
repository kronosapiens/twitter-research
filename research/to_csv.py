'''
Daniel Kronovet
dbk2123@columbia.edu

Code to convert a tweet JSON to a compact CSV.

Use:
    python to_csv.py <file_name> <flags>

Flags:
    -t -- will include text
    -c -- will include created_at
    -u -- will include user_name

The script will print the output to the screen. This output can be written
to a file of your choice by adding "> <destination>" to the command.
'''

import argparse
import json
import sys

### Command Line Options
parser = argparse.ArgumentParser(description='Filter tweets to find those with location data')
parser.add_argument('file', type=str)
parser.add_argument('-t', '--text', dest='text', action='store_true', default=False)
parser.add_argument('-c', '--created_at', dest='created_at', action='store_true', default=False)
parser.add_argument('-u', '--user_name', dest='user_name', action='store_true', default=False)
# parser.add_argument('-m', '--mention', dest='mention', action='store_true', default=False)
# parser.add_argument('-r', '--retweet', dest='retweet', action='store_true', default=False)
# parser.add_argument('-p', '--reply', dest='reply', action='store_true', default=False)
args = parser.parse_args()

def write(string):
    sys.stdout.write(string)

### Filter file
write('ID')
if args.text:
    write(',')
    write('TEXT')
if args.created_at:
    write(',')
    write('CREATED_AT')
if args.user_name:
    write(',')
    write('USER_NAME')
sys.stdout.write('\n')

with open(args.file, 'r') as f:
    for tweet in f:
        tweet_json = json.loads(tweet)
        if not tweet_json.get('id_str'):
            continue
        write(tweet_json.get('id_str', ''))
        if args.text:
            write(',')
            write(repr(tweet_json.get('text', '').replace(',', ' ').encode('utf-8')))
        if args.created_at:
            write(',')
            write(tweet_json.get('created_at', ''))
        if args.user_name:
            write(',')
            write(tweet_json.get('user', {}).get('name', '').encode('utf-8'))
        sys.stdout.write('\n')