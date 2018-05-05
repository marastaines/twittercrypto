import os
import time
import smtplib
import datetime

pid = 19490

def check_pid(pid):
	try:
		os.kill(pid, 0)
		return True
	except OSError as e:
		return False

def send_mail():
	server = smtplib.SMTP('smtp.gmail.com', 587)
	server.ehlo()
	server.starttls()
	#Next, log in to the server
	server.login("tweetscrapealert@gmail.com", "#1Smarty")

	#Send the mail
	msg = "\nScraping interrupted"
	server.sendmail("tweetscrapealert@gmail.com", "marastaines@gmail.com", msg)
	server.quit()

next_day = datetime.date.today() + datetime.timedelta(days=1)
cont = True
while(cont):
	pid = os.fork()
	if pid == 0:
		os.system("python ./tweet_scrape.py " + str(datetime.date.today()) + ".txt")
	else:
		while(datetime.date.today() != next_day):
			if not check_pid(pid):
				send_mail()
				cont = False
			time.sleep(1200)
		os.kill(pid, 9)
		next_day = datetime.date.today() + datetime.timedelta(days=1)

