from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
import os
import shutil
import zipfile
import requests
import datetime
from clip import run

gauth = None
drive_id = "1ddfF-WwTx4anjp4P2w1fzd87xSACkYs3"
drive = None

def initGDrive():
    global gauth, drive
    gauth = GoogleAuth()
    gauth.LocalWebserverAuth()
    drive = GoogleDrive(gauth)

def quiery(query: str, folder_name: str):
    datetimenow_timestamp = datetime.datetime.now().timestamp()
    temp_path = "temp_" + str(datetimenow_timestamp) + '/'
    os.makedirs(temp_path, exist_ok=True)

    file_list = drive.ListFile({'q': "'" +drive_id + "' in parents and trashed=false"}).GetList()
    print('file_list: %s' % file_list)

    for file1 in file_list:
        print('title: %s, id: %s' % (file1['title'], file1['id']))
        if file1['mimeType'] == 'application/vnd.google-apps.folder':
            if file1['title'] == folder_name:
                file_list2 = drive.ListFile({'q': "'%s' in parents and trashed=false" % file1['id']}).GetList()
                for file2 in file_list2:
                    print('title: %s, id: %s' % (file2['title'], file2['id']))
                    file2.GetContentFile(os.path.join(temp_path, file2['title']))

    results = run(temp_path + "/*", query)
    shutil.rmtree(temp_path)
    return results