"""
Application header component for the Calorie Counter app
"""

from kivy.uix.boxlayout import BoxLayout
from kivy.metrics import dp
from src.StyledLabel import StyledLabel


class AppHeader(BoxLayout):
    """Header section with app title"""
    
    def __init__(self, **kwargs):
        # Set default properties
        default_props = {
            'orientation': 'horizontal',
            'size_hint_y': None,
            'height': dp(80),
            'spacing': dp(15)
        }
        
        # Merge with any custom kwargs
        default_props.update(kwargs)
        super().__init__(**default_props)
        
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
        
        self.add_widget(title)
