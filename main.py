"""
Główny plik aplikacji - alias dla strukturyzowanej aplikacji
Buildozer domyślnie szuka main.py
"""

import os
from kivy.config import Config
from kivy.utils import platform

# Symulacja rozmiaru i DPI tylko na komputerze
if platform != 'android':
    # Typowy ekran telefonu: 360x640 dp, gęstość: ~2.5
    from kivy.core.window import Window
    Window.size = (360, 640)
    
    os.environ['KIVY_METRICS_DENSITY'] = '2.5'  # Skala jak na telefonach 1080p
    Config.set('graphics', 'dpi', '160')  # Referencyjne DPI (dla dp/sp przeliczeń)
    Config.set('graphics', 'width', '360')
    Config.set('graphics', 'height', '640')
    Config.set('graphics', 'resizable', False)

# Dla debugowania - wypisz DPI i density
from kivy.metrics import Metrics
from kivy.logger import Logger

Logger.info(f"APP: DPI = {Metrics.dpi}, Density = {Metrics.density}, FontScale = {Metrics.fontscale}")

from src.CalorieCounterApp.CalorieCounterApp import CalorieCounterApp

if __name__ == '__main__':
    CalorieCounterApp().run()
