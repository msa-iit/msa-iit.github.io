from flask import Flask, jsonify
from flask_cors import CORS
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
from oauth2client.client import GoogleCredentials
from oauth2client.service_account import ServiceAccountCredentials
from googleapiclient.discovery import build
from google.oauth2 import service_account
import gspread
from datetime import datetime, timedelta
import sys
import time
import os
import requests
import json


def Start_Drive():
    filename = app.config['drive_creds_filename']
    gauth = GoogleAuth()
    # Try to load saved client credentials
    gauth.LoadCredentialsFile(filename)
    if gauth.credentials is None:
        # Authenticate if they're not there
        gauth.LocalWebserverAuth()
    elif gauth.access_token_expired:
        # Refresh them if expired
        gauth.Refresh()
    else:
        # Initialize the saved creds
        gauth.Authorize()
    # Save the current credentials to a file
    gauth.SaveCredentialsFile(filename)
<<<<<<< HEAD
    return GoogleDrive(gauth)

# def Get_Docs():
#     docs_creds_filename = app.config['docs_creds_filename']
#     credentials = service_account.Credentials.from_service_account_file(docs_creds_filename, scopes=['https://www.googleapis.com/auth/documents'])
#     docs = build('docs', 'v1', credentials=credentials)
#     return docs

# def Get_Docs_File_Content(file_id) -> str:
#     service = app.config['google_docs']
#     if(service == None):
#         return "Docs not initialized"
=======

    app.config['google_drive'] = GoogleDrive(gauth)

def Refresh_Drive():
    gauth:GoogleAuth = app.config['google_drive']
    if gauth.access_token_expired:
        filename = app.config['drive_creds_filename']
        gauth.Refresh()
        gauth.SaveCredentialsFile(filename)
        app.config['google_drive'] = gauth

def Start_Docs():
    docs_creds_filename = app.config['docs_creds_filename']
    credentials = service_account.Credentials.from_service_account_file(docs_creds_filename, scopes=['https://www.googleapis.com/auth/documents'])
    service = build('docs', 'v1', credentials=credentials)
    app.config['google_docs'] = service

def Get_Folder_ID() -> str:
    drive = app.config['google_drive']
    folder_name = app.config['folder_name']
    folder_list = drive.ListFile({'q': f"title='{folder_name}' and mimeType='application/vnd.google-apps.folder'"}).GetList()
    # If the folder is found, use its ID
    if len(folder_list) > 0:
        return folder_list[0]['id']
    else:
        return None

def Get_FileID(filename) -> str:
    drive = app.config['google_drive']
    folder_list = drive.ListFile({'q': f"title='{filename}' and mimeType='application/vnd.google-apps.folder'"}).GetList()
    # If the folder is found, use its ID
    if len(folder_list) > 0:
        return folder_list[0]['id']
    else:
        return None

def Get_File_Content(file_id) -> str:
    service = app.config['google_docs']
    if(service == None):
        return "Docs not initialized"
>>>>>>> parent of 606e8c8 (commit in order to pull working TV configuration)
    
#     document = service.documents().get(documentId=file_id).execute()
#     document_content = document.get('body', {}).get('content', '')

<<<<<<< HEAD
#     # Extract and print the text content
#     doc_text = ''
#     for elem in document_content:
#         if 'paragraph' in elem:
#             doc_text += elem['paragraph']['elements'][0]['textRun']['content']
=======
    # Extract and print the text content
    doc_text = ''
    for elem in document_content:
        if 'paragraph' in elem:
            doc_text += elem['paragraph']['elements'][0]['textRun']['content']

    return doc_text

def init_app() -> Flask:
    app = Flask(__name__)
    # app.config.from_object('config.Config')
    
    with app.app_context():
        Start_Drive()
        Start_Docs()

        app.config['Last Refresh'] = datetime.now()

        folder_id = Get_Folder_ID()
        if folder_id == None:
            print("'MSA TV' folder not found in drive")
            sys.exit()
        app.config['folder_id'] = folder_id

        announcements_fileid = Get_FileID('announcements')
        if announcements_fileid == None:
            print("'announcements' folder not found in drive")
            app.config['announcements_fileid'] = announcements_fileid
            sys.exit()
        app.config['announcements_fileid'] = None

        from . import routes

        return app 
