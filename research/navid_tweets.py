'''
Daniel Kronovet
dbk2123@columbia.edu

Code snippets for handling Navid's string escape tweet files.
'''

# To download:
# wget -O file.tar "http://www.ncbi.nlm.nih.gov/geo/download/?acc=GSE46130&format=file"

import json

def clean_tweets(input_file, output_file):
    with open(input_file) as f:
        with open(output_file) as output:
            tweets = f.read().decode('string_escape').split('\n')
            for t in tweets:
                try:
                    tweet = json.loads(t[2:])
                    tweet = json.dumps(tweet)
                    out.write(tweet + '\n')
                except ValueError as ex:
                    print ex

if __name__ == '__main__':
    import sys
    input_file = sys.argv[1]
    output_file = sys.argv[2]
    clean_tweets(input_file, output_file)


