#!/usr/bin/env python3

'''
src/cluster2.py

Second pass at outlier detection and removal. Seems to perform well if you take
a few passes at the target cluster, i.e. one pass sifts out the REALLY
out-there tweets, and subsequent passes (on 0.txt if 1 is the outlier class)
will further refine the target cluster.

Will Badart <netid:wbadart>
created: APR 2018
'''

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
            yield loads(line)['text']


def mkpipeline(tweets):
    return Pipeline([
        ('vectorize', CountVectorizer(tokenizer=TweetTokenizer().tokenize)),
        ('kmeans', KMeans(n_clusters=2))]).fit(
        # np.random.choice(tweets, min(2000, len(tweets)), replace=False))
        tweets)


def write_clusters(clusters, tweets, n_clusters=2):
    with ExitStack() as stack:
        files = [stack.enter_context(open('{}.txt'.format(f), 'w'))
                for f in range(n_clusters)]
        for t, c in zip(tweets, clusters):
            files[c].write(dumps({'text': t}) + '\n')


def main():
    with fileinput() as fs:
        tweets = list(load_tweets(fs))
    write_clusters(mkpipeline(tweets).predict(tweets), tweets)


if __name__ == '__main__':
    from sys import exit
    exit(main())
