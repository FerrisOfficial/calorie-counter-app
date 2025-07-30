"""
Meals header component for the Calorie Counter app
"""

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.utils import get_color_from_hex
from kivy.metrics import dp
from src.CalorieCounterApp.ClearAllButton import ClearAllButton
from src.Styled.StyledButton import StyledButton
from src.consts import Colors


class MealsHeader(BoxLayout):
    """Header for the meals list section with clear all button"""
    
    def __init__(self, clear_all_callback, add_meal_callback=None, **kwargs):
        self.clear_all_callback = clear_all_callback
        self.add_meal_callback = add_meal_callback
        
        # Set default properties
        default_props = {
            'orientation': 'horizontal',
            'size_hint_y': None,
            'height': dp(40),
            'spacing': dp(3)  # Minimal spacing to maximize button space
        }
        
        # Merge with any custom kwargs
        default_props.update(kwargs)
        super().__init__(**default_props)
        
        # Create UI elements
        self._create_add_button()
        self._create_clear_button()
    
    def _create_title(self):
        """Creates the meals title"""
        self.meals_title = Label(
            text='',  # Empty text to take no visual space
            font_size=dp(6),  # Even smaller font
            color=get_color_from_hex('#333333'),
            halign='left',
            size_hint_x=None,  # Fixed width instead of percentage
            width=dp(5),  # Absolute minimal width - reduced from 10dp to 5dp
            markup=True
        )
        self.meals_title.bind(size=self.meals_title.setter('text_size'))
        
        self.add_widget(self.meals_title)
    
    def _create_add_button(self):
        """Creates the add meal button"""
        if self.add_meal_callback:
            self.add_meal_btn = StyledButton(
                text='+ Add meal',
                size_hint_x=0.75,  # 75% of total width
                bg_color=Colors.GREEN_HEX,  # Green color for add action
                font_size=dp(20),
                bold=True,
                on_press=self.add_meal_callback
            )
            self.add_widget(self.add_meal_btn)
        else:
            # Add spacer if no add button
            spacer = Label(size_hint_x=0.75)
            self.add_widget(spacer)
    
    def _create_clear_button(self):
        """Creates the clear all button"""
        self.clear_all_btn = ClearAllButton(self.clear_all_callback)
        # Using default size from ClearAllButton class (0.25)
        
        self.add_widget(self.clear_all_btn)
