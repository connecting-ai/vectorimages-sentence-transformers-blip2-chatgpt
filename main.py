import datetime
from fastapi import FastAPI, File, Form, UploadFile, status
from fastapi.exceptions import HTTPException
import aiofiles
import os
from zipfile import ZipFile
from clip import run
import shutil
import pydrive
import drive

drive.initGDrive()

CHUNK_SIZE = 1024 * 1024  # adjust the chunk size as desired
app = FastAPI()
main_path = "all_images/"

if not os.path.exists(main_path):
    os.mkdir(main_path)

@app.post("/query")
async def upload(file: UploadFile = File(...), query: str = Form(...), search_all: str = Form(...)):
    datetimenow_timestamp = datetime.datetime.now().timestamp()
    images_path = "images_" + str(datetimenow_timestamp) + '/'
    current_path = os.path.dirname(os.path.realpath(__file__))
    filepath = os.path.join(current_path, os.path.basename(file.filename))
    async with aiofiles.open(filepath, 'wb') as f:
        while chunk := await file.read(CHUNK_SIZE):
            await f.write(chunk)
            
    with ZipFile(filepath, 'r') as zipObj:
        zipObj.extractall(images_path)

    with ZipFile(filepath, 'r') as zipObj:
        zipObj.extractall(main_path)
    
    os.remove(filepath)
    result = []
    if search_all: 
        result = run(main_path + "*", query)
    else:
        result = run(images_path + "*", query)

    shutil.rmtree(images_path)

    return result

@app.get("/query")
async def query(query: str):
    result = run(main_path + "*", query)
    return result

@app.get("/query_drive")
async def query_drive(query: str, folder_name: str):
    result = drive.quiery(query, folder_name)
    return result   

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=7777)