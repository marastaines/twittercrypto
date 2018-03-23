import requests
import json
import time

class _price_scraper:
	def __init__(self):
		self.SITE_URL = 'https://min-api.cryptocompare.com/data'
		self.PRICE_URL = self.SITE_URL + '/price'
		self.HISTORICAL_URL = self.SITE_URL + '/pricehistorical'

	def get_price(self, symbol, output="USD"):
		r = requests.get(self.PRICE_URL + "?fsym=" + str(symbol) + "&tsyms=" + str(output))
		resp = json.loads(r.content)
		return resp[str(output)]

	def get_historical_price(self, symbol, timestamp, output="USD"):
		r = requests.get(self.HISTORICAL_URL + "?fsym=" + str(symbol) + "&tsyms=" + str(output) + "&ts=" + str(int(timestamp)))
		resp = json.loads(r.content)
		return resp[str(symbol)][str(output)]

	def get_price_change(self, symbol, seconds, output="USD"):
		old_time = int(time.time()) - int(seconds)
		return self.get_price(symbol, output) - self.get_historical_price(symbol, old_time, output)