"""
Custom colored text input widget that actually works with color changes
"""

from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.graphics import Color, RoundedRectangle, Line
from kivy.utils import get_color_from_hex
from kivy.metrics import dp
from kivy.clock import Clock
from src.consts import Colors


class ColoredTextInput(RelativeLayout):
    """Custom text input with working color changes"""
    
    def __init__(self, hint_text='', **kwargs):
        # Extract TextInput specific properties
        self.hint_text = hint_text
        self.multiline = kwargs.pop('multiline', False)
        self.input_filter = kwargs.pop('input_filter', None)
        self.font_size = kwargs.pop('font_size', dp(14))
        self.halign = kwargs.pop('halign', 'left')
        self.padding = kwargs.pop('padding', [dp(10), dp(15), dp(10), dp(15)])
        
        super().__init__(**kwargs)
        
        self.text = ""
        self.is_focused = False
        
        # Schedule widget creation after this widget is properly initialized
        Clock.schedule_once(self.create_widgets, 0)
        
    def create_widgets(self, dt):
        """Create child widgets after parent is initialized"""
        
        # Create TextInput for actual input handling - make text very light but not transparent
        self.text_input = TextInput(
            background_normal='',
            background_active='',
            foreground_color=[0.95, 0.95, 0.95, 0.1],  # Almost transparent but not completely
            cursor_color=get_color_from_hex('#4CAF50'),
            multiline=self.multiline,
            input_filter=self.input_filter,
            font_size=self.font_size,
            pos=self.pos,
            size=self.size,
            padding=self.padding
        )
        
        # Create Label for visible text with proper color
        self.label = Label(
            text=self.hint_text,
            color=Colors.GRAYER,  # Gray hint text
            font_size=self.font_size,
            halign=self.halign,
            valign='center',
            pos=self.pos,
            size=self.size,
            text_size=self.size
        )
        
        # Bind events
        self.text_input.bind(text=self.on_text_change)
        self.text_input.bind(focus=self.on_focus_change)
        self.bind(size=self.update_layout, pos=self.update_layout)
        
        # Setup graphics first
        with self.canvas.before:
            Color(*Colors.WHITE)
            self.bg_rect = RoundedRectangle(
                pos=self.pos,
                size=self.size,
                radius=[dp(10)]
            )
            
        # Add widgets - TextInput first (behind), then Label (in front)
        self.add_widget(self.text_input)
        self.add_widget(self.label)
        
        # Initial layout update
        self.update_layout()
            
    def update_layout(self, *args):
        """Update positions and sizes of child widgets"""
        if hasattr(self, 'text_input') and self.text_input:
            self.text_input.pos = self.pos
            self.text_input.size = self.size
        if hasattr(self, 'label') and self.label:
            self.label.pos = self.pos
            self.label.size = self.size
            self.label.text_size = self.size
        if hasattr(self, 'bg_rect') and self.bg_rect:
            self.bg_rect.pos = self.pos
            self.bg_rect.size = self.size
        
    def on_text_change(self, instance, text):
        """Handle text changes"""
        self.text = text
        
        if text.strip():  # If there's content
            self.label.text = text
            self.label.color = Colors.INPUT_TEXT_ACTIVE  # Black color
        else:  # If empty, show hint
            self.label.text = self.hint_text
            self.label.color = Colors.GRAYER  # Gray hint color
            
    def on_focus_change(self, instance, focus):
        """Handle focus changes"""
        self.is_focused = focus
        self.update_graphics()
        
    def update_graphics(self, *args):
        """Update background graphics"""
        self.canvas.before.clear()
        with self.canvas.before:
            if self.is_focused:
                Color(*get_color_from_hex("#87E6A8"))  # Light green when focused
            else:
                Color(*Colors.WHITE)  # White background
            self.bg_rect = RoundedRectangle(
                pos=self.pos,
                size=self.size,
                radius=[dp(10)]
            )
            
            if self.is_focused:
                Color(*get_color_from_hex('#4CAF50'))  # Green border when focused
            else:
                Color(0.8, 0.8, 0.8, 1)  # Gray border
            Line(rounded_rectangle=(self.x, self.y, self.width, self.height, dp(10)), width=dp(2))
