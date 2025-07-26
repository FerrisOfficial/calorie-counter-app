"""
Meals header component for the Calorie Counter app
"""

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.utils import get_color_from_hex
from kivy.metrics import dp
from src.ClearAllButton import ClearAllButton


class MealsHeader(BoxLayout):
    """Header for the meals list section with clear all button"""
    
    def __init__(self, clear_all_callback, **kwargs):
        self.clear_all_callback = clear_all_callback
        
        # Set default properties
        default_props = {
            'orientation': 'horizontal',
            'size_hint_y': None,
            'height': dp(40),
            'spacing': dp(10)
        }
        
        # Merge with any custom kwargs
        default_props.update(kwargs)
        super().__init__(**default_props)
        
        # Create UI elements
        self._create_title()
        self._create_clear_button()
    
    def _create_title(self):
        """Creates the meals title"""
        self.meals_title = Label(
            text='[color=333333][b]Today\'s meals[/b][/color]',
            font_size=dp(18),
            color=get_color_from_hex('#333333'),
            halign='left',
            size_hint_x=0.8,
            markup=True
        )
        self.meals_title.bind(size=self.meals_title.setter('text_size'))
        
        self.add_widget(self.meals_title)
    
    def _create_clear_button(self):
        """Creates the clear all button"""
        self.clear_all_btn = ClearAllButton(self.clear_all_callback)
        
        self.add_widget(self.clear_all_btn)
