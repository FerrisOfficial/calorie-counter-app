@echo off
echo Building Calorie Counter APK...
echo.

REM Check if buildozer is installed
C:/Users/Maciej/AppData/Local/Programs/Python/Python312/python.exe -m buildozer --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Buildozer is not installed!
    echo Installing buildozer...
    C:/Users/Maciej/AppData/Local/Programs/Python/Python312/python.exe -m pip install buildozer
)

echo.
echo Building Android APK...
echo This may take 15-30 minutes on first build...
echo.

C:/Users/Maciej/AppData/Local/Programs/Python/Python312/python.exe -m buildozer android debug

if exist bin\*.apk (
    echo.
    echo SUCCESS! APK built successfully!
    echo APK location: %cd%\bin\
    echo.
    echo To install on your phone:
    echo 1. Enable Developer Options and USB Debugging on your phone
    echo 2. Connect your phone via USB
    echo 3. Run: adb install bin\calorie_counter-1.0-debug.apk
    echo.
) else (
    echo.
    echo Build failed. Check the output above for errors.
    echo.
)

pause
