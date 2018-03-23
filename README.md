# twittercrypto

## Use:

    $ python tweet_scrape.py <output_file>

    $ python is_running.py

Note:

Pretty please use your own twitter account codes for OAuth if you're running tweet_scrape. If you don't have an account or whatever, I can send you mine, but I'm not gonna leave them in a public repo haha.

Please set the environment variables `TWEEPY_HANDLE` (for the tweepy OAuthHandler argument) and `TWEEPY_TOKEN` (for the twitter access token) before running.

## Status:

tweet_scrape starts running fine, appending to output file. But when I check on it after a couple hours, the process is dead and the text file exists but with nothing in it.

price_scrape.py runs as expected. It is currently configured to append the price of BTC, BCH, ETH, RPL, and XRP to prices.txt once every minute.
