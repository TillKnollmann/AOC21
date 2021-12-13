import numpy as np
import time
import pprint
from aocd import get_data
from aocd import submit


def main():

    data = get_data(day=14, year=2021).splitlines()

    result_1 = 0
    result_2 = 0

    print(data)
    startTime = time.time()

    print(" ")
    executionTime = round(time.time() - startTime, 2)
    print("Execution time in seconds: " + str(executionTime))

    # submit(result_1, part="a", day=14, year=2021)
    # submit(result_2, part="b", day=14, year=2021)


if __name__ == "__main__":
    main()

