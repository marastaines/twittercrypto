"""Takes CSV, does a regression
CHANGE FILE PATH ON LINE 15 to where your instances file is located"""



from sklearn import linear_model
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as dates
import datetime as dt

listx = []
listy = []
graphx = []
with open("instances.txt") as f:
	for line in f:
		line = line.rstrip().split(",")
		listx.append(line[2:-1])
		listy.append(line[-1])
		t = dt.datetime.strptime(line[1], "%Y-%m-%d %H:%M:%S")
		graphx.append(dates.date2num(t))
X = np.array(listx, dtype='float64')
y = np.array(listy, dtype='float64')
reg = linear_model.Ridge()
reg.fit(X, y)
print(reg.score(X, y))
test_y = reg.predict(X)

# Plot outputs
# Plot outputs
plt.scatter(graphx, y,  color='black')
plt.plot(graphx, test_y, color='blue', linewidth=3)

plt.xlabel('24 Hour Time (1 Day)')
plt.ylabel('Bitcoin Value USD')
plt.title('Inital Regression Model')
plt.gcf().autofmt_xdate()
myFmt = dates.DateFormatter('%H:%M')
plt.gca().xaxis.set_major_formatter(myFmt)

plt.show()
