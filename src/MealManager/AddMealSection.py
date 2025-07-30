"""
Add meal section component for the Calorie Counter app
"""

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.graphics import Color, RoundedRectangle
from kivy.utils import get_color_from_hex
from kivy.metrics import dp
from src.Styled.StyledTextInput import StyledTextInput
from src.consts import Colors


class AddMealSection(BoxLayout):
    """Section for adding new meals with input fields"""
    
    def __init__(self, add_meal_callback, **kwargs):
        self.add_meal_callback = add_meal_callback
        
        # Set default properties
        default_props = {
            'orientation': 'vertical',
            'size_hint_y': None,
            'height': dp(70),  # Reduced height since no header button
            'padding': [dp(10), dp(5), dp(10), dp(10)],
            'spacing': dp(5)
        }
        
        # Merge with any custom kwargs
        default_props.update(kwargs)
        super().__init__(**default_props)
        
        # Card background
        with self.canvas.before:
            Color(*Colors.WHITE_HEX)
            self.add_card_rect = RoundedRectangle(
                pos=self.pos, 
                size=self.size, 
                radius=[dp(20)]
            )
        self.bind(size=self.update_card, pos=self.update_card)
        
        # Create UI elements
        self._create_inputs()
    
    def _create_inputs(self):
        """Creates the input fields"""
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
        
        self.add_widget(input_layout)
    
    def update_card(self, *args):
        """Updates card background position and size"""
        self.add_card_rect.pos = self.pos
        self.add_card_rect.size = self.size
    
    def get_inputs(self):
        """Returns the input field widgets for external access"""
        return self.meal_name_input, self.calories_input
