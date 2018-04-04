#!/usr/bin/env python3

'''
tweet_scrape.py

Stream crypto-related tweets into a file via tweepy.
created: MAR 2018
'''

import tweepy
from json import dumps
from wbutil import PersistentDict

TERMS = [
    "bitcoin", "BTC",
    "bitcoin cash", "BCH",
    "ethereum", "ETH", "ether",
    "ripple", "XRP",
    "litecoin", "LTC",
    "cryptocurrency", "crypto", "altcoin", "blockchain",
]


class MyStreamListener(tweepy.StreamListener):

    def __init__(self, path, api, batch_size=1000):
        self.path = path
        self.api = api
        self.batch_size = batch_size
        try:
            with open(path) as fs:
                self.count = sum(1 for _ in fs)
        except FileNotFoundError:
            self.count = 0

    def __enter__(self):
        self.fs = open(self.path, 'a')
        self.batch = []
        return self

    def __exit__(self, *args):
        self.write_batch()
        self.fs.close()

    def write_batch(self):
        self.fs.write('\n'.join(self.batch))
        self.batch.clear()

    def on_status(self, status):
        try:
            self.count += 1
            print(('Got tweet %d' % self.count), '\r', end='')
            tweet = {
                "id": status.id_str,
                "text": status.text,
                "hashtags": status.entities.get('hashtags'),
                "retweets": status.retweet_count,
                "user_id": status.user.id_str,
                "time": str(status.created_at)
            }
            self.batch.append(dumps(tweet))
            if len(self.batch) >= self.batch_size:
                self.write_batch()
        except Exception:
            pass

    def on_error(self, status_code):
        return False


def main():
    from argparse import ArgumentParser
    parser = ArgumentParser(description='Stream tweets into a file.')
    parser.add_argument('-o', '--output', help='destination for json data')
    parser.add_argument('--consumerkey')
    parser.add_argument('--consumersecret')
    parser.add_argument('--accesskey')
    parser.add_argument('--accesssecret')
    args = parser.parse_args()

    auth = tweepy.OAuthHandler(consumer_key=args.consumerkey,
                               consumer_secret=args.consumersecret)
    auth.set_access_token(key=args.accesskey, secret=args.accesssecret)
    api = tweepy.API(auth)

    with MyStreamListener(args.output, api) as streamlistener:
        stream = tweepy.Stream(auth=api.auth, listener=streamlistener)
        try:
            stream.filter(track=TERMS)
        finally:
            stream.disconnect()


if __name__ == '__main__':
    from sys import exit
    exit(main())
