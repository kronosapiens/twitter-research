'''
Daniel Kronovet
dbk2123@columbia.edu

Code to filter out tweet JSON which do not contain location or lat/long coords.

Use:
    python filter_locations.py <file_name> <flags>

Flags:
    -l -- will include tweets with user locations
    -c -- will include tweets with lat/long coordinates
    -p -- will include tweets with place attribute

The script will print the output to the screen. This output can be written
to a file of your choice by adding "> <destination>" to the command.
'''

import argparse
import json
import sys

COORDS = 'coordinates'
LOC = 'location'
PLACE = 'place'
USR = 'user'

### Command Line Options
parser = argparse.ArgumentParser(description='Filter tweets to find those with location data')
parser.add_argument('file', type=str)
parser.add_argument('-c', '--coordinates', dest='coordinates', action='store_true', default=False)
parser.add_argument('-l', '--location', dest='location', action='store_true', default=False)
parser.add_argument('-p', '--place', dest='place', action='store_true', default=False)
args = parser.parse_args()

### Filter file
with open(args.file, 'r') as f:
    for tweet in f:
        tweet_json = json.loads(tweet)
        if not tweet_json.get('id_str'):
            continue # Null tweet
        if args.coordinates and tweet_json.get(COORDS) is None:
            pass
        elif args.location and tweet_json.get(USR, {}).get(LOC) is None:
            pass
        elif args.place and tweet_json.get(PLACE) is None:
            pass
        else:
            sys.stdout.write(tweet)