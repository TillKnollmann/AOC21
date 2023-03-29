from os import sep
import numpy as np
import time

import math

path = "Day 7/input.txt"

def getCost(crabs, position):
	""" Returns the sum of all costs of crabs to the chosen position """
	result = 0
	for j in range(0, len(crabs)):
		#for i in range(1, abs(crabs[j] - position) + 1):
		#	result += i
		result += gausSum(abs(crabs[j] - position))
	return result

def gausSum(n):
	"""Returns the gaussian sum to n """
	return float(math.pow(n,2) + n)/2.

def getMinimum(crabs):
	""" Returns approximately the optimal position for part 2
	Observe we want to find best m to minimize 
	sum((abs(crab[i]-m)))
	deriving yields
	m - crab[i] +- 1/2
	<=> 0 = sum_(i) (m - crab[i] +- 1/2)
	<=> len(crabs) * m = sum_(i) (crab[i] +- 1/2)
	<=> m = sum_(i) (crab[i] +- 1/2) / len(crabs)

	We approximate by calculating m that fullfills
	m = sum_(i) crab[i] / len(crabs)
	We assume here that the 1/2 part roughly cancels out over all crabs
	"""

	result = 0
	for i in range(0, len(crabs)):
		result += float(crabs[i])
	return result / len(crabs)

def main():
	with open(path, "r") as file:
		startTime = time.time()
		lines = file.readlines()

		# read the crabs
		crabs = np.array(lines[0].replace('\n', '').split(sep=","), dtype=np.int32)

		# the median is the solution for part 1
		median = np.median(crabs)

		median_array = np.ones(len(crabs)) * median

		result_median = int(sum(np.absolute(crabs - median_array)))

		# calculate solution for part 2
		part_2 = getMinimum(crabs)

		sol = int(min(getCost(crabs, math.ceil(part_2)), getCost(crabs, math.floor(part_2))))

		print("Position Median: " + str(median) + " Result Median: " + str(result_median) + "\nPosition Part 2: " + str(part_2) + " Result Part 2: " + str(sol))
		
		executionTime = round(time.time() - startTime, 2)
		print("Execution time in seconds: " + str(executionTime))

if __name__ == "__main__":
	main()