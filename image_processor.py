from PIL import Image

def findHeight(img):
    width, height = img.size
    for y in range(height):
        for x in range(width):
            if img.getpixel((x,y)) != (0,0,0,0):
                return y
    return 0

def cutWhite(img):
    width, height = img.size
    img = img.crop((0, findHeight(img), width, height))
    return img

def cutWhiteBottom(img):
    width, height = img.size
    for y in range(height-1, 0, -1):
        for x in range(width):
            if img.getpixel((x,y)) != (0,0,0,0):
                img = img.crop((0, 0, width, y))
                return img
    return img

def cutWhiteLeft(img):
    width, height = img.size
    for x in range(width):
        for y in range(height):
            if img.getpixel((x,y)) != (0,0,0,0):
                img = img.crop((x, 0, width, height))
                return img
    return img

def cutWhiteRight(img):
    width, height = img.size
    for x in range(width-1, 0, -1):
        for y in range(height):
            if img.getpixel((x,y)) != (0,0,0,0):
                img = img.crop((0, 0, x, height))
                return img
    return img

def cleanImage(imgPath):
    img = Image.open(imgPath)
    img = cutWhite(img)
    img = cutWhiteBottom(img)
    img = cutWhiteLeft(img)
    img = cutWhiteRight(img)
    return img

def resize_image(img, width, height):
    if width == 0 and height == 0:
        (width, height) = img.size
        width //= 2
        height //= 2
        
    new_width = width
    new_height = height
    resized_img = img.resize((new_width, new_height), Image.LANCZOS)
    return resized_img