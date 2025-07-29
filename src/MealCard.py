"""
Meal card component for the Calorie Counter app
"""

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.graphics import Color, RoundedRectangle
from kivy.utils import get_color_from_hex
from kivy.metrics import dp
from src.MealDeleteButton import MealDeleteButton
from src.consts import Colors


class MealCard(BoxLayout):
    """Card representing a single meal"""
    def __init__(self, meal_data, delete_callback, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'horizontal'
        self.size_hint_y = None
        self.height = dp(60)
        self.spacing = dp(10)
        self.padding = [dp(15), dp(5)]
        
        # Card background
        with self.canvas.before:
            Color(*get_color_from_hex('#F5F5F5'))
            self.rect = RoundedRectangle(pos=self.pos, size=self.size, radius=[dp(15)])
        self.bind(size=self.update_rect, pos=self.update_rect)
        
        # Meal icon (simple symbol)
        icon_label = Label(
            text='[color=4CAF50][size=20][b]MEAL[/b][/size][/color]',
            size_hint_x=None,
            width=dp(40),
            markup=True
        )
        
        # Meal information
        meal_info_layout = BoxLayout(orientation='vertical', size_hint_x=0.7)
        
        meal_name = Label(
            text=meal_data['name'],
            font_size=dp(16),
            bold=True,
            color=Colors.BLACK,
            halign='left',
            size_hint_y=0.6
        )
        meal_name.bind(size=meal_name.setter('text_size'))
        
        meal_details = Label(
            text='{} • {} kcal'.format(meal_data['time'], meal_data['calories']),
            font_size=dp(12),
            color=Colors.GRAY,
            halign='left',
            size_hint_y=0.4
        )
        meal_details.bind(size=meal_details.setter('text_size'))
        
        meal_info_layout.add_widget(meal_name)
        meal_info_layout.add_widget(meal_details)
        
        # Delete button using the new component
        delete_btn = MealDeleteButton(delete_callback)
        
        self.add_widget(icon_label)
        self.add_widget(meal_info_layout)
        self.add_widget(delete_btn)
    
    def update_rect(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size
