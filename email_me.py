"""The first step is to create an SMTP object, each object is used for connection 
with one server."""

import smtplib
server = smtplib.SMTP('smtp.gmail.com', 587)
server.ehlo()
server.starttls()
#Next, log in to the server
server.login("tweetscrapealert@gmail.com", "#1Smarty")

#Send the mail
msg = "\nScraping interrupted"
server.sendmail("tweetscrapealert@gmail.com", "marastaines@gmail.com", msg)
server.quit()
