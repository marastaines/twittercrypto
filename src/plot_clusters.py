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
from wbutil import lmap

from nltk.tokenize import TweetTokenizer
from sklearn.cluster import KMeans, SpectralClustering
from sklearn.decomposition import TruncatedSVD
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.preprocessing import scale
from sklearn.svm import OneClassSVM

from cluster2 import load_tweets, mkpipeline, write_clusters

COLORS = 'rbgk'
N_CLUSTERS = 3


def main():
    with fileinput() as fs:
        tweets = list(load_tweets(fs))

    tvecs = CountVectorizer().fit_transform(tweets)
    svd = TruncatedSVD().fit_transform(tvecs)

    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2)
    fig.title('{}-Clustering Strategies for {} Tweets'.format(
        N_CLUSTERS, len(tweets)))

    ax1.set_title('Spectral Clustering on SVD')
    spect = SpectralClustering(n_clusters=N_CLUSTERS).fit_predict(svd)
    ax1.scatter(svd[:,0], svd[:,1], c=lmap(COLORS.__getitem__, spect))

    ax2.set_title('KMeans on SVD')
    kmean = KMeans(n_clusters=N_CLUSTERS).fit_predict(svd)
    ax2.scatter(svd[:,0], svd[:,1], c=lmap(COLORS.__getitem__, kmean))

    ax3.set_title('Spectral Clustering on Tweet Vectors')
    spect1 = SpectralClustering(n_clusters=N_CLUSTERS).fit_predict(tvecs)
    ax3.scatter(svd[:,0], svd[:,1], c=lmap(COLORS.__getitem__, spect1))

    ax4.set_title('KMeans on Tweet Vectors')
    kmean1 = KMeans(n_clusters=N_CLUSTERS).fit_predict(tvecs)
    ax4.scatter(svd[:,0], svd[:,1], c=lmap(COLORS.__getitem__, kmean1))

    plt.show()

    # write_clusters(clustering, tweets, n_clusters=N_CLUSTERS)


if __name__ == '__main__':
    from sys import exit
    exit(main())
