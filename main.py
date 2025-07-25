"""
Główny plik aplikacji - alias dla strukturyzowanej aplikacji
Buildozer domyślnie szuka main.py
"""

from src.CalorieCounterApp import CalorieCounterApp

if __name__ == '__main__':
    CalorieCounterApp().run()