>>>>>>> parent of 606e8c8 (commit in order to pull working TV configuration)

#     return doc_text

app = Flask(__name__)
CORS(app)

# Global Variables
# Store results of previous endpoints to avoid unnecessary computation.
app.config['Iqamahs'] = {}
<<<<<<< HEAD
app.config['drive_creds_filename'] = "mycreds.txt"
app.config['docs_creds_filename'] = "msa_service_account_key.json"
=======
app.config['google_drive'] = None
app.config['google_docs'] = None
app.config['Last Refresh'] = None
app.config['drive_creds_filename'] = "mycreds.txt"
app.config['docs_creds_filename'] = "msa_service_account_key.json"
app.config['folder_name'] = "MSA TV"
app.config['folder_id'] = None
app.config['announcements_filename'] = "announcements"
app.config['announcements_fileid'] = None
app.config['announcements'] = None
>>>>>>> parent of 606e8c8 (commit in order to pull working TV configuration)

@app.route('/LoadImages')
def LoadImages():
    drive = Get_Drive()
    with open('./data/MetaData.json', 'r') as file:
        file_data = json.load(file)
        folder_id = file_data["SlideshowPictures_folder_id"]

    drive_images_raw = drive.ListFile({'q': f"'{folder_id}' in parents and mimeType contains 'image/' and trashed = false"}).GetList()
    drive_images = {file['title']:file['modifiedDate'] for file in drive_images_raw if file['mimeType'].startswith('image/')}
    # image_list = [file['webContentLink'].replace('&export=download','') for file in file_list]
    # image_list = [f"https://lh3.google.com/u/0/d/{file['id']}" for file in file_list]
    # image_list = [f"https://drive.google.com/uc?export=view&id={file['id']}" for file in file_list]


    with open('./data/slide_image_data.json', 'r') as file:
        current_images = json.load(file)

    images_to_add = []
    if drive_images:
        for image_title in drive_images.keys():
            if (image_title not in current_images) or (drive_images[image_title] != current_images[image_title]): 
                images_to_add.append(image_title)

    images_to_delete = []
    if current_images:
        for image_title in current_images.keys():
            if (image_title not in drive_images) or (current_images[image_title] != drive_images[image_title]): 
                images_to_delete.append(image_title)

    current_directory = os.path.dirname(os.path.realpath(__file__))
    destination_folder = os.path.join(current_directory, '..' ,'iitmsatv', 'src', 'images', 'Slideshow')

    for file in drive_images_raw:
        if file['title'] in images_to_add:
            file.GetContentFile(os.path.join(destination_folder, file['title']))

    for file in images_to_delete:
        os.remove(os.path.join(destination_folder, file))

    with open('./data/slide_image_data.json', 'w') as file:
        json.dump(drive_images, file)

    return jsonify(drive_images)

@app.route('/Iqamahs')
def Iqamahs():
    with open('./data/MetaData.json', 'r') as file:
        file_data = json.load(file)
        file_id = file_data["Iqamahs_file_id"]

    docs_creds_filename = app.config['docs_creds_filename']

    # Define the scope and credentials
    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    credentials = ServiceAccountCredentials.from_json_keyfile_name(docs_creds_filename, scope)
    
    # Authorize the client with the credentials
    client = gspread.authorize(credentials)
    sheet = client.open_by_key(file_id).sheet1

    prayers = sheet.range('A2:A8')
    times = sheet.range('B2:B8')
    iqamahs = {prayers[i].value : times[i].value for i in range(len(prayers))}

    return jsonify(iqamahs)

