"""
Custom styled widgets for the Calorie Counter app
"""

from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.boxlayout import BoxLayout
from kivy.graphics import Color, RoundedRectangle, Line
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


class StyledTextInput(TextInput):
    """Stylizowany TextInput z zaokrąglonymi rogami"""
    def __init__(self, **kwargs):
        # Get halign before calling super()
        halign = kwargs.pop('halign', 'left')
        super().__init__(**kwargs)
        self.background_normal = ''
        self.background_active = ''
        self.foreground_color = get_color_from_hex('#333333')
        self.cursor_color = get_color_from_hex('#4CAF50')
        self.halign = halign
        self.valign = 'center'  # Vertical centering
        self.is_focused = False
        # Settings for centering
        self.bind(size=self.update_text_size)
        self.bind(size=self.update_graphics, pos=self.update_graphics)
        self.bind(focus=self.on_focus_change)
        
    def update_text_size(self, *args):
        # Center text horizontally and vertically
        self.text_size = (self.width, self.height)
        
    def on_focus_change(self, instance, focus):
        """Handles focus change - highlights field when clicked"""
        self.is_focused = focus
        self.update_graphics()
        
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


class MealCard(BoxLayout):
    """Card representing a single meal"""
    def __init__(self, meal_data, delete_callback, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'horizontal'
        self.size_hint_y = None
        self.height = dp(60)
        self.spacing = dp(10)
        self.padding = [dp(15), dp(5)]
        
        # Card background
        with self.canvas.before:
            Color(*get_color_from_hex('#F5F5F5'))
            self.rect = RoundedRectangle(pos=self.pos, size=self.size, radius=[dp(15)])
        self.bind(size=self.update_rect, pos=self.update_rect)
        
        # Meal icon (simple symbol)
        icon_label = Label(
            text='[color=4CAF50][size=20][b]MEAL[/b][/size][/color]',
            size_hint_x=None,
            width=dp(40),
            markup=True
        )
        
        # Meal information
        meal_info_layout = BoxLayout(orientation='vertical', size_hint_x=0.7)
        
        meal_name = Label(
            text=meal_data['name'],
            font_size=dp(16),
            bold=True,
            color=get_color_from_hex('#333333'),
            halign='left',
            size_hint_y=0.6
        )
        meal_name.bind(size=meal_name.setter('text_size'))
        
        meal_details = Label(
            text='{} • {} kcal'.format(meal_data['time'], meal_data['calories']),
            font_size=dp(12),
            color=get_color_from_hex('#666666'),
            halign='left',
            size_hint_y=0.4
        )
        meal_details.bind(size=meal_details.setter('text_size'))
        
        meal_info_layout.add_widget(meal_name)
        meal_info_layout.add_widget(meal_details)
        
        # Delete button - rounded
        delete_btn = Button(
            text='DELETE',
            size_hint_x=None,
            width=dp(80),
            background_normal='',
            background_color=[0, 0, 0, 0],  # Transparent - custom background
            color=get_color_from_hex('#FFFFFF'),
            font_size=dp(12),
            on_press=delete_callback
        )
        
        # Add rounded background to delete button
        with delete_btn.canvas.before:
            Color(*get_color_from_hex('#F44336'))
            self.delete_btn_rect = RoundedRectangle(
                pos=delete_btn.pos, 
                size=delete_btn.size, 
                radius=[dp(15)]
            )
        delete_btn.bind(size=self.update_delete_btn, pos=self.update_delete_btn)
        
        self.add_widget(icon_label)
        self.add_widget(meal_info_layout)
        self.add_widget(delete_btn)
    
    def update_rect(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size
    
    def update_delete_btn(self, *args):
        """Updates rounded background of delete button"""
        self.delete_btn_rect.pos = args[0].pos
        self.delete_btn_rect.size = args[0].size
