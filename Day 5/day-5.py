import numpy as np
import time

path = "Day 5/input.txt"

def getLineFromString(line: str):
	"""Returns a 2 dim numpy array containing the line
	The first coordinate contains x_1, x_2,
	The second coordinate contains y_1, y_2
	"""
	temp = line.replace('\n', '').split(sep=" -> ")
	A = np.array(temp[0].split(sep=","), dtype=np.int32)
	B = np.array(temp[1].split(sep=","), dtype=np.int32)
	return np.array([[A[0], B[0]],[A[1], B[1]]])

def isLineValid(line, ignoreDiagonal):
	"""Returns true if the line is not horizontal, vertical 
	or (if ignoreDiagonal) diagonal in 45 degree
	"""
	if ignoreDiagonal:
		if line[0,0] == line[0,1] or line[1,0] == line[1,1]:
			return True
		else:
			return False
	else:
		if line[0,0] == line[0,1] or line[1,0] == line[1,1]:
			return True # Line is not diagonal
		elif abs(line[0,1] - line[0,0]) == abs(line[1,1] - line[1,0]):
			return True
		else:
			return False

def generateSpace(lines):
	"""Generates an empty 2d numpy array 
	where all lines fit in
	"""
	max_x = max(lines[:,0,:].reshape(-1)) + 1
	max_y = max(lines[:,1,:].reshape(-1)) + 1
	print("Space size: " + str(max_x) + "x" + str(max_y))
	return np.zeros((max_y, max_x))

def embedLineInSpace(line, space):
	"""Draws a line into the space array
	"""
	if line[0,0] == line[0,1] or line[1,0] == line[1,1]:
		# Draw horizontal/vertical lines
		for x in range(min(line[0,0], line[0,1]), max(line[0,0], line[0,1]) + 1):
			for y in range(min(line[1,0], line[1,1]), max(line[1,0], line[1,1]) + 1):
				space[y,x] += 1
	else:
		# Draw diagonal lines
		x = line[0,0]
		orient_x = 1
		y = line[1,0]
		orient_y = 1
		if line[0,0] > line[0,1]:
			orient_x = -1
		if line[1,0] > line[1,1]:
			orient_y = -1
		for i in range(0, abs(line[0,1] - line[0,0])+1):
			space[y + orient_y * i, x + orient_x * i] += 1
	return space

def getScore(space):
	"""Returns at how many positions in the space
	at least two lines are located
	"""
	return len(space[space>=2])

def main():
	with open(path, "r") as file:

		# whether or not to include 45 degree diagonal lines
		ignoreDiagonal = False

		startTime = time.time()
		lines = file.readlines()

		coordinates = []

		# parse the input and filter invalid lines
		for line in lines:
			coordinate = getLineFromString(line)
			if isLineValid(coordinate, ignoreDiagonal):
				coordinates.append(coordinate)

		coordinates = np.array(coordinates)

		# create the 2d space
		space = generateSpace(coordinates)

		# populate the space with the lines
		for line in coordinates:
			space = embedLineInSpace(line, space)

		# output
		print(space)

		print(str(getScore(space)) + " points with at least 2 lines")
		executionTime = round(time.time() - startTime, 2)
		print("Execution time in seconds: " + str(executionTime))

if __name__ == "__main__":
	main()