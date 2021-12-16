from datetime import date
import numpy as np
import time
import pprint
import math
from functools import reduce
import functools

from importlib.machinery import SourceFileLoader

lib = SourceFileLoader("lib", "lib.py").load_module()

from aocd import get_data
from aocd import submit

day = 16
path = ""


flatten_list = (
    lambda irregular_list: [
        element for item in irregular_list for element in flatten_list(item)
    ]
    if type(irregular_list) is list
    else [irregular_list]
)


def parseInput(input):
    return str((bin(int(input[0], base=16))[2:]).zfill(len(input[0]) * 4))


def parseBinString(bin_string, outermost=False):
    try:
        orig = str(bin_string)
        packet_version = int(bin_string[0:3], 2)
        packet_typeID = int(bin_string[3:6], 2)
        bin_string = bin_string[6:]
        # print("".join(["\n", orig, " ", str(packet_version), " ", str(packet_typeID)]))

        if packet_typeID == 4:
            # literal
            groups = [
                (bin_string[i * 5 : i * 5 + 1], bin_string[i * 5 + 1 : i * 5 + 5])
                for i in range(math.floor(len(bin_string) / 5.0))
            ]

            groups_new = []
            carry = True
            for i in range(len(groups)):
                if carry:
                    groups_new.append(groups[i][1])
                    if groups[i][0] == "0":
                        carry = False
            groups = groups_new

            # cut binstring
            bin_string = (
                bin_string[len(groups) * 5 :]
                if len(bin_string) > len(groups) * 5 and not int(bin_string, 2) == 0
                else ""
            )

            number = int("".join(groups), 2) if len(groups) > 0 else 0

            # print(number)

            if len(bin_string) > 0 and not int(bin_string, 2) == 0 and not outermost:
                return flatten_list(
                    [
                        (packet_version, packet_typeID, number),
                        parseBinString(bin_string),
                    ]
                )
            else:
                return [(packet_version, packet_typeID, number)]

        else:
            length_type_ID = bin_string[0]
            bin_string = bin_string[1:]
            # print("".join(["Length Type ID: ", str(length_type_ID)]))

            if length_type_ID == "0":
                # is 0
                length = int(bin_string[0:15], 2)
                # print("Length " + str(length))

                bin_string = bin_string[15:]
                sub_packets = parseBinString(bin_string[0:length])
                bin_string = bin_string[length:]

                if (
                    len(bin_string) > 0
                    and not int(bin_string, 2) == 0
                    and not outermost
                ):
                    return [
                        (packet_version, packet_typeID, sub_packets),
                        parseBinString(bin_string),
                    ]
                else:
                    return [(packet_version, packet_typeID, sub_packets)]
            if length_type_ID == "1":
                length = int(bin_string[0:11], 2)
                # print("Length " + str(length))
                bin_string = bin_string[11:]
                if length == 0:
                    print("Length 0 requested")
                    return [(packet_version, packet_typeID, ())]
                else:
                    potential_subpackets = parseBinString(bin_string)

                    # print(str(potential_subpackets))

                    if len(potential_subpackets) > length and not outermost:
                        return [
                            (
                                packet_version,
                                packet_typeID,
                                potential_subpackets[0:length],
                            ),
                            potential_subpackets[length:],
                        ]
                    else:
                        return [(packet_version, packet_typeID, potential_subpackets)]
    except Exception as e:
        print("Parsing Error!")
        print(e)
        return


def getVersionSum(result):
    if isinstance(result, list):
        return sum(map(getVersionSum, result))
    elif isinstance(result, tuple) and len(result) > 0:
        number = result[0]
        if len(result) > 2:
            number += getVersionSum(result[2])
        return number
    else:
        return 0


def part1(data, measure=False):
    startTime = time.time()
    result_1 = None

    input = parseInput(data)

    # print("\n\nDecoding " + str(data[0]))

    result = parseBinString(input, True)

    # print(result)

    result_1 = getVersionSum(result)

    # Todo program part 1

    executionTime = round(time.time() - startTime, 2)
    if measure:
        print("\nPart 1 took: " + str(executionTime) + " s")
    return result_1


def prod(*args):
    return functools.reduce(lambda a, b: a * b, *args)


def interpretResultPart2(result):
    # print("Interpreting " + str(result))
    if isinstance(result, list):
        # contains list of packets
        return flatten_list(list(map(interpretResultPart2, result)))
    elif isinstance(result, tuple) and len(result) > 0:
        # switch over typeID
        packet_version, packet_typeID, packet_value = result
        if packet_typeID == 4:
            print("Literal " + str(int(packet_value)))
            return [int(packet_value)]
        elif packet_typeID == 0:
            # sum
            res_1 = interpretResultPart2(packet_value)
            res = sum(res_1)
            print("Sum of " + str(res_1) + " is " + str(res))
            return flatten_list([res])
        elif packet_typeID == 1:
            res_1 = interpretResultPart2(packet_value)
            res = prod(res_1) if len(res_1) > 1 else res_1
            print("Prod of " + str(res_1) + " is " + str(res))
            return flatten_list([res])
        elif packet_typeID == 2:
            res_1 = interpretResultPart2(packet_value)
            res = min(res_1)
            print("Min of " + str(res_1) + " is " + str(res))
            return flatten_list([res])
        elif packet_typeID == 3:
            res_1 = interpretResultPart2(packet_value)
            res = max(res_1)
            print("Max of " + str(res_1) + " is " + str(res))
            return flatten_list([res])
        elif packet_typeID == 5:
            res_1 = [
                interpretResultPart2(packet_value[0])[0],
                interpretResultPart2(packet_value[1])[0],
            ]
            res = 1 if res_1[0] > res_1[1] else 0
            print("Greater than of " + str(res_1) + " is " + str(res))
            return flatten_list([res])
        elif packet_typeID == 6:
            res_1 = [
                interpretResultPart2(packet_value[0])[0],
                interpretResultPart2(packet_value[1])[0],
            ]
            res = 1 if res_1[0] < res_1[1] else 0
            print("Less than of " + str(res_1) + " is " + str(res))
            return flatten_list([res])
        elif packet_typeID == 7:
            res_1 = [
                interpretResultPart2(packet_value[0])[0],
                interpretResultPart2(packet_value[1])[0],
            ]
            res = 1 if res_1[0] == res_1[1] else 0
            print("Equal of " + str(res_1) + " is " + str(res))
            return flatten_list([res])

    else:
        print("error")
        return 0


def part2(data, measure=False):
    startTime = time.time()
    result_2 = None

    input = parseInput(data)

    result = parseBinString(input, True)

    # print(str(result))

    # print("\nInterpreting " + str(result))

    result_2 = interpretResultPart2(result)[0]

    # print("Result is " + str(result_2))

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

    test = False  # Todo

    checks = [3, 54, 7, 9, 1, 0, 0, 1]

    results = list(
        map(
            part2,
            [
                ["C200B40A82"],
                ["04005AC33890"],
                ["880086C3E88112"],
                ["CE00C43D881120"],
                ["D8005AC2A8F0"],
                ["F600BC2D8F"],
                ["9C005AC2F8F0"],
                ["9C0141080250320F1802104A08"],
            ],
        )
    )

    results = [results[i] == checks[i] for i in range(len(results))]

    print(results)

    sol1 = sub1 = True  # Todo
    sol2 = sub2 = True  # Todo

    sub1 = False

    sub2 = False

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

