@echo off

REM This batch file runs the Python script for the voice-based Google search.

REM Enable delayed environment variable expansion
setlocal enabledelayedexpansion

REM Specify the path to the Python interpreter
REM Run below command in CMD to get your interpreter location
REM where python
set PYTHON_PATH=C:/Users/{USERNAME}/path/to/interpreter/python.exe

REM Specify the path to the Python script
set SCRIPT_PATH=C:/path/to/echoSurf.py

REM Run the Python script
%PYTHON_PATH% %SCRIPT_PATH%

REM End the delayed environment variable expansion
endlocal
