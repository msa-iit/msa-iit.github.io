from flask import Flask, jsonify
import json
from datetime import datetime, timedelta
import requests
from flask_cors import CORS
import os
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
from oauth2client.client import GoogleCredentials
from googleapiclient.discovery import build
from google.oauth2 import service_account
import sys
import time

def Start_Drive():
    filename = drive_creds_filename
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

    google_drive = GoogleDrive(gauth)

def Refresh_Drive():
    gauth:GoogleAuth = google_drive
    if gauth.access_token_expired:
        filename = drive_creds_filename
        gauth.Refresh()
        gauth.SaveCredentialsFile(filename)
        google_drive = gauth

def Start_Docs():
    credentials = service_account.Credentials.from_service_account_file(docs_creds_filename, scopes=['https://www.googleapis.com/auth/documents'])
    service = build('docs', 'v1', credentials=credentials)
    google_docs = service

def Get_Folder_ID() -> str:
    drive = google_drive
    folder_list = drive.ListFile({'q': f"title='{folder_name}' and mimeType='application/vnd.google-apps.folder'"}).GetList()
    # If the folder is found, use its ID
    if len(folder_list) > 0:
        return folder_list[0]['id']
    else:
        return None

def Get_FileID(filename) -> str:
    drive = google_drive
    folder_list = drive.ListFile({'q': f"title='{filename}' and mimeType='application/vnd.google-apps.folder'"}).GetList()
    # If the folder is found, use its ID
    if len(folder_list) > 0:
        return folder_list[0]['id']
    else:
        return None

def Get_File_Content(file_id) -> str:
    service = google_docs
    if(service == None):
        return "Docs not initialized"
    
    document = service.documents().get(documentId=file_id).execute()
    document_content = document.get('body', {}).get('content', '')

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

        Last_Refresh = datetime.now()

        folder_id = Get_Folder_ID()
        if folder_id == None:
            print("'MSA TV' folder not found in drive")
            sys.exit()
        folder_id = folder_id

        announcements_fileid = Get_FileID('announcements')
        if announcements_fileid == None:
            print("'announcements' folder not found in drive")
            announcements_fileid = announcements_fileid
            sys.exit()
        announcements_fileid = None

        from . import routes

        return app 


# Global Variables
# Store results of previous endpoints to avoid unnecessary computation.
Iqamahs_save = {}
google_drive = None
google_docs = None
Last_Refresh = None
drive_creds_filename = "mycreds.txt"
docs_creds_filename = "msa_service_account_key.json"
folder_name = "MSA TV"
folder_id = None
announcements_filename = "announcements"
announcements_fileid = None
announcements = None
# app = Flask(__name__)
app = init_app()
CORS(app)


@app.route('/Announcements')
def Announcements():
    # with open('./data/announcements.txt', 'r') as file:
    #     file_data = file.read()
    # announcements = file_data.replace('\r','').split('\n')
    # return announcements

    last_refresh:datetime = Last_Refresh
    if last_refresh.hour != datetime.now().hour:
        Refresh_Drive()
        Last_Refresh = datetime.now()
        announcements = Get_File_Content(announcements_fileid)
    return announcements

@app.route('/Iqamahs')
def Iqamahs():
    with open('./data/IqamahTimes.json', 'r') as file:
        file_data = json.load(file)
    Iqamahs = dict(file_data)
    return jsonify(file_data)

