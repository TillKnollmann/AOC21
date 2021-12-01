with open("Day 1/input.txt", "r") as file:
    increases = 0
    lastValue = -1
    for line in file.readlines():
        currentValue = int(line)
        if lastValue != -1 and lastValue < currentValue:
            increases += 1
        lastValue = currentValue
    print(increases)