import datetime
from fastapi import FastAPI, File, Form, UploadFile, status
from fastapi.exceptions import HTTPException
import aiofiles
import os
from zipfile import ZipFile
from clip import run
import shutil

CHUNK_SIZE = 1024 * 1024  # adjust the chunk size as desired
app = FastAPI()

@app.post("/query")
async def upload(file: UploadFile = File(...), query: str = Form(...)):
    datetimenow_timestamp = datetime.datetime.now().timestamp()
    images_path = "images_" + str(datetimenow_timestamp) + '/'
    current_path = os.path.dirname(os.path.realpath(__file__))
    filepath = os.path.join(current_path, os.path.basename(file.filename))
    async with aiofiles.open(filepath, 'wb') as f:
        while chunk := await file.read(CHUNK_SIZE):
            await f.write(chunk)
            
    with ZipFile(filepath, 'r') as zipObj:
        zipObj.extractall(images_path)
    
    os.remove(filepath)
    result = run(images_path + "*", query)
    shutil.rmtree(images_path)

    return result

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=7777)