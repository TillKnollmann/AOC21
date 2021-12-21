from datetime import date
import numpy as np
import time
import pprint
from copy import deepcopy

from importlib.machinery import SourceFileLoader

lib = SourceFileLoader("lib", "lib.py").load_module()

from aocd import get_data
from aocd import submit

day = 21
path = ""


def parseInput(input):
    result = []
    for line in input:
        current_line = line.replace("\n", "").strip()
        result.append(int(current_line.split(" ")[len(current_line.split(" ")) - 1]))
    return result


# the dice for part one
dice = 0
# the total number of rolls for part one
total_rolls = 0


def roll_dice(scores: list, pos: list, turn: int) -> list:
    """Rolls the dice for one player three times

    Args:
        scores (list): The current scores
        pos (list): The current positions
        turn (int): The player who's turn it is

    Returns:
        list: The new scores and the new positions
    """
    global dice
    global total_rolls

    # do three steps directly
    total_rolls += 3
    # increase the dice by three
    dice += 3
    # flip the dice back to 1 if it is at 101
    if dice > 100:
        dice = dice % 100
    # increase the position by dice + dice - 1 + dice - 2
    pos[turn] += 3 * dice - 3
    if pos[turn] > 10:
        pos[turn] = pos[turn] % 10
        if pos[turn] % 10 == 0:
            pos[turn] = 10
    # calculate score
    scores[turn] += pos[turn]

    return scores, pos


def apply_dice(scores: list, pos: list, turn: int, incr: int):
    """Applies the dice on the scores and the positions for the given player who's turn it is by an increment incr

    Args:
        scores (list): The current scores
        pos (list): The current positions
        turn (int): The player who's turn it is
        incr (int): The increment (Result of dice roll)

    Returns:
        list: the new scores and new positions
    """
    pos_new = deepcopy(pos)
    scores_new = deepcopy(scores)
    # calculate new positions
    pos_new[turn] += incr
    # if position gets too large, correct
    if pos_new[turn] > 10:
        pos_new[turn] = pos_new[turn] % 10
        if pos_new[turn] % 10 == 0:
            pos_new[turn] = 10
    # calculate new scores
    scores_new[turn] += pos_new[turn]

    return scores_new, pos_new


# possible dice results after three rolls and the number of possibilities
possible_dice_rolls = [(3, 1), (4, 3), (5, 6), (6, 7), (7, 6), (8, 3), (9, 1)]

# cache for part two
cache = {}


def roll_dice_recursive(scores: list, pos: list, turn: int):
    """Returns the possible wins for each player when starting at the state given by the scores, the positions and the identifier who's turn it is

    Args:
        scores (list): The current scores
        pos (list): The current positions
        turn (int): The index of the player who's turn it is

    Returns:
        list: A list containing the number of possible wins for each player
    """
    global possible_dice_rolls, cache
    # generate key
    key = str(scores) + str(pos) + str(turn)
    # look if we already calculated this situation
    if key in cache:
        return cache[key]
    # if one player wins, return 1 possibility
    if scores[0] >= 21:
        return [1, 0]
    if scores[1] >= 21:
        return [0, 1]
    # count the possibilities for each player
    wins_one = 0
    wins_two = 0
    # calculate possible ways
    for i in range(len(possible_dice_rolls)):
        # get new scores and positions if the dice shows possible_dice_rolls[i][0]
        scores_new, pos_new = apply_dice(scores, pos, turn, possible_dice_rolls[i][0])
        # get recursion results
        if turn == 0:
            recursive_result = roll_dice_recursive(scores_new, pos_new, 1)
        else:
            recursive_result = roll_dice_recursive(scores_new, pos_new, 0)
        # calculate possible ways of getting the recursion result
        wins_one += recursive_result[0] * possible_dice_rolls[i][1]
        wins_two += recursive_result[1] * possible_dice_rolls[i][1]
    # set cache entry
    cache[key] = [wins_one, wins_two]
    return [wins_one, wins_two]


def part1(data, measure=False):
    global total_rolls, dice

    total_rolls = 0
    dice = 0
    startTime = time.time()

    pos = parseInput(data)

    scores = [0 for _ in range(len(pos))]

    turn = 0
    while max([1 if scores[i] >= 1000 else 0 for i in range(len(scores))]) < 1:
        scores, pos = roll_dice(scores, pos, turn)
        turn += 1
        turn = turn % len(pos)

    result_1 = total_rolls * min(scores)

    executionTime = round(time.time() - startTime, 2)
    if measure:
        print("\nPart 1 took: " + str(executionTime) + " s")
    return result_1


def part2(data, measure=False):
    global cache
    cache = {}
    startTime = time.time()

    pos = parseInput(data)

    scores = [0 for _ in range(len(pos))]

    turn = 0

    result = roll_dice_recursive(scores, pos, turn)

    result_2 = max(result)

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

    test_sol = [739785, 444356092776315]  # Todo put in test solutions

    test = True  # Todo

    sol1 = sub1 = True  # Todo
    sol2 = sub2 = True  # Todo

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

