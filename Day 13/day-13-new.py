from datetime import date
from unittest import result
import numpy as np
import time
import pprint
import os
import unittest

from aocd import get_data
from aocd import submit

day = 13
path = ""


def parseInput(lines):
    points = []
    instructions = []

    # parse input
    isInput = True
    for line in lines:
        cleaned = line.replace("\n", "")
        if isInput:
            if len(cleaned) == 0:
                isInput = False
            else:
                point = np.array(cleaned.split(","), dtype=int)
                points.append(point)
        else:
            instr = cleaned.split(" ")[2]
            instr = np.array(instr.split("="))
            instructions.append(instr)

    points = np.array(points)
    return (points, instructions)


def printMatrix(matrix):
    output = matrix.copy().astype("str")
    output[output == "0.0"] = " "
    output[output == "1.0"] = "#"
    output[output == "-1.0"] = "O"

    print("")
    for i in range(0, len(output)):
        line = ""
        for j in range(0, len(output[0])):
            line += str(output[i, j])
        print(line)


def getDataLines(path: str) -> list:
    with open(path, "r") as file:
        lines = file.readlines()
    lines = [lines[i].replace("\n", "") for i in range(0, len(lines))]
    return lines


def getTestPaths() -> list:
    paths = []
    for root, dirs, files in os.walk(path):
        # select file name
        for file in files:
            # check the extension of files
            if file.endswith(".txt"):
                # print whole path of files
                paths.append(os.path.join(root, file))
    return paths


def part1(data, measure):
    startTime = time.time()
    result_1 = None

    input = parseInput(data)

    points = input[0]
    instructions = input[1]

    # build initial matrix
    matrix = np.zeros((max(points[:, 1]) + 1, max(points[:, 0]) + 1))

    for point in points:
        matrix[point[1], point[0]] = 1

    for instruction in instructions:

        if instruction[0] == "y":
            # rotate the matrix leftwise
            matrix = np.rot90(matrix, 1).copy()

        # split matrix
        left_part = matrix[:, 0 : int(instruction[1])].copy()

        # fill right part with trailing zeros
        right_part = matrix[:, int(instruction[1]) + 1 :].copy()
        temp = np.zeros(left_part.shape)
        temp[:, 0 : len(right_part[0])] = right_part
        right_part = temp.copy()

        # flip the right part
        right_part = np.fliplr(right_part)

        # fold
        matrix = left_part + right_part
        # rotate back
        if instruction[0] == "y":
            matrix = np.rot90(matrix, 3).copy()

        # normalize
        matrix[matrix >= 1] = 1

        # determine result part 1
        if result_1 is None:
            result_1 = sum(matrix[matrix > 0])
            break

    executionTime = round(time.time() - startTime, 2)
    if measure:
        print("Part 1 took: " + str(executionTime) + " seconds\n")
    return result_1


def part2(data, measure):
    startTime = time.time()
    result_2 = None

    input = parseInput(data)

    points = input[0]
    instructions = input[1]

    # build initial matrix
    matrix = np.zeros((max(points[:, 1]) + 1, max(points[:, 0]) + 1))

    for point in points:
        matrix[point[1], point[0]] = 1

    for instruction in instructions:

        if instruction[0] == "y":
            # rotate the matrix leftwise
            matrix = np.rot90(matrix, 1).copy()

        # split matrix
        left_part = matrix[:, 0 : int(instruction[1])].copy()

        # fill right part with trailing zeros
        right_part = matrix[:, int(instruction[1]) + 1 :].copy()
        temp = np.zeros(left_part.shape)
        temp[:, 0 : len(right_part[0])] = right_part
        right_part = temp.copy()

        # flip the right part
        right_part = np.fliplr(right_part)

        # fold
        matrix = left_part + right_part
        # rotate back
        if instruction[0] == "y":
            matrix = np.rot90(matrix, 3).copy()

        # normalize
        matrix[matrix >= 1] = 1

        result_2 = sum(matrix[matrix > 0])

    # print result
    printMatrix(matrix)

    executionTime = round(time.time() - startTime, 2)
    if measure:
        print("Part 2 took: " + str(executionTime) + " seconds\n")
    return result_2


def main():

    global path
    path = "Day " + str(day) + "/"

    # enter test solutions here
    test_sol = [17]

    test_res = []

    # run tests
    for path in getTestPaths():
        test_res.append(part1(getDataLines(path), False))
    for path in getTestPaths():
        test_res.append(part2(getDataLines(path), False))

    for i in range(0, len(test_sol)):
        output = "Test " + str(i + 1)
        if test_sol[i] == test_res[i]:
            output += " Success!"
        else:
            output += (
                " Failed! Expected "
                + str(test_sol[i])
                + " received "
                + str(test_res[i])
            )
        print(output)

    print("\n")

    data_main = get_data(day=day, year=2021).splitlines()

    result_1 = part1(data_main, True)
    result_2 = part2(data_main, True)

    print("\nResult Part 1: " + str(result_1))
    print("\nResult Part 2: " + str(result_2))

    # submit(result_1, part="a", day=day, year=2021)
    # submit(result_2, part="b", day=day, year=2021)


if __name__ == "__main__":
    main()

