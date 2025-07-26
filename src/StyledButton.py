"""
Custom styled button widget for the Calorie Counter app
"""

from kivy.uix.button import Button
from kivy.graphics import Color, RoundedRectangle
from kivy.utils import get_color_from_hex
from kivy.metrics import dp


class StyledButton(Button):
    """Custom styled button with rounded corners - requires explicit parameters"""
    def __init__(self, bg_color, **kwargs):
        self.bg_color_hex = bg_color
        super().__init__(**kwargs)

        # Remove default button background
        self.background_normal = ''
        self.background_down = ''
        self.background_color = (0, 0, 0, 0)  # Completely transparent

        # Handle both hex strings and RGBA tuples/lists for bg_color
        if isinstance(bg_color, str):
            # bg_color is a hex string
            r, g, b, _ = get_color_from_hex(bg_color)
        else:
            # bg_color is already an RGBA tuple/list
            if len(bg_color) >= 3:
                r, g, b = bg_color[0], bg_color[1], bg_color[2]
            else:
                raise ValueError("Invalid bg_color format. Must be hex string or RGBA tuple/list with at least 3 values.")
        
        # Use original color without darkening
        self.bg_color = (r, g, b, 1)

        # Set text alignment
        self.halign = 'center'
        self.valign = 'middle'

        # Create rounded background
        with self.canvas.before:
            self.bg_color_instruction = Color(rgba=self.bg_color)
            self.bg_rect = RoundedRectangle(pos=self.pos, size=self.size, radius=[dp(15)])

        self.bind(pos=self.update_graphics, size=self.update_graphics)

        # Handle markup if specified
        if kwargs.get('markup', False):
            self.bind(size=self.setter('text_size'))

    def update_graphics(self, *args):
        """Updates the button graphics when size or position changes"""
        self.bg_rect.pos = self.pos
        self.bg_rect.size = self.size
        self.bg_color_instruction.rgba = self.bg_color
