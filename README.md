
# Visualizations

## Keyword Count Bar Chart

You can generate a bar chart of keyword counts as follows:

```
$ python research/wordcount_visualizer 'keyword1 keyword2 keyword3' data_file(optional)
```

This command will parse the given `data_file` (by default, will use `data/tweets.txt`), tokenize the text of the tweets, and generate an html bar chart of the given keywords.

A copy of `tweets.txt` (containing ~100,000 tweets) can be downloaded [here](https://console.aws.amazon.com/s3/home?region=us-east-1&bucket=primary-tweets) (requires access to the AWS console)

**Example**

```
$ python research/wordcount_visualizer.py 'hillary bernie cruz trump'
```

Generates [this chart](https://rawgit.com/kronosapiens/twitter_research/master/bar.html).


# Command reference

## Managing the stream

To start/restart the tweet collecting process using Upstart (recommended):
```
sudo service stream restart
```

Alternative manual restart code (use only if previous command fails):
```
cd ~/twitter_research
nohup python research/stream.py nosql &
```

To check if the tweet collecting process is running:
```
sudo service stream status

# alternatively

ps -aux | grep research/stream.py
```

## Additional commands

To configure a new instance with the necessary Ubuntu packages:
```
sudo apt-get install libpq-dev python-dev lib32ncurses5-dev python-psycopg2
```

To connect to a remote PostgreSQL database:
```
psql -h <db url> -p 5432 -U <username> -d <db name>
```

To connect to the current EC2 instance (must have the .pem file):
```
ssh -i QMSS_TP.pem ubuntu@ec2-54-172-89-178.compute-1.amazonaws.com
```


# Logs and Output

Output from the stream process will go to several locations, depending on the type of output.

For regular log messages, check `stream.log`.

For tweet output (not main storage, just a sanity check that tweets are coming in), check `tweets.txt` or `nohup.out`.

For Upstart logs, check `/var/log/upstart/stream.log` (you will probably need `sudo`).

When looking at these files, the following commands may be helfpul:

```
# Prints the last 10 lines of the file
tail <log file>

# Will continually output new additions to the file
tail -f <log file>

# Outputs the entire file (can be large)
cat <log file>
```


# tweepy

Tweepy is the third-party package we are using to interact with the Twitter api.

Docs: http://tweepy.readthedocs.org/en/v3.5.0/getting_started.html

# Queries

https://dev.twitter.com/streaming/overview/request-parameters

## Tracking
```
track=["Hillary Clinton", "Bernie Sanders", "Ted Cruz", "Donald Trump"]
```

## Following
```
follow=[]
```

# Resources

https://dev.twitter.com/streaming/reference/post/statuses/filter
http://tweepy.readthedocs.org/en/v3.5.0/streaming_how_to.html#summary
http://adilmoujahid.com/posts/2014/07/twitter-analytics/


# Back-of-the-envelope calculations
```
Sample Tweet: tweet.json

2-4kb / tweet JSON
500m tweets / day (unfiltered)
1b - 2b kb / day (unfiltered)

1 byte = 256 (2**8) bits
1 kb = 1,024 (2**10) bytes [2**18 1024 * 256 = 262,144 bits]
1 mb = 1,048,576 (2**20) bytes [2**28 = 268,435,456 bits]
1 gb = 1,073,741,824 (2**30) bytes [2**38 = 274,877,906,944 bits]
1 tb = 1,099,511,627,776 (2**40) bytes [2**48 = 281,474,976,710,656 bits]

1m = 1,000,000 (10**6)
1b = 1,000,000,000 (10**9)

So:
1b kb = 10**9 * 2**10
      = 10**9 * 2**10
      < 2**30 * 2**10
      = 2**40 bytes
      = 2**48 bits
      = 1tb

** 500m tweets are 1tb-2tb

How many tweets in a gb?
2-4kb / tweet JSON

so between (2**20)/2 and (2**20)/4
           2**19 and 2***18 tweets

2**18 = 262,144
2**19 = 524,288

So:
Conservatively, 250k tweets/gb

We would like to collect less than (t) tb of data
(restriction would make the data easier to handle
    and would also require us to find good filters.)

Collection period is Feb 1 - July 28, ~6mo
Feb 1: Iowa Caucus
July 28: End of Democratic National Convention
6mo ~= 30*6 = 180 days

180 days * 1tb / day = 180 tb of unfiltered twitter data

To limit ourselves to (t) tb, we need to filter down to (t * 1024) / 180 gb / day.

t = 4
1024 * 4 = 4096
4096 / 180 = 22.76gb/day

At 250k tweets/gb, we can capture 5,690,000 tweets/day
Or approx 1 percent tweets.

Over 180 days, this gives 1,024,200,000 tweets.
```

Function to return tweet limit based on constraints:

```
def tweets_per_day(storage, days=180):
    return round(float(storage) / days), 2) * 250000
```