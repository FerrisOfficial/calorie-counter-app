"""
Custom styled text input widget for the Calorie Counter app
"""

from kivy.uix.textinput import TextInput
from kivy.graphics import Color, RoundedRectangle, Line
from kivy.utils import get_color_from_hex
from kivy.metrics import dp
from src.consts import Colors


class StyledTextInput(TextInput):
    """Stylizowany TextInput z zaokrąglonymi rogami"""
    def __init__(self, **kwargs):
        # Get halign before calling super()
        halign = kwargs.pop('halign', 'left')
        super().__init__(**kwargs)
        self.background_normal = ''
        self.background_active = ''
        self.cursor_color = get_color_from_hex('#4CAF50')
        self.halign = halign
        self.is_focused = False
        # Disable markup to avoid display issues
        self.markup = False
        # Set colors based on content
        self.default_foreground_color = Colors.LIGHT_GRAY  # Light grey for hint text
        self.active_foreground_color = Colors.INPUT_TEXT_ACTIVE
        self.foreground_color = self.default_foreground_color
        # Track if field has content for visual feedback
        self.has_content = False
        # Settings for centering
        self.bind(size=self.update_text_size)
        self.bind(size=self.update_graphics, pos=self.update_graphics)
        self.bind(focus=self.on_focus_change)
        self.bind(text=self.on_text_change)
        # Ustaw padding_y: dolny większy niż górny dla lepszego centrowania
        self.padding_y = [13, 5]
        # Spróbuj ustawić valign jeśli obsługiwane przez TextInput
        try:
            self.valign = 'middle'
        except Exception:
            pass

    # Usunięto dynamiczne centrowanie przez update_vertical_padding
        
    def update_text_size(self, *args):
        # Center text horizontally and vertically
        self.text_size = (self.width, self.height)
        
    def on_focus_change(self, instance, focus):
        """Handles focus change - highlights field when clicked"""
        self.is_focused = focus
        self.update_graphics()
        
    def on_text_change(self, instance, text):
        """Handle text changes and update color"""
        old_has_content = self.has_content
        self.has_content = bool(text.strip())
        
        if self.has_content:
            # Text exists - make it black and change cursor/selection colors
            self.foreground_color = self.active_foreground_color
            self.cursor_color = Colors.INPUT_TEXT_ACTIVE  # Black cursor when text exists
            if hasattr(self, 'selection_color'):
                self.selection_color = [0.3, 0.3, 0.3, 0.5]  # Dark selection
        else:
            # No text - make it gray and green cursor
            self.foreground_color = self.default_foreground_color
            self.cursor_color = get_color_from_hex('#4CAF50')  # Green cursor when empty
            if hasattr(self, 'selection_color'):
                self.selection_color = [0.2, 0.8, 0.4, 0.5]  # Green selection
        
        # Update graphics if content status changed
        if old_has_content != self.has_content:
            self.update_graphics()
        
    def update_graphics(self, *args):
        self.canvas.before.clear()
        with self.canvas.before:
            if self.is_focused:
                # Light highlight when field has focus
                Color(*get_color_from_hex("#87E6A8"))  # Slightly darker green
            elif self.has_content:
                # Subtle blue tint when field has content (visual feedback)
                Color(*get_color_from_hex("#F0F8FF"))  # Very light blue
            else:
                Color(1, 1, 1, 1)  # White background
            RoundedRectangle(pos=self.pos, size=self.size, radius=[dp(10)])
            
            if self.is_focused:
                # Green border when field has focus
                Color(*get_color_from_hex('#4CAF50'))
            elif self.has_content:
                # Darker border when field has content
                Color(0.4, 0.4, 0.4, 1)  # Dark gray border
            else:
                Color(0.8, 0.8, 0.8, 1)  # Light gray border
            Line(rounded_rectangle=(self.x, self.y, self.width, self.height, dp(10)), width=dp(2))
