import numpy as np
import time
import bisect

path = "Day 6/input.txt"

def main():
	with open(path, "r") as file:
		startTime = time.time()
		lines = file.readlines()

		total_steps = 256

		fish = np.array(lines[0].split(sep=","), np.int32)
		print("Initial state: " + str(fish))

		for i in range(1,total_steps + 1):
			zeros = len(fish[fish == 0])
			# reduce all fish counters
			fish = fish - 1
			# set zeros to 6
			fish[fish==-1] = 6
			# append eights
			eights = np.full(zeros, 8)		
			fish = np.concatenate((fish, eights))
			print("\nDay " + str(i) + " " + str(fish))

		print("\nThere are " + str(len(fish)) + " fish")
		executionTime = round(time.time() - startTime, 2)
		print("Execution time in seconds: " + str(executionTime))

if __name__ == "__main__":
	main()