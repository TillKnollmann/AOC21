from datetime import date
import numpy as np
import time
import pprint
import math

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
        mapping[temp[0].strip()] = temp[1].strip()

    result.append(mapping)

    return result


def processData(input_string, mapping):
    result = ""
    for i in range(0, len(input_string) - 1):
        try:
            result += input_string[i]
            to_add = mapping["" + input_string[i] + input_string[i + 1]]
            result += to_add
        except KeyError:
            lol = ""
    result += input_string[len(input_string) - 1]

    return result


def processDataFast(current_res, mapping):
    # new pairs will be here
    new_dict = {}

    for entry in current_res:
        if entry in mapping:
            # get the first new pair
            new_entry_1 = str(entry)[0] + str(mapping[entry])
            # get the second new pair
            new_entry_2 = str(mapping[entry]) + str(entry)[1]
            # count both new pairs in new_dict
            if not new_entry_1 in new_dict:
                new_dict[new_entry_1] = 0
            if not new_entry_2 in new_dict:
                new_dict[new_entry_2] = 0
            new_dict[new_entry_1] += current_res[entry]
            new_dict[new_entry_2] += current_res[entry]

    return new_dict.copy()


def part1(data, measure):
    # run for 10 iterations
    return processIterations(data, measure, 10)


def part2(data, measure):
    # run for 40 iterations
    return processIterations(data, measure, 40)


def processIterations(data, measure, iterations):

    # parse the data
    input = parseInput(data)

    # initial string
    current_string = input[0]

    # possible replacement rules
    mapping = input[1]

    count = {}

    # count the initial pairs
    for i in range(0, len(current_string) - 1):
        entry = current_string[i] + current_string[i + 1]
        if not entry in count:
            count[entry] = 1
        else:
            count[entry] += 1

    current_res = count

    for i in range(0, iterations):
        # process all iterations
        current_res = processDataFast(current_res, mapping)

    # count each element
    count_result = {}

    for entry in current_res:
        if not str(entry)[0] in count_result:
            count_result[str(entry)[0]] = 0
        if not str(entry)[1] in count_result:
            count_result[str(entry)[1]] = 0
        count_result[str(entry)[0]] += current_res[entry]
        count_result[str(entry)[1]] += current_res[entry]

    # we overestimate each element by a factor of two
    for entry in count_result:
        count_result[entry] = math.ceil(count_result[entry] / 2.0)

    # count max occurrence and min occurrence
    return (
        count_result[max(count_result.keys(), key=(lambda new_k: count_result[new_k]))]
        - count_result[
            min(count_result.keys(), key=(lambda new_k: count_result[new_k]))
        ]
    )


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

    # enter test solutions here
    test_sol = [1588, 2188189693529]

    test = True
    sol1 = True
    sol2 = True

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
