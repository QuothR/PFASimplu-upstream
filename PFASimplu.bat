@echo off
title PFASimplu
cd /d "%~dp0"

rem Daca serverul ruleaza deja, doar deschide browserul.
curl -s -o NUL http://127.0.0.1:8000 && goto open

echo Pornesc PFASimplu...
start "PFASimplu - inchide fereastra ca sa opresti aplicatia" ".venv\Scripts\python.exe" manage.py runserver 127.0.0.1:8000 --noreload

rem Asteapta pana cand serverul raspunde (maxim 60 s).
set /a n=0
:wait
set /a n+=1
if %n% gtr 60 goto fail
timeout /t 1 >nul
curl -s -o NUL http://127.0.0.1:8000 && goto open
goto wait

:open
start "" http://127.0.0.1:8000
exit

:fail
echo Serverul nu a pornit in 60 de secunde. Verifica fereastra "PFASimplu".
pause
