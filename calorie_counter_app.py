"""
Aplikacja do liczenia kalorii na Android
Stworzona z użyciem Kivy - Wersja z upiększonym GUI
"""

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.popup import Popup
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.clock import Clock
from kivy.storage.jsonstore import JsonStore
from kivy.graphics import Color, RoundedRectangle, Line
from kivy.utils import get_color_from_hex
from kivy.metrics import dp
from datetime import datetime, timedelta
import os
from kivy.graphics import Rectangle, Color


class StyledLabel(Label):
    """Stylizowany Label z kolorowym tłem"""
    def __init__(self, bg_color='#FFFFFF', text_color='#000000', **kwargs):
        super().__init__(**kwargs)
        self.bg_color = get_color_from_hex(bg_color)
        self.color = get_color_from_hex(text_color)
        self.bind(size=self.update_graphics, pos=self.update_graphics)
        
    def update_graphics(self, *args):
        self.canvas.before.clear()
        with self.canvas.before:
            Color(*self.bg_color)
            RoundedRectangle(pos=self.pos, size=self.size, radius=[dp(10)])


from kivy.uix.button import Button
from kivy.graphics import Color, RoundedRectangle
from kivy.utils import get_color_from_hex
from kivy.metrics import dp

class StyledButton(Button):
    def __init__(self, bg_color="#84B5FF", markup=False, **kwargs):
        self.bg_color_hex = bg_color
        super().__init__(**kwargs)

        # Usuń domyślne tło przycisku
        self.background_normal = ''
        self.background_down = ''
        self.background_color = (0, 0, 0, 0)  # całkowicie przezroczyste

        # Kolor tła (przyciemniony)
        r, g, b, _ = get_color_from_hex(bg_color)
        darker_color = (r * 0.7, g * 0.7, b * 0.7, 1)
        self.bg_color = darker_color

        self.color = kwargs.get('color', get_color_from_hex('#FFFFFF'))
        self.font_size = kwargs.get('font_size', dp(14))
        self.bold = kwargs.get('bold', True)
        self.markup = markup
        self.halign = 'center'
        self.valign = 'middle'

        with self.canvas.before:
            self.bg_color_instruction = Color(rgba=self.bg_color)
            self.bg_rect = RoundedRectangle(pos=self.pos, size=self.size, radius=[dp(15)])

        self.bind(pos=self.update_graphics, size=self.update_graphics)

        if markup:
            self.bind(size=self.setter('text_size'))

    def update_graphics(self, *args):
        self.bg_rect.pos = self.pos
        self.bg_rect.size = self.size
        self.bg_color_instruction.rgba = self.bg_color



class StyledTextInput(TextInput):
    """Stylizowany TextInput z zaokrąglonymi rogami"""
    def __init__(self, **kwargs):
        # Pobieranie halign przed wywołaniem super()
        halign = kwargs.pop('halign', 'left')
        super().__init__(**kwargs)
        self.background_normal = ''
        self.background_active = ''
        self.foreground_color = get_color_from_hex('#333333')
        self.cursor_color = get_color_from_hex('#4CAF50')
        self.halign = halign
        self.valign = 'center'  # Wyśrodkowanie pionowe
        self.is_focused = False
        # Ustawienia dla wyśrodkowania
        self.bind(size=self.update_text_size)
        self.bind(size=self.update_graphics, pos=self.update_graphics)
        self.bind(focus=self.on_focus_change)
        
    def update_text_size(self, *args):
        # Wyśrodkowanie tekstu poziomo i pionowo
        self.text_size = (self.width, self.height)
        
    def on_focus_change(self, instance, focus):
        """Obsługuje zmianę focusu - podświetla pole po kliknięciu"""
        self.is_focused = focus
        self.update_graphics()
        
    def update_graphics(self, *args):
        self.canvas.before.clear()
        with self.canvas.before:
            if self.is_focused:
                # Lekkie podświetlenie gdy pole ma focus
                Color(*get_color_from_hex("#87E6A8"))  # Trochę ciemniejszy zielony
            else:
                Color(1, 1, 1, 1)  # Białe tło
            RoundedRectangle(pos=self.pos, size=self.size, radius=[dp(10)])
            
            if self.is_focused:
                # Zielona ramka gdy pole ma focus
                Color(*get_color_from_hex('#4CAF50'))
            else:
                Color(0.8, 0.8, 0.8, 1)  # Szara ramka
            Line(rounded_rectangle=(self.x, self.y, self.width, self.height, dp(10)), width=dp(2))


