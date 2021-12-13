import numpy as np
import time
import pprint

path = "Day 13/input.txt"


def printMatrix(matrix):
    output = matrix.copy().astype("str")
    output[output == "0.0"] = " "
    output[output == "1.0"] = "#"
    output[output == "-1.0"] = "O"

    print("")
    for i in range(0, len(output)):
        line = ""
        for j in range(0, len(output[0])):
            line += str(output[i, j])
        print(line)


def main():
    with open(path, "r") as file:
        startTime = time.time()
        lines = file.readlines()

        points = []
        instructions = []

        # parse input
        isInput = True
        for line in lines:
            cleaned = line.replace("\n", "")
            if isInput:
                if len(cleaned) == 0:
                    isInput = False
                else:
                    point = np.array(cleaned.split(","), dtype=int)
                    points.append(point)
            else:
                instr = cleaned.split(" ")[2]
                instr = np.array(instr.split("="))
                instructions.append(instr)

        points = np.array(points)

        # build initial matrix
        matrix = np.zeros((max(points[:, 1]) + 1, max(points[:, 0]) + 1))

        for point in points:
            matrix[point[1], point[0]] = 1

        first_fold = None

        for instruction in instructions:

            if instruction[0] == "y":
                # rotate the matrix leftwise
                matrix = np.rot90(matrix, 1).copy()

            # split matrix
            left_part = matrix[:, 0 : int(instruction[1])].copy()

            # fill right part with trailing zeros
            right_part = matrix[:, int(instruction[1]) + 1 :].copy()
            temp = np.zeros(left_part.shape)
            temp[:, 0 : len(right_part[0])] = right_part
            right_part = temp.copy()

            # flip the right part
            right_part = np.fliplr(right_part)

            # fold
            matrix = left_part + right_part
            # rotate back
            if instruction[0] == "y":
                matrix = np.rot90(matrix, 3).copy()

            # normalize
            matrix[matrix >= 1] = 1

            # determine result part 1
            if first_fold is None:
                first_fold = sum(matrix[matrix > 0])

        # print result
        printMatrix(matrix)

        print("\nResult Part 1: " + str(first_fold))

        executionTime = round(time.time() - startTime, 2)
        print("Execution time in seconds: " + str(executionTime))


if __name__ == "__main__":
    main()
