#!/usr/bin/env python3

'''
src/sentiment.py

First stab at tweet sentiment analysis.

created: APR 2018
'''

from fileinput import input as fileinput
from nltk.sentiment.vader import SentimentIntensityAnalyzer

from cluster2 import load_tweets


def main():
    with fileinput() as fs:
        tweets = list(load_tweets(fs))

    sia = SentimentIntensityAnalyzer()
    for tweet in tweets:
        tweet = ' '.join(tweet.split())
        ss = sia.polarity_scores(tweet)
        if ss['neu'] <= 0.8:
            print(tweet)
            print(ss)
            print()


if __name__ == '__main__':
    from sys import exit
    exit(main())
