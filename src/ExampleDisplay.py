"""
Example implementation of BaseDisplayStyle
Demonstrates how to create a custom display using the base style abstraction
"""

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.metrics import dp

from src.BaseDisplayStyle import BaseDisplayStyle
from src.consts import Colors


class ExampleDisplay(BaseDisplayStyle):
    """Example implementation showing how to use BaseDisplayStyle"""
    
    def __init__(self, data_manager=None):
        super().__init__(data_manager)
    
    @property
    def title_text(self):
        """Title for this example display"""
        return 'Example Display'
    
    @property
    def title_color(self):
        """Custom title color"""
        return Colors.GREEN
    
    @property
    def close_button_text(self):
        """Custom close button text"""
        return 'Close Example'
    
    @property
    def close_button_color(self):
        """Custom close button color"""
        return Colors.GREEN
    
    def create_content(self):
        """Creates the main content for this example display"""
        content_container = BoxLayout(orientation='vertical', spacing=dp(20))
        
        # Example content 1
        info_label = Label(
            text='This is an example of how to use BaseDisplayStyle!',
            font_size=dp(16),
            color=Colors.GRAYER,
            text_size=(None, None),
            halign='center'
        )
        
        # Example content 2
        details_label = Label(
            text='[color=666666]You can customize:\n• Title text and color\n• Button text and colors\n• Content layout\n• Popup size[/color]',
            font_size=dp(14),
            markup=True,
            text_size=(None, None),
            halign='left'
        )
        
        # Add content to container
        content_container.add_widget(info_label)
        content_container.add_widget(details_label)
        
        return content_container
    
    def show_example(self):
        """Shows the example display"""
        self.show_display()


# Usage example:
# example_display = ExampleDisplay()
# example_display.show_example()
