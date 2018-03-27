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

We are currently assembling an archive of tweets by keeping `tweet_scrape.py`
running on a server. `price_scrape.py` has also been successful in retrieving
current and historical data on the prices of various currencies.

The next steps will be to curate our historical dataset and provide initial
analysis, and, at the same time, prepare our real-time models to accept and
act on tweets streamed directly from `tweet_scrape`.
