import csv
import numpy
import math

with open('firstrun.csv', 'rb') as csvfile:
	reader = csv.reader(csvfile, delimiter=',')
	count = -1
	backgroungmag = 0
	carbufcount = 0
	carEnc = False;
	for row in reader:
		count += 1
		time = row[0]
		x = float(row[2])
		y = float(row[3])
		z = float(row[4])
		magnitude = math.sqrt(math.pow(x,2)+math.pow(y,2)+math.pow(z,2))
		# print str(count) + ": " + str(magnitude)

		if count < 150:
			backgroungmag += magnitude
		elif count == 150:
			backgroungmag /= 150
			print backgroungmag
		else:
			normMage = (magnitude - backgroungmag)
			if (normMage) < -40:
				if not carEnc:
					print str(count) + ": " + str(normMage)
					carEnc = not carEnc
					continue
			elif normMage > -10:
				if carEnc:
					print "Car left: " + str(count)
					carEnc = not carEnc
					continue