import numpy as np
import time
import pprint
import sys

file_path = "Day 12/input-test.txt"

current_path = []
simple_paths = []
visited = {}


def dfs_iterative(adj_list, start, target, visitedTwice):
    stack, path = [start], []

    while stack:
        vertex = stack.pop()
        if visited[vertex] and not visitedTwice is None:
            continue
        if not str.isupper(vertex):
            if visited[vertex]:
                if not (vertex == "start" or vertex == "end"):
                    visitedTwice = vertex
                else:
                    continue
            visited[vertex] = True
        path.append(vertex)
        if vertex == target:
            simple_paths.append(path)
            visited[vertex] = False
            continue
        for neighbor in adj_list[vertex]:
            stack.append(neighbor)
        if visitedTwice == vertex:
            visitedTwice = None
        else:
            visited[vertex] = False

    return path


def dfs(adj_list, start, target, visitedTwice):
    print(str(visitedTwice) + " " + str(current_path))
    param = visitedTwice
    if visited[start] and visitedTwice:
        return
    if not str.isupper(start):
        if visited[start]:
            if not (start == "start" or start == "end"):
                param = True
            else:
                return
        visited[start] = True
    current_path.append(start)
    if start == target:
        simple_paths.append(current_path)
        visited[start] = False
        current_path.pop()
        return
    for neighbor in adj_list[start]:
        dfs(adj_list, neighbor, target, param)
    current_path.pop()
    visited[start] = False


def main():
    with open(file_path, "r") as file:

        sys.setrecursionlimit(40)
        startTime = time.time()
        lines = file.readlines()

        nodes = set()

        adj_list = {}

        edges = []

        for line in lines:
            edge = line.replace("\n", "").split("-")
            nodes.add(edge[0])
            nodes.add(edge[1])
            edges.append(edge)

        for node in nodes:
            adj_list[node] = []
            visited[node] = False

        for edge in edges:
            adj_list[edge[0]].append(edge[1])
            adj_list[edge[1]].append(edge[0])

        # pprint.pprint(adj_list)

        # for part 1

        for node in nodes:
            visited[node] = False
        # dfsOld(adj_list, "start", "end")
        dfs(adj_list, "start", "end", False)
        # dfs_iterative(adj_list, "start", "target", "dsayf")
        print(str(len(simple_paths)))

        for node in nodes:
            visited[node] = False

        # part 2
        # dfs(adj_list, "start", "end", False)
        # print(str(len(simple_paths)))

        executionTime = round(time.time() - startTime, 2)
        print("Execution time in seconds: " + str(executionTime))


if __name__ == "__main__":
    main()
