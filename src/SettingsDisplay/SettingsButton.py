"""
Settings button component for the Calorie Counter app
"""

from kivy.uix.floatlayout import FloatLayout
from kivy.uix.image import Image
from kivy.metrics import dp
import os

from src.Styled.StyledButton import StyledButton
from src.consts import Colors


class SettingsButton(FloatLayout):
    """Settings button with icon and callback functionality"""
    
    def __init__(self, settings_callback=None, **kwargs):
        # Set default properties
        default_props = {
            'size_hint': (None, 1),  # Full height, fixed width
            'width': dp(50)
        }
        
        # Merge with any custom kwargs
        default_props.update(kwargs)
        super().__init__(**default_props)
        
        self.settings_callback = settings_callback
        
        # Create the styled button
        self.settings_btn = StyledButton(
            text='',  # Empty text since we're using an icon
            size_hint=(None, None),
            size=(dp(50), dp(50)),
            pos_hint={'center_x': 0.5, 'center_y': 0.5},
            bg_color=(Colors.BLACK[0], Colors.BLACK[1], Colors.BLACK[2], 0.1),  # Black with transparency
            font_size=dp(20)
        )
        
        # Add settings icon
        self._setup_icon()
        
        # Bind settings button callback
        if self.settings_callback:
            self.settings_btn.bind(on_press=self.settings_callback)
    
    def _setup_icon(self):
        """Sets up the settings icon or fallback text"""
        icon_path = os.path.join('src', 'textures', 'settings_icon.png')
        if os.path.exists(icon_path):
            # Add button first
            self.add_widget(self.settings_btn)
            
            # Add icon as overlay
            settings_icon = Image(
                source=icon_path,
                size_hint=(None, None),
                size=(dp(30), dp(30)),
                pos_hint={'center_x': 0.5, 'center_y': 0.5}
            )
            self.add_widget(settings_icon)
        else:
            # Fallback to text if icon not found
            self.settings_btn.text = '⚙'
            self.add_widget(self.settings_btn)
    
    def set_callback(self, callback):
        """Sets or updates the callback function"""
        self.settings_callback = callback
        if callback:
            self.settings_btn.bind(on_press=callback)
