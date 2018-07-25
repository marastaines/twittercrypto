import price_scrape as ps
import datetime as dt
import time
import json

delta = dt.timedelta(hours = 1)
start = dt.datetime(2018, 4, 7, hour=0, minute=0, second=0)
end = start + delta
end_final = dt.datetime(2018, 4, 14, hour=0, minute=0, second=0)

with open("price_series.txt", "w+") as out:
	while(end_final >= end):
		price = ps.get_historical("BTC", end.timestamp())
		out.write(str(end) + "," + str(price) + "\n")
		time.sleep(1)
		start = end
		end += delta
