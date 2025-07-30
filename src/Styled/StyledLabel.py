"""
Custom styled label widget for the Calorie Counter app
"""

from kivy.uix.label import Label
from kivy.graphics import Color, RoundedRectangle
from kivy.utils import get_color_from_hex
from kivy.metrics import dp


class StyledLabel(Label):
    """Stylizowany Label z kolorowym tłem"""
    def __init__(self, bg_color='#FFFFFF', text_color='#000000', **kwargs):
        super().__init__(**kwargs)
        self.bg_color = get_color_from_hex(bg_color)
        self.color = get_color_from_hex(text_color)
        self.bind(size=self.update_graphics, pos=self.update_graphics)
        
    def update_graphics(self, *args):
        self.canvas.before.clear()
        with self.canvas.before:
            Color(*self.bg_color)
            RoundedRectangle(pos=self.pos, size=self.size, radius=[dp(10)])
