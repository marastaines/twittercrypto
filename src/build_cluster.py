import sys
import numpy as np

from contextlib import suppress
from fileinput import input as fileinput
from json import decoder, dumps, loads

from nltk.tokenize import TweetTokenizer
from sklearn.cluster import MiniBatchKMeans
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.pipeline import Pipeline
from sklearn.externals import joblib

def load_tweets(fs):
    for line in fs:
        with suppress(decoder.JSONDecodeError):
            yield loads(line)

def build(tweets):
	cv = CountVectorizer(tokenizer=TweetTokenizer().tokenize)
	matrix = cv.fit_transform(tweets)
	km = MiniBatchKMeans(n_clusters=2)
	clusts = km.fit(matrix)
	joblib.dump(km, "cluster_model.pkl")
	joblib.dump(cv, "vectorizer.pkl")

if __name__ == '__main__':
	fs = open(sys.argv[1])
	tweets = list(load_tweets(fs))
	texts = [x['text'] for x in tweets]
	build(texts)
	fs.close()
