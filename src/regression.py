"""Takes CSV, does a regression
CHANGE FILE PATH ON LINE 15 to where your instances file is located"""



from sklearn import linear_model
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as dates
import datetime as dt
from sklearn import metrics
from sklearn import svm

listx = []
listy = []
graphx = []
with open("instances_without_noise.txt") as f:
	for line in f:
		line = line.rstrip().split(",")
		listx.append(line[2:])
		t = dt.datetime.strptime(line[1], "%Y-%m-%d %H:%M:%S")
		graphx.append(dates.date2num(t))
print("instances loaded")
with open("../data/price_series.txt") as f:
	for line in f:
		line = line.rstrip().split(",")
		listy.append(float(line[-1]))
X = np.array(listx, dtype='float64')
y = np.array(listy, dtype='float64')
print(X.size)
print(y.size)
print(X)
print(y)
reg = linear_model.Lasso(alpha = 0.1)
#reg = svm.SVR(kernel='linear', epsilon=0.05)
reg.fit(X, y)
print("model built")
print(reg.score(X, y))
test_y = reg.predict(X)
print("R2")
print(metrics.r2_score(y, test_y))
# Plot outputs
# Plot outputs
plt.scatter(graphx, y,  color='black')
plt.plot(graphx, test_y, color='blue', linewidth=3)

plt.xlabel('7-Apr-2018 to 13-Apr-2018 (delta = 1hr)')
plt.ylabel('Bitcoin Value USD')
plt.title('Regression Model')
plt.gcf().autofmt_xdate()
myFmt = dates.DateFormatter('%m/%d')
plt.gca().xaxis.set_major_formatter(myFmt)

plt.show()


#0.1858734448927718
#0.14955317499263565

