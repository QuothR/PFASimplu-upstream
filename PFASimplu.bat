@echo off
title PFASimplu
cd /d "%~dp0"
echo Pornesc PFASimplu... Inchide aceasta fereastra ca sa opresti aplicatia.
start "" cmd /c "timeout /t 3 >nul & start http://127.0.0.1:8000"
".venv\Scripts\python.exe" manage.py runserver 127.0.0.1:8000 --noreload
