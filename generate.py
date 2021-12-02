import os
import shutil

def main():
    path = os.getcwd()
    template_path = os.path.join(path, "Template")
    for i in range(1, 25):
        current_path = os.path.join(path, "Day " + str(i))
        if not os.path.exists(current_path):
            shutil.copytree(template_path, current_path)
            os.rename(str(current_path) + "\\part-1.py", str(current_path) + "\\day-" + str(i) + "-part-1.py" )
            os.rename(str(current_path) + "\\part-2.py", str(current_path) + "\\day-" + str(i) + "-part-2.py" )

if __name__ == "__main__":
    main()