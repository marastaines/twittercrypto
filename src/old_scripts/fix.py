from datetime import datetime, timedelta

td = timedelta(0, 3600)
with open("instances.txt") as f:
	with open("instances2.txt", "w+") as out:
		for line in f:
			time = line.rstrip().split(",")
			time[0] = datetime.strptime(time[0], "%Y-%m-%d %H:%M:%S") - td
			time[1] = datetime.strptime(time[1], "%Y-%m-%d %H:%M:%S") - td
			newline = ",".join([str(x) for x in time])
			out.write(newline + "\n")