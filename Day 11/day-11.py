import numpy as np
import time

path = "Day 11/input.txt"


def main():
    with open(path, "r") as file:
        startTime = time.time()
        lines = file.readlines()

        map = []

        # read data
        for line in lines:
            map.append([char for char in line.replace("\n", "")])

        # parse to np array
        map = np.array(map, dtype=np.int32)

        print("Initial data:")
        print(map)

        # length of simulation for part 1
        sim_length = 100

        # total number of flashes within the first sim_length steps
        no_flashes = 0

        # determines if the simulation should stop
        keep_on = True

        # first time step in which all octopus flash simultaneously
        first_step_all = 1

        # current time step
        current_step = 0

        # number of entries
        no_entries = len(map) * len(map[0])

        while keep_on:
            current_step += 1
            # increase by one
            map = map + 1

            # determine flashing
            flashed = True
            while flashed:
                # only continue while we achieved progress in the last iteration
                flashed = False
                for j in range(0, len(map)):
                    for k in range(0, len(map[0])):
                        # select an entry >9 to flash
                        if map[j, k] > 9:
                            # invalidate the entry for the time step
                            map[j, k] = -1
                            for l in range(max(j - 1, 0), min(j + 2, len(map))):
                                for m in range(max(k - 1, 0), min(k + 2, len(map[0]))):
                                    # if the adjacent entry not already can flash, increase its counter
                                    if map[l, m] <= 9 and map[l, m] > -1:
                                        map[l, m] += 1
                                        flashed = True

            # mark all entries that flashed
            map[map > 9] = -1

            # get number of total flashed in this step
            current_flashes = len(map[map == -1])

            # remember number of total flashes if relevant for part 1
            if current_step <= sim_length:
                no_flashes += current_flashes

            # check if all octopus flashed
            if current_flashes == no_entries:
                keep_on = False
                first_step_all = current_step

            print("\nStep " + str(current_step))

            # normalize
            map[map == -1] = 0

        print("\nAfter 100 time steps there are " + str(no_flashes) + " flashes!")
        print(
            "\nAfter "
            + str(first_step_all)
            + " time steps all octopus flash simultaneously!"
        )

        executionTime = round(time.time() - startTime, 2)
        print("Execution time in seconds: " + str(executionTime))


if __name__ == "__main__":
    main()
