import numpy as np
import time
import math
from itertools import chain, combinations, permutations

import networkx as nx

file_path = "Day 12/input-test.txt"


def removeFromList(list, thing):
    while thing in list:
        list.remove(thing)
    return list


def check_same_contents(nums1, nums2):
    for x in set(nums1 + nums2):
        if nums1.count(x) != nums2.count(x):
            return False
    return True


def powerset(iterable):
    "powerset([1,2,3]) --> () (1,) (2,) (3,) (1,2) (1,3) (2,3) (1,2,3)"
    s = list(iterable)
    return chain.from_iterable(combinations(s, r) for r in range(1, len(s) + 1))


def main():
    with open(file_path, "r") as file:
        startTime = time.time()
        lines = file.readlines()

        G = nx.Graph()  # create a graph

        for line in lines:
            edge = line.replace("\n", "").split("-")
            G.add_edge(edge[0], edge[1])

        paths = list(nx.all_simple_paths(G, source="start", target="end"))
        paths_new = paths.copy()

        possibilities = len(paths)

        # find all cycles
        cycles = nx.cycle_basis(G)

        # store nices
        cycles_node = {}

        for node in G.nodes():
            if str.isupper(str(node)):
                temp = []
                for cycle in cycles:
                    if node in cycle:
                        temp.append(cycle)
                cycles_node[str(node)] = temp

        print(cycles_node)

        for path in paths:
            for node in path:
                if str.isupper(str(node)):
                    # find all cycles
                    # get all simple neighbors not start or end
                    neighbors = list(G.neighbors(node))
                    neighbors = removeFromList(neighbors, "start")
                    neighbors = removeFromList(neighbors, "end")
                    for node2 in path:
                        neighbors = removeFromList(neighbors, str(node2))
                    # generate possibilities
                    ps = list(powerset(neighbors))
                    for set in ps:
                        # print(list(set))
                        for perm in permutations(list(set)):
                            # construct new path
                            proposed = []
                            for node2 in path:
                                if str(node2) != str(node):
                                    proposed.append(node2)
                                else:
                                    proposed.append(node2)
                                    for elem in perm:
                                        proposed.append(elem)
                                        proposed.append(node2)
                            already = False
                            for path2 in paths_new:
                                if path2 == proposed:
                                    already = True
                            if not already:
                                paths_new.append(proposed)

        print("\nFound:\n")
        for path in paths_new:
            print(path)
        print("\n")

        with open("Day 12/check.txt", "r") as checker:

            checker_array = []
            for line in checker.readlines():
                checker_array.append(line.replace("\n", "").split(","))

            # check missing paths
            for check_path in checker_array:
                if not check_path in paths_new:
                    print("\nPath " + str(check_path) + " not detected")

            print("\n There are " + str(len(paths_new)) + " paths!")

        executionTime = round(time.time() - startTime, 2)
        print("Execution time in seconds: " + str(executionTime))


if __name__ == "__main__":
    main()
