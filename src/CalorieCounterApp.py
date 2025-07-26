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

from src.CalorieDataManager import CalorieDataManager
from src.StyledLabel import StyledLabel
from src.StyledButton import StyledButton
from src.StyledTextInput import StyledTextInput
from src.UIUtils import UIUtils
from src.StatsDisplay import StatsDisplay
from src.MealManager import MealManager
from src.StatsButton import StatsButton
from src.AppHeader import AppHeader
from src.DailyInfoCard import DailyInfoCard
from src.AddMealSection import AddMealSection
from src.MealsHeader import MealsHeader
from src.consts import Colors


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
            Color(*Colors.GRAYER)  # Slightly darker light shade
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
        self.add_meal_card = self._create_add_meal_section()

        # Meals list section
        self.meals_header = self._create_meals_header()        # Container for meal cards
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
        content_layout.add_widget(self.add_meal_card)
        content_layout.add_widget(self.meals_header)
        content_layout.add_widget(self.meals_layout)
        content_layout.add_widget(weekly_stats_btn)
        
        scroll.add_widget(content_layout)
        main_layout.add_widget(scroll)
        
        # Initialize MealManager with UI components
        meal_name_input, calories_input = self.add_meal_card.get_inputs()
        self.meal_manager = MealManager(
            self.data_manager,
            self.meals_layout,
            meal_name_input,
            calories_input,
            self.update_daily_info
        )
        
        # Load today's meals
        self.meal_manager.load_today_meals()
        
        # Update interface every second
        Clock.schedule_interval(self.update_display, 1)
        
        return main_layout
    
    def _create_header(self):
        """Creates the header section"""
        return AppHeader()
    
    def _create_daily_info_card(self):
        """Creates the daily information card"""
        return DailyInfoCard(self.data_manager)
    
    def _create_add_meal_section(self):
        """Creates the add meal section"""
        return AddMealSection(lambda x: self.meal_manager.add_meal(x) if hasattr(self, 'meal_manager') else None)
    
    def _create_meals_header(self):
        """Creates the meals list header"""
        return MealsHeader(lambda x: self.meal_manager.clear_all_meals(x) if hasattr(self, 'meal_manager') else None)
    
    def _create_stats_button(self):
        """Creates the weekly statistics button"""
        return StatsButton(self.show_weekly_stats)
    
    def update_bg(self, *args):
        """Updates application background"""
        self.bg_rect.pos = args[0].pos
        self.bg_rect.size = args[0].size
    
    def show_weekly_stats(self, instance):
        """Shows weekly statistics"""
        self.stats_display.show_weekly_stats()
    
    def update_display(self, dt):
        """Updates display every second"""
        # Check if day has changed
        current_date = datetime.now().strftime('%Y-%m-%d')
        if current_date != self.today:
            self.today = current_date
            self.meal_manager.load_today_meals()
        
        self.update_daily_info()
    
    def update_daily_info(self):
        """Updates daily requirement information with colors"""
        self.daily_info_card.update_info()
