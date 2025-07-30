"""
Abstract base class for display styles in the Calorie Counter app
Provides common styling, layout, and behavior patterns for popup displays
"""

from abc import ABC, abstractmethod
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.graphics import Color, RoundedRectangle
from kivy.utils import get_color_from_hex
from kivy.metrics import dp

from src.StyledButton import StyledButton
from src.consts import Colors


class BaseDisplayStyle(ABC):
    """
    Abstract base class for display styles.
    
    Provides common functionality for:
    - Color schemes and styling
    - Title positioning and styling
    - Exit button creation and positioning
    - Popup creation and management
    """
    
    def __init__(self, data_manager=None):
        self.data_manager = data_manager
        self.popup = None
        
    @property
    @abstractmethod
    def title_text(self):
        """Abstract property for the display title"""
        pass
    
    @property
    def title_color(self):
        """Color for the main title"""
        return Colors.BLUE
    
    @property
    def title_font_size(self):
        """Font size for the main title"""
        return dp(24)
    
    @property
    def background_color(self):
        """Background color for the main container"""
        return Colors.WHITE
    
    @property
    def content_spacing(self):
        """Spacing between content elements"""
        return dp(15)
    
    @property
    def content_padding(self):
        """Padding for the main content container"""
        return dp(20)
    
    @property
    def popup_size_hint(self):
        """Size hint for the popup (width, height)"""
        return (0.95, 0.9)
    
    @property
    def close_button_text(self):
        """Text for the close button"""
        return 'OK Close'
    
    @property
    def close_button_color(self):
        """Background color for the close button"""
        return Colors.BLUE
    
    @property
    def close_button_text_color(self):
        """Text color for the close button"""
        return Colors.BLACK
    
    def create_title_widget(self):
        """Creates the styled title widget"""
        return Label(
            text=f'[color={Colors.to_hex(self.title_color).replace("#", "")}][b]{self.title_text}[/b][/color]',
            font_size=self.title_font_size,
            color=self.title_color,
            size_hint_y=None,
            height=dp(30),
            markup=True
        )
    
    def create_close_button(self):
        """Creates the styled close button"""
        close_btn = StyledButton(
            text=self.close_button_text,
            size_hint_y=None,
            height=dp(50),
            bg_color=self.close_button_color,
            font_size=dp(16),
            bold=True,
            color=self.close_button_text_color
        )
        return close_btn
    
    def create_main_container(self):
        """Creates the main content container with styling"""
        return BoxLayout(
            orientation='vertical', 
            spacing=self.content_spacing, 
            padding=self.content_padding
        )
    
    def create_popup(self, content):
        """Creates and configures the popup with the given content"""
        popup = Popup(
            title='',
            content=content,
            size_hint=self.popup_size_hint,
            separator_height=0
        )
        return popup
    
    def create_card_background(self, widget, bg_color):
        """Creates a rounded background for card widgets"""
        with widget.canvas.before:
            Color(*get_color_from_hex(bg_color))
            card_rect = RoundedRectangle(pos=widget.pos, size=widget.size, radius=[dp(12)])
        
        widget.bind(
            size=lambda x, *args: setattr(card_rect, 'size', x.size),
            pos=lambda x, *args: setattr(card_rect, 'pos', x.pos)
        )
        return card_rect
    
    @abstractmethod
    def create_content(self):
        """Abstract method to create the main content for the display"""
        pass
    
    def show_display(self):
        """Main method to show the display with proper styling and layout"""
        # Create main container
        content = self.create_main_container()
        
        # Add title
        title_widget = self.create_title_widget()
        content.add_widget(title_widget)
        
        # Add main content (implemented by subclasses)
        main_content = self.create_content()
        if main_content:
            content.add_widget(main_content)
        
        # Add close button
        close_btn = self.create_close_button()
        content.add_widget(close_btn)
        
        # Create and configure popup
        self.popup = self.create_popup(content)
        close_btn.bind(on_press=self.popup.dismiss)
        
        # Show popup
        self.popup.open()
    
    def dismiss_display(self):
        """Dismisses the current display"""
        if self.popup:
            self.popup.dismiss()
