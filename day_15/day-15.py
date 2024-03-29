from datetime import date
import numpy as np
import time
import pprint
import networkx as nx

from importlib.machinery import SourceFileLoader

lib = SourceFileLoader("lib", "lib.py").load_module()

from aocd import get_data
from aocd import submit

day = 15
path = ""


def parseInput(input):
    result = []
    for line in input:
        result.append(list(line.replace("\n", "")))
    result = np.array(result, dtype=np.int32)
    return result


def processMap(map):
    shortest = np.zeros(map.shape)

    for i in range(1, len(shortest)):
        shortest[i, 0] = shortest[i - 1, 0] + map[i, 0]

    # print(map[:, 0])
    # print(shortest[:, 0])

    for j in range(0, len(shortest[0])):
        if j == 0:
            shortest[0, 0] = map[0, 0]
        else:
            shortest[0, j] = shortest[0, j - 1] + map[0, j]

    # print(shortest)

    for i in range(1, len(shortest)):
        for j in range(1, len(shortest[0])):
            left = shortest[i, j - 1]
            top = shortest[i - 1, j]
            shortest[i, j] = min(left, top) + map[i, j]

    return shortest.copy()


def part1(data, measure=False):
    startTime = time.time()

    input = parseInput(data)

    G = buildGraph(input)

    path = nx.shortest_path(
        G, source=(0, 0), target=(len(input) - 1, len(input) - 1), weight="weight",
    )
    risk = sum(input[x][y] for x, y in path[1:])

    executionTime = round(time.time() - startTime, 2)
    if measure:
        print("\nPart 1 took: " + str(executionTime) + " seconds")
    return int(risk)


def part2(data, measure=False):
    startTime = time.time()

    input = parseInput(data)

    # print(input.shape)

    # generate giant map
    giant_map = np.zeros((5 * len(input), 5 * len(input[0]))).reshape(
        (5, 5, len(input), len(input[0]))
    )
    giant_map[0, 0] = input.copy()

    # fill giant map
    for j in range(1, 5):
        temp_map = giant_map[0, j - 1].copy()
        temp_map += 1
        temp_map[temp_map > 9] = 1
        giant_map[0, j] = temp_map.copy()

    for i in range(1, 5):
        for j in range(0, 5):
            temp_map = giant_map[i - 1, j].copy()
            temp_map += 1
            temp_map[temp_map > 9] = 1
            giant_map[i, j] = temp_map.copy()

    # print(giant_map[:, 0, :, 0])

    giant_map_new = np.zeros((5 * len(input), 5 * len(input[0])))

    for i in range(0, 5):
        for j in range(0, 5):
            for k in range(0, len(input)):
                for l in range(0, len(input[0])):
                    giant_map_new[
                        (i * len(input)) + k, (j * len(input[0])) + l
                    ] = giant_map[i, j, k, l]

    # print(giant_map_new)

    G = buildGraph(giant_map_new)

    path = nx.shortest_path(
        G,
        source=(0, 0),
        target=(len(giant_map_new) - 1, len(giant_map_new) - 1),
        weight="weight",
    )
    risk = sum(giant_map_new[x][y] for x, y in path[1:])

    executionTime = round(time.time() - startTime, 2)
    if measure:
        print("\nPart 2 took: " + str(executionTime) + " seconds")

    return int(risk)


def buildGraph(map):
    G = nx.DiGraph()

    for i in range(0, len(map)):
        for j in range(0, len(map[0])):
            if i > 0:
                G.add_edge((i - 1, j), (i, j), weight=map[i - 1, j])
            if j > 0:
                G.add_edge((i, j - 1), (i, j), weight=map[i, j - 1])
            if i < len(map) - 1:
                G.add_edge((i + 1, j), (i, j), weight=map[i + 1, j])
            if j < len(map[0]) - 1:
                G.add_edge((i, j + 1), (i, j), weight=map[i, j + 1])
    return G


def part2Old(data, measure):
    startTime = time.time()
    result_2 = None

    input = parseInput(data)

    # generate giant map
    giant_map = np.zeros((5 * len(input), 5 * len(input[0]))).reshape(
        (5, 5, len(input), len(input[0]))
    )
    giant_map[0, 0] = input.copy()

    # fill giant map
    for j in range(1, 5):
        temp_map = giant_map[0, j - 1].copy()
        temp_map += 1
        temp_map[temp_map > 9] = 1
        giant_map[0, j] = temp_map.copy()

    for i in range(1, 5):
        for j in range(0, 5):
            temp_map = giant_map[i - 1, j].copy()
            temp_map += 1
            temp_map[temp_map > 9] = 1
            giant_map[i, j] = temp_map.copy()

    # print(giant_map[:, 0, :, 0])

    giant_map_new = np.zeros((5 * len(input), 5 * len(input[0])))

    for i in range(0, 5):
        for j in range(0, 5):
            for k in range(0, len(input)):
                for l in range(0, len(input[0])):
                    giant_map_new[
                        (i * len(input)) + k, (j * len(input[0])) + l
                    ] = giant_map[i, j, k, l]

    shortest = processMap(giant_map_new)

    result_2 = shortest[len(shortest) - 1, len(shortest[0]) - 1]

    executionTime = round(time.time() - startTime, 2)
    if measure:
        print("Part 2 took: " + str(executionTime) + " seconds")
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

    test_sol = [40, 315]  # Todo put in test solutions

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

