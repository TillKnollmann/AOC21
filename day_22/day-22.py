from datetime import date
from typing import ChainMap
import numpy as np
import time
import pprint

from copy import deepcopy

from tqdm import tqdm

from importlib.machinery import SourceFileLoader

lib = SourceFileLoader("lib", "lib.py").load_module()

from aocd import get_data
from aocd import submit

day = 22
path = ""


def parseInput(input):
    """Parses the input and returns a list of commands that contain the ranges

    Args:
        input (list): List of strings

    Returns:
        list: List of commands
    """
    result = []

    # calculate area in which commands apply
    min_x = min_y = min_z = 0
    max_x = max_y = max_z = 0

    for line in input:
        current_line = line.replace("\n", "").strip().split(" ")
        # get command
        command = current_line[0]
        ranges = current_line[1].split(",")
        range_x = None
        range_y = None
        range_z = None
        # get ranges
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
    """Processes a command on a core array with the given offsets within the given area

    Args:
        command (tuple): The command
        cores (np.array): The cores on which we work
        offset_x (int): The offset in x direction
        offset_y (int): The offset in y direction
        offset_z (int): The offset in z direction
        area (tuple): The area which we only consider for commands

    Returns:
        np.array: The resulting core array
    """
    # if the command applies outside of the area, do nothing
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

    # get the bounds of the command mapped by the offsets
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

    return cores


def get_on_lamps_in_area(commands: tuple, area: tuple):
    """Process all commands and get the number of lamps which are on in the given area

    Args:
        commands (tuple): The commands
        area (tuple): The area of interest

    Returns:
        int: The number of lamps which are on in the given area after applying the commands
    """

    # calculate offsets
    offset_x = -area[0][0]
    offset_y = -area[1][0]
    offset_z = -area[2][0]

    # generate set of cores of interest
    cores = np.zeros(
        (
            area[0][1] + offset_x + 1,
            area[1][1] + offset_y + 1,
            area[2][1] + offset_z + 1,
        ),
        dtype=np.int8,
    )

    # apply the commands
    for command in commands:
        cores = process_command(command, cores, offset_x, offset_y, offset_z, area)

    return np.sum(cores)


def get_volume(cube: tuple) -> int:
    """Returns the volume of a given cube

    Args:
        cube (tuple): A 3D cube

    Returns:
        int: The volume of the cube
    """
    return int(
        (cube[0][1] - cube[0][0] + 1)
        * (cube[1][1] - cube[1][0] + 1)
        * (cube[2][1] - cube[2][0] + 1)
    )


def part1(data, measure=False):
    startTime = time.time()
    result_1 = None

    commands, x_range, y_range, z_range = parseInput(data)

    # define the area
    area = ((-50, 50), (-50, 50), (-50, 50))

    # process on the given area
    result_1 = get_on_lamps_in_area(commands, area)

    executionTime = round(time.time() - startTime, 2)
    if measure:
        print("\nPart 1 took: " + str(executionTime) + " s")
    return result_1


def part2(data, measure=False):
    startTime = time.time()
    result_2 = None

    commands, x_range, y_range, z_range = parseInput(data)

    # contains cubes where all lamps are on
    cubes = []

    bar = None

    if measure:
        bar = tqdm(total=len(commands))

    for command in commands:
        # get the cube of the command
        new_cube = command[1:]
        # print(new_cube)
        cubes_processed = []
        for cube in cubes:
            # check if there is an intersection
            if not (
                new_cube[0][1] < cube[0][0]
                or new_cube[0][0] > cube[0][1]
                or new_cube[1][1] < cube[1][0]
                or new_cube[1][0] > cube[1][1]
                or new_cube[2][1] < cube[2][0]
                or new_cube[2][0] > cube[2][1]
            ):
                # remove intersection and split the old cube
                intersection = (
                    (max(new_cube[0][0], cube[0][0]), min(new_cube[0][1], cube[0][1]),),
                    (max(new_cube[1][0], cube[1][0]), min(new_cube[1][1], cube[1][1]),),
                    (max(new_cube[2][0], cube[2][0]), min(new_cube[2][1], cube[2][1]),),
                )
                """ print(
                    "Cube "
                    + str(new_cube)
                    + " and "
                    + str(cube)
                    + " intersect in "
                    + str(intersection)
                ) """
                # get remaining fractions of the cube
                if cube[0][0] < intersection[0][0]:
                    cubes_processed.append(
                        (
                            (cube[0][0], intersection[0][0] - 1),
                            (cube[1][0], cube[1][1]),
                            (cube[2][0], cube[2][1]),
                        )
                    )
                if intersection[0][1] < cube[0][1]:
                    cubes_processed.append(
                        (
                            (intersection[0][1] + 1, cube[0][1]),
                            (cube[1][0], cube[1][1]),
                            (cube[2][0], cube[2][1]),
                        )
                    )
                if cube[1][0] < intersection[1][0]:
                    cubes_processed.append(
                        (
                            (intersection[0][0], intersection[0][1]),
                            (cube[1][0], intersection[1][0] - 1),
                            (cube[2][0], cube[2][1]),
                        )
                    )
                if intersection[1][1] < cube[1][1]:
                    cubes_processed.append(
                        (
                            (intersection[0][0], intersection[0][1]),
                            (intersection[1][1] + 1, cube[1][1]),
                            (cube[2][0], cube[2][1]),
                        )
                    )
                if cube[2][0] < intersection[2][0]:
                    cubes_processed.append(
                        (
                            (intersection[0][0], intersection[0][1]),
                            (intersection[1][0], intersection[1][1]),
                            (cube[2][0], intersection[2][0] - 1),
                        )
                    )
                if intersection[2][1] < cube[2][1]:
                    cubes_processed.append(
                        (
                            (intersection[0][0], intersection[0][1]),
                            (intersection[1][0], intersection[1][1]),
                            (intersection[2][1] + 1, cube[2][1]),
                        )
                    )
            else:
                # the cube was intersection free
                cubes_processed.append(cube)

        if command[0] == "on":
            # add the current cube
            cubes_processed.append(new_cube)
        cubes = deepcopy(cubes_processed)
        if bar:
            bar.update(1)

    if bar:
        bar.close()

    # calculate total volume of all cubes (equals the lamps which are on since all cubes are disjoint)
    result_2 = 0
    for cube in cubes:
        result_2 += get_volume(cube)

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
    sol2 = sub2 = True  # Todo

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

