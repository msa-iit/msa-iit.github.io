@echo off

:: Start flask backend
cd flask_api
start cmd /C python api.py

:: Start react frontend
cd ..
cd iitmsatv
npm start

:: Open in chrome
start chrome.exe 127.0.0.1
pause