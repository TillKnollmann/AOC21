with open("Day 2/input.txt", "r") as file:
    lines = file.readlines()
    forward = 0
    depth = 0
    aim = 0
    for line in lines:
        line_split = line.split(" ")
        command = line_split[0]
        value = int(line_split[1])
        if command == "forward":
            forward += value
            depth += (value * aim) 
        elif command == "down":
            aim += value
        elif command == "up":
            aim -= value
    print("Forward: " + str(forward) + " Downwards: " + str(depth) + " Aim: " + str(aim) + " Multiplication: " + str(forward * depth))