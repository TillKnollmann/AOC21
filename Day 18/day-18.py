from datetime import date
import numpy as np
import time
import ast
import math

from copy import deepcopy

from importlib.machinery import SourceFileLoader

lib = SourceFileLoader("lib", "lib.py").load_module()

from aocd import get_data
from aocd import submit

day = 18
path = ""


class SnailFishNumber:
    """Represents one snail fish number

    """

    # The number in a representation: (element, depth), ...
    content: list

    def __init__(self):
        """Constructor
        """
        content = []
        levels = []

    def set_string_content(self, content: str):
        self.set_content_from_string(content)

    def set_content(self, content: list):
        self.content = content

    def set_content_from_string(self, input: str):
        """sets the content of this object by a string representing a nested list

        Args:
            input (str): a string representation of a nested list
        """

        # parse list
        list_input = ast.literal_eval(input)
        self.content = list(self.get_level_elem(list_input))

    def __str__(self):
        # generate string representation
        return str(self.content)

    def generate_levels(self):
        self.levels = self.get_level(self.content)

    def get_level_elem(self, l: list, depth=-1) -> list:
        """Calculates the set of elements in l and returns a list of (element, depth) 

        Args:
            l ([list]): [description]
            depth (int, optional): [description]. Defaults to -1.

        Yields:
            [list]: a list containing the elements and their depths in the order of l
        """
        if not isinstance(l, list):
            yield [l, depth]
        else:
            for sublist in l:
                yield from self.get_level_elem(sublist, depth + 1)

    def explode(self, print_it=False) -> bool:
        """Applies one explode step and returns if explode was applied

        Args:
            print_it (bool, optional): Whether or not to print debug output. Defaults to False.

        Returns:
            bool: If an explode step was applied
        """

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
        """Tries to apply a split step. Returns true if one step was applied.

        Args:
            print_it (bool, optional): Whether or not to print debug output. Defaults to False.

        Returns:
            bool: If a split step was applied
        """
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
                self.content = new_list.copy()
                break
        if done and print_it:
            print("Result: " + str(self.content))
        return done

    def reduce(self):
        """Reduced the object by applying as many explode and split steps as possible
        """
        action_done = True
        while action_done:
            action_done = self.explode()
            if not action_done:
                action_done = self.split()

    def __copy__(self):
        res = SnailFishNumber()
        res.set_content(self.content.copy())
        return res

    def get_magnitude(self) -> int:
        """Returns the magnitude of this snail fish number

        Returns:
            int: the magnitude
        """

        # do not work on the acutal data
        mag = self.content.copy()
        while len(mag) > 1:
            mag_backup = mag.copy()
            find = True
            i = 0
            while find and i < len(mag) - 1:
                if mag[i][1] == mag[i + 1][1]:
                    # pair found -> Merge them
                    list_new = (
                        mag[0:i]
                        + [[3 * mag[i][0] + 2 * mag[i + 1][0], mag[i][1] - 1]]
                        + mag[i + 2 :]
                    )
                    mag = list_new.copy()
                    find = False
                i = i + 1
            # print(str(mag))
            if mag_backup == mag and len(mag) != 1:
                raise Exception("Error")
        return mag[0][0]


def add(num_A: SnailFishNumber, num_B: SnailFishNumber) -> SnailFishNumber:
    """Adds two snail fish numbers and returns the reduced result

    Args:
        num_A (SnailFishNumber): First snail fish number
        num_B (SnailFishNumber): Second snail fish number

    Raises:
        Exception: Error if both numbers are None

    Returns:
        SnailFishNumber: The reduced addition of both numbers
    """

    # print("\nAdding " + str(num_A) + " and " + str(num_B))

    if not num_A and not num_B:
        raise Exception("Adding two Snail Fish Numbers which are None")
    elif not num_A:
        return num_B
    elif not num_B:
        return num_A

    # increase the depth for every element

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

    # print("Result is " + str(num))

    return num


def parseInput(input: list) -> list:
    """Parses the input and returns a set of SnailFishNumbers

    Args:
        input ([list]): A list of string representations of nested lists   

    Returns:
        list: A list of SnailFishNumbers. One per input element. 
    """
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

    # add all snail fish numbers

    res = None
    for sf_number in input:
        res = add(res, sf_number)

    # get final magnitude
    result_1 = res.get_magnitude()

    executionTime = round(time.time() - startTime, 2)
    if measure:
        print("\nPart 1 took: " + str(executionTime) + " s")
    return result_1


def get_max_magnitude(sf_1: SnailFishNumber, sf_2: SnailFishNumber) -> int:
    """Calculates the maximum magnitude when adding sf_1 and sf_2 in any order

    Args:
        sf_1 (SnailFishNumber): First snail fish number
        sf_2 (SnailFishNumber): Second snail fish number

    Returns:
        int: The maximum magnitude that can be achieved when adding both numbers
    """
    if sf_1.content == sf_2.content:
        return 0

    res_1 = add(deepcopy(sf_1), deepcopy(sf_2))
    res_2 = add(deepcopy(sf_2), deepcopy(sf_1))

    mag_1 = res_1.get_magnitude()
    mag_2 = res_2.get_magnitude()

    return max(mag_1, mag_2)


def part2(data, measure=False):
    startTime = time.time()
    result_2 = None

    input = parseInput(data)

    possibilities = [(x, y) for x in input for y in input]

    results = [
        get_max_magnitude(possibilities[i][0], possibilities[i][1])
        for i in range(len(possibilities))
    ]

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

    sol1 = sub1 = True  # Todo
    sol2 = sub2 = True  # Todo

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

