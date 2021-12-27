from datetime import date
import numpy as np
import time
import pprint
import math

from tqdm import tqdm

from importlib.machinery import SourceFileLoader

lib = SourceFileLoader("lib", "lib.py").load_module()

from aocd import get_data
from aocd import submit

day = 24
path = ""


values = {}


def initialize():
    global values
    values = {"w": 0, "x": 0, "y": 0, "z": 0}


def inp(a: str, value):
    global values
    values[a] = int(value)


def add(a, b):
    global values
    value_b = int(b) if b.lstrip("-").isdigit() else values[b]
    values[a] = values[a] + value_b


def mul(a, b):
    global values
    value_b = int(b) if b.lstrip("-").isdigit() else values[b]
    values[a] = values[a] * value_b


def div(a, b):
    global values
    value_b = int(b) if b.lstrip("-").isdigit() else values[b]
    if value_b == 0:
        raise Exception("Dividing by zero!")
    values[a] = math.floor(values[a] / float(value_b))


def mod(a, b):
    global values
    value_b = int(b) if b.lstrip("-").isdigit() else values[b]
    values[a] = values[a] % value_b


def eql(a, b):
    global values
    value_b = int(b) if b.lstrip("-").isdigit() else values[b]
    values[a] = int(values[a] == value_b)


def run_instructions(instructions, number):

    number = str(number)

    initialize()
    for instr in instructions:
        if instr[0] == "inp":
            inp(instr[1], number[0])
            number = number[1:]
        elif instr[0] == "add":
            add(instr[1], instr[2])
        elif instr[0] == "mul":
            mul(instr[1], instr[2])
        elif instr[0] == "div":
            div(instr[1], instr[2])
        elif instr[0] == "mod":
            mod(instr[1], instr[2])
        elif instr[0] == "eql":
            eql(instr[1], instr[2])
        else:
            raise Exception("Unknown instruction " + str(instr))

    return values["w"], values["x"], values["y"], values["z"]


def parseInput(input):
    result = []

    for line in input:
        current_line = line.replace("\n", "").strip()
        result.append(tuple(current_line.split(" ")))

    return tuple(result)


def part1(data, measure=False):
    global cache

    startTime = time.time()
    result_1 = None

    instructions = parseInput(data)

    start = 99999999999999
    w, x, y, z = run_instructions(instructions, int(start))
    while z != 0:
        start -= 1
        w, x, y, z = run_instructions(instructions, int(start))

    result_1 = start

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

    test_sol_1 = []  # Todo put in test solutions part 1
    test_sol_2 = []  # Todo put in test solutions part 2

    test = False  # Todo

    sol1 = sub1 = True  # Todo
    sol2 = sub2 = False  # Todo

    sub1 = True

    if test:
        if not runTests(test_sol_1, test_sol_2, path):
            sub1 = sub2 = False

    # data_main = get_data(day=day, year=2021).splitlines()
    data_main = lib.getDataLines(path + "/input_orig.txt")

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

