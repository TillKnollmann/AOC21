import os
import shutil

def getTemplateCode(day):
    result = 'import numpy as np\nimport time\n\n'
    result += 'path = "Day ' + str(day) + '/input-test.txt"\n\n'
    result += 'with open(path, "r") as file:\n'
    result += '\tstartTime = time.time()\n'
    result += '\tlines = file.readlines()\n'
    result += '\n\tfor line in lines:\n'
    result += "\t\tbreak\n\n"
    result += '\tprint(" ")\n'
    result += '\texecutionTime = round(time.time() - startTime, 2)\n'
    result += '\tprint("Execution time in seconds: " + str(executionTime))'
    return result
    

def main():
    path = os.getcwd()
    template_path = os.path.join(path, "Template")
    for i in range(1, 25):
        current_path = os.path.join(path, "Day " + str(i))
        if not os.path.exists(current_path):
            shutil.copytree(template_path, current_path)
            day_1_name = "day-" + str(i) + "-part-1.py"
            day_2_name = "day-" + str(i) + "-part-2.py"
            os.rename(str(current_path) + "\\part-1.py", str(current_path) + "\\" + day_1_name )
            os.rename(str(current_path) + "\\part-2.py", str(current_path) + "\\" + day_2_name )
            with open(current_path + "\\" + day_1_name, "w") as file:
                file.write(getTemplateCode(i))
            with open(current_path + "\\" + day_2_name, "w") as file:
                file.write(getTemplateCode(i))

if __name__ == "__main__":
    main()