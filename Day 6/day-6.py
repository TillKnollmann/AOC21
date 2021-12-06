import numpy as np
import time
import bisect

path = "Day 6/input.txt"


def main():
	with open(path, "r") as file:
		startTime = time.time()
		lines = file.readlines()

		# defines how many time steps are considered
		total_steps = 256

		# read the initial fish
		fish = np.array(lines[0].split(sep=","), np.int32)
		#print("Initial state: " + str(fish))

		# other way of representing fish
		# at position i the number of fish with counter
		# i are stored
		fish_improved = np.ones(9)
		for i in range(0, 9):
			fish_improved[i] = len(fish[fish == i])
		
		fish = fish_improved

		for i in range(1, total_steps + 1):
			# move every number to the left by one 
			# (decreases every fish counter)
			# except for the zero counters
			fish_new = np.zeros(9)
			for j in range(0,8):
				fish_new[j] = fish[j+1]
			
			# each fish of counter 0 adds a 6 and an 8
			fish_new[6] += fish[0]
			fish_new[8] += fish[0]
			fish = fish_new
			#print("\nDay " + str(i) + " " + str(fish))
			print("\n" + str(i) + "/" + str(total_steps))

		print("\nThere are " + str(sum(fish)) + " fish")
		executionTime = round(time.time() - startTime, 2)
		print("Execution time in seconds: " + str(executionTime))

if __name__ == "__main__":
	main()
