import numpy as np
import time

path = "Day 9/input.txt"


def findBasinLine(line, position):
	""" Given a 1-dim line and a position on it,
		find the longest subsequence decreasing towards the position
		and mark it with -1
	"""
	# normalize the line
	line_work = line.copy().reshape(-1)
	line_work[position] = -1
	position_left = position - 1
	position_right = position + 1
	worked = False
	# go to the left of position
	while position_left >= 0 and line[position_left] > line[position_left + 1] and line[position_left] != 9:
		line_work[position_left] = -1
		position_left -= 1
		worked = True
	# go to the right of position
	while position_right < len(line) and line[position_right] > line[position_right - 1] and line[position_right] != 9:
		line_work[position_right] = -1
		position_right += 1
		worked = True
	# return the marked line and if work has been done
	return (line_work, worked)


def main():
	with open(path, "r") as file:
		startTime = time.time()
		lines = file.readlines()

		# Parse input
		heightmap = np.zeros((len(lines), len(lines[0])-1))

		for i in range(0, len(lines)):
			heightmap[i] = np.array(
				[char for char in lines[i].replace('\n', '')])

		# calculate solutions of part 1
		result_1 = 0

		for i in range(0, len(heightmap)):
			for j in range(0, len(heightmap[0])):
				isLocalMinimum = True
				if not (i == 0 or heightmap[i][j] < heightmap[i-1][j]):
					isLocalMinimum = False
				if not (i == len(heightmap)-1 or heightmap[i][j] < heightmap[i+1][j]):
					isLocalMinimum = False
				if not (j == 0 or heightmap[i][j] < heightmap[i][j-1]):
					isLocalMinimum = False
				if not (j == len(heightmap[0])-1 or heightmap[i][j] < heightmap[i][j+1]):
					isLocalMinimum = False
				if isLocalMinimum:
					result_1 += heightmap[i][j] + 1

		print("\nResult Part 1: " + str(result_1))

		# Solution for part 2
		sizes = []

		for i in range(0, len(heightmap)):
			for j in range(0, len(heightmap[0])):
				if heightmap[i][j] != -2:
					isLocalMinimum = True
					if not (i == 0 or heightmap[i][j] < heightmap[i-1][j]):
						isLocalMinimum = False
					if not (i == len(heightmap)-1 or heightmap[i][j] < heightmap[i+1][j]):
						isLocalMinimum = False
					if not (j == 0 or heightmap[i][j] < heightmap[i][j-1]):
						isLocalMinimum = False
					if not (j == len(heightmap[0])-1 or heightmap[i][j] < heightmap[i][j+1]):
						isLocalMinimum = False
					if isLocalMinimum:
						# found start of a basin
						heightmap[i][j] = -1
						worked = True
						# while we discover a connected field, continue
						# a field connected to the current basin is marked with a -1
						while worked:
							worked = False
							for k in range(0, len(heightmap)):
								for l in range(0, len(heightmap[0])):
									if heightmap[k][l] == -1:
										result_x = findBasinLine(
											heightmap[k, :], l)
										if result_x[1]:
											# we found a connected field
											worked = True
											heightmap[k] = result_x[0]
										result_y = findBasinLine(
											heightmap[:, l], k)
										if result_y[1]:
											# we found a connected field
											worked = True
											heightmap[:, l] = result_y[0]
						# append the size of the current basin
						sizes.append(len(heightmap[heightmap == -1]))
						# mark all tackled basins with -2
						heightmap[heightmap == -1] = -2
						# print(heightmap)

		# get the largest basins
		sizes.sort(reverse=True)

		print("\nThree largest basins are: " +
			  str(sizes[0:3]) + "\nMultiplied: " + str(sizes[0] * sizes[1] * sizes[2]))

		executionTime = round(time.time() - startTime, 2)
		print("Execution time in seconds: " + str(executionTime))


if __name__ == "__main__":
	main()
