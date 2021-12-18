from datetime import date
import numpy as np
import time
import pprint
import ast
import math
from joblib import Parallel, delayed
from tqdm import tqdm
import os

import itertools
from importlib.machinery import SourceFileLoader

lib = SourceFileLoader("lib", "lib.py").load_module()

from aocd import get_data
from aocd import submit

day = 18
path = ""


class SnailFishNumber:

    content: list
    levels: list

    def __init__(self):  # constructor method
        content = []
        levels = []

    def set_string_content(self, content: str):
        self.set_content_from_string(content)

    def set_content(self, content: list):
        self.content = content

    def set_content_from_string(self, input: str):
        list_input = ast.literal_eval(input)
        # print(list(list_input))
        self.content = list(self.get_level_elem(list_input))
        # print(str(self.content))

    def __str__(self):
        # generate list representation
        return str(self.content)

    def generate_levels(self):
        self.levels = self.get_level(self.content)

    def get_level_elem(self, l, depth=-1):
        if not isinstance(l, list):
            yield [l, depth]
        else:
            for sublist in l:
                yield from self.get_level_elem(sublist, depth + 1)

    def get_level(self, l, depth=1):
        isLeaf = True
        for elem in l:
            if isinstance(elem, list):
                isLeaf = False
                break
        if isLeaf:
            yield (l, depth)
        else:
            for sublist in l:
                yield from self.get_level(sublist, depth + 1)

    def explode(self, print_it=False) -> bool:
        if print_it:
            print("\nExploding " + str(self.content))
        done = False
        # find list nested at depth 4
        i = 0
        while i < len(self.content) - 1:
            if self.content[i][1] == self.content[i + 1][1] and self.content[i][1] >= 4:
                done = True
                # depth 4 reached
                value_1 = self.content[i][0]
                value_2 = self.content[i + 1][0]
                if i > 0:
                    self.content[i - 1][0] += value_1
                if i < (len(self.content) - 2):
                    self.content[i + 2][0] += value_2
                self.content[i][0] = 0
                self.content[i][1] = self.content[i][1] - 1
                del self.content[i + 1]
                break
            elif self.content[i][1] == self.content[i + 1][1]:
                i = i + 2
            else:
                i = i + 1
        if done and print_it:
            print("Result: " + str(self.content))
        return done

    def split(self, print_it=False) -> bool:
        done = False
        if print_it:
            print("\nSplitting " + str(self.content))
        for i in range(len(self.content)):
            if self.content[i][0] >= 10:
                # split
                done = True
                value_left = math.floor(self.content[i][0] / 2.0)
                value_right = math.ceil(self.content[i][0] / 2.0)
                new_list = (
                    self.content[0:i]
                    + [[value_left, self.content[i][1] + 1]]
                    + [[value_right, self.content[i][1] + 1]]
                    + self.content[i + 1 :]
                )
                self.content = new_list
                break
        if done and print_it:
            print("Result: " + str(self.content))
        return done

    def reduce(self):
        action_done = True
        while action_done:
            action_done = self.explode()
            if not action_done:
                action_done = self.split()

    def get_magnitude(self):
        mag = self.content.copy()
        # print(str(mag))
        while len(mag) > 1:
            find = True
            i = 0
            while find and i < len(mag) - 1:
                if mag[i][1] == mag[i + 1][1]:
                    # pair found
                    list_new = (
                        mag[0:i]
                        + [[3 * mag[i][0] + 2 * mag[i + 1][0], mag[i][1] - 1]]
                        + mag[i + 2 :]
                    )
                    mag = list_new
                    find = False
                i = i + 1
        return mag[0][0]


def add(num_A: SnailFishNumber, num_B: SnailFishNumber) -> SnailFishNumber:

    if not num_A and not num_B:
        raise Exception("Adding two Snail Fish Numbers which are None")
    elif not num_A:
        return num_B
    elif not num_B:
        return num_A

    list_A = num_A.content.copy()
    for i in range(len(list_A)):
        list_A[i][1] += 1

    list_B = num_B.content.copy()
    for i in range(len(list_B)):
        list_B[i][1] += 1

    res = list_A + list_B

    num = SnailFishNumber()
    num.set_content(res)
    num.reduce()

    return num


def parseInput(input):
    result = []
    for value in input:
        sf_num = SnailFishNumber()
        sf_num.set_content_from_string(value)
        result.append(sf_num)
    return result


def part1(data, measure=False):
    startTime = time.time()
    result_1 = None

    input = parseInput(data)

    res = None
    for sf_number in input:
        res = add(res, sf_number)

    result_1 = res.get_magnitude()
    # print(res.get_magnitude())

    executionTime = round(time.time() - startTime, 2)
    if measure:
        print("\nPart 1 took: " + str(executionTime) + " s")
    return result_1


def get_max_magnitude(sf_1: SnailFishNumber, sf_2: SnailFishNumber) -> int:
    res_1 = add(sf_1, sf_2)
    res_2 = add(sf_2, sf_1)
    return max(res_1.get_magnitude(), res_2.get_magnitude())


def part2(data, measure=False):
    startTime = time.time()
    result_2 = None

    input = parseInput(data)

    cart_prod = [input, input]

    possibilities = [p for p in itertools.product(*cart_prod)]

    backend = "loky"
    results = Parallel(n_jobs=int(os.cpu_count()), backend=backend)(
        delayed(get_max_magnitude)(possibilities[i][0], possibilities[i][1])
        for i in tqdm(range(len(possibilities)))
    )

    # matrix = [add(sf_1, sf_2) for sf_1 in input for sf_2 in input if sf_1 != sf_2]

    # magnitudes = [sf.get_magnitude() for sf in results]

    result_2 = max(results)

    executionTime = round(time.time() - startTime, 2)
    if measure:
        print("\nPart 2 took: " + str(executionTime) + " s")
    return result_2


def runTests(test_sol, path):
    test_res = []

    all_check = True

    paths = lib.getTestPaths(path)

    test_res += list(map(part1, map(lib.getDataLines, paths)))
    test_res += list(map(part2, map(lib.getDataLines, paths)))

    success = [test_sol[i] == test_res[i] for i in range(len(test_sol))]

    for i in range(len(test_sol)):
        output = "Test " + str(i + 1)
        output = (
            "".join([output, " Success!"])
            if test_sol[i] == test_res[i]
            else "".join(
                [
                    output,
                    " Failed! Expected ",
                    str(test_sol[i]),
                    " received ",
                    str(test_res[i]),
                ]
            )
        )
        all_check = False if test_sol[i] != test_res[i] else all_check
        print(output)

    return all_check


def main():
    global path
    path = "Day " + str(day) + "/"

    test_sol = [4140, 3993]  # Todo put in test solutions

    test = True  # Todo

    sol1 = sub1 = False  # Todo
    sol2 = sub2 = False  # Todo

    if test:
        if not runTests(test_sol, path):
            sub1 = sub2 = False

    data_main = get_data(day=day, year=2021).splitlines()

    if sol1:
        result_1 = part1(data_main, True)
        print("Result Part 1: " + str(result_1))

    if sol2:
        result_2 = part2(data_main, True)
        print("Result Part 2: " + str(result_2))

    print("\n")

    if sub1:
        submit(int(result_1), part="a", day=day, year=2021)

    if sub2:
        submit(int(result_2), part="b", day=day, year=2021)


if __name__ == "__main__":
    main()

