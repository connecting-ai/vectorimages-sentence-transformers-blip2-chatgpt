import os
import shutil
from image_processor import cleanImage

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
        file = file.replace(" ", "_").replace("-", "_").replace("(", "").replace(")", "").lower().strip()
        input_file_name = input_path + folder + "/" + prevFileName
        output_file_name = output_path + folder + "/" + file
        img = cleanImage(input_file_name)
        img.save(output_file_name)
