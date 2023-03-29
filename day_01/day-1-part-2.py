import numpy as np

values = np.loadtxt("Day 1/input.txt")

window_size = 3
increase = 0
for i in range(0, len(values) - window_size):
    if (values[i + window_size] > values[i]):
        increase += 1
print(increase)