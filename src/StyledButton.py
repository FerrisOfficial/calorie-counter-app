"""
Custom styled button widget for the Calorie Counter app
"""

from kivy.uix.button import Button
from kivy.graphics import Color, RoundedRectangle
from kivy.utils import get_color_from_hex
from kivy.metrics import dp


class StyledButton(Button):
    """Custom styled button with rounded corners"""
    def __init__(self, bg_color="#84B5FF", markup=False, **kwargs):
        self.bg_color_hex = bg_color
        super().__init__(**kwargs)

        # Remove default button background
        self.background_normal = ''
        self.background_down = ''
        self.background_color = (0, 0, 0, 0)  # Completely transparent

        # Background color (darkened)
        r, g, b, _ = get_color_from_hex(bg_color)
        darker_color = (r * 0.7, g * 0.7, b * 0.7, 1)
        self.bg_color = darker_color

        self.color = kwargs.get('color', get_color_from_hex('#FFFFFF'))
        self.font_size = kwargs.get('font_size', dp(14))
        self.bold = kwargs.get('bold', True)
        self.markup = markup
        self.halign = 'center'
        self.valign = 'middle'

        with self.canvas.before:
            self.bg_color_instruction = Color(rgba=self.bg_color)
            self.bg_rect = RoundedRectangle(pos=self.pos, size=self.size, radius=[dp(15)])

        self.bind(pos=self.update_graphics, size=self.update_graphics)

        if markup:
            self.bind(size=self.setter('text_size'))

    def update_graphics(self, *args):
        self.bg_rect.pos = self.pos
        self.bg_rect.size = self.size
        self.bg_color_instruction.rgba = self.bg_color
