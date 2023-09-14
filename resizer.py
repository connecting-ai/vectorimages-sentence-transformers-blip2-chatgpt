from PIL import Image
import os

def resize(img, width, height):
    img = img.resize((width, height), Image.NEAREST)
    return img

path = "t/"
for filename in os.listdir(path):
    img = Image.open(path + filename)
    img = resize(img, 32, 32)
    img.save(path + filename)