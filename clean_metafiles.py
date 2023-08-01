import os

folder_name = "images/"

for folder in os.listdir(folder_name):
    for file in os.listdir(folder_name + folder):
        if file.endswith(".meta"):
            os.remove(folder_name + folder + "/" + file)