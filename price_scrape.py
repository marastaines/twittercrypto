from _price_scraper import _price_scraper
import time
import json

def main():
	ps = _price_scraper()
	coins = ("BTC", "ETH", "LTC", "BCH", "XRP")
	delay = 60

	with open("prices.txt", "a") as f:
		while True:
			for coin in coins:
				print coin
				price = {
			        "time"  : int(time.time()),
			        "name"  : coin,
			        "value" : ps.get_price(coin)
		    	}
				f.write(json.dumps(price)+"\n")
			time.sleep(delay)


if __name__ == '__main__':
    from sys import exit
    exit(main())