@app.route('/prayerAPI')
def prayerAPI():
    date = datetime.now()
    with open('./data/AppSettings.json') as f: 
        file_content = json.load(f) 
    month = int(file_content["last_aladhanAPI_call"][:2]) 
    year = int(file_content["last_aladhanAPI_call"][3:7])

    if date.year > year or (date.month > month): 
        method = 2 # TODO Add feature to modify method or school if user wants 
        school = 1 
        api_response = requests.get(f"https://api.aladhan.com/v1/calendarByCity/{date.year}/{date.month}?city=Chicago&country=United%20States&method={method}&school={school}").json() 
        with open('./data/aladhanAPIsave.json', 'w') as f: 
            json.dump(api_response, f) # Update Settings File to remember that we grabbed new data for this month 
        file_content["last_aladhanAPI_call"] = f"{date.month:02d}/{date.year}" 
        with open('./data/appSettings.json', 'w') as f: 
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
    if Iqamahs:
        Iqamah_Times = Iqamahs
    else:
        Iqamah_Times = dict(Iqamahs().json)

    
    Today_Times = dict(prayerTimesToday().json)
    
    currentTime = datetime(2023,9,26,10,20)
    StartOfDay = datetime(currentTime.year, currentTime.month, currentTime.day, 0, 0, 0, 0)

    FajrHour = int(Iqamah_Times['Fajr'][:2]) if len(Iqamah_Times['Fajr']) else int(Today_Times['Fajr'][:2])
    FajrMinute = int(Iqamah_Times['Fajr'][3:5]) if len(Iqamah_Times['Fajr']) else int(Today_Times['Fajr'][3:5])
    FajrToday = datetime(currentTime.year, currentTime.month, currentTime.day, FajrHour, FajrMinute, 0, 0)

    SunriseHour = int(Today_Times['Sunrise'][:2])
    SunriseMinute = int(Today_Times['Sunrise'][3:5])
    Sunrise = datetime(currentTime.year, currentTime.month, currentTime.day, SunriseHour, SunriseMinute, 0, 0)

    DhuhrHour = int(Iqamah_Times['Dhuhr'][:2]) if len(Iqamah_Times['Dhuhr']) else int(Today_Times['Dhuhr'][:2])
    DhuhrMinute = int(Iqamah_Times['Dhuhr'][3:5]) if len(Iqamah_Times['Dhuhr']) else int(Today_Times['Dhuhr'][3:5])
    Dhuhr = datetime(currentTime.year, currentTime.month, currentTime.day, DhuhrHour, DhuhrMinute, 0, 0)

    JummahHour = int(Iqamah_Times['Jummah'][:2])
    JummahMinute = int(Iqamah_Times['Jummah'][3:5])
    Jummah = datetime(currentTime.year, currentTime.month, currentTime.day, JummahHour, JummahMinute, 0, 0)

    AsrHour = int(Iqamah_Times['Asr'][:2]) if len(Iqamah_Times['Asr']) else int(Today_Times['Asr'][:2])
    AsrMinute = int(Iqamah_Times['Asr'][3:5]) if len(Iqamah_Times['Asr']) else int(Today_Times['Asr'][3:5])
    Asr = datetime(currentTime.year, currentTime.month, currentTime.day, AsrHour, AsrMinute, 0, 0)

    MaghribHour = int(Iqamah_Times['Maghrib'][:2]) if len(Iqamah_Times['Maghrib']) else int(Today_Times['Maghrib'][:2])
    MaghribMinute = int(Iqamah_Times['Maghrib'][3:5]) if len(Iqamah_Times['Maghrib']) else int(Today_Times['Maghrib'][3:5])
    Maghrib = datetime(currentTime.year, currentTime.month, currentTime.day, MaghribHour, MaghribMinute, 0, 0)

    IshaHour = int(Iqamah_Times['Isha'][:2]) if len(Iqamah_Times['Isha']) else int(Today_Times['Isha'][:2])
    IshaMinute = int(Iqamah_Times['Isha'][3:5]) if len(Iqamah_Times['Isha']) else int(Today_Times['Isha'][3:5])
    Isha = datetime(currentTime.year, currentTime.month, currentTime.day, IshaHour, IshaMinute, 0, 0)

    if (currentTime - StartOfDay).total_seconds() > 0 and (FajrToday - currentTime).total_seconds() > 0:
        result = {
            'salah': 'Fajr',
            'time': FajrToday.strftime("%a, %d %b %Y %H:%M")
        }
    elif (currentTime - FajrToday).total_seconds() > 0 and (Sunrise - currentTime).total_seconds() > 0:
        result = {
            'salah': 'Sunrise',
            'time': Sunrise.strftime("%a, %d %b %Y %H:%M")
        }
    elif currentTime.weekday() == 4 and (currentTime - Sunrise).total_seconds() > 0 and (Jummah - currentTime).total_seconds() > 0:
        result = {
            'salah': 'Jummah',
            'time': Jummah.strftime("%a, %d %b %Y %H:%M")
        }
    elif currentTime.weekday() == 4 and (currentTime - Sunrise).total_seconds() > 0 and (Asr - currentTime).total_seconds() > 0:
        result = {
            'salah': 'Asr',
            'time': Asr.strftime("%a, %d %b %Y %H:%M")
        }
    elif (currentTime - Sunrise).total_seconds() > 0 and (Dhuhr - currentTime).total_seconds() > 0:
        result = {
            'salah': 'Dhuhr',
            'time': Dhuhr.strftime("%a, %d %b %Y %H:%M")
        }
    elif (currentTime - Dhuhr).total_seconds() > 0 and (Asr - currentTime).total_seconds() > 0: 
        result = { 
            'salah': 'Asr', 
            'time': Asr.strftime("%a, %d %b %Y %H:%M")
        } 
    elif (currentTime - Asr).total_seconds() > 0 and (Maghrib - currentTime).total_seconds() > 0: 
        result = { 
            'salah': 'Maghrib', 
            'time': Maghrib.strftime("%a, %d %b %Y %H:%M")
        } 
    elif (currentTime - Maghrib).total_seconds() > 0 and (Isha - currentTime).total_seconds() > 0: 
        result = { 
            'salah': 'Isha', 
            'time': Isha.strftime("%a, %d %b %Y %H:%M")
        } 
    else: 
        result = { 
            'salah': 'Fajr', 
            'time': (FajrToday + timedelta(days=1)).strftime("%a, %d %b %Y %H:%M")
        }

    # result['time'] = (datetime.now() + timedelta(minutes=1)).strftime("%a, %d %b %Y %H:%M") #For Testing countdown restart only
    print(result['time'])
    return jsonify(result)

@app.route('/todayGreg')
def todayGreg():
    return datetime.now().strftime('%A, %B %d, %Y')

@app.route('/slideshowDelay')
def slideshowDelay():
    with open('./data/AppSettings.json') as f: 
        file_content = dict(json.load(f))
    return str(int(file_content["slideshow_delay"]))

# @app.route('/weatherAPI')
# def weatherAPI():
#     API_Key = 'a6f7364a3cec410c8bf00401232706'
#     return

if __name__ == '__main__':
    Start_Drive()
    Start_Docs()

    Last_Refresh = datetime.now()

    folder_id = Get_Folder_ID()
    if folder_id == None:
        print("'MSA TV' folder not found in drive")
        sys.exit()
    folder_id = folder_id

    announcements_fileid = Get_FileID('announcements')
    if announcements_fileid == None:
        print("'announcements' file not found in drive")
        announcements_fileid = announcements_fileid
        sys.exit()
    announcements_fileid = None

    app.run(host='0.0.0.0', port=7000)

    # app.run(port=7000)