#!/usr/bin/env python3

'''
src/plot_clusters.py

Plot the clusters from clusters2.py to heuristically evaluate clustering
quality.

Will Badart <netid:wbadart>
created: APR 2018
'''

import matplotlib.pyplot as plt
from fileinput import input as fileinput
from sklearn.decomposition import TruncatedSVD
from wbutil import lmap

from cluster2 import load_tweets, mkpipeline, write_clusters

COLORS = 'rb'


def main():
    with fileinput() as fs:
        tweets = list(load_tweets(fs))

    pipeline = mkpipeline(tweets)
    t_vectors = pipeline.named_steps.vectorize.transform(tweets)
    svd = TruncatedSVD().fit_transform(t_vectors)
    clustering = pipeline.predict(tweets)

    plt.title(f'Tweet Clusters w/ SVD to 2-dimensional '
              f'space and {len(tweets)} tweets')

    plt.scatter(svd[:,0], svd[:,1], c=lmap(COLORS.__getitem__, clustering))
    plt.show()

    write_clusters(clustering, tweets)


if __name__ == '__main__':
    from sys import exit
    exit(main())
