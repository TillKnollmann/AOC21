import numpy as np
import time
import math
import pprint
from itertools import chain, combinations, permutations

from collections import deque

import networkx as nx

file_path = "Day 12/input.txt"


def removeFromList(list, thing):
    while thing in list:
        list.remove(thing)
    return list


def shift(seq, n=0):
    a = n % len(seq)
    return seq[-a:] + seq[:-a]


def check_same_contents(nums1, nums2):
    for x in set(nums1 + nums2):
        if nums1.count(x) != nums2.count(x):
            return False
    return True


def isContained(listA, listList):
    for otherList in listList:
        if list(otherList) == list(listA):
            return True
    return False


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

        G_prime = G.copy()
        G_prime.remove_nodes_from(["start", "end"])

        # find cycles
        # cycles = nx.cycle_basis(G_prime)
        cycles = nx.simple_cycles(G_prime.to_directed())

        cycles_new = []
        for cycle in cycles:
            cycles_new.append(cycle)
            temp = cycle.copy()
            list.reverse(temp)
            cycles_new.append(temp)
        cycles = cycles_new

        # pprint.pprint(list(cycles))

        # print(cycles)
        cycles_nice = {}
        for node in G.nodes():
            if str.isupper(str(node)):
                temp = []
                for cycle in cycles:
                    if str(node) in cycle:
                        # orient cycle
                        temp2 = cycle
                        while temp2[0] != node:
                            temp2 = shift(temp2, 1)
                        if not temp2 in temp:
                            temp.append(temp2[1 : len(temp2)])
                cycles_nice[str(node)] = temp

        # cycles_new = []
        # for cycle in cycles:
        #    string_cycle = [str(x) for x in cycle]
        #    if not "start" in string_cycle:
        #        if not "end" in string_cycle:
        #            cycles_new.append(cycle)
        # temp = cycle.copy()
        # list.reverse(temp)
        # cycles_new.append(temp)
        # cycles = cycles_new

        # pprint.pprint(cycles)

        # cycles_nice = {}
        # for node in G.nodes():
        #   if str.isupper(str(node)):
        #      temp = []
        #     for cycle in cycles:
        #        if node in cycle:
        #           # orient cycle
        #          temp2 = cycle
        #         while temp2[0] != node:
        #            temp2 = shift(temp2, 1)
        #       temp.append(temp2)
        # cycles_nice[str(node)] = temp

        # pprint.pprint(cycles_nice)

        # find all paths with movements to neighbors

        progress = True
        iterations = 100

        i = 0

        all_paths = paths.copy()

        while progress and i < iterations:
            i += 1
            progress = False
            current_size = len(paths_new)

            generated_paths = []

            for path in paths_new:
                for i in range(0, len(list(path))):
                    node = list(path)[i]
                    if str.isupper(str(node)):
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
                                for j in range(0, len(list(path))):
                                    if i != j:
                                        proposed.append(list(path)[j])
                                    else:
                                        proposed.append(list(path)[j])
                                        for elem in perm:
                                            proposed.append(elem)
                                            proposed.append(list(path)[j])
                                generated_paths.append(proposed.copy())

            # build in cycles
            for path in paths_new:
                for i in range(0, len(list(path))):
                    node = list(path)[i]
                    if str.isupper(str(node)):
                        # get all cycles
                        current_cycles = cycles_nice[str(node)]
                        # remove cycles which contain nodes of the path
                        cycles_temp = []
                        for cycle in current_cycles:
                            clean = True
                            for cycle_node in cycle:
                                if cycle_node in path:
                                    if not str.isupper(str(cycle_node)):
                                        clean = False
                            if clean:
                                cycles_temp.append(cycle)
                        current_cycles = cycles_temp

                        # generate path for each cycle
                        for cycle in current_cycles:
                            # construct new path
                            proposed = []
                            for j in range(0, len(list(path))):
                                if i != j:
                                    proposed.append(list(path)[j])
                                else:
                                    proposed.append(list(path)[j])
                                    for elem in cycle:
                                        proposed.append(elem)
                                    proposed.append(list(path)[j])
                            generated_paths.append(proposed.copy())

            if len(generated_paths) > 0:
                progress = True

            # check for duplicates
            temp = []
            for path in generated_paths:
                if not isContained(list(path), list(paths_new)):
                    if not isContained(list(path), temp):
                        # check if path is valid
                        use = True
                        for node in path:
                            if list(path).count(str(node)) > 1:
                                if not str.isupper(str(node)):
                                    use = False
                        if use:
                            temp.append(path)

            all_paths += paths_new
            paths_new = temp.copy()

        print("\nIterations:" + str(i))

        # remove invalid paths
        paths_temp = []
        for path in all_paths:
            if not isContained(list(path), paths_temp):
                # check if element comes twice
                use = True
                for node in path:
                    if list(path).count(str(node)) > 1:
                        if not str.isupper(str(node)):
                            use = False
                if use:
                    paths_temp.append(path)
        all_paths = paths_temp

        # for path in paths_new:
        #   print(path)

        with open("Day 12/check.txt", "r") as checker:

            check = False
            checker_array = []
            for line in checker.readlines():
                checker_array.append(line.replace("\n", "").split(","))

            # check missing paths
            if check:
                for check_path in checker_array:
                    if not check_path in paths_new:
                        print("\nPath " + str(check_path) + " not detected")

            print("\n There are " + str(len(all_paths)) + " paths!")

        executionTime = round(time.time() - startTime, 2)
        print("Execution time in seconds: " + str(executionTime))


if __name__ == "__main__":
    main()
