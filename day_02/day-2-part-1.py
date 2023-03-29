with open("Day 2/input.txt", "r") as file:
    lines = file.readlines()
    forward = 0
    down = 0
    for line in lines:
        line_split = line.split(" ")
        command = line_split[0]
        value = int(line_split[1])
        if command == "forward":
            forward += value
        elif command == "down":
            down += value
        elif command == "up":
            down -= value
    print("Forward: " + str(forward) + " Downwards: " + str(down) + " Multiplication: " + str(forward * down))