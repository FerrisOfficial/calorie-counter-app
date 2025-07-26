"""
Custom stats button component for the Calorie Counter app
"""

from kivy.utils import get_color_from_hex
from kivy.metrics import dp
from src.StyledButton import StyledButton
from src.consts import Colors


class StatsButton(StyledButton):
    """Custom styled button for displaying weekly statistics"""
    
    def __init__(self, stats_callback, **kwargs):
        # Set default properties for stats button
        default_props = {
            'text': 'Stats',
            'size_hint_y': None,
            'height': dp(80),
            'bg_color': Colors.BLUE_HEX,  # Same blue as stats page
            'font_size': dp(18),
            'bold': True,
            'color': Colors.BLACK,
            'on_press': stats_callback
        }
        
        # Merge with any custom kwargs
        default_props.update(kwargs)
        
        super().__init__(**default_props)
