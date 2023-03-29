import numpy as np

with open("Day 3/input.txt", "r") as file:
    lines = file.readlines()
    values = []
    for line in lines:
        for char in line:
            if not char == "\n":
                values.append(int(char))

    values = np.array(values).reshape(len(lines), -1)
    gamma = ""
    epsilon = ""

    for i in range(0, len(values[0])):
        if sum(values[:,i]) > (len(values) / 2.):
            # 1 is most common
            gamma += "1"
            epsilon += "0"
        else:
            # 0 is most common
            gamma += "0"
            epsilon += "1"
        
    print("Gamma: " + gamma + " Epsilon: " + epsilon+ "\n")
    print("Multiplication: " + str(int(gamma,2) * int(epsilon,2)))
        


