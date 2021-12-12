import numpy as np
import time
import pprint

from itertools import chain, combinations, permutations

import networkx as nx

file_path = "Day 12/input-test.txt"


def removeFromList(list, thing):
    while thing in list:
        list.remove(thing)
    return list


def shift(seq, n):
    a = n % len(seq)
    return seq[-a:] + seq[:-a]


def isContained(listA: list, listList: list) -> bool:
    for otherList in listList:
        if list(otherList) == list(listA):
            return True
    return False


def powerset(iterable):
    "powerset([1,2,3]) --> () (1,) (2,) (3,) (1,2) (1,3) (2,3) (1,2,3)"
    s = list(iterable)
    return chain.from_iterable(combinations(s, r) for r in range(1, len(s) + 1))


def generateNewPath(path: tuple, pos: int, toInsert: tuple) -> tuple:
    result = []
    result += path[0 : pos + 1]
    result += toInsert
    result += path[pos + 1 : len(path)]
    return tuple(result)


def isValid(path: tuple, nodes: list, allowed: int) -> bool:
    count = 0
    for node in nodes:
        if not str.isupper(str(node)):
            number = path.count(str(node))
            if number > 1:
                count += number
                if count > allowed:
                    return False
    return True


def main():
    with open(file_path, "r") as file:
        startTime = time.time()
        lines = file.readlines()

        check = False
        part_2 = True

        allowed = 1
        if part_2:
            allowed = 2

        G = nx.Graph()  # create a graph

        for line in lines:
            edge = line.replace("\n", "").split("-")
            G.add_edge(edge[0], edge[1])

        paths = tuple(nx.all_simple_paths(G, source="start", target="end"))

        temp = []
        for path in paths:
            temp.append(tuple(path))
        paths = tuple(temp)

        G_prime = G.copy()
        G_prime.remove_nodes_from(["start", "end"])

        # find cycles
        cycles = nx.simple_cycles(G_prime.to_directed())

        cycles_new = []
        for cycle in cycles:
            cycles_new.append(cycle)
            temp = cycle.copy()
            list.reverse(temp)
            cycles_new.append(temp)
        cycles = cycles_new

        cycles_nice = {}
        for node in G.nodes():
            temp = {""}
            temp.clear()
            for cycle in cycles:
                if str(node) in cycle:
                    # orient cycle
                    temp2 = cycle
                    temp2 = tuple(shift(temp2, temp2.index(node)))
                    temp.add(temp2[1 : len(temp2)])
            if len(temp) > 0:
                cycles_nice[str(node)] = temp

        progress = True

        paths_new = {"a"}
        paths_new.clear()
        paths_new.update(paths)

        all_paths = {""}
        all_paths.clear()

        while progress:
            progress = False

            generated_paths = {"a"}
            generated_paths.clear()

            for path in paths_new:
                for i in range(0, len(path)):
                    if str.isupper(path[i]) or (
                        part_2 and str(path[i]) != "start" and str(path[i]) != "end"
                    ):
                        node = path[i]

                        # get all simple neighbors not start or end
                        neighbors = list(G.neighbors(node))
                        neighbors = removeFromList(neighbors, "start")
                        neighbors = removeFromList(neighbors, "end")
                        # generate possibilities
                        ps = list(powerset(neighbors))
                        for set in ps:
                            for perm in permutations(list(set)):
                                insert = []
                                for elem in list(perm):
                                    insert.append(elem)
                                    insert.append(node)
                                generated = generateNewPath(path, i, tuple(insert))
                                if isValid(generated, G.nodes(), allowed):
                                    generated_paths.add(generated)

            # build in cycles
            for path in paths_new:
                for i in range(0, len(path)):
                    if str.isupper(path[i]) or (
                        part_2 and str(path[i]) != "start" and str(path[i]) != "end"
                    ):
                        node = path[i]
                        # get all cycles
                        current_cycles = cycles_nice[str(node)]
                        # generate path for each cycle
                        for cycle in current_cycles:
                            insert = list(cycle)
                            insert.append(node)
                            generated = generateNewPath(path, i, tuple(insert))
                            if isValid(generated, G.nodes(), allowed):
                                generated_paths.add(generated)

            if len(generated_paths) > 0:
                progress = True

            all_paths.update(paths_new.copy())
            paths_new = generated_paths.copy()

            print(str(len(all_paths)) + " paths")

        # pprint.pprint(all_paths)

        with open("Day 12/check.txt", "r") as checker:

            checker_array = []
            for line in checker.readlines():
                checker_array.append(line.replace("\n", "").split(","))

            # check missing paths
            if check:
                for check_path in checker_array:
                    if not check_path in all_paths:
                        print("\nPath " + str(check_path) + " not detected")

            print("\nThere are " + str(len(all_paths)) + " paths!")

        executionTime = round(time.time() - startTime, 2)
        print("Execution time in seconds: " + str(executionTime))


if __name__ == "__main__":
    main()
