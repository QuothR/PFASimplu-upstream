@echo off
title PFASimplu - inchide fereastra ca sa opresti aplicatia
cd /d "%~dp0"
set LOG=%~dp0launcher.log

rem Interpretorul real (cel gestionat de uv), citit din .venv\pyvenv.cfg, si pachetele din .venv.
rem Nu folosim .venv\Scripts\python.exe (lansatorul mic da eroare cand e pornit din Explorer).
for /f "tokens=1,* delims== " %%a in ('findstr /b "home" ".venv\pyvenv.cfg"') do set PYHOME=%%b
set PYTHON=%PYHOME%\python.exe
set PYTHONPATH=%~dp0.venv\Lib\site-packages
set VIRTUAL_ENV=%~dp0.venv

rem Daca serverul ruleaza deja, doar deschide browserul si iesi.
curl -s -o NUL http://127.0.0.1:8000 && start "" http://127.0.0.1:8000 && exit

echo Pornesc PFASimplu... browserul se deschide cand serverul e gata.
echo [%date% %time%] pornire cu %PYTHON% > "%LOG%"
start "" /b cmd /c "%~dp0deschide-browser.cmd"

"%PYTHON%" manage.py runserver 127.0.0.1:8000 --noreload 2>> "%LOG%"

echo.
echo Serverul s-a oprit (cod %errorlevel%). Detalii in launcher.log:
type "%LOG%"
pause
