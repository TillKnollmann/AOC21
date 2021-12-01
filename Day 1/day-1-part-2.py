with open("Day 1/input.txt", "r") as file:
    lines = file.readlines()
    measure = [int(lines[0]), int(lines[1]), int(lines[2])]
    measure_sum = sum(measure)
    increase = 0
    for i in range(3, len(lines)):
        # get new measure
        measure_new = [measure[1], measure[2], int(lines[i])]
        measure_new_sum = sum(measure_new)
        if (measure_new_sum > measure_sum):
            increase += 1
        measure = measure_new
        measure_sum = measure_new_sum
    print(increase)
