@echo off

:: Start flask backend
cd flask_api
call venv\Scripts\activate
start cmd /K python api.py

:: Start react frontend
cd ..\iitmsatv
npm start

:: Open in chrome
start chrome.exe 127.0.0.1
pause