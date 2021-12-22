import os
import shutil

tab = "    "


def getTemplateCode(day):
    result = "import numpy as np\nimport time\nimport pprint\n\n"
    result += 'path = "Day ' + str(day) + '/input-test.txt"\n\n'
    result += "def main():\n"
    result += tab + 'with open(path, "r") as file:\n'
    result += tab + tab + "startTime = time.time()\n"
    result += tab + tab + "lines = file.readlines()\n"
    result += "\n" + tab + tab + "for line in lines:\n"
    result += tab + tab + tab + "break\n\n"
    result += tab + tab + 'print(" ")\n'
    result += tab + tab + "executionTime = round(time.time() - startTime, 2)\n"
    result += tab + tab + 'print("Execution time in seconds: " + str(executionTime))'
    result += '\n\nif __name__ == "__main__":\n\tmain()'
    return result


def main():
    path = os.getcwd()
    template_path = os.path.join(path, "Template")
    for i in range(1, 26):
        current_path = os.path.join(path, "Day " + str(i))
        if not os.path.exists(current_path):
            shutil.copytree(template_path, current_path)
            day_name = "day-" + str(i) + ".py"
            os.rename(
                str(current_path) + "\\template.py", str(current_path) + "\\" + day_name
            )
            file_data = ""
            with open(current_path + "\\" + day_name, "r") as file:
                file_data = file.read()
            file_data = file_data.replace("DAY", str(i))
            with open(current_path + "\\" + day_name, "w") as file:
                file.write(file_data)
            # with open(current_path + "\\" + day_name, "w") as file:
            # file.write(getTemplateCode(i))


if __name__ == "__main__":
    main()
