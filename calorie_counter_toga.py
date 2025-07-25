"""
Alternatywna wersja aplikacji używająca BeeWare/Toga
BeeWare pozwala na łatwiejsze budowanie aplikacji mobilnych na Windows
"""

import toga
from toga.style import Pack
from toga.style.pack import COLUMN, ROW
import json
import os
from datetime import datetime, timedelta


class CalorieCounter(toga.App):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.daily_target = 2000
        self.today = datetime.now().strftime('%Y-%m-%d')
        self.data_file = 'calorie_data.json'
        
    def startup(self):
        """Buduje główny interfejs aplikacji"""
        
        # Główny kontener
        main_box = toga.Box(style=Pack(direction=COLUMN, padding=10))
        
        # Tytuł
        title = toga.Label(
            'Licznik Kalorii',
            style=Pack(text_align='center', font_size=24, padding=(0, 0, 20, 0))
        )
        
        # Informacje o dziennym zapotrzebowaniu
        self.daily_info = toga.Label(
            self.get_daily_info_text(),
            style=Pack(text_align='center', padding=(0, 0, 20, 0))
        )
        
        # Sekcja dodawania posiłku
        input_box = toga.Box(style=Pack(direction=ROW, padding=(0, 0, 10, 0)))
        
        self.meal_name = toga.TextInput(
            placeholder='Nazwa posiłku',
            style=Pack(flex=1, padding=(0, 5, 0, 0))
        )
        
        self.calories_input = toga.NumberInput(
            style=Pack(width=100, padding=(0, 5, 0, 0))
        )
        
        add_button = toga.Button(
            '+ dodaj nowy posiłek',
            on_press=self.add_meal,
            style=Pack(width=160)
        )
        
        input_box.add(self.meal_name)
        input_box.add(self.calories_input)
        input_box.add(add_button)
        
        # Lista posiłków
        meals_label = toga.Label(
            'Dzisiejsze posiłki:',
            style=Pack(font_weight='bold', padding=(10, 0, 5, 0))
        )
        
        self.meals_table = toga.Table(
            headings=['Czas', 'Posiłek', 'Kalorie'],
            style=Pack(flex=1)
        )
        
        # Przycisk statystyk
        stats_button = toga.Button(
            'Statystyki tygodniowe',
            on_press=self.show_weekly_stats,
            style=Pack(padding=(10, 0, 0, 0))
        )
        
        # Dodanie wszystkich elementów
        main_box.add(title)
        main_box.add(self.daily_info)
        main_box.add(input_box)
        main_box.add(meals_label)
        main_box.add(self.meals_table)
        main_box.add(stats_button)
        
        self.main_window = toga.MainWindow(title=self.formal_name)
        self.main_window.content = main_box
        self.main_window.show()
        
        # Załaduj dzisiejsze posiłki
        self.load_today_meals()
        
    def get_daily_info_text(self):
        """Zwraca tekst z informacjami o dziennym zapotrzebowaniu"""
        consumed = self.get_daily_calories()
        remaining = self.daily_target - consumed
        
        return f"Dzienne zapotrzebowanie: {self.daily_target} kcal\nSpożyte dzisiaj: {consumed} kcal\nPozostało: {remaining} kcal"
    
    def get_daily_calories(self):
        """Zwraca sumę kalorii spożytych dzisiaj"""
        data = self.load_data()
        if self.today in data:
            return sum(meal['calories'] for meal in data[self.today]['meals'])
        return 0
    
    def load_data(self):
        """Ładuje dane z pliku JSON"""
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except:
                return {}
        return {}
    
    def save_data(self, data):
        """Zapisuje dane do pliku JSON"""
        with open(self.data_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    
    async def add_meal(self, widget):
        """Dodaje nowy posiłek"""
        meal_name = self.meal_name.value.strip()
        calories = self.calories_input.value
        
        if not meal_name or not calories or calories <= 0:
            await self.main_window.error_dialog('Błąd', 'Proszę wypełnić wszystkie pola poprawnie!')
            return
        
        # Dodanie posiłku do danych
        data = self.load_data()
        if self.today not in data:
            data[self.today] = {'meals': []}
        
        meal = {
            'name': meal_name,
            'calories': int(calories),
            'time': datetime.now().strftime('%H:%M')
        }
        
        data[self.today]['meals'].append(meal)
        self.save_data(data)
        
        # Czyszczenie pól
        self.meal_name.value = ''
        self.calories_input.value = 0
        
        # Odświeżenie interfejsu
        self.load_today_meals()
        self.daily_info.text = self.get_daily_info_text()
        
        await self.main_window.info_dialog('Sukces', f'Dodano posiłek: {meal_name} ({calories} kcal)')
    
    def load_today_meals(self):
        """Ładuje dzisiejsze posiłki do tabeli"""
        data = self.load_data()
        self.meals_table.data = []
        
        if self.today in data:
            for meal in data[self.today]['meals']:
                self.meals_table.data.append([
                    meal['time'],
                    meal['name'],
                    f"{meal['calories']} kcal"
                ])
    
    async def show_weekly_stats(self, widget):
        """Wyświetla statystyki tygodniowe"""
        data = self.load_data()
        today = datetime.now()
        total_calories = 0
        
        for i in range(7):
            day = today - timedelta(days=i)
            day_str = day.strftime('%Y-%m-%d')
            
            if day_str in data:
                daily_calories = sum(meal['calories'] for meal in data[day_str]['meals'])
                total_calories += daily_calories
        
        target_weekly = 7 * self.daily_target
        percentage = (total_calories / target_weekly * 100) if target_weekly > 0 else 0
        
        stats_text = f"""Statystyki ostatnich 7 dni:

Spożyte kalorie: {total_calories} kcal
Cel tygodniowy: {target_weekly} kcal
Procent realizacji: {percentage:.1f}%

Średnia dzienna: {total_calories / 7:.0f} kcal
Cel dzienny: {self.daily_target} kcal"""
        
        await self.main_window.info_dialog('Statystyki tygodniowe', stats_text)


def main():
    return CalorieCounter('Licznik Kalorii', 'org.example.calorie_counter')


if __name__ == '__main__':
    app = main()
    app.main_loop()
