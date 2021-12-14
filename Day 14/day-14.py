from datetime import date
import numpy as np
import time
import pprint

from importlib.machinery import SourceFileLoader

from numpy.core.records import array

lib = SourceFileLoader("lib", "lib.py").load_module()

from aocd import get_data
from aocd import submit

day = 14
path = ""


def parseInput(data):
    result = []
    result.append(data[0].replace("\n", ""))

    mapping = {}

    for i in range(2, len(data)):
        temp = data[i].split("->")
        if not temp[0].strip() in mapping:
            mapping[temp[0].strip()] = []
        mapping[temp[0].strip()].append(temp[1].strip())

    result.append(mapping)

    return result


def processData(input_string, mapping):
    result = ""
    for i in range(0, len(input_string) - 1):
        try:
            result += input_string[i]
            to_add = mapping["" + input_string[i] + input_string[i + 1]]
            result += to_add[0]
        except KeyError:
            lol = ""
    result += input_string[len(input_string) - 1]

    return result


def part1(data, measure):
    startTime = time.time()
    result_1 = None

    input = parseInput(data)

    current_string = input[0]

    for i in range(0, 10):
        current_string = processData(current_string, input[1])

    char_array = [current_string[i] for i in range(0, len(current_string))]

    result = np.unique(np.array(char_array), return_counts=True)

    result_1 = max(result[1]) - min(result[1])

    # print(input[0])
    # print(input[1])

    executionTime = round(time.time() - startTime, 2)
    if measure:
        print("Part 1 took: " + str(executionTime) + " seconds\n")
    return result_1


def part2(data, measure):
    startTime = time.time()
    result_2 = None

    input = parseInput(data)

    current_string = input[0]

    for i in range(0, 10):
        current_string = processData(current_string, input[1])

    char_array = [current_string[i] for i in range(0, len(current_string))]

    result = np.unique(np.array(char_array), return_counts=True)

    result_2 = max(result[1]) - min(result[1])

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

    print("\n")


def main():

    global path
    path = "Day " + str(day) + "/"

    # enter test solutions here
    test_sol = [1588, 2188189693529]

    # runTests(test_sol, path)

    data_main = get_data(day=day, year=2021).splitlines()

    # result_1 = part1(data_main, True)
    result_2 = part2(data_main, True)

    # print("\nResult Part 1: " + str(result_1))
    print("\nResult Part 2: " + str(result_2))

    # submit(result_1, part="a", day=day, year=2021)
    # submit(result_2, part="b", day=day, year=2021)


if __name__ == "__main__":
    main()

