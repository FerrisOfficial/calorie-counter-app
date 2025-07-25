# Aplikacja Licznik Kalorii

Aplikacja mobilna na Android do liczenia kalorii napisana w Pythonie z użyciem frameworka Kivy.

## Funkcjonalności

- ✅ Dzienne zapotrzebowanie na poziomie 2000 kcal
- ✅ Dodawanie posiłków (nazwa i ilość kalorii)
- ✅ Wyświetlanie ile z dziennego zapotrzebowania zostało
- ✅ Statystyki tygodniowe (spożyte kalorie / (7 * 2000))
- ✅ Usuwanie dodanych posiłków
- ✅ Automatyczne przechowywanie danych
- ✅ Historia posiłków z godzinami

## Instalacja środowiska

### Windows

1. **Zainstaluj Python 3.8+**
   ```powershell
   # Pobierz z python.org lub używając winget
   winget install Python.Python.3.11
   ```

2. **Zainstaluj wymagane pakiety**
   ```powershell
   pip install -r requirements.txt
   ```

3. **Uruchom aplikację lokalnie (do testowania)**
   ```powershell
   python calorie_counter_app.py
   ```

### Linux (Ubuntu/Debian)

1. **Zainstaluj zależności systemowe**
   ```bash
   sudo apt update
   sudo apt install python3-pip python3-dev build-essential
   sudo apt install libgl1-mesa-dev libgles2-mesa-dev
   sudo apt install zlib1g-dev libncurses5-dev libgdbm-dev libnss3-dev
   sudo apt install libssl-dev libreadline-dev libffi-dev wget
   ```

2. **Zainstaluj pakiety Python**
   ```bash
   pip3 install -r requirements.txt
   ```

3. **Uruchom aplikację**
   ```bash
   python3 calorie_counter_app.py
   ```

## Tworzenie APK dla Android

### Używając Buildozer (Linux/WSL)

1. **Zainstaluj Buildozer**
   ```bash
   pip3 install buildozer
   ```

2. **Zainstaluj zależności Android**
   ```bash
   sudo apt install openjdk-8-jdk
   sudo apt install autoconf libtool pkg-config zlib1g-dev libncurses5-dev libncursesw5-dev libtinfo5
   ```

3. **Zbuduj APK**
   ```bash
   buildozer android debug
   ```

4. **APK zostanie utworzony w folderze** `bin/`

### Używając GitHub Actions (zalecane)

Możesz również skonfigurować automatyczne budowanie APK używając GitHub Actions. Stwórz plik `.github/workflows/build.yml` w swoim repozytorium.

## Tworzenie aplikacji na iOS

### Używając kivy-ios (macOS wymagany)

1. **Zainstaluj zależności systemowe**
   ```bash
   brew install autoconf automake libtool pkg-config libffi openssl cmake
   ```

2. **Zainstaluj kivy-ios**
   ```bash
   pip3 install kivy-ios cython==0.29.33
   ```

3. **Zbuduj zależności iOS**
   ```bash
   kivy-ios build python3 kivy pillow
   ```

4. **Stwórz projekt iOS**
   ```bash
   kivy-ios create "Licznik Kalorii" org.dudek.caloriecounter
   ```

5. **Skopiuj pliki aplikacji**
   ```bash
   cp main.py "Licznik Kalorii-ios/"
   cp calorie_counter_app.py "Licznik Kalorii-ios/"
   ```

6. **Otwórz w Xcode**
   ```bash
   cd "Licznik Kalorii-ios"
   open "Licznik Kalorii.xcodeproj"
   ```

### Używając Buildozer na macOS

1. **Zainstaluj Buildozer**
   ```bash
   pip3 install buildozer
   ```

2. **Zbuduj aplikację iOS**
   ```bash
   buildozer ios debug
   ```

### Automatyczne budowanie iOS (GitHub Actions)

Projekt zawiera workflow dla automatycznego budowania na iOS używając GitHub Actions na macOS runners.

### Wymagania dla iOS

- **macOS** (dla lokalnego budowania)
- **Xcode** zainstalowany
- **Apple Developer Account** (dla instalacji na prawdziwych urządzeniach)
- **iOS 11.0+** (minimalna wersja iOS)

## Struktura aplikacji

```
calorie_counter_app.py  # Główny plik aplikacji
requirements.txt        # Wymagane pakiety Python  
buildozer.spec         # Konfiguracja dla budowania APK
README.md              # Ta dokumentacja
calorie_data.json      # Plik z danymi (tworzony automatycznie)
```

## Jak używać aplikacji

1. **Dodawanie posiłku:**
   - Wpisz nazwę posiłku (np. "Śniadanie", "Jabłko", "Pizza")
   - Wpisz liczbę kalorii
   - Naciśnij "Dodaj posiłek"

2. **Wyświetlanie dziennego zapotrzebowania:**
   - Na górze ekranu widzisz:
     - Dzienne zapotrzebowanie: 2000 kcal
     - Spożyte dzisiaj: XXX kcal  
     - Pozostało: XXX kcal

3. **Lista dzisiejszych posiłków:**
   - Pokazuje wszystkie dodane dziś posiłki z godziną
   - Możliwość usunięcia każdego posiłku przyciskiem "Usuń"

4. **Statystyki tygodniowe:**
   - Naciśnij "Pokaż statystyki tygodniowe"
   - Zobacz spożyte kalorie za ostatnie 7 dni
   - Procent realizacji celu (7 * 2000 kcal)
   - Średnią dzienną i szczegóły dla każdego dnia

## Przechowywanie danych

- Dane są przechowywane lokalnie w pliku `calorie_data.json`
- Każdy dzień ma osobny wpis z listą posiłków
- Dane nie są synchronizowane między urządzeniami
- Backup: skopiuj plik `calorie_data.json` aby zachować dane

## Dostosowywanie

### Zmiana celu dziennego
W pliku `calorie_counter_app.py` zmień wartość:
```python
self.daily_target = 2000  # Zmień na swoją wartość
```

### Dostosowanie wyglądu
Możesz modyfikować:
- Kolory i czcionki w kodzie
- Rozmiary przycisków i pól tekstowych
- Dodać nowe funkcjonalności

## Rozwiązywanie problemów

### "Import kivy could not be resolved"
```powershell
pip install --upgrade kivy kivymd
```

### Problemy z budowaniem na Windows
Użyj WSL (Windows Subsystem for Linux) lub maszyny wirtualnej z Ubuntu.

### Aplikacja nie uruchamia się
1. Sprawdź czy masz Python 3.8+: `python --version`
2. Zainstaluj ponownie dependencje: `pip install -r requirements.txt`
3. Sprawdź logi błędów

## Licencja

Ten projekt jest open source. Możesz go modyfikować i dystrybuować zgodnie z potrzebami.
