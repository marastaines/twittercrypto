#!/usr/bin/env python3

import numpy as np

from contextlib import ExitStack, suppress
from fileinput import input as fileinput
from json import decoder, dumps, loads

from nltk.tokenize import TweetTokenizer
from sklearn.cluster import KMeans
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.pipeline import Pipeline


def load_tweets(fs):
    for line in fs:
        with suppress(decoder.JSONDecodeError):
            yield loads(line)


def mkpipeline(tweets):
    return Pipeline([
        ('vectorize', CountVectorizer(tokenizer=TweetTokenizer().tokenize)),
        ('kmeans', KMeans(n_clusters=2))]).fit(
        np.random.choice(tweets, min(20000, len(tweets)), replace=False))
        #tweets)


def write_clusters(clusters, tweets):
    with ExitStack() as stack:
        files = [stack.enter_context(open(f, 'w')) for f in ('0.txt', '1.txt')]
        for t, c in zip(tweets, clusters):
            files[c].write(dumps(t) + '\n')


def main():
    with fileinput() as fs:
        tweets = list(load_tweets(fs))
        texts = [x['text'] for x in tweets]
    write_clusters(mkpipeline(texts).predict(texts), tweets)


if __name__ == '__main__':
    from sys import exit
    exit(main())
