from os import sep
import numpy as np
import re

def getBoardFromStringArray(string_array):
    result = []
    for line in string_array:
        numbers = np.array(re.split("\s+", line.replace('\n', '').strip()), dtype=np.int32)
        result.append(numbers)
    return np.array(result)

def processBoard(board, number):
    board[board == number] = -1
    return board

def checkBoard(board):
    if len(board[board==-1]) < 5:
        return False
    else:
        for i in range(0, 5):
            if len(board[i,:][board[i,:]==-1]) == 5 or len(board[:,i][board[:,i]==-1]) == 5:
                return True
        return False


def calculateScore(board, last_number):
    print(board)
    board_sum = sum(board[board>=0])
    print("Last Number: " + str(last_number) + " Sum: " + str(board_sum))
    return last_number * board_sum


with open("Day 4/input.txt", "r") as file:
    lines = file.readlines()

    random_numbers = np.array(lines[0].replace('\n', '').split(sep=","), dtype=np.int32)

    # now get the boards
    board_size = 5

    boards = []

    for i in range(2, len(lines), board_size+1):
        boards.append(getBoardFromStringArray(lines[i:i+board_size]))

    boards = np.array(boards)

    i = 0
    won = False

    while i < len(random_numbers) and not won:
        for board in boards:
            board = processBoard(board, random_numbers[i])
            if (checkBoard(board)):
                won = True
                print(calculateScore(board, random_numbers[i]))
        i += 1