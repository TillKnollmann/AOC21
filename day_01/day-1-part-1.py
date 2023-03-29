import numpy as np

values = np.loadtxt("Day 1/input.txt")

increases = 0

for i in range(0, len(values)-1):
    if values[i] < values[i+1]:
        increases += 1
print(increases)