import numpy as np
import time

path = "Day 8/input.txt"

def parsePut(put):
	array = np.array(put.replace('\n', '').strip().split(' '))
	for i in range(0,len(array)):
		array[i] = str("".join(sorted(array[i])))
	return array

def processEntryPartOne(line):
	mapping = ['']*10
	input = parsePut(line.split('|')[0])
	output = parsePut(line.split('|')[1])
	length_checker = np.vectorize(len)
	mapping[1] = input[length_checker(input)==2][0]
	mapping[4] = input[length_checker(input)==4][0]
	mapping[7] = input[length_checker(input)==3][0]
	mapping[8] = input[length_checker(input)==7][0]
	return len(output[(output == mapping[1]) | (output == mapping[4]) | (output == mapping[7]) | (output == mapping[8])])

def substract(a, b):  
	result = a
	for char in b:
		result = result.replace(char, '')
	return result

def processEntryPartTwo(line):
	mapping = ['']*10
	input = parsePut(line.split('|')[0])
	output = parsePut(line.split('|')[1])
	length_checker = np.vectorize(len)
	mapping[1] = input[length_checker(input)==2][0]
	mapping[4] = input[length_checker(input)==4][0]
	mapping[7] = input[length_checker(input)==3][0]
	mapping[8] = input[length_checker(input)==7][0]

	character_mapping = ['']*7
	# first is the difference between 1 and 7
	character_mapping[0] = substract(mapping[1], mapping[7])
	# get candidate for 2
	candidates = input[length_checker(input)==5]
	for candidate in candidates:
		temp = substract(substract(candidate, mapping[4]), mapping[7])
		if len(temp) ==2:
			# this is the 2
			mapping[2] = candidate
	# get the 3
	candidates = candidates[candidates!=mapping[2]]
	for candidate in candidates:
		temp = substract(candidate, mapping[2])
		if len(temp)==1:
			# this is the 3
			mapping[3] = candidate
			character_mapping[5] = temp
	# get the 5
	mapping[5] = (candidates[candidates!=mapping[3]])[0]
	# get the 9
	candidates = input[length_checker(input)==6]
	for candidate in candidates:
		temp = substract(candidate, mapping[3])
		if len(temp)==1:
			# this is the 9
			mapping[9] = candidate
			character_mapping[1] = temp
	# get candidates for 0
	candidates = candidates[candidates!=mapping[9]]
	for candidate in candidates:
		temp = substract(candidate, mapping[1])
		if len(temp)==4:
			# this is the 0
			mapping[0] = candidate
		else:
			# this is the 6
			mapping[6] = candidate
	output_string = ""
	for out in output:
		for i in range(0,10):
			if out == mapping[i]: 
				output_string += str(i)
	#print(mapping)
	print("\n" + str(int(output_string)) + " " + str(mapping))
	return int(output_string)

def main():
	with open(path, "r") as file:
		startTime = time.time()
		lines = file.readlines()

		result_1 = 0
		for line in lines:
			result_1 += processEntryPartOne(line)

		print("\nResult Part 1: " + str(result_1))

		result_2 = 0
		for line in lines:
			result_2 += processEntryPartTwo(line)

		print("\nResult Part 2: " + str(result_2))

		executionTime = round(time.time() - startTime, 2)
		print("Execution time in seconds: " + str(executionTime))

if __name__ == "__main__":
	main()