import json
from datetime import datetime

start = datetime(2018, 4, 7, hour=0, minute=0, second=0)
end = datetime(2018, 4, 14, hour=0, minute=0, second=0)

with open("../../appa.out.txt") as f:
	with open("appa_select.txt", "w+") as out:
		for line in f:
			if "}{" in line:
				tweets = line.split("}{")
				tweets[0] = tweets[0] + "}"
				tweets[1] = "{" + tweets[1]
			else:
				tweets = [line]
			#print(tweets)
			for tweet in tweets:
				#print tweet
				try:
					t = json.loads(tweet)
				except:
					continue
				dt = datetime.strptime(t['time'], '%Y-%m-%d %H:%M:%S')
				if dt >= start and dt < end:
					out.write(line)