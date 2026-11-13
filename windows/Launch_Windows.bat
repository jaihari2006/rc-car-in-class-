@echo off
setlocal
title RC Car in Class - Windows Edition

echo ========================================================
echo         RC Car in Class - Windows Desktop Edition
echo ========================================================
echo.

set APP_DIR=%~dp0
set INDEX_FILE=%APP_DIR%index.html

:: 1. Check if compiled/portable executable exists
if exist "%APP_DIR%RcCarInClass.exe" (
    echo Launching native Windows executable...
    start "" "%APP_DIR%RcCarInClass.exe"
    exit /b
)

:: 2. Try Microsoft Edge in standalone App Mode (built-in on Windows 10 & 11)
set EDGE_PATH1="%ProgramFiles(x86)%\Microsoft\Edge\Application\msedge.exe"
set EDGE_PATH2="%ProgramFiles%\Microsoft\Edge\Application\msedge.exe"
set EDGE_PATH3="%LOCALAPPDATA%\Microsoft\Edge\Application\msedge.exe"

if exist %EDGE_PATH1% (
    echo Launching via Microsoft Edge Standalone App Mode...
    start "" %EDGE_PATH1% --app="file:///%INDEX_FILE:\=/%" --allow-file-access-from-files --start-maximized
    exit /b
)

if exist %EDGE_PATH2% (
    echo Launching via Microsoft Edge Standalone App Mode...
    start "" %EDGE_PATH2% --app="file:///%INDEX_FILE:\=/%" --allow-file-access-from-files --start-maximized
    exit /b
)

if exist %EDGE_PATH3% (
    echo Launching via Microsoft Edge Standalone App Mode...
    start "" %EDGE_PATH3% --app="file:///%INDEX_FILE:\=/%" --allow-file-access-from-files --start-maximized
    exit /b
)

:: 3. Try Google Chrome in standalone App Mode
set CHROME_PATH1="%ProgramFiles%\Google\Chrome\Application\chrome.exe"
set CHROME_PATH2="%ProgramFiles(x86)%\Google\Chrome\Application\chrome.exe"
set CHROME_PATH3="%LOCALAPPDATA%\Google\Chrome\Application\chrome.exe"

if exist %CHROME_PATH1% (
    echo Launching via Google Chrome Standalone App Mode...
    start "" %CHROME_PATH1% --app="file:///%INDEX_FILE:\=/%" --allow-file-access-from-files --start-maximized
    exit /b
)

if exist %CHROME_PATH2% (
    echo Launching via Google Chrome Standalone App Mode...
    start "" %CHROME_PATH2% --app="file:///%INDEX_FILE:\=/%" --allow-file-access-from-files --start-maximized
    exit /b
)

if exist %CHROME_PATH3% (
    echo Launching via Google Chrome Standalone App Mode...
    start "" %CHROME_PATH3% --app="file:///%INDEX_FILE:\=/%" --allow-file-access-from-files --start-maximized
    exit /b
)

:: 4. Fallback: Open in default browser
echo Launching in default web browser...
start "" "%INDEX_FILE%"
exit /b
