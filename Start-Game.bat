@echo off
REM Double-click this file to play Mathipelago on Windows.
REM It starts a tiny local web server (needs Python) and opens your browser.
REM No Python? Just double-click index.html instead - the game also works straight from the file.
cd /d "%~dp0"
where python >nul 2>nul
if %errorlevel%==0 (
  start "" http://localhost:8000/index.html
  python -m http.server 8000
) else (
  echo Python was not found. Opening index.html directly instead...
  start "" index.html
)
