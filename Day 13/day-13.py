import numpy as np
import time
import pprint

path = "Day 13/input.txt"


def printMatrix(matrix):
    output = matrix.copy().astype("str")
    output[output == "0.0"] = " "
    output[output == "1.0"] = "#"

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

        matrix = np.zeros((max(points[:, 1]) + 1, max(points[:, 0]) + 1))

        for point in points:
            matrix[point[1], point[0]] = 1

        # printMatrix(matrix)

        first_fold = None

        for instruction in instructions:
            print(instruction)
            # print(matrix.shape)
            if instruction[0] == "y":
                # rotate the matrix leftwise
                matrix = np.rot90(matrix)
            # split matrix
            left_part = matrix[:, 0 : int(instruction[1])]
            right_part = np.fliplr(matrix[:, (len(matrix[0]) - int(instruction[1])) :])
            # print(left_part.shape)
            # print(right_part.shape)
            matrix = left_part + right_part
            # print(matrix)
            if instruction[0] == "y":
                # rotate back
                matrix = np.rot90(matrix, 3)
            matrix[matrix > 1] = 1
            if first_fold is None:
                first_fold = sum(matrix[matrix > 0])
                print(first_fold)
            # printMatrix(matrix)

        printMatrix(matrix)

        print("\nResult Part 1: " + str(first_fold))
        executionTime = round(time.time() - startTime, 2)
        print("Execution time in seconds: " + str(executionTime))


if __name__ == "__main__":
    main()
