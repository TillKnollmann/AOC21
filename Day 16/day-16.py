import numpy as np
import time
import pprint

path = "Day 16/input-test.txt"

def main():
    with open(path, "r") as file:
        startTime = time.time()
        lines = file.readlines()

        for line in lines:
            break

        print(" ")
        executionTime = round(time.time() - startTime, 2)
        print("Execution time in seconds: " + str(executionTime))

if __name__ == "__main__":
	main()