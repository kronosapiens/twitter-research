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



# Command reference

```
sudo apt-get install libpq-dev python-dev lib32ncurses5-dev python-psycopg2
```

```
psql -h <db url> -p 5432 -U <username> -d <db name>
```

```
ssh -i QMSS_TP.pem ubuntu@ec2-54-172-89-178.compute-1.amazonaws.com
```