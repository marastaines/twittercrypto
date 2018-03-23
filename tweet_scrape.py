import json
import smtplib
import time

import tweepy

from os import environ

TERMS = [
    "bitcoin", "BTC",
    "bitcoin cash", "BCH",
    "ethereum", "ETH", "ether",
    "ripple", "XRP",
    "litecoin", "LTC",
    "cryptocurrency", "crypto", "altcoin", "blockchain",
]


class MyStreamListener(tweepy.StreamListener):

    def __init__(path):
        self.path = path
        self.file_out = None

    def __enter__(self):
        self.file_out = open(path, 'a')
        return self

    def __exit__(self, *args):
        self.file_out.close()

    def on_status(self, status):
        try:
            tweet = {
                "id" : status.id_str,
                "text" : status.text,
                "hashtags" : status.entities.get('hashtags'),
                "retweets" : status.retweet_count,
                "user_id" : status.user.id_str,
                "time" : str(status.created_at)
            }
            file_out.write(json.dumps(tweet) + "\n")
        except:
            pass

    def on_error(self, status_code):
        return False


def main():
    from sys import argv
    auth = tweepy.OAuthHandler(environ.get('TWEEPY_HANDLE'))
    auth.set_access_token(environ.get('TWEEPY_TOKEN'))
    api = tweepy.API(auth)

    with MyStreamListener(argv[1]) as streamlistener:
        stream = tweepy.Stream(auth=api.auth, listener=streamlistener)
        stream.filter(track=TERMS)
        stream.disconnect()


if __name__ == '__main__':
    from sys import exit
    exit(main())