@app.route('/prayerAPI')
def prayerAPI():
    date = datetime.now()
    with open('./data/MetaData.json') as f: 
        file_content = json.load(f) 
    month = int(file_content["last_aladhanAPI_call"][:2]) 
    year = int(file_content["last_aladhanAPI_call"][3:7])

    if date.year > year or (date.month > month): 
        method = 2
        school = 1 
        api_response = requests.get(f"https://api.aladhan.com/v1/calendarByCity/{date.year}/{date.month}?city=Chicago&country=United%20States&method={method}&school={school}").json() 
        with open('./data/aladhanAPIsave.json', 'w') as f: 
            json.dump(api_response, f) # Update Settings File to remember that we grabbed new data for this month 
        file_content["last_aladhanAPI_call"] = f"{date.month:02d}/{date.year}" 
        with open('./data/MetaData.json', 'w') as f: 
            json.dump(file_content, f) 
            return jsonify(api_response)
    else: 
        with open('./data/aladhanAPIsave.json', encoding='utf-8') as f:
            api_save = json.load(f)
        return jsonify(api_save)

@app.route('/prayerTimesToday')
def prayerTimesToday():
    jsonAPIdata = dict(prayerAPI().json)
    today = datetime.now()
    idx = today.day - 1

    today_data = jsonAPIdata['data'][idx]['timings']

    return jsonify(today_data)

@app.route('/todayHijri')
def todayHijri():
    jsonAPIdata = dict(prayerAPI().json)
    MONTHS = ["Muharram", "Safar", "Rabi al-Awwal", "Rabi al-Thani", "Jumada al-Awwal", "Jumada al-Thani", "Rajab", "Shaban", "Ramadan", "Shawwal", "Dhu al-Qadah", "Dhu al-Hijjah"];
    today = datetime.now()
    day_idx = today.day - 1

    weekday = jsonAPIdata['data'][day_idx]['date']['hijri']['weekday']['en']
    day = jsonAPIdata['data'][day_idx]['date']['hijri']['day']
    month_idx = int(jsonAPIdata['data'][day_idx]['date']['hijri']['month']['number']) - 1
    year = jsonAPIdata['data'][day_idx]['date']['hijri']['year']
    month = MONTHS[month_idx]

    return (weekday + ", " + month + " " + day + ", " + year)

@app.route('/NextSalah')
def NextSalah():
    if app.config['Iqamahs']:
        Iqamah_Times = app.config['Iqamahs']
    else:
        Iqamah_Times = dict(Iqamahs().json)

    
    Today_Times = dict(prayerTimesToday().json)
    
<<<<<<< HEAD
    currentTime = datetime.now()
    # currentTime = datetime(2023, 10, 21, 12, 0, 0)
=======
    currentTime = datetime(2023,9,26,10,20)
