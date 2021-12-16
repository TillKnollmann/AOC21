from datetime import date
import time
import math
import functools

from importlib.machinery import SourceFileLoader

lib = SourceFileLoader("lib", "lib.py").load_module()

from aocd import get_data
from aocd import submit

day = 16
path = ""


# used to deep-flatten a list
flatten_list = (
    lambda irregular_list: [
        element for item in irregular_list for element in flatten_list(item)
    ]
    if type(irregular_list) is list
    else [irregular_list]
)


def parseInput(input):
    """ Makes a hexadecimal input a binary with leading zeros """
    return str((bin(int(input[0], base=16))[2:]).zfill(len(input[0]) * 4))


def parseBinString(bin_string, outermost=False):
    """ Parses the binary input """
    if len(bin_string) < 7:
        # no valid string
        return
    try:
        # get version and type id
        packet_version = int(bin_string[0:3], 2)
        packet_typeID = int(bin_string[3:6], 2)

        # shorten the string
        bin_string = bin_string[6:]

        if packet_typeID == 4:
            # find literals
            groups = [
                (bin_string[i * 5 : i * 5 + 1], bin_string[i * 5 + 1 : i * 5 + 5])
                for i in range(math.floor(len(bin_string) / 5.0))
            ]

            groups_new = []
            # throw away all false groups
            for i in range(len(groups)):
                groups_new.append(groups[i][1])
                if groups[i][0] == "0":
                    break
            groups = groups_new

            # cut literals out of binstring
            bin_string = bin_string[len(groups) * 5 :]

            # determine number of literal
            number = int("".join(groups), 2)

            if len(bin_string) > 0 and not outermost:
                # parse the rest of the string and return the concatenation
                rest = parseBinString(bin_string)
                return (
                    [(packet_version, packet_typeID, number)] + rest
                    if rest
                    else [(packet_version, packet_typeID, number)]
                )
            else:
                # return the packet
                return [(packet_version, packet_typeID, number)]

        else:
            # get length type id
            length_type_ID = bin_string[0]
            bin_string = bin_string[1:]

            if length_type_ID == "0":
                # get length
                length = int(bin_string[0:15], 2)

                # cut the length from the bitstring
                bin_string = bin_string[15:]

                # get all subpackets
                sub_packets = parseBinString(bin_string[0:length])

                # cut subpackets out of bitstring
                bin_string = bin_string[length:]

                # either concatenate the result with the parsing of the rest of the bitstring or return the result if the string ends
                if len(bin_string) > 0 and not outermost:
                    rest = parseBinString(bin_string)
                    return (
                        [(packet_version, packet_typeID, sub_packets)] + rest
                        if rest
                        else [(packet_version, packet_typeID, sub_packets)]
                    )
                else:
                    return [(packet_version, packet_typeID, sub_packets)]

            if length_type_ID == "1":

                # get the length
                length = int(bin_string[0:11], 2)

                # cut the length out of the string
                bin_string = bin_string[11:]

                # get all coming packets
                potential_subpackets = parseBinString(bin_string)

                # declare length many packets as being from this one and concatenate the rest
                return [
                    (packet_version, packet_typeID, potential_subpackets[0:length])
                ] + potential_subpackets[length:]

    except Exception as e:
        print("Parsing Error!")
        print(e)
        return


def getVersionSum(result):
    """ Returns the sum of all versions of packets """
    if isinstance(result, list):
        # Unwrap the list
        return sum(map(getVersionSum, result))
    elif isinstance(result, tuple) and len(result) > 0:
        # get the current number
        number = result[0]
        # add numbers of other packets
        if len(result) > 2:
            number += getVersionSum(result[2])
        return number
    else:
        return 0


def part1(data, measure=False):
    """ Solves part 1 of the puzzle """

    startTime = time.time()
    result_1 = None

    # parse input
    input = parseInput(data)

    # create packets
    result = parseBinString(input, True)

    # evaluate packets
    result_1 = getVersionSum(result)

    executionTime = round(time.time() - startTime, 2)
    if measure:
        print("\nPart 1 took: " + str(executionTime) + " s")
    return result_1


def interpretResultPart2(result):
    """ Interprets the packets and returns the result """
    if isinstance(result, list):
        # unwrap the tuples
        if len(result) == 1:
            return interpretResultPart2(result[0])
        else:
            # contains list of packets
            return flatten_list(list(map(interpretResultPart2, result)))
    elif isinstance(result, tuple) and len(result) > 0:
        # switch over typeID
        packet_version, packet_typeID, packet_value = result
        if packet_typeID == 4:
            # Literal found
            return [int(packet_value)]
        elif packet_typeID == 0:
            # Sum
            return flatten_list([sum(interpretResultPart2(packet_value))])
        elif packet_typeID == 1:
            # Product
            res = interpretResultPart2(packet_value)
            return flatten_list(
                [functools.reduce(lambda a, b: a * b, res) if len(res) > 1 else res]
            )
        elif packet_typeID == 2:
            # Min
            return flatten_list([min(interpretResultPart2(packet_value))])
        elif packet_typeID == 3:
            # Max
            return flatten_list([max(interpretResultPart2(packet_value))])
        elif packet_typeID == 5:
            if len(packet_value) != 2:
                raise Exception("ERROR!")
            # Greater than
            return flatten_list(
                [
                    int(
                        interpretResultPart2(packet_value[0])[0]
                        > interpretResultPart2(packet_value[1])[0]
                    )
                ]
            )
        elif packet_typeID == 6:
            if len(packet_value) != 2:
                raise Exception("ERROR!")
            # Less than
            return flatten_list(
                [
                    int(
                        interpretResultPart2(packet_value[0])[0]
                        < interpretResultPart2(packet_value[1])[0]
                    )
                ]
            )
        elif packet_typeID == 7:
            if len(packet_value) != 2:
                raise Exception("ERROR!")
            # Equals
            return flatten_list(
                [
                    int(
                        interpretResultPart2(packet_value[0])[0]
                        == interpretResultPart2(packet_value[1])[0]
                    )
                ]
            )
    else:
        print("error")
        return 0


def part2(data, measure=False):
    """ Solves part two of the puzzle """
    startTime = time.time()
    result_2 = 0

    # parse input
    input = parseInput(data)

    # create packages
    result = parseBinString(input, True)

    # get result
    result_2 = interpretResultPart2(result)[0]

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

    # test cases for part 1
    test_sol = [6, 9, 14, 16, 12, 23, 31]

    test = True

    # Test part 2
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

    if test:
        if not runTests(test_sol, path) or sum(results) < len(results):
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

