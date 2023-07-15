import os
import shutil

input_path = "images_input/"
output_path = "images/"

if os.path.exists(output_path):
    shutil.rmtree(output_path, ignore_errors=True)

os.mkdir(output_path)

for folder in os.listdir(input_path):
    os.mkdir(output_path + folder)
    for file in os.listdir(input_path + folder):
        print(file)
        prevFileName = file
        file = file.replace(" ", "_").lower().strip()
        shutil.copy(input_path + folder + "/" + prevFileName, output_path + folder + "/" + file)
