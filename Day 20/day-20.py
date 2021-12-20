from datetime import date
import numpy as np
import time
import pprint

from tqdm import tqdm

from importlib.machinery import SourceFileLoader

lib = SourceFileLoader("lib", "lib.py").load_module()

from aocd import get_data
from aocd import submit

day = 20
path = ""


def parseInput(input):
    result = None

    # get image enhancement algorithm
    img_enh_algo = ""
    # get image
    img = []
    is_img = False
    for line in input:
        current_line = line.replace("\n", "").strip()
        if len(current_line) == 0:
            is_img = True
        elif not is_img:
            img_enh_algo += current_line
        else:
            img.append(current_line)

    # convert the algo to a 0,1 string
    img_enh_algo = tuple(
        [1 if img_enh_algo[i] == "#" else 0 for i in range(len(img_enh_algo))]
    )

    # convert the image to a 0,1 matrix
    init_img = np.zeros((len(img) + 2, len(img[0]) + 2), dtype=np.int8)
    for i in range(len(img)):
        for j in range(len(img[i])):
            if img[i][j] == "#":
                init_img[i + 1][j + 1] = 1

    return img_enh_algo, init_img


def apply_img_enh_algo_on(img_enh_alg: tuple, img: np.array, position: tuple) -> str:
    """Applies the image enhancement algorithm at the position to the image and returns the resulting string

    Args:
        img_enh_alg (tuple): The image enhancement algorithm
        img (np.array): The image
        position (tuple): The position

    Returns:
        str: The resulting character
    """

    sub_img = (
        img[position[0] - 1 : position[0] + 2, position[1] - 1 : position[1] + 2]
    ).reshape(-1)
    bin_value = "".join([str(sub_img[i]) for i in range(len(sub_img))])
    int_value = int(bin_value, 2)
    return img_enh_alg[int_value]


def apply_img_enh_algo(img_enh_algo: tuple, img: np.array, infty_ext: int) -> np.array:
    """Applies the image enhancement algorithm and returns the new image

    Args:
        img_enh_algo (tuple): The algorithm
        img (np.array): The current image

    Returns:
        np.array: The resulting image
    """
    # extend original image
    img_ext = np.zeros((len(img) + 4, len(img[0]) + 4), dtype=np.int8)
    # flush infinity extension
    img_ext = img_ext + infty_ext
    # embed original image
    img_ext[2 : len(img_ext) - 2, 2 : len(img_ext[0]) - 2] = img

    # fill calculated pixels
    res_img = np.zeros((len(img) + 4, len(img[0]) + 4), dtype=np.int8)
    for i in range(1, len(res_img) - 1):
        for j in range(1, len(res_img[i]) - 1):
            res_img[i][j] = apply_img_enh_algo_on(img_enh_algo, img_ext, (i, j))

    # calculate how the pixels in infinity extension look like
    infty_ext_new = img_enh_algo[int("".join([str(infty_ext) for i in range(9)]), 2)]

    # fill border
    res_img[:, 0] = infty_ext_new
    res_img[:, len(res_img) - 1] = infty_ext_new
    res_img[0, :] = infty_ext_new
    res_img[len(res_img[0]) - 1, :] = infty_ext_new

    return res_img, infty_ext_new


def print_img(img: np.array):
    """Prints the image with # (one) and _ (zero)

    Args:
        img (np.array): The image to be printed
    """
    complete = ""
    for line in img:
        out = ""
        for elem in line:
            out += "#" if elem > 0 else "_"
        complete += out + "\n"
    print(complete)


def part1(data, measure=False):
    startTime = time.time()
    result_1 = None

    img_enh_algo, init_img = parseInput(data)

    img = init_img.copy()
    infty_ext = 0

    for i in range(2):
        img, infty_ext = apply_img_enh_algo(img_enh_algo, img, infty_ext)

    result_1 = int(np.sum(img))

    executionTime = round(time.time() - startTime, 2)
    if measure:
        print("\nPart 1 took: " + str(executionTime) + " s")
    return result_1


def part2(data, measure=False):
    startTime = time.time()
    result_2 = None

    img_enh_algo, init_img = parseInput(data)

    img = init_img.copy()
    infty_ext = 0

    print("\nProcessing image")

    for i in tqdm(range(50)):
        img, infty_ext = apply_img_enh_algo(img_enh_algo, img, infty_ext)

    result_2 = int(np.sum(img))

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

    test_sol = [35, 3351]  # Todo put in test solutions

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

