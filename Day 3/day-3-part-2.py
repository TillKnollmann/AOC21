import numpy as np

def find_most_common(input_array, position):
    if sum(input_array[:, position]) >= len(input_array) / 2.:
        return 1
    else:
        return 0

with open("Day 3/input.txt", "r") as file:
    lines = file.readlines()
    values = []
    for line in lines:
        for char in line:
            if not char == "\n":
                values.append(int(char))

    values = np.array(values).reshape(len(lines), -1)
    oxygen_gen_rat = values.copy()
    co2_scr_rat = values.copy()

    i = 0
    while i < len(values[0]) and len(oxygen_gen_rat) > 1:
        most_common = find_most_common(oxygen_gen_rat, i)
        if len(oxygen_gen_rat) > 1:
            oxygen_gen_rat = oxygen_gen_rat[oxygen_gen_rat[:,i] == most_common]
        i += 1

    i = 0
    while i < len(values[0]) and len(co2_scr_rat) > 1:
        most_common = find_most_common(co2_scr_rat, i)
        if len(co2_scr_rat) > 1:
            co2_scr_rat = co2_scr_rat[co2_scr_rat[:,i] != most_common]
        i += 1

    chars_to_replace = {
        '[': '',
        ']': '',
        ' ': ''
    }

    oxy_str = str(oxygen_gen_rat[0]).translate(str.maketrans(chars_to_replace))
    co2_str = str(co2_scr_rat[0]).translate(str.maketrans(chars_to_replace))
        
    print("Oxy: " + oxy_str + " CO2: " + co2_str + "\n")
    print("Multiplication: " + str(int(oxy_str,2) * int(str(co2_str),2)))
        


