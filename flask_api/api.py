from flask import Flask, jsonify
import json
from datetime import datetime, timedelta
import requests
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)

@app.route('/Announcements')
def Announcements():
    with open('./flask_api/data/announcements.txt', 'r') as file:
        file_data = file.read()
    announcements = file_data.replace('\r','').split('\n')
    return announcements

@app.route('/Iqamahs')
def Iqamahs():
    with open('./flask_api/data/IqamahTimes.json', 'r') as file:
        file_data = json.load(file)
    return jsonify(file_data)

@app.route('/prayerAPI')
def prayerAPI():
    date = datetime.now()
    with open('./flask_api/data/AppSettings.json') as f: 
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
        with open('./flask_api/data/appSettings.json', 'w') as f: 
            json.dump(file_content, f) 
            return jsonify(api_response)
    else: 
        with open('./flask_api/data/aladhanAPIsave.json', encoding='utf-8') as f:
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
    Iqamah_Times = dict(Iqamahs().json)
    Today_Times = dict(prayerTimesToday().json)
    
    currentTime = datetime.now()
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


@app.route('/weatherAPI')
def weatherAPI():
    API_Key = 'a6f7364a3cec410c8bf00401232706'

if __name__ == '__main__':
    app.run(port=7000)