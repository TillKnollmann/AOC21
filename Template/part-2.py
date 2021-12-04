import numpy as np
import time

with open(path, "r") as file:
    startTime = time.time()
    
    lines = file.readlines()
    
    for line in lines:
        break
    
    print("\n" + " ")

    executionTime = round(time.time() - startTime, 2)
    print('\nExecution time in seconds: ' + str(executionTime))