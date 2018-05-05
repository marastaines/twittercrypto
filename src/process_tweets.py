#!usr/bin/python

## Shane Ryan + Mara
"""
Usage:
$python3 process_tweets.py <tweet-json-file>

Outputs to:
instances.txt


This program takes a text file of tweet json objects as input.
It uses a start time, end time, and size of time division (eg 1 hour) to create blocks of tweets
Each block of tweets is used to generate 1 instance with 4 features.
Import_tweets_by_block is weird due to the size of the text files. 
Any data structure holding the entire text file in RAM would be a significant resource drain.
This solution allows the file to be opened, read from, and closed. The returned tweets are processed into an instance, then the file is opened for the next chunk
To avoid reading from the start of the file every time, the end read location is returned by the function.
When this location is passed to the next function call, it jumps to that location in the file.
"""

import json
import re
from textblob import TextBlob
import datetime as dt
import numpy as np
import sys

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

    #Store raw tweet jsons where s (start time) < tweet time < e (end time)
    raw_tweets = list()
    #Return the location in the file after the last tweet, so next call of function can jump there in file
    end_loc = 0
    with open(filename) as source:
        #Jump to where last call left off
        source.seek(start_loc)

        #The scraper occasionally didn't put a newline between two json dumps. This looks for that ("}{"), and handles it
        prob_string = "}{\"id\""
        curr_tweets = []
        inrange = 1
        line = source.readline()
        print(line)
        #While there are lines to read and the end-datetime flag hasn't been switched
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

if __name__ == '__main__':
    filename = sys.argv[1]
    delta = dt.timedelta(seconds = 3600)                                #Size of time chunk for each instance
    start = dt.datetime(2018, 4, 7, hour=0, minute=0, second=0)         #Start of first chunk
    end = start + delta                                                 #End of first chunk
    end_final = dt.datetime(2018, 4, 14, hour=0, minute=0, second=0)    #End of entire range
    start_loc = 0

    out = open("instances_without_noise.txt", "w+")
    while end_final >= end:
        print(str(end))
        print(end.timestamp())
        #Get raw tweets for 1 time chunk, save location reached in file
        raw_tweets, start_loc = import_tweets_by_block(filename, start, end, start_loc)
        
        #Create list of Tweet objects
        tweet_data = []
        for tweet in raw_tweets:
            tweet_data.append(process_tweet(tweet))

        #Iterate over tweet objects to calculate features
        sentiment_block_score = 0           #Average sentiment in block
        retweet_block_score = 0             #Average # Retweets in block
        sentiment_sd = 0                    #Sentiment standard deviation in block
        sent = []
        for n, tweet in enumerate(tweet_data):
            sentiment_block_score += tweet.sentiment
            sent.append(tweet.sentiment)
            retweet_block_score += tweet.retweets
            
        #If this time chunk has >0 tweets, finish calculations
        if len(tweet_data) != 0:
            sentiment_block_score /= len(tweet_data)
            sent = np.array(sent)
            sentiment_sd = np.std(sent)
            retweet_block_score /= len(tweet_data)

        #Write time chunk, features to file
        out.write(str(start) + "," + str(end) + "," + str(len(tweet_data)) + "," +str(sentiment_block_score) + "," + str(sentiment_sd) + "," + str(retweet_block_score) +"\n")
        start = end
        end += delta
    out.close()

