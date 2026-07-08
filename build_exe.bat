@echo off
setlocal
cd /d "%~dp0"

echo Installiere benoetigte Pakete fuer die EXE-Erstellung ...
py -m pip install -r requirements.txt -r requirements-build.txt
if errorlevel 1 goto error

echo Erstelle Ausbildungsnachweis.exe ...
py -m PyInstaller Ausbildungsnachweis.spec
if errorlevel 1 goto error

echo.
echo Fertig! Die EXE liegt hier:
echo %cd%\dist\Ausbildungsnachweis.exe
echo.
pause
exit /b 0

:error
echo.
echo Fehler beim Erstellen der EXE.
pause
exit /b 1
