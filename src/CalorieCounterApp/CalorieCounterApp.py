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

from src.CalorieCounterApp.CalorieDataManager import CalorieDataManager
from src.Styled.StyledLabel import StyledLabel
from src.Styled.StyledButton import StyledButton
from src.Styled.StyledTextInput import StyledTextInput
from src.UIUtils import UIUtils
from src.Stats.StatsDisplay import StatsDisplay
from src.SettingsDisplay.SettingsDisplay import SettingsDisplay
from src.MealManager.MealManager import MealManager
from src.Stats.StatsButton import StatsButton
from src.CalorieCounterApp.AppHeader import AppHeader
from src.CalorieCounterApp.DailyInfoCard import DailyInfoCard
from src.MealManager.AddMealSection import AddMealSection
from src.MealManager.MealsHeader import MealsHeader
from src.consts import Colors


class CalorieCounterApp(App):
    """Main application class"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.data_manager = CalorieDataManager()
        self.stats_display = StatsDisplay(self.data_manager)
        self.settings_display = SettingsDisplay(self.data_manager)
        self.today = datetime.now().strftime('%Y-%m-%d')
        
    def build(self):
        """Builds the main application interface with fixed elements and scrollable meal cards"""
        # Main layout with gradient background
        main_layout = BoxLayout(orientation='vertical')
        
        # Application background
        with main_layout.canvas.before:
            Color(*Colors.GRAYER)  # Slightly darker light shade
            self.bg_rect = RoundedRectangle(pos=main_layout.pos, size=main_layout.size)
        main_layout.bind(size=self.update_bg, pos=self.update_bg)
        
        # Fixed header at the top
        header = self._create_header()
        main_layout.add_widget(header)
        
        # Fixed content layout with padding
        fixed_content = BoxLayout(
            orientation='vertical', 
            padding=[dp(20), 0, dp(20), 0],  # Only horizontal padding
            spacing=dp(15),
            size_hint_y=None
        )
        
        # Calculate fixed height for all fixed elements
        fixed_height = dp(70 + 70 + 40 + 45)  # daily_info + add_meal + meals_header + spacing (3*15)
        fixed_content.height = fixed_height
        
        # Daily information card (fixed)
        self.daily_info_card = self._create_daily_info_card()
        fixed_content.add_widget(self.daily_info_card)

        # Add meal section (fixed)
        self.add_meal_card = self._create_add_meal_section()
        fixed_content.add_widget(self.add_meal_card)

        # Meals list header (fixed)
        self.meals_header = self._create_meals_header()
        fixed_content.add_widget(self.meals_header)
        
        # Add fixed content to main layout
        main_layout.add_widget(fixed_content)
        
        # ScrollView only for meal cards with padding
        scroll_container = BoxLayout(
            orientation='vertical',
            padding=[dp(20), dp(15), dp(20), 0],  # Add top padding for spacing between header and meal cards
            size_hint=(1, 1)  # Takes remaining space
        )
        
        scroll = ScrollView()
        
        # Container for meal cards only
        self.meals_layout = BoxLayout(
            orientation='vertical',
            size_hint_y=None,
            spacing=dp(8)
        )
        self.meals_layout.bind(minimum_height=self.meals_layout.setter('height'))
        
        # Ensure meals_layout is transparent
        with self.meals_layout.canvas.before:
            Color(0, 0, 0, 0)  # Completely transparent
        
        scroll.add_widget(self.meals_layout)
        scroll_container.add_widget(scroll)
        main_layout.add_widget(scroll_container)
        
        # Fixed stats button at the bottom
        stats_container = BoxLayout(
            orientation='vertical',
            padding=[dp(20), dp(15), dp(20), dp(20)],
            size_hint_y=None,
            height=dp(95)  # Height for smaller stats button + padding (60 + 35 padding)
        )
        
        weekly_stats_btn = self._create_stats_button()
        stats_container.add_widget(weekly_stats_btn)
        main_layout.add_widget(stats_container)
        
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
        return AppHeader(settings_callback=self._show_settings)
    
    def _create_daily_info_card(self):
        """Creates the daily information card"""
        return DailyInfoCard(self.data_manager)
    
    def _create_add_meal_section(self):
        """Creates the add meal section"""
        return AddMealSection(lambda x: self.meal_manager.add_meal(x) if hasattr(self, 'meal_manager') else None)
    
    def _create_meals_header(self):
        """Creates the meals list header"""
        return MealsHeader(
            self._clear_all_meals,
            self._add_meal
        )
    
    def _clear_all_meals(self, instance):
        """Callback for clear all meals button"""
        if hasattr(self, 'meal_manager'):
            self.meal_manager.clear_all_meals(instance)
    
    def _add_meal(self, instance):
        """Callback for add meal button"""
        if hasattr(self, 'meal_manager'):
            self.meal_manager.add_meal(instance)
    
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
    
    def _show_settings(self, instance):
        """Shows the settings display"""
        self.settings_display.show_settings()
