# twittercrypto

Forecasting cryptocurrency prices with Twitter data.

## Installation

Please ensure you are using a valid installation of Python 3, and run the
following to install the project's dependencies:

    $ pip install --user -r requirements.txt

## Usage

To build the dataset, we stream tweets directly from the Twitter API. You
can start streaming tweets into a file with the `tweet_scrape` module:

    $ pwd
    /my/path/to/twittercrypto
    $ python -m src.tweet_scrape --help
    usage: tweet_scrape.py [-h] [-o OUTPUT] [--consumerkey CONSUMERKEY]
                           [--consumersecret CONSUMERSECRET]
                           [--accesskey ACCESSKEY] [--accesssecret ACCESSSECRET]

    Stream tweets into a file.

    optional arguments:
      -h, --help            show this help message and exit
      -o OUTPUT, --output OUTPUT
                            destination for json data
      --consumerkey CONSUMERKEY
      --consumersecret CONSUMERSECRET
      --accesskey ACCESSKEY
      --accesssecret ACCESSSECRET

Please find the appropriate keys and secrets in the Twitter developer portal at
[apps.twitter.com](https://apps.twitter.com) (you will need to register an
application in order to obtain these credentials).

To start streaming currency price data, please use the `price_scrape` module
provided in `src/`:

    $ pwd
    /my/path/to/twittercrypto
    $ python -m src.price_scrape --help
    usage: price_scrape.py [-h] [-o OUTPUT] [-d DELAY] COIN [COIN ...]

    Get realtime data on crypto prices

    positional arguments:
      COIN                  currencies to track

    optional arguments:
      -h, --help            show this help message and exit
      -o OUTPUT, --output OUTPUT
                            path to save location
      -d DELAY, --delay DELAY
                            seconds to sleep between scans (default:60)

## Status

Project has been completed, compile final.tex for report. General pipeline of scripts is 

-Use selection.py to grab a subset of appa.out.txt

-Run it through process_tweets.py to generate features

-Use price_hist.py to get hourly prices over same date range

-Use output of process_tweets.py as feature data and output of price_hist.py as target data in regression.py

To remove noise:

-build_model.py builds model on subset of data (you should use a file with < 100k tweets) and outputs .pkl files to disk

-apply_model.py uses the vectorize and cluster models from disk on each tweet from a file and only outputs "relevant tweets"

-Use the file from apply_model.py as input to process_tweets.py to generate features for this data, then proceed as above.


## Download data

Snapshots of the data can be retrieved over the web from [appa.ndlug.org/tweets.tar.gz](tweets). You must be connected to the internal ND network (i.e. eduroam) to make a connection.

[tweets][http://appa.ndlug.org/tweets.tar.gz]
