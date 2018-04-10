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

from cluster2 import load_tweets, mkpipeline

COLORS = 'rb'


def main():
    with fileinput() as fs:
        tweets = list(load_tweets(fs))

    pipeline = mkpipeline(tweets)
    t_vectors = pipeline.named_steps.vectorize.transform(tweets)
    svd = TruncatedSVD().fit_transform(t_vectors)
    clustering = pipeline.predict(tweets)

    plt.title('Tweet Clusters w/ SVD to 2-dimensional space')
    for cluster, (x, y) in zip(clustering, svd):
        plt.scatter([x], [y], color=COLORS[cluster])
    plt.show()


if __name__ == '__main__':
    from sys import exit
    exit(main())
