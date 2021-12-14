from datetime import date
import numpy as np
import time
import pprint

from importlib.machinery import SourceFileLoader

lib = SourceFileLoader("lib", "lib.py").load_module()

from aocd import get_data
from aocd import submit

day = 16
path = ""


def parseInput(input):
    result = None

    return result


def part1(data, measure):
    startTime = time.time()
    result_1 = None

    input = parseInput(data)

    executionTime = round(time.time() - startTime, 2)
    if measure:
        print("Part 1 took: " + str(executionTime) + " seconds\n")
    return result_1


def part2(data, measure):
    startTime = time.time()
    result_2 = None

    input = parseInput(data)

    executionTime = round(time.time() - startTime, 2)
    if measure:
        print("Part 2 took: " + str(executionTime) + " seconds\n")
    return result_2


def runTests(test_sol, path):
    test_res = []

    paths = lib.getTestPaths(path)

    # run tests
    for path in paths:
        test_res.append(part1(lib.getDataLines(path), False))

    for path in paths:
        test_res.append(part2(lib.getDataLines(path), False))

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


def main():
    global path
    path = "Day " + str(day) + "/"

    test_sol = []  # todo

    test = True
    sol1 = False  # todo
    sol2 = False  # todo

    if test:
        runTests(test_sol, path)

    data_main = get_data(day=day, year=2021).splitlines()

    if sol1:
        result_1 = part1(data_main, True)
        print("Result Part 1: " + str(result_1))

    if sol2:
        result_2 = part2(data_main, True)
        print("Result Part 2: " + str(result_2))

    print("\n")

    # submit(result_1, part="a", day=day, year=2021)
    # submit(result_2, part="b", day=day, year=2021)


if __name__ == "__main__":
    main()

