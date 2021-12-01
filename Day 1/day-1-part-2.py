with open("Day 1/input.txt", "r") as file:
    window_size = 3
    lines = file.readlines()
    measure = -1
    increase = 0
    for i in range(0, len(lines)-window_size):
        # get new measure
        measure = int(lines[i])
        measure_new = int(lines[i + window_size])
        if (measure_new > measure):
            increase += 1
    print(increase)
