@echo off
REM -----------------------------------------------------------------
REM  predict_api.bat   [sepal_len sepal_wid petal_len petal_wid]
REM
REM  Example with defaults:
REM      predict_api.bat
REM
REM  Example with custom values:
REM      predict_api.bat 6.3 2.9 5.6 1.8
REM -----------------------------------------------------------------

SETLOCAL EnableDelayedExpansion

:: Default values
SET "SL=5.1"
SET "SW=3.5"
SET "PL=1.4"
SET "PW=2.2"

:: If four numeric arguments are supplied, override defaults
IF "%~4" NEQ "" (
    SET "SL=%~1"
    SET "SW=%~2"
    SET "PL=%~3"
    SET "PW=%~4"
) ELSE IF NOT "%~1"=="" (
    echo Invalid usage.^&echo.
    echo Expected 4 numeric arguments or none.
    echo Example:  predict_api.bat 6.3 2.9 5.6 1.8
    goto :EOF
)

:: Build JSON payload (no escaping headaches)
SET "PAYLOAD={\"sepal_length\":%SL%,\"sepal_width\":%SW%,\"petal_length\":%PL%,\"petal_width\":%PW%}"

echo.
echo Sending: !PAYLOAD!
echo -----------------------------------------------------
curl.exe -s -o response.json -w "HTTP %%{http_code}\n" ^
        -X POST http://localhost:8000/predict ^
        -H "Content-Type: application/json" ^
        --data "!PAYLOAD!"
type response.json & del response.json
echo -----------------------------------------------------

:: Keep window open only if double-clicked (not when run from an open shell)
IF "%CMDCMDLINE:cmd.exe=%"=="%CMDCMDLINE%" pause
ENDLOCAL
