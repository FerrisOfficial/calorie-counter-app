"""
Settings display components for the Calorie Counter app
"""

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.metrics import dp

from src.BaseDisplayStyle import BaseDisplayStyle
from src.consts import Colors


class SettingsDisplay(BaseDisplayStyle):
    """Handles settings display using base display style"""
    
    def __init__(self, data_manager=None):
        super().__init__(data_manager)
        
    @property
    def title_text(self):
        """Title for the settings display"""
        return 'Settings'
    
    @property
    def title_color(self):
        """Color for the settings title"""
        return Colors.ORANGE
    
    @property
    def close_button_color(self):
        """Background color for the close button"""
        return Colors.ORANGE
    
    def create_content(self):
        """Creates the main content for settings display"""
        content_container = BoxLayout(orientation='vertical', spacing=dp(20))
        
        # Placeholder content
        placeholder_label = Label(
            text='Settings will be implemented here',
            font_size=dp(16),
            color=Colors.GRAY,
            text_size=(None, None),
            halign='center'
        )
        
        # Additional info
        info_label = Label(
            text='[color=666666]This is a placeholder for future settings:\n• Daily calorie goals\n• Theme preferences\n• Data export options\n• Notification settings[/color]',
            font_size=dp(14),
            markup=True,
            text_size=(None, None),
            halign='left'
        )
        
        content_container.add_widget(placeholder_label)
        content_container.add_widget(info_label)
        
        return content_container
    
    def show_settings(self):
        """Shows the settings display"""
        self.show_display()
