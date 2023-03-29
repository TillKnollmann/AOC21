import numpy as np
import time
import pprint
import sys

file_path = "Day 12/input.txt"

current_path = []
simple_paths = []
visited = {}
any_Twice = False


def dfs(adj_list, start, target):
    global any_Twice
    if visited[start] > 0 and any_Twice:
        # Path is invalid
        return
    if not str.isupper(start):
        if visited[start] > 0:
            if not (start == "start" or start == "end"):
                # we visit this node twice
                any_Twice = True
            else:
                return
        visited[start] += 1
    # append the node to the path
    current_path.append(start)
    if start == target:
        # reached the target
        simple_paths.append(current_path)
        visited[start] -= 1
        current_path.pop()
        return
    for neighbor in adj_list[start]:
        # call for all neighbors
        dfs(adj_list, neighbor, target)
    current_path.pop()
    visited[start] -= 1
    if visited[start] > 0:
        # we set any_twice
        any_Twice = False


def main():

    global any_Twice
    global current_path
    global simple_paths

    with open(file_path, "r") as file:
        startTime = time.time()
        lines = file.readlines()

        nodes = set()

        adj_list = {}

        edges = []

        # create nodes
        for line in lines:
            edge = line.replace("\n", "").split("-")
            nodes.add(edge[0])
            nodes.add(edge[1])
            edges.append(edge)

        # build adjacency list
        for node in nodes:
            adj_list[node] = []
            visited[node] = 0

        for edge in edges:
            adj_list[edge[0]].append(edge[1])
            adj_list[edge[1]].append(edge[0])

        # for part 1 we don't allow double visits
        any_Twice = True

        dfs(adj_list, "start", "end")

        print("\nSolution Part 1: " + str(len(simple_paths)))

        # part 2
        for node in nodes:
            visited[node] = 0

        any_Twice = False
        simple_paths = []
        current_path = []

        dfs(adj_list, "start", "end")

        print("Solution Part 2: " + str(len(simple_paths)))

        executionTime = round(time.time() - startTime, 2)
        print("Execution time in seconds: " + str(executionTime))


if __name__ == "__main__":
    main()
