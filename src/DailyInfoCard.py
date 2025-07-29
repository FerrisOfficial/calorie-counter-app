"""
Daily information card component for the Calorie Counter app
"""

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.graphics import Color, RoundedRectangle
from kivy.utils import get_color_from_hex
from kivy.metrics import dp

from src.consts import Colors


class DailyInfoCard(BoxLayout):
    """Card displaying daily calorie information"""
    
    def __init__(self, data_manager, **kwargs):
        self.data_manager = data_manager
        
        # Set default properties
        default_props = {
            'orientation': 'vertical',
            'size_hint_y': None,
            'height': dp(120),
            'padding': dp(20),
            'spacing': dp(5)
        }
        
        # Merge with any custom kwargs
        default_props.update(kwargs)
        super().__init__(**default_props)
        
        # Card background (bez cienia)
        with self.canvas.before:
            Color(*get_color_from_hex('#FFFFFF'))
            self.daily_card_rect = RoundedRectangle(
                pos=self.pos, 
                size=self.size, 
                radius=[dp(20)]
            )

        self.bind(size=self.update_card, pos=self.update_card)

        # Create labels
        self._create_labels()
        
    def _create_labels(self):
        """Creates the calorie information labels"""
        # Calorie information with colorful accents
        consumed = self.data_manager.get_daily_calories()
        remaining = self.data_manager.get_daily_target() - consumed
        
        # Target label
        self.target_label = Label(
            text='Daily target: {} kcal [color=2196F3][b]TARGET[/b][/color]'.format(
                self.data_manager.get_daily_target()
            ),
            font_size=dp(16),
            color=Colors.GRAYER,
            size_hint_y=0.33,
            markup=True
        )
        
        # Consumed label
        consumed_color = Colors.GREEN_HEX if consumed <= self.data_manager.get_daily_target() else Colors.RED_HEX
        self.consumed_label = Label(
            text='Consumed: {} kcal [color=4CAF50][b]EATEN[/b][/color]'.format(consumed),
            font_size=dp(16),
            color=consumed_color,
            size_hint_y=0.33,
            bold=True,
            markup=True
        )
        
        # Remaining label
        remaining_color = '#2196F3' if remaining >= 0 else '#F44336'
        self.remaining_label = Label(
            text='Remaining: {} kcal [color={}]{}[/color]'.format(
                remaining, 
                '4CAF50' if remaining >= 0 else 'F44336',
                'OK' if remaining >= 0 else 'OVER'
            ),
            font_size=dp(16),
            color=get_color_from_hex(remaining_color),
            size_hint_y=0.33,
            bold=True,
            markup=True
        )
        
        # Add labels to layout
        self.add_widget(self.target_label)
        self.add_widget(self.consumed_label)
        self.add_widget(self.remaining_label)
    
    def update_card(self, *args):
        """Updates card background position and size"""
        self.daily_card_rect.pos = self.pos
        self.daily_card_rect.size = self.size
    
    def update_info(self):
        """Updates daily requirement information with colors"""
        consumed = self.data_manager.get_daily_calories()
        remaining = self.data_manager.get_daily_target() - consumed
        
        # Color update based on progress
        consumed_color = '#4CAF50' if consumed <= self.data_manager.get_daily_target() else '#FF5722'
        remaining_color = '#2196F3' if remaining >= 0 else '#F44336'
        
        self.consumed_label.text = 'Consumed: {} kcal [color=4CAF50][b]EATEN[/b][/color]'.format(consumed)
        self.consumed_label.color = get_color_from_hex(consumed_color)
        
        self.remaining_label.text = 'Remaining: {} kcal [color={}]{}[/color]'.format(
            remaining, 
            '4CAF50' if remaining >= 0 else 'F44336',
            'OK' if remaining >= 0 else 'OVER'
        )
        self.remaining_label.color = get_color_from_hex(remaining_color)
