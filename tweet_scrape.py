#!/usr/bin/env python3

'''
tweet_scrape.py

Stream crypto-related tweets into a file via tweepy.
created: MAR 2018
'''

import tweepy
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

    def __init__(self, path, api, batch_size=100):
        self.data = PersistentDict({'tweets': []}, path=path)
        self.api = api
        self.batch_size = batch_size

    def on_status(self, status):
        print(('Got tweet %d' % len(self.data['tweets'])), '\r', end='')
        try:
            tweet = {
                "id": status.id_str,
                "text": status.text,
                "hashtags": status.entities.get('hashtags'),
                "retweets": status.retweet_count,
                "user_id": status.user.id_str,
                "time": str(status.created_at)
            }
            self.data['tweets'].append(tweet)
            if len(self.data['tweets']) % self.batch_size == 0:
                print('Writing batch. Saving %d tweets...'
                      % (len(self.data['tweets'])))
                self.data.save()
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

    streamlistener = MyStreamListener(args.output, api)
    stream = tweepy.Stream(auth=api.auth, listener=streamlistener)
    try:
        stream.filter(track=TERMS)
    finally:
        stream.disconnect()


if __name__ == '__main__':
    from sys import exit
    exit(main())
