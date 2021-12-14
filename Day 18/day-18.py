from datetime import date
from unittest import result
import numpy as np
import time
import pprint
import os
import unittest

from aocd import get_data
from aocd import submit

day = 18
path = ""


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

    executionTime = round(time.time() - startTime, 2)
    if measure:
        print("Part 1 took: " + str(executionTime) + " seconds\n")
    return result_1


def part2(data, measure):
    startTime = time.time()
    result_2 = None

    executionTime = round(time.time() - startTime, 2)
    if measure:
        print("Part 2 took: " + str(executionTime) + " seconds\n")
    return result_2


def main():

    global path
    path = "Day " + str(day) + "/"

    # enter test solutions here
    test_sol = []

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

