"""
Clear all button component for the Calorie Counter app
"""

from src.StyledButton import StyledButton
from kivy.metrics import dp

from src.consts import Colors


class ClearAllButton(StyledButton):
    """Styled button for clearing all meals with red styling"""
    
    def __init__(self, clear_callback, **kwargs):
        # Set default properties for clear all button
        default_props = {
            'text': 'DEL',
            'size_hint_x': 0.25,
            'bg_color': Colors.RED_HEX,  # Red color for delete action
            'font_size': dp(12),
            'bold': True,
            'on_press': clear_callback
        }
        
        # Merge with any custom kwargs
        default_props.update(kwargs)
        super().__init__(**default_props)
