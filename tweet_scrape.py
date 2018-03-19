import tweepy
import time
import json
import smtplib
import sys

auth = tweepy.OAuthHandler("""PUT AUTH STUFF HERE""")
auth.set_access_token("""PUT ACCESS TOKEN HERE""")

api = tweepy.API(auth)

terms = ["bitcoin", "BTC", 
		 "bitcoin cash", "BCH", 
		 "ethereum", "ETH", "ether",
		 "ripple", "XRP",
		 "litecoin", "LTC",
		 "cryptocurrency", "crypto", "altcoin", "blockchain", 
		 ]

global count
global timer
count = 0

global file_out 
file_out = open(sys.argv[1], "w+")
class MyStreamListener(tweepy.StreamListener):

	def on_status(self, status):
		global file_out
		try:
			tweet = {"id" : status.id_str,
					 "text" : status.text,
					 "hashtags" : status.entities.get('hashtags'),
					 "retweets" : status.retweet_count,
					 "user_id" : status.user.id_str,
					 "time" : str(status.created_at)
					}
			file_out.write(json.dumps(tweet) + "\n")
			count += 1
		except:
			pass
			
	def on_error(self, status_code):
		return False

streamlistener = MyStreamListener()

stream = tweepy.Stream(auth=api.auth, listener=streamlistener)
stream.filter(track=terms)
stream.disconnect()