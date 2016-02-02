'''
Daniel Kronovet
dbk2123@columbia.edu

Visualize wordcounts for election tweets.

Command line interface:
$ python research/wordcount_visualizer 'keyword1 keyword2 keyword3' source_file(optional)
'''

from collections import Counter

from bokeh.charts import Bar, output_file, show
import nltk
import pandas as pd


def read_tweets(file_path):
    with open(file_path, 'r') as f:
        return [tweet.strip().split(' ] ')[-1].lower() for tweet in f]

def count_words(tweets):
    counter = Counter()
    for tweet in tweets:
        try:
            tokens = nltk.word_tokenize(tweet)
            counter.update(tokens)
        except UnicodeDecodeError as ex:
            print ex, tweet
    return counter

def filter_counter(counter, keywords):
    return {kw: counter[kw] for kw in keywords}

def make_bar(counter, keywords, output_filename):
    data = pd.Series(filter_counter(counter, keywords))
    bar = Bar(data, title='Word Counts')
    output_file(output_filename)
    bar.show()


if __name__ == '__main__':
    import sys

    keywords = sys.argv[1].split()
    data_file = sys.argv[2] if len(sys.argv) > 2 else 'data/tweets.txt'

    tweets = read_tweets(data_file)
    counts = count_words(tweets)
    make_bar(counts, keywords, 'bar.html')