import envReader
envReader.read()

import datetime
from fastapi import FastAPI, File, Form, UploadFile
import aiofiles
import os
from zipfile import ZipFile
from clip import run
import shutil
import base64
import random
from PIL import Image
import io
from image_processor import resize_image

if envReader.getBool('USE_GDRIVE'):
    import drive
    drive.initGDrive()

if not os.path.exists('images'):
    os.mkdir('images')
    
CHUNK_SIZE = 1024 * 1024  # adjust the chunk size as desired
app = FastAPI()

@app.post("/query")
async def upload(file: UploadFile = File(...), query: str = Form(...)):
    datetimenow_timestamp = datetime.datetime.now().timestamp()
    images_path = "images_" + str(datetimenow_timestamp) + '/'
    current_path = os.path.dirname(os.path.realpath(__file__))
    filepath = os.path.join(current_path, os.path.basename(file.filename))
    async with aiofiles.open(filepath, 'wb') as f:
        chunk = await file.read(CHUNK_SIZE)
        while chunk:
            await f.write(chunk)
            
    with ZipFile(filepath, 'r') as zipObj:
        zipObj.extractall(images_path)
    
    os.remove(filepath)
    result = run(images_path + "*", query)

    images = []
    for res in result:
        base_path = images_path
        imgPath = base_path + res
        with open(imgPath, "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read())
            images.append(encoded_string.decode('utf-8'))

    shutil.rmtree(images_path)
    return images

@app.get("/query_local")
async def query_local(query: str, folder_name: str):
    path = "images/" + folder_name + "/"
    result = run(path + "*", query)
    
    images = []
    for res in result:
        base_path = path
        imgPath = base_path + res
        with open(imgPath, "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read())
            images.append(encoded_string.decode('utf-8'))
    
    return images

@app.get("/get_images")
async def query_images(query: str, folder_name: str, randomize: bool, width: int, height: int):
    path = "images/" + folder_name + "/"
    result = run(path + "*", query)
    image_path = result[0]
    if randomize:
        topChoices = result[:3]
        image_path = random.choice(topChoices)
    with open(path + image_path, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read())
        b64 = encoded_string.decode('utf-8')
        if width > -1 and height > -1:
            img = Image.open(io.BytesIO(base64.b64decode(b64)))
            resized_img = resize_image(img, width, height)
            print("resizing to: " + str(width) + "x" + str(height) + " resized: " + str(resized_img.size))
            buffered = io.BytesIO()
            resized_img.save(buffered, format="PNG")
            b64 = base64.b64encode(buffered.getvalue())
        return b64
@app.get("/query_drive")
async def query_drive(query: str, folder_name: str):
    if envReader.getBool('USE_GDRIVE'):
        import drive
        result = drive.quiery(query, folder_name)
        return result   
    else:
        return []

@app.get('/healthz', status_code=200, response_model=dict)
async def healthz():
    """"
    Health check endpoint required for Kubernetes LB periodic pings
    """
    return {'status': 'OK'}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)