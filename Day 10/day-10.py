import numpy as np
import time
import math

path = "Day 10/input.txt"

# points for missing closing parenthesis
points = {")": 3, "]": 57, "}": 1197, ">": 25137}

# points for completions
compl_points = {")": 1, "]": 2, "}": 3, ">": 4}

opening = ["(", "[", "{", "<"]
closing = [")", "]", "}", ">"]


def calculatePointsPartTwo(compl_string):
    """ Returns the completion score based on the completion string """
    result = 0
    for char in compl_string[::-1]:
        result *= 5
        result += compl_points[char]
    return result


def processLinePart(line: str):
    """ Processes a line
    Returns the points if the line is corrupt,
    returns -1 if the line is incomplete,
    returns 0 if the line is correct.
    The stack of missing parenthesis is appended and returned as well """
    line = line.replace("\n", "")
    stack = []
    for char in line:
        if char in opening:
            # append the respective closing tag
            stack.append(closing[opening.index(char)])
        elif char in closing:
            if len(stack) > 0 and stack[len(stack) - 1] == char:
                # remove the last element of the stack
                if len(stack) > 1:
                    stack = stack[0 : len(stack) - 1]
                else:
                    stack = []
            else:
                # line is corrupt
                return (points[char], stack)
    if len(stack) > 0:
        # line is incomplete
        return (-1, stack)
    # line is complete
    return (0, [])


def main():
    with open(path, "r") as file:
        startTime = time.time()
        lines = file.readlines()

        result_1 = 0
        results_2 = []
        for line in lines:
            temp = processLinePart(line)
            if temp[0] > 0:
                result_1 += temp[0]
            elif temp[0] == -1:
                results_2.append(calculatePointsPartTwo(temp[1]))

        print("\nResult Part 1: " + str(result_1))

        results_2.sort()

        print("\nResult Part 2: " + str(results_2[math.floor(len(results_2) / 2.0)]))

        executionTime = round(time.time() - startTime, 2)
        print("Execution time in seconds: " + str(executionTime))


if __name__ == "__main__":
    main()

