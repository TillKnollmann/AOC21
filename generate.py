import os
import shutil

def getTemplateCode(day):
    result = 'import numpy as np\nimport time\n\n'
    result += 'path = "Day ' + str(day) + '/input-test.txt"\n\n'
    result += 'def main():\n'
    result += '\twith open(path, "r") as file:\n'
    result += '\t\tstartTime = time.time()\n'
    result += '\t\tlines = file.readlines()\n'
    result += '\n\t\tfor line in lines:\n'
    result += "\t\t\tbreak\n\n"
    result += '\t\tprint(" ")\n'
    result += '\t\texecutionTime = round(time.time() - startTime, 2)\n'
    result += '\t\tprint("Execution time in seconds: " + str(executionTime))'
    result += '\n\nif __name__ == "__main__":\n\tmain()'
    return result
    

def main():
    path = os.getcwd()
    template_path = os.path.join(path, "Template")
    for i in range(1, 25):
        current_path = os.path.join(path, "Day " + str(i))
        if not os.path.exists(current_path):
            shutil.copytree(template_path, current_path)
            day_name = "day-" + str(i) + ".py"
            os.rename(str(current_path) + "\\template.py", str(current_path) + "\\" + day_name )
            with open(current_path + "\\" + day_name, "w") as file:
                file.write(getTemplateCode(i))

if __name__ == "__main__":
    main()