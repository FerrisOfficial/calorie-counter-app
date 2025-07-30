"""
Application header component for the Calorie Counter app
"""

from kivy.uix.boxlayout import BoxLayout
from kivy.metrics import dp

from src.Styled.StyledLabel import StyledLabel
from src.SettingsDisplay.SettingsButton import SettingsButton
from src.consts import Colors

class AppHeader(BoxLayout):
    """Header section with app title and settings button, including container with padding"""
    
    def __init__(self, settings_callback=None, **kwargs):
        # Set default properties for the container
        default_props = {
            'orientation': 'vertical',
            'size_hint_y': None,
            'height': dp(80),  # Fixed height for header container
            'padding': [dp(20), dp(10), dp(20), dp(0)]  # Removed bottom padding to match other sections
        }
        
        # Merge with any custom kwargs
        default_props.update(kwargs)
        super().__init__(**default_props)
        
        self.settings_callback = settings_callback
        
        # Create the inner header layout
        header_layout = BoxLayout(
            orientation='horizontal',
            size_hint_y=None,
            height=dp(60),  # Reduced height for more compact header
            spacing=dp(15)
        )
        
        # Title with beautiful font
        title = StyledLabel(
            text='Calorie Counter',
            font_size=dp(28),
            bold=True,
            bg_color=Colors.BLUE_HEX,
            text_color=Colors.BLACK_HEX,
            halign='center',
            valign='middle'
        )
        title.bind(size=title.setter('text_size'))
        
        # Settings button
        settings_button = SettingsButton(settings_callback=self.settings_callback)
        
        header_layout.add_widget(title)
        header_layout.add_widget(settings_button)
        
        # Add the header layout to the container
        self.add_widget(header_layout)
