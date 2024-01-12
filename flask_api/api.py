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


def Get_Drive():
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
    
#     document = service.documents().get(documentId=file_id).execute()
#     document_content = document.get('body', {}).get('content', '')

#     # Extract and print the text content
#     doc_text = ''
#     for elem in document_content:
#         if 'paragraph' in elem:
#             doc_text += elem['paragraph']['elements'][0]['textRun']['content']

#     return doc_text

app = Flask(__name__)
CORS(app)

# Global Variables
# Store results of previous endpoints to avoid unnecessary computation.
app.config['Iqamahs'] = {}
app.config['drive_creds_filename'] = "mycreds.txt"
app.config['docs_creds_filename'] = "msa_service_account_key.json"

@app.route('/SlideshowImageURLs')
def SlideshowImageURLs():
    drive = Get_Drive()
    with open('./data/MetaData.json', 'r') as file:
        file_data = json.load(file)
        folder_id = file_data["SlideshowPictures_folder_id"]

    file_list = drive.ListFile({'q': f"'{folder_id}' in parents and mimeType contains 'image/' and trashed = false"}).GetList()
    # image_list = [file['webContentLink'].replace('&export=download','') for file in file_list]
    image_list = [f"https://lh3.google.com/u/0/d/{file['id']}" for file in file_list]
    # image_list = [f"https://drive.google.com/uc?export=view&id={file['id']}" for file in file_list]

    return jsonify(image_list)

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
    
    currentTime = datetime.now()
    # currentTime = datetime(2023, 10, 21, 12, 0, 0)
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