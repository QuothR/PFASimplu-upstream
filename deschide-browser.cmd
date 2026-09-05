@echo off
set /a n=0
:wait
set /a n+=1
if %n% gtr 90 exit
timeout /t 1 >nul
curl -s -o NUL http://127.0.0.1:8000 || goto wait
start "" http://127.0.0.1:8000
exit
