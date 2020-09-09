import csv
import matplotlib.pyplot as plt

csvfile =  open('results.csv', newline='')
reader = csv.reader(csvfile, delimiter=',', quotechar='"')

times = []
response = []
response_hermes = []

curr = 0
change = 0
for row in reader:
	if row[0] == "interval":
		continue

	if int(row[0]) < curr:
		change = 1

	if change == 0:
		response.append(float(row[1]))
		times.append(int(row[0]))
	else:
		response_hermes.append(float(row[1]))

	curr = int(row[0])

print(times)
print(response)
print(response_hermes)
print(len(times), len(response), len(response_hermes))


plt.plot(times, response)
plt.plot(times, response_hermes)
plt.ylabel("Average response time")
plt.xlabel("Interval")
plt.show()

