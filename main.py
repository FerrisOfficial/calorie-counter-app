"""
Główny plik aplikacji - alias dla strukturyzowanej aplikacji
Buildozer domyślnie szuka main.py
"""

import os
from kivy.config import Config

# Development window size - ignored on mobile platforms
os.environ['KIVY_WINDOW_WIDTH'] = '360'
os.environ['KIVY_WINDOW_HEIGHT'] = '640'
Config.set('graphics', 'width', '360')
Config.set('graphics', 'height', '640')
Config.set('graphics', 'resizable', False)

from src.CalorieCounterApp import CalorieCounterApp

if __name__ == '__main__':
    CalorieCounterApp().run()
