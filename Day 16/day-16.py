from datetime import date
import numpy as np
import time
import pprint
import math

from importlib.machinery import SourceFileLoader

lib = SourceFileLoader("lib", "lib.py").load_module()

from aocd import get_data
from aocd import submit

day = 16
path = ""


def parseInput(input):
    return str((bin(int(input[0], base=16))[2:]).zfill(len(input[0]) * 4))


def parseBinString(bin_string):
    try:
        orig = str(bin_string)
        packet_version = int(bin_string[0:3], 2)
        packet_typeID = int(bin_string[3:6], 2)
        bin_string = bin_string[6:]
        print("".join(["\n", orig, " ", str(packet_version), " ", str(packet_typeID)]))

        if packet_typeID == 4:
            # literal
            groups = [
                (bin_string[i * 5 : i * 5 + 1], bin_string[i * 5 + 1 : i * 5 + 5])
                for i in range(math.floor(len(bin_string) / 5.0))
            ]

            groups_new = []
            for i in range(len(groups)):
                groups_new.append(groups[i][1])
                if groups[i][0] == "0":
                    break
            groups = groups_new

            # cut binstring
            bin_string = (
                bin_string[len(groups) * 5 :]
                if len(bin_string) > len(groups) * 5 and int(bin_string, 2) != 0
                else ""
            )

            number = int("".join(groups), 2) if len(groups) > 0 else 0

            print(number)

            if len(bin_string) > 0 and not int(bin_string, 2) == 0:
                return (
                    (packet_version, packet_typeID, number),
                    parseBinString(bin_string),
                )
            else:
                return (packet_version, packet_typeID, number)

        else:
            length_type_ID = bin_string[0]
            bin_string = bin_string[1:]
            print("".join(["Length Type ID: ", str(length_type_ID)]))

            if length_type_ID == "0":
                # is 0
                length = int(bin_string[0:15], 2)
                print("Length " + str(length))
                bin_string = bin_string[15:]
                sub_packets = parseBinString(bin_string[0:length])
                bin_string = bin_string[length:]

                if len(bin_string) > 0 and not int(bin_string, 2) == 0:
                    return (
                        (packet_version, packet_typeID, sub_packets),
                        parseBinString(bin_string),
                    )
                else:
                    return (packet_version, packet_typeID, sub_packets)
            if length_type_ID == "1":
                length = int(bin_string[0:15], 2)
                print("Length " + str(length))
                bin_string = bin_string[15:]
                if length == 0:
                    return (packet_version, packet_typeID, ())
                else:
                    potential_subpackets = parseBinString(bin_string)
                    sub_packets = (
                        potential_subpackets[0:length]
                        if len(potential_subpackets) > length
                        else potential_subpackets
                    )
                    if len(potential_subpackets) > length:
                        return (
                            (packet_version, packet_typeID, sub_packets),
                            potential_subpackets[length:],
                        )
                    else:
                        return (packet_version, packet_typeID, sub_packets)
    except Exception as e:
        print("Parsing Error!")
        return


def getVersionSum(result):
    try:
        iter(result)
        if len(result) == 3:
            # valid packet
            return result[0] + getVersionSum(result[2])
        elif len(result) > 1:
            # a list of packets
            return sum(map(getVersionSum, result))
        else:
            return 0
    except TypeError:
        return 0


def part1(data, measure=False):
    startTime = time.time()
    result_1 = None

    input = parseInput(data)

    result = parseBinString(input)
    print(result)

    result_1 = getVersionSum(result)

    # Todo program part 1

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

    test_sol = [6, 9, 14, 16, 12, 23, 31]  # Todo put in test solutions

    test = True  # Todo

    sol1 = sub1 = False  # Todo
    sol2 = sub2 = False  # Todo

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