class MealCard(BoxLayout):
    """Karta reprezentująca pojedynczy posiłek"""
    def __init__(self, meal_data, delete_callback, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'horizontal'
        self.size_hint_y = None
        self.height = dp(60)
        self.spacing = dp(10)
        self.padding = [dp(15), dp(5)]
        
        # Tło karty
        with self.canvas.before:
            Color(*get_color_from_hex('#F5F5F5'))
            self.rect = RoundedRectangle(pos=self.pos, size=self.size, radius=[dp(15)])
        self.bind(size=self.update_rect, pos=self.update_rect)
        
        # Ikona posiłku (prosty symbol)
        icon_label = Label(
            text='[color=4CAF50][size=20][b]MEAL[/b][/size][/color]',
            size_hint_x=None,
            width=dp(40),
            markup=True
        )
        
        # Informacje o posiłku
        meal_info_layout = BoxLayout(orientation='vertical', size_hint_x=0.7)
        
        meal_name = Label(
            text=meal_data['name'],
            font_size=dp(16),
            bold=True,
            color=get_color_from_hex('#333333'),
            halign='left',
            size_hint_y=0.6
        )
        meal_name.bind(size=meal_name.setter('text_size'))
        
        meal_details = Label(
            text='{} • {} kcal'.format(meal_data['time'], meal_data['calories']),
            font_size=dp(12),
            color=get_color_from_hex('#666666'),
            halign='left',
            size_hint_y=0.4
        )
        meal_details.bind(size=meal_details.setter('text_size'))
        
        meal_info_layout.add_widget(meal_name)
        meal_info_layout.add_widget(meal_details)
        
        # Przycisk usuwania - zaokrąglony
        delete_btn = Button(
            text='DELETE',
            size_hint_x=None,
            width=dp(80),
            background_normal='',
            background_color=[0, 0, 0, 0],  # Przezroczyste - custom background
            color=get_color_from_hex('#FFFFFF'),
            font_size=dp(12),
            on_press=delete_callback
        )
        
        # Dodaj zaokrąglone tło do przycisku delete
        with delete_btn.canvas.before:
            Color(*get_color_from_hex('#F44336'))
            self.delete_btn_rect = RoundedRectangle(
                pos=delete_btn.pos, 
                size=delete_btn.size, 
                radius=[dp(15)]
            )
        delete_btn.bind(size=self.update_delete_btn, pos=self.update_delete_btn)
        
        self.add_widget(icon_label)
        self.add_widget(meal_info_layout)
        self.add_widget(delete_btn)
    
    def update_rect(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size
    
    def update_delete_btn(self, *args):
        """Aktualizuje zaokrąglone tło przycisku delete"""
        self.delete_btn_rect.pos = args[0].pos
        self.delete_btn_rect.size = args[0].size


class CalorieCounterApp(App):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.daily_target = 2000  # Dzienne zapotrzebowanie na kalorie
        self.store = JsonStore('calorie_data.json')
        self.today = datetime.now().strftime('%Y-%m-%d')
        
    def build(self):
        """Buduje główny interfejs aplikacji z pięknym designem"""
        # Główny layout z gradientowym tłem
        main_layout = FloatLayout()
        
        # Tło aplikacji
        with main_layout.canvas.before:
            Color(*get_color_from_hex("#5D9BFFDA"))  # Trochę ciemniejszy jasny odcień
            self.bg_rect = RoundedRectangle(pos=main_layout.pos, size=main_layout.size)
        main_layout.bind(size=self.update_bg, pos=self.update_bg)
        
        # ScrollView dla całej zawartości
        scroll = ScrollView(
            pos_hint={'center_x': 0.5, 'center_y': 0.5},
            size_hint=(0.95, 0.95)
        )
        
        content_layout = BoxLayout(
            orientation='vertical', 
            padding=dp(20), 
            spacing=dp(15),
            size_hint_y=None
        )
        content_layout.bind(minimum_height=content_layout.setter('height'))
        
        # Header z tytułem i ikoną
        header_layout = BoxLayout(
            orientation='horizontal',
            size_hint_y=None,
            height=dp(80),
            spacing=dp(15)
        )
        
        # Tytuł z piękną czcionką
        # Tytuł z piękną czcionką
        title = StyledLabel(
            text='Calorie Counter',
            font_size=dp(28),
            bold=True,
            bg_color='#2196F3',
            text_color='#FFFFFF',
            halign='center',
            valign='middle'
        )
        title.bind(size=title.setter('text_size'))
        
        header_layout.add_widget(title)
        
        # Karta z informacjami dziennymi
        self.daily_info_card = BoxLayout(
            orientation='vertical',
            size_hint_y=None,
            height=dp(120),
            padding=dp(20),
            spacing=dp(5)
        )
        
        with self.daily_info_card.canvas.before:
            Color(*get_color_from_hex('#FFFFFF'))
            self.daily_card_rect = RoundedRectangle(
                pos=self.daily_info_card.pos, 
                size=self.daily_info_card.size, 
                radius=[dp(20)]
            )
            # Cień
            Color(0, 0, 0, 0.1)
            RoundedRectangle(
                pos=(self.daily_info_card.x + dp(2), self.daily_info_card.y - dp(2)), 
                size=self.daily_info_card.size, 
                radius=[dp(20)]
            )
        self.daily_info_card.bind(size=self.update_daily_card, pos=self.update_daily_card)
        
        # Informacje o kaloriach z kolorowymi akcentami
        consumed = self.get_daily_calories()
        remaining = self.daily_target - consumed
        progress = min(consumed / self.daily_target, 1.0) if self.daily_target > 0 else 0
        
        target_label = Label(
            text='Daily target: {} kcal [color=2196F3][b]TARGET[/b][/color]'.format(self.daily_target),
            font_size=dp(16),
            color=get_color_from_hex('#333333'),
            size_hint_y=0.33,
            markup=True
        )
        
        consumed_color = '#4CAF50' if consumed <= self.daily_target else '#FF5722'
        self.consumed_label = Label(
            text='Consumed: {} kcal [color=4CAF50][b]EATEN[/b][/color]'.format(consumed),
            font_size=dp(16),
            color=get_color_from_hex(consumed_color),
            size_hint_y=0.33,
            bold=True,
            markup=True
        )
        
        remaining_color = '#2196F3' if remaining >= 0 else '#F44336'
        self.remaining_label = Label(
            text='Remaining: {} kcal [color={}]{}[/color]'.format(
                remaining, 
                '4CAF50' if remaining >= 0 else 'F44336',
                'OK' if remaining >= 0 else 'OVER'
            ),
            font_size=dp(16),
            color=get_color_from_hex(remaining_color),
            size_hint_y=0.33,
            bold=True,
            markup=True
        )
        
        self.daily_info_card.add_widget(target_label)
        self.daily_info_card.add_widget(self.consumed_label)
        self.daily_info_card.add_widget(self.remaining_label)
        
        # Sekcja dodawania posiłku z piękną kartą
        add_meal_card = BoxLayout(
            orientation='vertical',
            size_hint_y=None,
            height=dp(100),
            padding=[dp(10), dp(5), dp(10), dp(10)],  # left, top, right, bottom
            spacing=dp(5)
        )
        
        with add_meal_card.canvas.before:
            Color(*get_color_from_hex('#FFFFFF'))
            self.add_card_rect = RoundedRectangle(
                pos=add_meal_card.pos, 
                size=add_meal_card.size, 
                radius=[dp(20)]
            )
        add_meal_card.bind(size=self.update_add_card, pos=self.update_add_card)
        
        # Nagłówek sekcji - klikalny
        add_header = Button(
            text='[color=333333][b]+ Add new meal[/b][/color]',
            font_size=dp(18),
            color=get_color_from_hex('#333333'),
            size_hint_y=None,
            height=dp(25),
            markup=True,
            background_normal='',
            background_color=[0, 0, 0, 0],  # Przezroczyste
            on_press=self.add_meal
        )
        
        # Pola input w poziomie
        input_layout = BoxLayout(
            orientation='horizontal',
            size_hint_y=None,
            height=dp(50),
            spacing=dp(10)
        )
        
        self.meal_name_input = StyledTextInput(
            hint_text='[MEAL]',
            multiline=False,
            size_hint_x=0.6,
            font_size=dp(14),
            halign='center',
            padding=[dp(10), dp(15), dp(10), dp(15)]  # left, top, right, bottom
        )
        
        self.calories_input = StyledTextInput(
            hint_text='[CAL]',
            multiline=False,
            size_hint_x=0.4,
            input_filter='int',
            font_size=dp(14),
            halign='center',
            padding=[dp(10), dp(15), dp(10), dp(15)]  # left, top, right, bottom
        )
        
        input_layout.add_widget(self.meal_name_input)
        input_layout.add_widget(self.calories_input)
        
        add_meal_card.add_widget(add_header)
        add_meal_card.add_widget(input_layout)
        
        # Sekcja z listą posiłków
        meals_header = BoxLayout(
            orientation='horizontal',
            size_hint_y=None,
            height=dp(40),
            spacing=dp(10)
        )
        
        meals_title = Label(
            text='[color=333333][b]Today\'s meals[/b][/color]',
            font_size=dp(18),
            color=get_color_from_hex('#333333'),
            halign='left',
            size_hint_x=0.8,
            markup=True
        )
        meals_title.bind(size=meals_title.setter('text_size'))
        
        clear_all_btn = StyledButton(
            text='Clear all',
            size_hint_x=0.25,
            bg_color='#FF1744',
            font_size=dp(12),
            bold=True,
            on_press=self.clear_all_meals
        )
        
        meals_header.add_widget(meals_title)
        meals_header.add_widget(clear_all_btn)
        
        # Kontener dla kart posiłków
        self.meals_layout = BoxLayout(
            orientation='vertical',
            size_hint_y=None,
            spacing=dp(8)
        )
        self.meals_layout.bind(minimum_height=self.meals_layout.setter('height'))
        
        # Przycisk statystyk tygodniowych - zaokrąglony
        weekly_stats_btn = Button(
            text='[color=E3F2FD]Stats[/color]',
            size_hint_y=None,
            height=dp(80),
            background_normal='',
            background_down='',
            background_color=[0, 0, 0, 0],  # Przezroczyste - custom background
            font_size=dp(18),
            markup=True,
            on_press=self.show_weekly_stats
        )
        
        # Dodaj zaokrąglone tło do przycisku Stats
        with weekly_stats_btn.canvas.before:
            Color(*get_color_from_hex('#6d1b7b'))
            self.stats_btn_rect = RoundedRectangle(
                pos=weekly_stats_btn.pos, 
                size=weekly_stats_btn.size, 
                radius=[dp(20)]
            )
        weekly_stats_btn.bind(size=self.update_stats_btn, pos=self.update_stats_btn)
        
        # Dodanie wszystkich elementów do głównego layoutu
        content_layout.add_widget(header_layout)
        content_layout.add_widget(self.daily_info_card)
        content_layout.add_widget(add_meal_card)
        content_layout.add_widget(meals_header)
        content_layout.add_widget(self.meals_layout)
        content_layout.add_widget(weekly_stats_btn)
        
        scroll.add_widget(content_layout)
        main_layout.add_widget(scroll)
        
        # Załadowanie dzisiejszych posiłków
        self.load_today_meals()
        
        # Aktualizacja interfejsu co sekundę
        Clock.schedule_interval(self.update_display, 1)
        
        return main_layout
    
    def update_bg(self, *args):
        """Aktualizuje tło aplikacji"""
        self.bg_rect.pos = args[0].pos
        self.bg_rect.size = args[0].size
    
    def update_daily_card(self, *args):
        """Aktualizuje kartę z informacjami dziennymi"""
        self.daily_card_rect.pos = self.daily_info_card.pos
        self.daily_card_rect.size = self.daily_info_card.size
    
    def update_add_card(self, *args):
        """Aktualizuje kartę dodawania posiłku"""
        self.add_card_rect.pos = args[0].pos
        self.add_card_rect.size = args[0].size
    
    def update_stats_btn(self, *args):
        """Aktualizuje zaokrąglone tło przycisku Stats"""
        self.stats_btn_rect.pos = args[0].pos
        self.stats_btn_rect.size = args[0].size
    
    def get_daily_info_text(self):
        """Zwraca tekst z informacjami o dziennym zapotrzebowaniu"""
        consumed = self.get_daily_calories()
        remaining = self.daily_target - consumed
        
        return f"""Daily requirement: {self.daily_target} kcal
Consumed today: {consumed} kcal
Remaining: {remaining} kcal"""
    
    def get_daily_calories(self):
        """Zwraca sumę kalorii spożytych dzisiaj"""
        if self.store.exists(self.today):
            meals = self.store.get(self.today)['meals']
            return sum(meal['calories'] for meal in meals)
        return 0
    
    def add_meal(self, instance):
        """Dodaje nowy posiłek"""
        meal_name = self.meal_name_input.text.strip()
        calories_text = self.calories_input.text.strip()
        
        if not meal_name or not calories_text:
            self.show_popup('Error', 'Please fill in all fields!')
            return
            
        try:
            calories = int(calories_text)
            if calories <= 0:
                raise ValueError("Calories must be greater than 0")
        except ValueError:
            self.show_popup('Error', 'Please enter a valid number of calories!')
            return
        
        # Dodanie posiłku do bazy danych
        if not self.store.exists(self.today):
            self.store.put(self.today, meals=[])
        
        meals = self.store.get(self.today)['meals']
        meal = {
            'name': meal_name,
            'calories': calories,
            'time': datetime.now().strftime('%H:%M')
        }
        meals.append(meal)
        self.store.put(self.today, meals=meals)
        
        # Czyszczenie pól input
        self.meal_name_input.text = ''
        self.calories_input.text = ''
        
        # Odświeżenie wyświetlania
        self.load_today_meals()
        self.update_daily_info()
        
        self.show_popup('Success', f'Added meal: {meal_name} ({calories} kcal)')
    
    def load_today_meals(self):
        """Ładuje i wyświetla dzisiejsze posiłki jako piękne karty"""
        self.meals_layout.clear_widgets()
        
        if self.store.exists(self.today):
            meals = self.store.get(self.today)['meals']
            
            if not meals:
                # Komunikat gdy brak posiłków
                empty_card = BoxLayout(
                    orientation='vertical',
                    size_hint_y=None,
                    height=dp(80),
                    padding=dp(20)
                )
                
                with empty_card.canvas.before:
                    Color(*get_color_from_hex('#F5F5F5'))
                    empty_rect = RoundedRectangle(
                        pos=empty_card.pos, 
                        size=empty_card.size, 
                        radius=[dp(15)]
                    )
                empty_card.bind(
                    size=lambda x, *args: setattr(empty_rect, 'size', x.size),
                    pos=lambda x, *args: setattr(empty_rect, 'pos', x.pos)
                )
                
                empty_label = Label(
                    text='[color=999999]MEAL No meals for today\nAdd your first meal![/color]',
                    font_size=dp(14),
                    halign='center',
                    markup=True
                )
                empty_label.bind(size=empty_label.setter('text_size'))
                
                empty_card.add_widget(empty_label)
                self.meals_layout.add_widget(empty_card)
            else:
                for i, meal in enumerate(meals):
                    # Użyj funkcji wewnętrznej aby poprawnie zamknąć indeks
                    def create_meal_card(index, meal_data):
                        meal_card = MealCard(
                            meal_data=meal_data,
                            delete_callback=lambda x: self.delete_meal(index)
                        )
                        return meal_card
                    
                    meal_card = create_meal_card(i, meal)
                    self.meals_layout.add_widget(meal_card)
    
    def clear_all_meals(self, instance):
        """Usuwa wszystkie posiłki z dzisiaj"""
        def confirm_clear():
            if self.store.exists(self.today):
                self.store.put(self.today, meals=[])
                self.load_today_meals()
                self.update_daily_info()
            self.show_popup('Success', 'TRASH All meals have been deleted!')
        
        self.show_popup(
            'Confirmation', 
            'Are you sure you want to delete\nall today\'s meals?',
            size_hint=(0.8, 0.4),
            confirm_callback=confirm_clear,
            confirm_text='Delete all',
            cancel_text='Cancel'
        )
    
    def create_delete_callback(self, meal_index):
        """Tworzy funkcję callback dla usuwania posiłku"""
        def delete_callback(instance):
            self.delete_meal(meal_index)
        return delete_callback
    
    def delete_meal(self, meal_index):
        """Usuwa posiłek z listy z potwierdzeniem"""
        if self.store.exists(self.today):
            meals = self.store.get(self.today)['meals']
            if 0 <= meal_index < len(meals):
                meal_to_delete = meals[meal_index]
                
                # Popup potwierdzenia
                content = BoxLayout(orientation='vertical', spacing=dp(15), padding=dp(20))
                
                message = Label(
                    text=f'Are you sure you want to delete meal:\n"{meal_to_delete["name"]}" ({meal_to_delete["calories"]} kcal)?',
                    font_size=dp(16),
                    halign='center',
                    text_size=(dp(300), None)
                )
                
                buttons_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=dp(50), spacing=dp(10))
                
                def confirm_delete(confirm_instance):
                    meals.pop(meal_index)
                    self.store.put(self.today, meals=meals)
                    self.load_today_meals()
                    self.update_daily_info()
                    popup.dismiss()
                    self.show_popup('Success', f'Deleted meal: {meal_to_delete["name"]}')
                
                confirm_btn = Button(
                    text='YES - Delete',
                    background_color=get_color_from_hex('#F44336'),
                    color=get_color_from_hex('#FFFFFF'),
                    on_press=confirm_delete
                )
                
                cancel_btn = Button(
                    text='Cancel',
                    background_color=get_color_from_hex('#9E9E9E'),
                    color=get_color_from_hex('#FFFFFF')
                )
                
                buttons_layout.add_widget(cancel_btn)
                buttons_layout.add_widget(confirm_btn)
                
                content.add_widget(message)
                content.add_widget(buttons_layout)
                
                popup = Popup(
                    title='Delete Meal?',
                    content=content,
                    size_hint=(0.8, 0.4),
                    auto_dismiss=False
                )
                
                cancel_btn.bind(on_press=popup.dismiss)
                popup.open()
    
    def show_weekly_stats(self, instance):
        """Wyświetla piękne statystyki tygodniowe"""
        # Obliczenie dat dla ostatniego tygodnia
        today = datetime.now()
        week_days = []
        total_calories = 0
        daily_data = []
        
        for i in range(7):
            day = today - timedelta(days=i)
            day_str = day.strftime('%Y-%m-%d')
            week_days.append(day_str)
            
            if self.store.exists(day_str):
                meals = self.store.get(day_str)['meals']
                daily_calories = sum(meal['calories'] for meal in meals)
                total_calories += daily_calories
                daily_data.append((day, daily_calories, len(meals)))
            else:
                daily_data.append((day, 0, 0))
        
        target_weekly = 7 * self.daily_target
        percentage = (total_calories / target_weekly * 100) if target_weekly > 0 else 0
        
        # Tworzenie pięknego popup ze statystykami
        content = BoxLayout(orientation='vertical', spacing=dp(15), padding=dp(20))
        
        # Header ze statystykami
        stats_header = BoxLayout(
            orientation='vertical',
            size_hint_y=None,
            height=dp(120),
            spacing=dp(5)
        )
        
        week_title = Label(
            text='[color=2196F3][b]Stats[/b][/color]',
            font_size=dp(24),
            color=get_color_from_hex('#2196F3'),
            size_hint_y=None,
            height=dp(30),
            markup=True
        )
        
        # Główne statystyki z kolorami
        main_stats = BoxLayout(orientation='horizontal', size_hint_y=None, height=dp(80))
        
        # Consumed calories
        consumed_box = BoxLayout(orientation='vertical', size_hint_x=0.33)
        consumed_title = Label(text='Consumed', font_size=dp(12), color=get_color_from_hex('#666666'))
        consumed_value = Label(
            text=f'{total_calories}',
            font_size=dp(18),
            bold=True,
            color=get_color_from_hex('#4CAF50')
        )
        consumed_unit = Label(text='kcal', font_size=dp(12), color=get_color_from_hex('#666666'))
        consumed_box.add_widget(consumed_title)
        consumed_box.add_widget(consumed_value)
        consumed_box.add_widget(consumed_unit)
        
        # Weekly target
        target_box = BoxLayout(orientation='vertical', size_hint_x=0.33)
        target_title = Label(text='Target', font_size=dp(12), color=get_color_from_hex('#666666'))
        target_value = Label(
            text=f'{target_weekly}',
            font_size=dp(18),
            bold=True,
            color=get_color_from_hex('#2196F3')
        )
        target_unit = Label(text='kcal', font_size=dp(12), color=get_color_from_hex('#666666'))
        target_box.add_widget(target_title)
        target_box.add_widget(target_value)
        target_box.add_widget(target_unit)
        
        # Progress percentage
        percent_box = BoxLayout(orientation='vertical', size_hint_x=0.33)
        percent_title = Label(text='Progress', font_size=dp(12), color=get_color_from_hex('#666666'))
        
        percent_color = '#4CAF50' if percentage >= 90 else '#FF9800' if percentage >= 70 else '#F44336'
        percent_value = Label(
            text=f'{percentage:.0f}%',
            font_size=dp(18),
            bold=True,
            color=get_color_from_hex(percent_color)
        )
        percent_emoji = Label(
            text='[color={}]{}[/color]'.format(
                percent_color.replace('#', ''),
                'TARGET' if percentage >= 90 else 'GOOD' if percentage >= 70 else 'LOW'
            ),
            font_size=dp(12),
            markup=True
        )
        percent_box.add_widget(percent_title)
        percent_box.add_widget(percent_value)
        percent_box.add_widget(percent_emoji)
        
        main_stats.add_widget(consumed_box)
        main_stats.add_widget(target_box)
        main_stats.add_widget(percent_box)
        
        stats_header.add_widget(week_title)
        stats_header.add_widget(main_stats)
        
        # Additional information
        avg_daily = total_calories / 7
        extra_info = Label(
            text='[color=666666]Daily average: {} kcal[/color]'.format(int(avg_daily)),
            font_size=dp(14),
            size_hint_y=None,
            height=dp(30),
            markup=True
        )
        
        # Szczegóły dzienne z progresem
        details_scroll = ScrollView()
        details_layout = BoxLayout(
            orientation='vertical',
            size_hint_y=None,
            spacing=dp(8)
        )
        details_layout.bind(minimum_height=details_layout.setter('height'))
        
        for day_data in reversed(daily_data):
            day_obj, calories, meals_count = day_data
            day_card = self.create_day_card(day_obj, calories, meals_count)
            details_layout.add_widget(day_card)
        
        details_scroll.add_widget(details_layout)
        
        # Close button
        close_btn = StyledButton(
            text='OK Close',
            size_hint_y=None,
            height=dp(50),
            bg_color='#4CAF50',
            font_size=dp(16),
            bold=True,
            color=get_color_from_hex("#000000")
        )
        content.add_widget(stats_header)
        content.add_widget(extra_info)
        content.add_widget(details_scroll)
        content.add_widget(close_btn)
        
        popup = Popup(
            title='',
            content=content,
            size_hint=(0.95, 0.9),
            separator_height=0
        )
        
        close_btn.bind(on_press=popup.dismiss)
        popup.open()
    
    def create_day_card(self, day_obj, calories, meals_count):
        """Tworzy kartę dla pojedynczego dnia w statystykach"""
        card = BoxLayout(
            orientation='horizontal',
            size_hint_y=None,
            height=dp(60),
            padding=dp(15),
            spacing=dp(15)
        )
        
        # Tło karty z kolorem zależnym od realizacji celu
        goal_percentage = (calories / self.daily_target) * 100 if self.daily_target > 0 else 0
        
        if goal_percentage >= 90:
            bg_color = '#E8F5E8'  # Zielony
            progress_color = '#4CAF50'
        elif goal_percentage >= 70:
            bg_color = '#FFF3E0'  # Pomarańczowy
            progress_color = '#FF9800'
        else:
            bg_color = '#FFEBEE'  # Czerwony
            progress_color = '#F44336'
        
        with card.canvas.before:
            Color(*get_color_from_hex(bg_color))
            card_rect = RoundedRectangle(pos=card.pos, size=card.size, radius=[dp(12)])
        card.bind(
            size=lambda x, *args: setattr(card_rect, 'size', x.size),
            pos=lambda x, *args: setattr(card_rect, 'pos', x.pos)
        )
        
        # Data
        day_name = day_obj.strftime('%a')  # Skrót dnia tygodnia
        day_date = day_obj.strftime('%d.%m')
        
        date_layout = BoxLayout(orientation='vertical', size_hint_x=0.25)
        date_layout.add_widget(Label(
            text=day_name,
            font_size=dp(12),
            bold=True,
            color=get_color_from_hex('#333333')
        ))
        date_layout.add_widget(Label(
            text=day_date,
            font_size=dp(10),
            color=get_color_from_hex('#666666')
        ))
        
        # Informacje o posiłku i kaloriach
        info_layout = BoxLayout(orientation='vertical', size_hint_x=0.5)
        info_layout.add_widget(Label(
            text='{} kcal'.format(calories),
            font_size=dp(16),
            bold=True,
            color=get_color_from_hex(progress_color),
            halign='left'
        ))
        info_layout.add_widget(Label(
            text='{} meals'.format(meals_count) if meals_count != 1 else '1 meal',
            font_size=dp(12),
            color=get_color_from_hex('#666666'),
            halign='left'
        ))
        
        # Procent realizacji
        percent_label = Label(
            text='{}%'.format(int(goal_percentage)),
            font_size=dp(14),
            bold=True,
            color=get_color_from_hex(progress_color),
            size_hint_x=0.25
        )
        
        card.add_widget(date_layout)
        card.add_widget(info_layout)
        card.add_widget(percent_label)
        
        return card
    
    def show_popup(self, title, message, size_hint=(0.8, 0.6), confirm_callback=None, confirm_text='OK', cancel_text='Cancel'):
        """Displays stylized popup with message"""
        content = BoxLayout(orientation='vertical', padding=dp(20), spacing=dp(15))
        
        # Icon depending on message type
        if 'Success' in title or 'success' in title.lower():
            icon = 'OK'
            title_color = '#4CAF50'
        elif 'Error' in title or 'error' in title.lower():
            icon = 'ERROR'
            title_color = '#F44336'
        elif 'Confirmation' in title or confirm_callback:
            icon = 'WARNING'
            title_color = '#FF9800'
        else:
            icon = 'INFO'
            title_color = '#2196F3'
        
        # Tytuł z ikoną
        title_label = Label(
            text='[color={}][b]{} {}[/b][/color]'.format(title_color.replace('#', ''), icon, title),
            font_size=dp(30),
            size_hint_y=None,
            height=dp(40),
            markup=True
        )
        
        # Wiadomość
        msg_label = Label(
            text=message,
            font_size=dp(25),
            color=get_color_from_hex("#898989"),
            text_size=(None, None),
            halign='center',
            valign='middle'
        )
        
        content.add_widget(title_label)
        content.add_widget(msg_label)
        
        # Przyciski - jeden lub dwa w zależności od tego czy jest confirm_callback
        if confirm_callback:
            # Dwa przyciski dla potwierdzenia
            buttons_layout = BoxLayout(orientation='horizontal', spacing=dp(10), size_hint_y=None, height=dp(50))
            
            cancel_btn = StyledButton(
                text=cancel_text,
                size_hint_y=None,
                height=dp(50),
                bg_color=title_color,
                font_size=dp(16),
                color=get_color_from_hex('#000000')
            )
            
            confirm_btn = StyledButton(
                text=confirm_text,
                size_hint_y=None,
                height=dp(50),
                bg_color=title_color,
                font_size=dp(16),
                color=get_color_from_hex('#000000')
            )
            
            buttons_layout.add_widget(cancel_btn)
            buttons_layout.add_widget(confirm_btn)
            content.add_widget(buttons_layout)
        else:
            # Pojedynczy przycisk OK
            close_btn = StyledButton(
                text='OK',
                size_hint_y=None,
                height=dp(50),
                bg_color=title_color,
                font_size=dp(16),
                color=get_color_from_hex('#000000')
            )
            content.add_widget(close_btn)
        
        popup = Popup(
            title='',
            content=content,
            size_hint=size_hint,
            separator_height=0,
            auto_dismiss=False if confirm_callback else True
        )
        
        if confirm_callback:
            def on_confirm(instance):
                popup.dismiss()
                confirm_callback()
            
            confirm_btn.bind(on_press=on_confirm)
            cancel_btn.bind(on_press=popup.dismiss)
        else:
            close_btn.bind(on_press=popup.dismiss)
        
        popup.open()
    
    def update_display(self, dt):
        """Updates display every second"""
        # Check if day has changed
        current_date = datetime.now().strftime('%Y-%m-%d')
        if current_date != self.today:
            self.today = current_date
            self.load_today_meals()
        
        self.update_daily_info()
    
    def update_daily_info(self):
        """Updates daily requirement information with colors"""
        consumed = self.get_daily_calories()
        remaining = self.daily_target - consumed
        
        # Color update based on progress
        consumed_color = '#4CAF50' if consumed <= self.daily_target else '#FF5722'
        remaining_color = '#2196F3' if remaining >= 0 else '#F44336'
        
        self.consumed_label.text = 'Consumed: {} kcal [color=4CAF50][b]EATEN[/b][/color]'.format(consumed)
        self.consumed_label.color = get_color_from_hex(consumed_color)
        
        self.remaining_label.text = 'Remaining: {} kcal [color={}]{}[/color]'.format(
            remaining, 
            '4CAF50' if remaining >= 0 else 'F44336',
            'OK' if remaining >= 0 else 'OVER'
        )
        self.remaining_label.color = get_color_from_hex(remaining_color)


if __name__ == '__main__':
    CalorieCounterApp().run()
