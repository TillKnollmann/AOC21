from datetime import date
from typing import ChainMap
import numpy as np
import time
import pprint

from tqdm import tqdm

from importlib.machinery import SourceFileLoader

lib = SourceFileLoader("lib", "lib.py").load_module()

from aocd import get_data
from aocd import submit

day = 22
path = ""


def parseInput(input):
    result = []

    min_x = min_y = min_z = 0
    max_x = max_y = max_z = 0

    for line in input:
        current_line = line.replace("\n", "").strip().split(" ")
        command = current_line[0]
        ranges = current_line[1].split(",")
        range_x = None
        range_y = None
        range_z = None
        for range in ranges:
            values = range[2:].split("..")
            values = tuple([int(x) for x in values])
            if range[0] == "x":
                range_x = values
                min_x = min(min_x, min(values))
                max_x = max(max_x, max(values))
            elif range[0] == "y":
                range_y = values
                min_y = min(min_y, min(values))
                max_y = max(max_y, max(values))
            elif range[0] == "z":
                range_z = values
                min_z = min(min_z, min(values))
                max_z = max(max_z, max(values))
        result.append((command, range_x, range_y, range_z))

    return result, (min_x, max_x), (min_y, max_y), (min_z, max_z)


def process_command(
    command: tuple,
    cores: np.array,
    offset_x: int,
    offset_y: int,
    offset_z: int,
    area: tuple,
) -> np.array:

    if (
        command[1][1] < area[0][0]
        or command[2][1] < area[1][0]
        or command[3][1] < area[2][0]
    ):
        return cores
    if (
        command[1][0] > area[0][1]
        or command[2][0] > area[1][1]
        or command[3][0] > area[2][1]
    ):
        return cores

    new_bounds = [
        (
            max(0, command[1][0] + offset_x),
            min(area[0][1] + offset_x, command[1][1] + offset_x,),
        ),
        (
            max(0, command[2][0] + offset_y),
            min(area[1][1] + offset_y, command[2][1] + offset_y),
        ),
        (
            max(0, command[3][0] + offset_z),
            min(area[2][1] + offset_z, command[3][1] + offset_z),
        ),
    ]

    # print(command)

    # print(new_bounds)

    # prepare array
    applier = np.zeros(
        (
            new_bounds[0][1] - new_bounds[0][0] + 1,
            new_bounds[1][1] - new_bounds[1][0] + 1,
            new_bounds[2][1] - new_bounds[2][0] + 1,
        ),
        dtype=np.int8,
    )
    if command[0] == "on":
        applier = applier + 1

    # apply array on cores
    cores[
        new_bounds[0][0] : new_bounds[0][1] + 1,
        new_bounds[1][0] : new_bounds[1][1] + 1,
        new_bounds[2][0] : new_bounds[2][1] + 1,
    ] = applier

    # normalize cores
    # cores[cores > 1] = 1

    return cores


def apply_command(command: tuple, lamps_on: set) -> set:
    if command[0] == "on":
        points = set(
            [
                (x, y, z)
                for x in range(command[1][0], command[1][1] + 1)
                for y in range(command[2][0], command[2][1] + 1)
                for z in range(command[3][0], command[3][1] + 1)
            ]
        )
        lamps_on = lamps_on.union(points)
    elif command == "off":
        points = set(
            [
                (x, y, z)
                for x in range(command[1][0], command[1][1] + 1)
                for y in range(command[2][0], command[2][1] + 1)
                for z in range(command[3][0], command[3][1] + 1)
            ]
        )
        lamps_on = lamps_on - points
    return lamps_on


def get_on_lamps_in_area(commands: tuple, area: tuple):
    offset_x = -area[0][0]
    offset_y = -area[1][0]
    offset_z = -area[2][0]

    cores = np.zeros(
        (
            area[0][1] + offset_x + 1,
            area[1][1] + offset_y + 1,
            area[2][1] + offset_z + 1,
        ),
        dtype=np.int8,
    )

    for command in commands:
        cores = process_command(command, cores, offset_x, offset_y, offset_z, area)

    return np.sum(cores)


def part1(data, measure=False):
    startTime = time.time()
    result_1 = None

    commands, x_range, y_range, z_range = parseInput(data)

    area = ((-50, 50), (-50, 50), (-50, 50))

    result_1 = get_on_lamps_in_area(commands, area)

    executionTime = round(time.time() - startTime, 2)
    if measure:
        print("\nPart 1 took: " + str(executionTime) + " s")
    return result_1


def part2(data, measure=False):
    startTime = time.time()
    result_2 = None

    commands, x_range, y_range, z_range = parseInput(data)

    # Todo program part 2

    executionTime = round(time.time() - startTime, 2)
    if measure:
        print("\nPart 2 took: " + str(executionTime) + " s")
    return result_2


def runTests(test_sol, path):
    test_res = []

    all_check = True

    paths = lib.getTestPaths(path)

    test_res += list(map(part1, map(lib.getDataLines, paths)))
    # test_res += list(map(part2, map(lib.getDataLines, paths)))

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

    test_sol = [39, 590784]  # Todo put in test solutions

    test = True  # Todo

    sol1 = sub1 = True  # Todo
    sol2 = sub2 = False  # Todo

    if test:
        if not runTests(test_sol, path):
            sub1 = sub2 = False

    # run test for part 2
    test_data = lib.getDataLines(path + "test3.txt")
    test_res = part2(test_data)
    if test_res != 2758514936282235:
        print(
            "Test for part 2 failed! Expected: "
            + str(2758514936282235)
            + " received "
            + str(test_res)
        )
        sub2 = False
    else:
        print("Test for part 2 succeeded!")

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

