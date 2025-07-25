"""
Main application class for the Calorie Counter app
"""

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.scrollview import ScrollView
from kivy.uix.floatlayout import FloatLayout
from kivy.clock import Clock
from kivy.graphics import Color, RoundedRectangle
from kivy.utils import get_color_from_hex
from kivy.metrics import dp
from datetime import datetime

from src.data_manager import CalorieDataManager
from src.widgets import StyledLabel, StyledButton, StyledTextInput, MealCard
from src.ui_utils import UIUtils
from src.stats_display import StatsDisplay


class CalorieCounterApp(App):
    """Main application class"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.data_manager = CalorieDataManager()
        self.stats_display = StatsDisplay(self.data_manager)
        self.today = datetime.now().strftime('%Y-%m-%d')
        
    def build(self):
        """Builds the main application interface with beautiful design"""
        # Main layout with gradient background
        main_layout = FloatLayout()
        
        # Application background
        with main_layout.canvas.before:
            Color(*get_color_from_hex("#5D9BFFDA"))  # Slightly darker light shade
            self.bg_rect = RoundedRectangle(pos=main_layout.pos, size=main_layout.size)
        main_layout.bind(size=self.update_bg, pos=self.update_bg)
        
        # ScrollView for all content
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
        
        # Header with title and icon
        header_layout = self._create_header()
        
        # Daily information card
        self.daily_info_card = self._create_daily_info_card()
        
        # Add meal section with beautiful card
        add_meal_card = self._create_add_meal_section()
        
        # Meals list section
        meals_header = self._create_meals_header()
        
        # Container for meal cards
        self.meals_layout = BoxLayout(
            orientation='vertical',
            size_hint_y=None,
            spacing=dp(8)
        )
        self.meals_layout.bind(minimum_height=self.meals_layout.setter('height'))
        
        # Weekly statistics button - rounded
        weekly_stats_btn = self._create_stats_button()
        
        # Add all elements to main layout
        content_layout.add_widget(header_layout)
        content_layout.add_widget(self.daily_info_card)
        content_layout.add_widget(add_meal_card)
        content_layout.add_widget(meals_header)
        content_layout.add_widget(self.meals_layout)
        content_layout.add_widget(weekly_stats_btn)
        
        scroll.add_widget(content_layout)
        main_layout.add_widget(scroll)
        
        # Load today's meals
        self.load_today_meals()
        
        # Update interface every second
        Clock.schedule_interval(self.update_display, 1)
        
        return main_layout
    
    def _create_header(self):
        """Creates the header section"""
        header_layout = BoxLayout(
            orientation='horizontal',
            size_hint_y=None,
            height=dp(80),
            spacing=dp(15)
        )
        
        # Title with beautiful font
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
        return header_layout
    
    def _create_daily_info_card(self):
        """Creates the daily information card"""
        daily_info_card = BoxLayout(
            orientation='vertical',
            size_hint_y=None,
            height=dp(120),
            padding=dp(20),
            spacing=dp(5)
        )
        
        with daily_info_card.canvas.before:
            Color(*get_color_from_hex('#FFFFFF'))
            self.daily_card_rect = RoundedRectangle(
                pos=daily_info_card.pos, 
                size=daily_info_card.size, 
                radius=[dp(20)]
            )
            # Shadow
            Color(0, 0, 0, 0.1)
            RoundedRectangle(
                pos=(daily_info_card.x + dp(2), daily_info_card.y - dp(2)), 
                size=daily_info_card.size, 
                radius=[dp(20)]
            )
        daily_info_card.bind(size=self.update_daily_card, pos=self.update_daily_card)
        
        # Calorie information with colorful accents
        consumed = self.data_manager.get_daily_calories()
        remaining = self.data_manager.get_daily_target() - consumed
        
        target_label = Label(
            text='Daily target: {} kcal [color=2196F3][b]TARGET[/b][/color]'.format(
                self.data_manager.get_daily_target()
            ),
            font_size=dp(16),
            color=get_color_from_hex('#333333'),
            size_hint_y=0.33,
            markup=True
        )
        
        consumed_color = '#4CAF50' if consumed <= self.data_manager.get_daily_target() else '#FF5722'
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
        
        daily_info_card.add_widget(target_label)
        daily_info_card.add_widget(self.consumed_label)
        daily_info_card.add_widget(self.remaining_label)
        
        return daily_info_card
    
    def _create_add_meal_section(self):
        """Creates the add meal section"""
        add_meal_card = BoxLayout(
            orientation='vertical',
            size_hint_y=None,
            height=dp(100),
            padding=[dp(10), dp(5), dp(10), dp(10)],
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
        
        # Section header - clickable
        add_header = Button(
            text='[color=333333][b]+ Add new meal[/b][/color]',
            font_size=dp(18),
            color=get_color_from_hex('#333333'),
            size_hint_y=None,
            height=dp(25),
            markup=True,
            background_normal='',
            background_color=[0, 0, 0, 0],  # Transparent
            on_press=self.add_meal
        )
        
        # Input fields horizontally
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
            padding=[dp(10), dp(15), dp(10), dp(15)]
        )
        
        self.calories_input = StyledTextInput(
            hint_text='[CAL]',
            multiline=False,
            size_hint_x=0.4,
            input_filter='int',
            font_size=dp(14),
            halign='center',
            padding=[dp(10), dp(15), dp(10), dp(15)]
        )
        
        input_layout.add_widget(self.meal_name_input)
        input_layout.add_widget(self.calories_input)
        
        add_meal_card.add_widget(add_header)
        add_meal_card.add_widget(input_layout)
        
        return add_meal_card
    
    def _create_meals_header(self):
        """Creates the meals list header"""
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
        
        return meals_header
    
    def _create_stats_button(self):
        """Creates the weekly statistics button"""
        weekly_stats_btn = Button(
            text='[color=E3F2FD]Stats[/color]',
            size_hint_y=None,
            height=dp(80),
            background_normal='',
            background_down='',
            background_color=[0, 0, 0, 0],  # Transparent - custom background
            font_size=dp(18),
            markup=True,
            on_press=self.show_weekly_stats
        )
        
        # Add rounded background to Stats button
        with weekly_stats_btn.canvas.before:
            Color(*get_color_from_hex('#6d1b7b'))
            self.stats_btn_rect = RoundedRectangle(
                pos=weekly_stats_btn.pos, 
                size=weekly_stats_btn.size, 
                radius=[dp(20)]
            )
        weekly_stats_btn.bind(size=self.update_stats_btn, pos=self.update_stats_btn)
        
        return weekly_stats_btn
    
    def update_bg(self, *args):
        """Updates application background"""
        self.bg_rect.pos = args[0].pos
        self.bg_rect.size = args[0].size
    
    def update_daily_card(self, *args):
        """Updates daily information card"""
        self.daily_card_rect.pos = self.daily_info_card.pos
        self.daily_card_rect.size = self.daily_info_card.size
    
    def update_add_card(self, *args):
        """Updates add meal card"""
        self.add_card_rect.pos = args[0].pos
        self.add_card_rect.size = args[0].size
    
    def update_stats_btn(self, *args):
        """Updates rounded background of Stats button"""
        self.stats_btn_rect.pos = args[0].pos
        self.stats_btn_rect.size = args[0].size
    
    def add_meal(self, instance):
        """Adds a new meal"""
        meal_name = self.meal_name_input.text.strip()
        calories_text = self.calories_input.text.strip()
        
        if not meal_name or not calories_text:
            UIUtils.show_popup('Error', 'Please fill in all fields!')
            return
            
        try:
            calories = int(calories_text)
            if calories <= 0:
                raise ValueError("Calories must be greater than 0")
        except ValueError:
            UIUtils.show_popup('Error', 'Please enter a valid number of calories!')
            return
        
        try:
            # Add meal using data manager
            meal = self.data_manager.add_meal(meal_name, calories)
            
            # Clear input fields
            self.meal_name_input.text = ''
            self.calories_input.text = ''
            
            # Refresh display
            self.load_today_meals()
            self.update_daily_info()
            
            UIUtils.show_popup('Success', f'Added meal: {meal_name} ({calories} kcal)')
            
        except ValueError as e:
            UIUtils.show_popup('Error', str(e))
    
    def load_today_meals(self):
        """Loads and displays today's meals as beautiful cards"""
        self.meals_layout.clear_widgets()
        
        meals = self.data_manager.get_today_meals()
        
        if not meals:
            # Message when no meals
            empty_card = self._create_empty_meals_card()
            self.meals_layout.add_widget(empty_card)
        else:
            for i, meal in enumerate(meals):
                # Use inner function to properly close the index
                def create_meal_card(index, meal_data):
                    meal_card = MealCard(
                        meal_data=meal_data,
                        delete_callback=lambda x: self.delete_meal(index)
                    )
                    return meal_card
                
                meal_card = create_meal_card(i, meal)
                self.meals_layout.add_widget(meal_card)
    
    def _create_empty_meals_card(self):
        """Creates empty meals message card"""
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
        return empty_card
    
    def clear_all_meals(self, instance):
        """Deletes all meals from today"""
        def confirm_clear():
            self.data_manager.clear_all_meals()
            self.load_today_meals()
            self.update_daily_info()
            UIUtils.show_popup('Success', 'TRASH All meals have been deleted!')
        
        UIUtils.show_popup(
            'Confirmation', 
            'Are you sure you want to delete\nall today\'s meals?',
            size_hint=(0.8, 0.4),
            confirm_callback=confirm_clear,
            confirm_text='Delete all',
            cancel_text='Cancel'
        )
    
    def delete_meal(self, meal_index):
        """Deletes meal from list with confirmation"""
        meals = self.data_manager.get_today_meals()
        
        if 0 <= meal_index < len(meals):
            meal_to_delete = meals[meal_index]
            
            def confirm_delete():
                deleted_meal = self.data_manager.delete_meal(meal_index)
                if deleted_meal:
                    self.load_today_meals()
                    self.update_daily_info()
                    UIUtils.show_popup('Success', f'Deleted meal: {deleted_meal["name"]}')
            
            UIUtils.show_popup(
                'Confirmation',
                f'Are you sure you want to delete meal:\n"{meal_to_delete["name"]}" ({meal_to_delete["calories"]} kcal)?',
                size_hint=(0.8, 0.4),
                confirm_callback=confirm_delete,
                confirm_text='YES - Delete',
                cancel_text='Cancel'
            )
    
    def show_weekly_stats(self, instance):
        """Shows weekly statistics"""
        self.stats_display.show_weekly_stats()
    
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
        consumed = self.data_manager.get_daily_calories()
        remaining = self.data_manager.get_daily_target() - consumed
        
        # Color update based on progress
        consumed_color = '#4CAF50' if consumed <= self.data_manager.get_daily_target() else '#FF5722'
        remaining_color = '#2196F3' if remaining >= 0 else '#F44336'
        
        self.consumed_label.text = 'Consumed: {} kcal [color=4CAF50][b]EATEN[/b][/color]'.format(consumed)
        self.consumed_label.color = get_color_from_hex(consumed_color)
        
        self.remaining_label.text = 'Remaining: {} kcal [color={}]{}[/color]'.format(
            remaining, 
            '4CAF50' if remaining >= 0 else 'F44336',
            'OK' if remaining >= 0 else 'OVER'
        )
        self.remaining_label.color = get_color_from_hex(remaining_color)
