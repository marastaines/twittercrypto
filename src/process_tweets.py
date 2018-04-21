#!usr/bin/python

## Shane Ryan + Mara
"""This is a big old frankensteined disaster that I built off of Shane's code.
    I know its really gross and confusing, its first thing up to fix.
    Just needed it done to get any sort of regression going.

    It uses price_scrape.py as a module
    CHANGE FILE PATH ON LINE 118 to correct tweet file

    Note: (1) Tweet chunking is done so that the whole file isn't stored in RAM.
          (2) The repeated calls to import_tweets_by_block don't start reading from the beginning of the file for each call, they jump to where the last call left off
    These should make this script efficient enough to not destroy your computer even with a massive tweet file"""

import json
import re
from textblob import TextBlob
import datetime as dt
import numpy as np
import price_scrape as ps

## read tweets in from source file in easily accessible object format
class Tweet(object):
    tweet_id = 0
    text = ""
    hashtags = list()
    retweets = 0
    user_id = 0
    time = ""
    sentiment = 0

    def __init__(self, tweet_id, text, hashtags, retweets, user_id, time):
        self.tweet_id = tweet_id
        self.text = text
        self.hashtags = hashtags
        self.retweets = retweets
        self.user_id = user_id
        self.time = time
        self.sentiment = self.get_tweet_sentiment()

    def get_tweet_sentiment(self):
        analysis = TextBlob(self.text)
        # sentiment
        """if analysis.sentiment.polarity > 0.5:
            return analysis.sentiment.polarity
        elif analysis.sentiment.polarity < -0.5:
            return analysis.sentiment.polarity
        else:
            return 0"""
        return analysis.sentiment.polarity


def process_tweet(raw_tweet):
    clean_text = ' '.join(re.sub("""(@[A-Za-z0-9]+)|([^0-9A-Za-z \t]) \\
        |(\w+:\/\/\S+)""", " ", raw_tweet['text']).split())
    tweet = Tweet(raw_tweet['id'], clean_text, raw_tweet['hashtags'],
            raw_tweet['retweets'], raw_tweet['user_id'], raw_tweet['time'])
    return tweet

def import_tweets(filename):
    raw_tweets = list()
    prob_string = "}{\"id\""
    with open(filename) as source:
        for line in source:
            prob = line.find(prob_string)
            if prob != -1:
                line1 = line[:prob + 1]
                line2 = line[prob + 1:]
                raw_tweets.append(json.loads(line1))
                raw_tweets.append(json.loads(line2))
            else:
                raw_tweets.append(json.loads(line))

    return raw_tweets
def import_tweets_by_block(filename, s, e, start_loc):

    raw_tweets = list()
    end_loc = 0
    with open(filename) as source:
        source.seek(start_loc)
        prob_string = "}{\"id\""
        curr_tweets = []
        inrange = 1
        line = source.readline()
        print(line)
        while(line and inrange):
            prob = line.find(prob_string)
            if prob != -1:
                line1 = line[:prob + 1]
                line2 = line[prob + 1:]
                curr_tweets.append(line1)
                curr_tweets.append(line2)
            else:
                curr_tweets.append(line)
            for l in curr_tweets:
                line_d = json.loads(l)
                line_t = dt.datetime.strptime(line_d["time"], "%Y-%m-%d %H:%M:%S")
                if line_t >= s:
                    if line_t <= e:
                        raw_tweets.append(line_d)
                    else:
                        inrange = 0
            curr_tweets = []
            line = source.readline()
        end_loc = source.tell()
    return raw_tweets, end_loc

delta = dt.timedelta(seconds = 3600)
start = dt.datetime(2018, 4, 6, hour=0, minute=0, second=0)
end = start + delta
end_final = dt.datetime(2018, 4, 7, hour=0, minute=0, second=0)
start_loc = 0

out = open("instances.txt", "w+")
while end_final >= end:
    print(str(end))
    print(end.timestamp())
    raw_tweets, start_loc = import_tweets_by_block("/home/mara/Documents/2018sp/ml/appa.out.txt", start, end, start_loc)
    start = end
    end += delta
    #raw_tweets = import_tweets_by_block("mini.txt", "2018-03-28 17:22:08", "2018-03-28 17:22:10")

    tweet_data = []
    for tweet in raw_tweets:
        tweet_data.append(process_tweet(tweet))

    sentiment_block_score = 0
    retweet_block_score = 0
    sentiment_sd = 0
    sent = []
    for n, tweet in enumerate(tweet_data):
        sentiment_block_score += tweet.sentiment
        sent.append(tweet.sentiment)
        retweet_block_score += tweet.retweets
        """print("Tweet %d\n\nContent:\n%s\n\nSentiment:\t%d\n\nTime:\t%s\n\n"
                % (n+1, tweet.text, tweet.sentiment, tweet.time))"""
    if len(tweet_data) != 0:
        sentiment_block_score /= len(tweet_data)
        sent = np.array(sent)
        sentiment_sd = np.std(sent)
        retweet_block_score /= len(tweet_data)
    price = ps.get_historical("BTC", end.timestamp())
    out.write(str(start) + "," + str(end) + "," + str(len(tweet_data)) + "," +str(sentiment_block_score) + "," + str(sentiment_sd) + "," + str(retweet_block_score) + "," + str(price) + "\n")
out.close()

