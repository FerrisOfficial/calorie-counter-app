"""
Custom styled text input widget for the Calorie Counter app
"""

from kivy.uix.textinput import TextInput
from kivy.graphics import Color, RoundedRectangle, Line
from kivy.utils import get_color_from_hex
from kivy.metrics import dp
from src.consts import Colors


class StyledTextInput(TextInput):
    """Stylizowany TextInput z zaokrąglonymi rogami i zmieniającym się kolorem tekstu"""
    def __init__(self, **kwargs):
        # Get halign before calling super()
        halign = kwargs.pop('halign', 'left')
        super().__init__(**kwargs)
        self.background_normal = ''
        self.background_active = ''
        self.foreground_color = Colors.GRAYER  # Default gray color from consts
        self.cursor_color = get_color_from_hex('#4CAF50')
        self.halign = halign
        self.valign = 'center'  # Vertical centering
        self.is_focused = False
        self.markup = True  # Enable markup
        
        # Settings for centering
        self.bind(size=self.update_text_size)
        self.bind(size=self.update_graphics, pos=self.update_graphics)
        self.bind(focus=self.on_focus_change)
        self.bind(text=self.on_text_change)
        
        # Track original text without markup
        self._original_text = ""
        self._updating_markup = False
        
    def update_text_size(self, *args):
        # Center text horizontally and vertically
        self.text_size = (self.width, self.height)
        
    def on_focus_change(self, instance, focus):
        """Handles focus change - highlights field when clicked"""
        self.is_focused = focus
        self.update_graphics()
        
    def on_text_change(self, instance, text):
        """Handle text changes and apply color markup"""
        # Prevent recursion when we're updating markup
        if self._updating_markup:
            return
            
        # Remove any existing markup to get clean text
        import re
        clean_text = re.sub(r'\[color=[^\]]*\]([^\[]*)\[/color\]', r'\1', text)
        self._original_text = clean_text
        
        # Apply color markup based on content
        if clean_text.strip():
            # Text exists - make it black
            markup_text = f'[color={Colors.INPUT_TEXT_ACTIVE_HEX}]{clean_text}[/color]'
        else:
            # No text - no markup needed
            markup_text = clean_text
            
        # Update with markup if different
        if markup_text != text:
            self._updating_markup = True
            self.text = markup_text
            self._updating_markup = False
    
    @property
    def plain_text(self):
        """Get text without markup"""
        return self._original_text
        
    def update_graphics(self, *args):
        self.canvas.before.clear()
        with self.canvas.before:
            if self.is_focused:
                # Light highlight when field has focus
                Color(*get_color_from_hex("#87E6A8"))  # Slightly darker green
            else:
                Color(1, 1, 1, 1)  # White background
            RoundedRectangle(pos=self.pos, size=self.size, radius=[dp(10)])
            
            if self.is_focused:
                # Green border when field has focus
                Color(*get_color_from_hex('#4CAF50'))
            else:
                Color(0.8, 0.8, 0.8, 1)  # Gray border
            Line(rounded_rectangle=(self.x, self.y, self.width, self.height, dp(10)), width=dp(2))
