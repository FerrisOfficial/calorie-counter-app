"""
Delete button component for individual meals in the Calorie Counter app
"""

from kivy.uix.button import Button
from kivy.graphics import Color, RoundedRectangle
from kivy.utils import get_color_from_hex
from kivy.metrics import dp


class MealDeleteButton(Button):
    """Styled delete button for individual meals with rounded background"""
    
    def __init__(self, delete_callback, **kwargs):
        self.delete_callback = delete_callback
        
        # Set default properties
        default_props = {
            'text': 'DEL',
            'size_hint': (None, None),  # Fixed size for both dimensions
            'size': (dp(50), dp(50)),   # Smaller square dimensions to fit better in meal card
            'background_normal': '',
            'background_color': [0, 0, 0, 0],  # Transparent - custom background
            'color': get_color_from_hex('#FFFFFF'),
            'font_size': dp(12),
            'on_press': self.delete_callback
        }
        
        # Merge with any custom kwargs
        default_props.update(kwargs)
        super().__init__(**default_props)
        
        # Create rounded background
        self._create_rounded_background()
        
        # Bind to update background on size/position changes
        self.bind(size=self._update_background, pos=self._update_background)
    
    def _create_rounded_background(self):
        """Creates the rounded red background for the delete button"""
        with self.canvas.before:
            Color(*get_color_from_hex('#F44336'))  # Red color
            self.bg_rect = RoundedRectangle(
                pos=self.pos, 
                size=self.size, 
                radius=[dp(15)]
            )
    
    def _update_background(self, *args):
        """Updates the rounded background position and size"""
        self.bg_rect.pos = self.pos
        self.bg_rect.size = self.size
