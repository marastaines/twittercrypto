#!/usr/bin/env python3

'''
src/price_scrape.py

Fetch current crypto prices from CryptoCompare.com.
created: MAR 2018
'''

import requests as r
from json import dump, load
from time import sleep, time
from wbutil import tryopen

API_FMT = 'https://min-api.cryptocompare.com/data/{endpoint}'
PRICE_URL = API_FMT.format(endpoint='price')
HISTORICAL_URL = API_FMT.format(endpoint='pricehistorical')


def get_price(coin, output='USD'):
    res = r.get(PRICE_URL, params={'fsym': coin, 'tsyms': output})
    return res.json()[output]


def get_historical(coin, timestamp, output='USD'):
    res = r.get(HISTORICAL_URL, params={
        'fsym': coin, 'tsyms': output, 'ts': str(int(timestamp))})
    return res.json()[coin][output]


def get_delta(coin, seconds_ago, output='USD'):
    old = int(time()) - int(seconds_ago)
    return get_price(coin, output) - get_historical(coin, old, output)


def main():
    from argparse import ArgumentParser
    parser = ArgumentParser(description='Get realtime data on crypto prices')
    parser.add_argument('-o', '--output', help='path to save location')
    parser.add_argument('-d', '--delay', type=int, default=60,
                        help='seconds to sleep between scans (default:60)')
    parser.add_argument('coins', metavar='COIN', nargs='+',
                        help='currencies to track')
    args = parser.parse_args()
    data = tryopen(args.output, process=load, default=[])

    while True:
        snap = {}
        for coin in args.coins:
            snap[coin] = {
                'value': get_price(coin),
                'time': int(time()),
            }
        data.append(snap)
        with open(args.output, 'w') as fs:
            dump(data, fs)
        sleep(args.delay)


if __name__ == '__main__':
    from sys import exit
    exit(main())
