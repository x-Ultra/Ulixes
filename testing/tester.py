import requests
import time

MIN_INTERVAL = 1800
MAX_INTERVAL = 21600

## 0 = foot
## 1 = driving
TRANSPORT = 0

ADDRESS = "http://load-balancer-ulixes-962120851.eu-central-1.elb.amazonaws.com:5005"

fd = open("results.csv", "a")

TRIES_PER_INTERVAL = 50

for interval in range(MIN_INTERVAL, MAX_INTERVAL, 600):
	time_sum = 0.0
	for _ in range(0, TRIES_PER_INTERVAL):

		start = time.time()

		params = { "latitude" : "41.89332", "longitude" : "12.482932", "interval": interval, "trans": TRANSPORT}

		requests.get(ADDRESS, params=params)

		end = time.time()

		time_sum += end - start

	print(time_sum)
	average = time_sum / float(TRIES_PER_INTERVAL*1.0)
	print("Testing complete for interval ", interval, ", average response time: ", average)	
	fd.write(str(interval) + ", " + str(average) + ", " + str(TRIES_PER_INTERVAL) + "\n")