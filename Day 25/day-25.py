from datetime import date
import numpy as np
import time
import pprint

from importlib.machinery import SourceFileLoader

lib = SourceFileLoader("lib", "lib.py").load_module()

from aocd import get_data
from aocd import submit

day = 25
path = ""


def parseInput(input):
    result = []

    for line in input:
        current_line = line.replace("\n", "").strip()
        result.append([char for char in current_line])

    array = np.array(result)

    return array


def simulate_step(sea_cucumbers):

    progress = False

    new_sea_cucumbers = sea_cucumbers.copy()
    # east facing
    for i in range(len(sea_cucumbers)):
        for j in range(len(sea_cucumbers[i])):
            if sea_cucumbers[i, j] == ">":
                # get neighbor
                neigh_i = i
                neigh_j = j + 1 if j < len(sea_cucumbers[i]) - 1 else 0
                if sea_cucumbers[neigh_i, neigh_j] == ".":
                    new_sea_cucumbers[neigh_i, neigh_j] = ">"
                    new_sea_cucumbers[i, j] = "."
                    progress = True

    new_new_sea_cucumbers = new_sea_cucumbers.copy()

    for i in range(len(new_sea_cucumbers)):
        for j in range(len(new_sea_cucumbers[i])):
            if new_sea_cucumbers[i, j] == "v":
                # get neighbor
                neigh_i = i + 1 if i < len(new_sea_cucumbers) - 1 else 0
                neigh_j = j
                if new_sea_cucumbers[neigh_i, neigh_j] == ".":
                    new_new_sea_cucumbers[neigh_i, neigh_j] = "v"
                    new_new_sea_cucumbers[i, j] = "."
                    progress = True

    return new_new_sea_cucumbers.copy(), progress


def part1(data, measure=False):
    startTime = time.time()
    result_1 = None

    sea_cucumbers = parseInput(data)

    sea_cucumbers, progress = simulate_step(sea_cucumbers)

    counter = 1

    while progress:
        sea_cucumbers, progress = simulate_step(sea_cucumbers)
        counter += 1

    result_1 = counter

    executionTime = round(time.time() - startTime, 2)
    if measure:
        print("\nPart 1 took: " + str(executionTime) + " s")
    return result_1


def part2(data, measure=False):
    startTime = time.time()
    result_2 = None

    input = parseInput(data)

    # Todo program part 2

    executionTime = round(time.time() - startTime, 2)
    if measure:
        print("\nPart 2 took: " + str(executionTime) + " s")
    return result_2


def runTests(test_sol_1, test_sol_2, path):
    test_res_1 = []
    test_res_2 = []

    all_check = True

    paths = lib.getTestPaths(path)

    test_res_1 += list(map(part1, map(lib.getDataLines, paths)))
    test_res_2 += list(map(part2, map(lib.getDataLines, paths)))

    success_1 = [(test_sol_1[i] == test_res_1[i]) for i in range(len(test_sol_1))]
    success_2 = [
        "Part 2 Test " + str(i + 1) + " " + (test_sol_2[i] == test_res_2[i])
        for i in range(len(test_sol_2))
    ]

    for i in range(len(test_sol_1)):
        if success_1[i]:
            print("Part 1 Test " + str(i + 1) + " Succeeded!")
        else:
            print(
                "Part 1 Test "
                + str(i + 1)
                + " Failed! Expected "
                + str(test_sol_1[i])
                + " received "
                + test_res_1[i]
            )
            all_check = False

    for i in range(len(test_sol_2)):
        if success_2[i]:
            print("Part 2 Test " + str(i + 1) + " Succeeded!")
        else:
            print(
                "Part 2 Test "
                + str(i + 1)
                + " Failed! Expected "
                + str(test_sol_2[i])
                + " received "
                + test_res_2[i]
            )
            all_check = False

    return all_check


def main():
    global path
    path = "Day " + str(day) + "/"

    test_sol_1 = [58]  # Todo put in test solutions part 1
    test_sol_2 = []  # Todo put in test solutions part 2

    test = True  # Todo

    sol1 = sub1 = True  # Todo
    sol2 = sub2 = False  # Todo

    if test:
        if not runTests(test_sol_1, test_sol_2, path):
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

