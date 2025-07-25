@echo off
REM Skrypt do budowania APK na Windows używając Docker

echo Budowanie APK przy użyciu Docker...
echo.

REM Sprawdź czy Docker jest zainstalowany
docker --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [BŁĄD] Docker nie jest zainstalowany!
    echo Pobierz Docker Desktop z: https://www.docker.com/products/docker-desktop
    pause
    exit /b 1
)

echo [INFO] Docker znaleziony, rozpoczynam budowanie...

REM Uruchom buildozer w kontenerze Docker
docker run --rm -v "%cd%":/home/user/hostapp kivy/buildozer android debug

if %errorlevel% equ 0 (
    echo.
    echo [SUKCES] APK został zbudowany!
    echo Sprawdź folder bin/ dla pliku .apk
) else (
    echo.
    echo [BŁĄD] Wystąpił problem podczas budowania
)

pause
