from datetime import date
import numpy as np
import time
import pprint
import math

from importlib.machinery import SourceFileLoader

lib = SourceFileLoader("lib", "lib.py").load_module()

from aocd import get_data
from aocd import submit

day = 17
path = ""


def parseInput(input):
    """Parses the input for today's puzzle

    Args:
        input (list<str>): input array of length 1

    Returns:
        tuple<tuple,tuple>: valid area. First part is x dimension, second part y dimension
    """

    split = input[0].replace("\n", "").split(" ")

    t_area_x = (
        int(split[2].split("..")[0][2:]),
        int(split[2].split("..")[1][:-1]),
    )
    t_area_y = (int(split[3].split("..")[0][2:]), int(split[3].split("..")[1]))

    return (t_area_x, t_area_y)


def generatePosition(pos, vel):
    """Generates new positions based on a position vector and a veloctiy

    Args:
        pos (tuple<int,int>): current positions in x,y
        vel (tuple<int,int>): velocity vector

    Returns:
        tuple<tuple<int,int>,tuple<int,int>: new position and new velocity
    """
    pos_x, pos_y = pos
    vel_x, vel_y = vel
    new_pos = (pos_x + vel_x, pos_y + vel_y)
    new_vel = (vel_x - np.sign(vel_x), vel_y - 1)
    return (new_pos, new_vel)


def isInTarget(pos, area):
    """Returns True if pos is in area

    Args:
        pos (tuple): The current position
        area (tuple<tuple,tuple>): The bounds of the tarbet area

    Returns:
        bool: True if pos is in area
    """
    if area[0][0] <= pos[0] <= area[0][1] and area[1][0] <= pos[1] <= area[1][1]:
        return True
    return False


def isBeforeTarget(pos, area):
    """Returns False if the position cannot meet the area no matter how the velocity is

    Args:
        pos (tuple): current position
        area (tuple<tuple,tuple>): target area

    Returns:
        bool: False if it is impossible to meet the area from this position
    """
    if pos[0] > area[0][1]:
        # The x value is already too large
        return False
    elif pos[1] < area[1][0]:
        # The y value is already too small
        return False
    else:
        return True


def getHeighest(init_pos, init_vel, t_area, Print=False):
    """Simulates movement based on initial position and velocity and returns if the area is met and what the maximum height is

    Args:
        init_pos (tuple): initial position
        init_vel (tuple): initial velocity
        t_area (tuple<tuple>): target area
        Print (bool, optional): Whether to print logs. Defaults to False.

    Returns:
        tuple: value 1 is the maximum height, value 2 is whether t_area is met
    """

    highest_y = 0

    pos = init_pos
    vel = init_vel

    reaches = False

    while isBeforeTarget(pos, t_area):
        # get new position
        pos, vel = generatePosition(pos, vel)
        # update height
        highest_y = max(highest_y, pos[1])
        if isInTarget(pos, t_area):
            # set flag
            reaches = True
            if Print:
                print(str(init_vel) + " reaches target with height " + str(highest_y))

    if not reaches:
        if Print:
            print(str(init_vel) + " misses target with height " + str(highest_y))

    return highest_y, reaches


def gaus(n):
    """Returns the result of the gaussian sum

    Args:
        n (int): parameter

    Returns:
        int: gaussian sum of n
    """
    return (math.pow(n, 2) + n) / 2.0


def isXinArea(x, area):
    """Checks if x is in its bounds based on area

    Args:
        x (int): x coordinate
        area (tuple): target area

    Returns:
        bool: True if x is within the range given by area
    """
    # print("Check if " + str(x) + " is in " + str(area[0]))
    if area[0][0] <= x <= area[0][1]:
        return True
    return False


def isYinArea(y, area):
    """Checks if y is in its bounds based on area

    Args:
        y (int): y coordinate
        area (tuple): target area

    Returns:
        bool: True if y is within the range given by area
    """
    if area[1][0] <= y <= area[1][1]:
        return True
    return False


def initialXreachesArea(x, area):
    """Returns true if an initial velocity of x in x direction could reach the target area

    Args:
        x (int): initial x velocity
        area (tuple): target area

    Returns:
        bool: True if the initial x velocity could reach the target area
    """
    # x behaves according to a gaussian distribution
    # i represents the step that we consider
    temp = [gaus(x) - gaus(i) for i in range(x)]
    temp = [isXinArea(temp_value, area) for temp_value in temp]
    return int(sum(temp) > 0)


def initialYreachesArea(y, area):
    """Returns true if an initial y velocity could reach the target area

    Args:
        y (int): y velocity
        area (tuple): target area

    Returns:
        bool: True if the initial y velocity could reach the target area
    """
    if y > 0:
        # if y is positive, we reach a maximum height of gaus(y)
        # after that, the distance to the target area is at most gaus(y) - area[1][0]
        # (since area is negative)
        # each step i after the maximum height behaves according to gaus(i)
        temp = [gaus(y) - gaus(i) for i in range(-area[1][0] + y)]
        temp = [isYinArea(temp_value, area) for temp_value in temp]
        return int(sum(temp) > 0)
    else:
        # if y is negative, i steps substract gaus(i) from the position with an offset of y
        temp = [gaus(i) + y for i in range(-area[1][0])]
        temp = [isYinArea(-temp_value, area) for temp_value in temp]
        return int(sum(temp) > 0)


def getPossibleVelocities(area):
    """Returns possible velocities that could reach the area, but significantly less than all possible velocities

    Args:
        area (tuple): target area

    Returns:
        list: Velocities that may reach the area
    """
    # get possible x values:
    x_vels = []
    for x in range(area[0][1] + 1):
        if initialXreachesArea(x, area):
            x_vels.append(x)

    # get possible y values:
    y_vels = []
    for y in range(area[1][0] - 1, -area[1][0] + 1):
        if initialYreachesArea(y, area):
            y_vels.append(y)

    # generate possible starting velocities
    possibilities = [(x, y) for x in x_vels for y in y_vels]

    return possibilities


def getValidVelocities(velocities, area):
    """Returns all velocities that reach the target area and the maximum valid height

    Args:
        velocities (list): list of initial velocities
        area (tuple): target area

    Returns:
        list, int: list of velocities that reach the target area, maximum valid height
    """
    results = []

    # evaluate
    number = 0
    for value in velocities:
        res = getHeighest((0, 0), value, area)
        if res[1]:
            number += 1
            results.append(res[0])

    return results, number


def part1(data, measure=False):
    startTime = time.time()
    result_1 = None

    input = parseInput(data)

    area = input

    results, number = getValidVelocities(getPossibleVelocities(area), area)

    result_1 = max(results)

    executionTime = round(time.time() - startTime, 2)
    if measure:
        print("\nPart 1 took: " + str(executionTime) + " s")
    return result_1


def part2(data, measure=False):
    startTime = time.time()
    result_2 = 0

    input = parseInput(data)

    area = input

    results, number = getValidVelocities(getPossibleVelocities(area), area)

    result_2 = number

    executionTime = round(time.time() - startTime, 2)
    if measure:
        print("\nPart 2 took: " + str(executionTime) + " s")
    return result_2


def runTests(test_sol, path):
    """Runs the test inputs

    Args:
        test_sol (list): the solutions for the tests in order
        path (str): folderPath for the test txt files

    Returns:
        bool: If all tests ran with the correct result
    """
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

    test_sol = [45, 112]  # Todo put in test solutions

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

