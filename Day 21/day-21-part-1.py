import numpy as np
import time

path = "Day21/input-text.txt"

with open(path, "r") as file:
	startTime = time.time()
	lines = file.readlines()

	for line in lines:
		break

	print(" ")
	executionTime = round(time.time() - startTime, 2)
	print("Execution time in seconds: " + str(executionTime))