>>>>>>> parent of 606e8c8 (commit in order to pull working TV configuration)
    StartOfDay = datetime(currentTime.year, currentTime.month, currentTime.day, 0, 0, 0, 0)

    FajrHour = int(Today_Times['Fajr'][:2])
    FajrMinute = int(Today_Times['Fajr'][3:5])
    FajrTime = datetime(currentTime.year, currentTime.month, currentTime.day, FajrHour, FajrMinute, 0, 0)

    FajrIqamahHour = int(Iqamah_Times['Fajr'][:2]) if len(Iqamah_Times['Fajr']) else None
    FajrIqamahMinute = int(Iqamah_Times['Fajr'][3:5]) if len(Iqamah_Times['Fajr']) else None
    FajrIqamah = datetime(currentTime.year, currentTime.month, currentTime.day, FajrHour, FajrMinute, 0, 0) if FajrIqamahHour and FajrIqamahMinute else None

    SunriseHour = int(Today_Times['Sunrise'][:2])
    SunriseMinute = int(Today_Times['Sunrise'][3:5])
    SunriseTime = datetime(currentTime.year, currentTime.month, currentTime.day, SunriseHour, SunriseMinute, 0, 0)

    DhuhrHour = int(Today_Times['Dhuhr'][:2])
    DhuhrMinute = int(Today_Times['Dhuhr'][3:5])
    DhuhrTime = datetime(currentTime.year, currentTime.month, currentTime.day, DhuhrHour, DhuhrMinute, 0, 0)

    DhuhrIqamahHour = int(Iqamah_Times['Dhuhr'][:2]) if len(Iqamah_Times['Dhuhr']) else None
    DhuhrIqamahMinute = int(Iqamah_Times['Dhuhr'][3:5]) if len(Iqamah_Times['Dhuhr']) else None
    DhuhrIqamah = datetime(currentTime.year, currentTime.month, currentTime.day, DhuhrHour, DhuhrMinute, 0, 0) if DhuhrIqamahHour and DhuhrIqamahMinute else None

    JummahKhutbahHour = int(Iqamah_Times['JummahKhutbah'][:2])
    JummahKhutbahMinute = int(Iqamah_Times['JummahKhutbah'][3:5])
    JummahKhutbah = datetime(currentTime.year, currentTime.month, currentTime.day, JummahKhutbahHour, JummahKhutbahMinute, 0, 0)

    JummahIqamahHour = int(Iqamah_Times['JummahIqamah'][:2])
    JummahIqamahMinute = int(Iqamah_Times['JummahIqamah'][3:5])
    JummahIqamah = datetime(currentTime.year, currentTime.month, currentTime.day, JummahIqamahHour, JummahIqamahMinute, 0, 0)

    AsrHour = int(Today_Times['Asr'][:2])
    AsrMinute = int(Today_Times['Asr'][3:5])
    AsrTime = datetime(currentTime.year, currentTime.month, currentTime.day, AsrHour, AsrMinute, 0, 0)

    AsrIqamahHour = int(Iqamah_Times['Asr'][:2]) if len(Iqamah_Times['Asr']) else None
    AsrIqamahMinute = int(Iqamah_Times['Asr'][3:5]) if len(Iqamah_Times['Asr']) else None
    AsrIqamah = datetime(currentTime.year, currentTime.month, currentTime.day, AsrIqamahHour, AsrIqamahMinute, 0, 0) if AsrIqamahHour and AsrIqamahMinute else None

    MaghribHour = int(Today_Times['Maghrib'][:2])
    MaghribMinute = int(Today_Times['Maghrib'][3:5])
    MaghribTime = datetime(currentTime.year, currentTime.month, currentTime.day, MaghribHour, MaghribMinute, 0, 0)

    MaghribIqamahHour = int(Iqamah_Times['Maghrib'][:2]) if len(Iqamah_Times['Maghrib']) else None
    MaghribIqamahMinute = int(Iqamah_Times['Maghrib'][3:5]) if len(Iqamah_Times['Maghrib']) else None
    MaghribIqamah = datetime(currentTime.year, currentTime.month, currentTime.day, MaghribIqamahHour, MaghribIqamahMinute, 0, 0) if MaghribIqamahHour and MaghribIqamahMinute else None

    IshaHour = int(Today_Times['Isha'][:2])
    IshaMinute = int(Today_Times['Isha'][3:5])
    IshaTime = datetime(currentTime.year, currentTime.month, currentTime.day, IshaHour, IshaMinute, 0, 0)

    IshaIqamahHour = int(Iqamah_Times['Isha'][:2]) if len(Iqamah_Times['Isha']) else None
    IshaIqamahMinute = int(Iqamah_Times['Isha'][3:5]) if len(Iqamah_Times['Isha']) else None
    IshaIqamah = datetime(currentTime.year, currentTime.month, currentTime.day, IshaIqamahHour, IshaIqamahMinute, 0, 0) if IshaIqamahHour and IshaIqamahMinute else None

    if StartOfDay <= currentTime <= FajrTime:
        result = {
            'prayer': 'Fajr',
            'type': 'time',
            'time': FajrTime.strftime("%a, %d %b %Y %H:%M")
        }
    elif FajrIqamah and FajrTime <= currentTime < FajrIqamah:
        result = {
            'prayer': 'Fajr',
            'type': 'iqamah',
            'time': FajrIqamah.strftime("%a, %d %b %Y %H:%M")
        }
    elif FajrTime <= currentTime < SunriseTime:
        result = {
            'prayer': 'Sunrise',
            'type': 'time',
            'time': SunriseTime.strftime("%a, %d %b %Y %H:%M")
        }
    elif currentTime.weekday() == 4 and SunriseTime <= currentTime < JummahKhutbah:
        result = {
            'prayer': 'Jummah',
            'type': 'khutbah',
            'time': JummahKhutbah.strftime("%a, %d %b %Y %H:%M")
        }
    elif currentTime.weekday() == 4 and JummahKhutbah <= currentTime < JummahIqamah:
        result = {
            'prayer': 'Jummah',
            'type': 'iqamah',
            'time': JummahIqamah.strftime("%a, %d %b %Y %H:%M")
        }    
    elif currentTime.weekday() == 4 and JummahIqamah <= currentTime < AsrTime:
        result = {
            'prayer': 'Asr',
            'type': 'time',
            'time': AsrTime.strftime("%a, %d %b %Y %H:%M")
        }
    elif SunriseTime <= currentTime < DhuhrTime:
        result = {
            'prayer': 'Dhuhr',
            'type': 'time',
            'time': DhuhrTime.strftime("%a, %d %b %Y %H:%M")
        }
    elif DhuhrIqamah and DhuhrTime <= currentTime < DhuhrIqamah:
        result = {
            'prayer': 'Dhuhr',
            'type': 'iqamah',
            'time': DhuhrIqamah.strftime("%a, %d %b %Y %H:%M")
        }
    elif DhuhrTime <= currentTime < AsrTime: 
        result = { 
            'prayer': 'Asr',
            'type': 'time', 
            'time': AsrTime.strftime("%a, %d %b %Y %H:%M")
        }
    elif AsrIqamah and AsrTime <= currentTime < AsrIqamah:
        result = {
            'prayer': 'Asr',
            'type': 'iqamah',
            'time': AsrIqamah.strftime("%a, %d %b %Y %H:%M")
        }
    elif AsrTime <= currentTime < MaghribTime: 
        result = { 
            'prayer': 'Maghrib',
            'type': 'time', 
            'time': MaghribTime.strftime("%a, %d %b %Y %H:%M")
        }
    elif MaghribIqamah and MaghribTime <= currentTime < MaghribIqamah:
        result = {
            'prayer': 'Maghrib',
            'type': 'iqamah',
            'time': MaghribIqamah.strftime("%a, %d %b %Y %H:%M")
        }
    elif MaghribTime <= currentTime < IshaTime: 
        result = { 
            'prayer': 'Isha',
            'type': 'time', 
            'time': IshaTime.strftime("%a, %d %b %Y %H:%M")
        }
    elif IshaIqamah and IshaTime <= currentTime < IshaIqamah:
        result = {
            'prayer': 'Isha',
            'type': 'iqamah',
            'time': IshaIqamah.strftime("%a, %d %b %Y %H:%M")
        }
    else:
        result = { 
            'prayer': 'Fajr',
            'type': 'time', 
            'time': (FajrTime + timedelta(days=1)).strftime("%a, %d %b %Y %H:%M")
        }

    return jsonify(result)

@app.route('/todayGreg')
def todayGreg():
    return datetime.now().strftime('%A, %B %d, %Y')

@app.route('/SlideshowDelay')
def slideshowDelay():
    with open('./data/MetaData.json') as f: 
        file_content = dict(json.load(f))
        file_id = file_content["TV_settings_file_id"]
    
    docs_creds_filename = app.config['docs_creds_filename']

    # Define the scope and credentials
    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    credentials = ServiceAccountCredentials.from_json_keyfile_name(docs_creds_filename, scope)
    
    # Authorize the client with the credentials
    client = gspread.authorize(credentials)
    sheet = client.open_by_key(file_id).sheet1

    i = 1
    setting_name = sheet.acell(f'A{i}').value
    while setting_name != "":
        if setting_name == "Slideshow Delay":
            return sheet.acell(f'B{i}').value
        else:
            i += 1
    return 15 # Setting not found in google sheet so a default value of 15 seconds is sent  

if __name__ == '__main__':
    app.run(port=7000)