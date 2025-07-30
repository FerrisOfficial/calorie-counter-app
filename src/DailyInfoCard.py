"""
Daily information card component for the Calorie Counter app
"""

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.widget import Widget
from kivy.graphics import Color, RoundedRectangle, Line
from kivy.utils import get_color_from_hex
from kivy.metrics import dp

from src.consts import Colors
from src.UIUtils import UIUtils


class DailyInfoCard(BoxLayout):
    """Card displaying daily calorie information"""
    
    def __init__(self, data_manager, **kwargs):
        self.data_manager = data_manager
        
        # Set default properties
        default_props = {
            'orientation': 'vertical',
            'size_hint_y': None,
            'height': dp(70),  # Further reduced for more compact card
            'padding': [dp(10), dp(10), dp(10), dp(5)],  # left, top, right, bottom - smaller bottom padding
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

        # Create boxes layout
        self._create_boxes()
        
    def _create_boxes(self):
        """Creates three boxes side by side for target, eaten, and remaining with separators"""
        # Horizontal layout for three boxes
        boxes_layout = BoxLayout(
            orientation='horizontal',
            size_hint=(1, 1),
            spacing=dp(5)  # Reduced spacing to make room for separators
        )
        
        # Create three boxes with separators
        self._create_target_box(boxes_layout)
        self._create_separator(boxes_layout)
        self._create_consumed_box(boxes_layout)
        self._create_separator(boxes_layout)
        self._create_remaining_box(boxes_layout)
        
        self.add_widget(boxes_layout)
    
    def _create_target_box(self, parent_layout):
        """Creates the target calories box"""
        target_box = BoxLayout(
            orientation='vertical',
            size_hint_x=0.33,
            spacing=dp(5)  # More negative spacing to bring much closer
        )
        
        target_title = Label(
            text='Target',
            font_size=dp(14),
            color=Colors.BLUE,
            size_hint_y=0.35,  # Smaller proportion
            bold=True,
            halign='center',
            valign='bottom'  # Align text to bottom of its space
        )
        target_title.bind(size=target_title.setter('text_size'))
        
        self.target_value = Label(
            text=f'{self.data_manager.get_daily_target()} kcal',
            font_size=dp(16),
            color=Colors.BLUE,
            size_hint_y=0.65,  # Larger proportion
            bold=True,
            halign='center',
            valign='top'  # Align text to top of its space
        )
        self.target_value.bind(size=self.target_value.setter('text_size'))
        
        target_box.add_widget(target_title)
        target_box.add_widget(self.target_value)
        parent_layout.add_widget(target_box)
    
    def _create_consumed_box(self, parent_layout):
        """Creates the consumed calories box"""
        consumed_box = BoxLayout(
            orientation='vertical',
            size_hint_x=0.33,
            spacing=dp(5)  # More negative spacing to bring much closer
        )
        
        consumed = self.data_manager.get_daily_calories()
        target = self.data_manager.get_daily_target()
        
        # Calculate progress percentage for consumed calories
        consumed_percentage = (consumed / target * 100) if target > 0 else 0
        consumed_color = UIUtils.get_color_based_on_progress(consumed_percentage)
        
        self.consumed_title = Label(
            text='Eaten',
            font_size=dp(14),
            color=consumed_color,
            size_hint_y=0.35,  # Smaller proportion
            bold=True,
            halign='center',
            valign='bottom'  # Align text to bottom of its space
        )
        self.consumed_title.bind(size=self.consumed_title.setter('text_size'))
        
        self.consumed_value = Label(
            text=f'{consumed} kcal',
            font_size=dp(16),
            color=consumed_color,
            size_hint_y=0.65,  # Larger proportion
            bold=True,
            halign='center',
            valign='top'  # Align text to top of its space
        )
        self.consumed_value.bind(size=self.consumed_value.setter('text_size'))
        
        consumed_box.add_widget(self.consumed_title)
        consumed_box.add_widget(self.consumed_value)
        parent_layout.add_widget(consumed_box)
    
    def _create_remaining_box(self, parent_layout):
        """Creates the remaining calories box"""
        remaining_box = BoxLayout(
            orientation='vertical',
            size_hint_x=0.33,
            spacing=dp(5)  # More negative spacing to bring much closer
        )
        
        remaining = self.data_manager.get_daily_target() - self.data_manager.get_daily_calories()
        target = self.data_manager.get_daily_target()
        consumed = self.data_manager.get_daily_calories()
        
        # Calculate progress percentage for remaining calories (inverted logic)
        # When we have more remaining, it's "better" (green), when less remaining it's "worse" (red)
        remaining_percentage = (consumed / target * 100) if target > 0 else 0
        remaining_color = UIUtils.get_color_based_on_progress(remaining_percentage)
        
        self.remaining_title = Label(
            text='Remaining',
            font_size=dp(14),
            color=remaining_color,
            size_hint_y=0.35,  # Smaller proportion
            bold=True,
            halign='center',
            valign='bottom'  # Align text to bottom of its space
        )
        self.remaining_title.bind(size=self.remaining_title.setter('text_size'))
        
        self.remaining_value = Label(
            text=f'{remaining} kcal',
            font_size=dp(16),
            color=remaining_color,
            size_hint_y=0.65,  # Larger proportion
            bold=True,
            halign='center',
            valign='top'  # Align text to top of its space
        )
        self.remaining_value.bind(size=self.remaining_value.setter('text_size'))
        
        remaining_box.add_widget(self.remaining_title)
        remaining_box.add_widget(self.remaining_value)
        parent_layout.add_widget(remaining_box)
    
    def _create_separator(self, parent_layout):
        """Creates a thin grey vertical separator line"""
        separator = Widget(
            size_hint_x=None,
            width=dp(2)  # Increased width for thicker line
        )
        
        with separator.canvas:
            Color(*Colors.LIGHT_GRAY)  # Use constant instead of hex
            separator_line = Line(points=[], width=dp(1.5))  # Increased line width
        
        # Update separator line when widget changes
        def update_separator(*args):
            # Center the line relative to the entire DailyInfoCard
            card_center_y = self.center_y
            separator_line.points = [
                separator.center_x, card_center_y - dp(32.5),  # Start 20dp below card center
                separator.center_x, card_center_y + dp(32.5)   # End 20dp above card center
            ]
        
        separator.bind(pos=update_separator, size=update_separator)
        parent_layout.add_widget(separator)
    
    def _update_separator(self, separator, *args):
        """Updates separator line position and size"""
        # Draw vertical line positioned lower
        self.separator_line.points = [
            separator.center_x, separator.y + dp(20),  # Start 20dp from bottom
            separator.center_x, separator.y + dp(50)   # End 50dp from bottom (30dp line)
        ]
    
    def update_card(self, *args):
        """Updates card background position and size"""
        self.daily_card_rect.pos = self.pos
        self.daily_card_rect.size = self.size
    
    def update_info(self):
        """Updates daily requirement information with colors"""
        consumed = self.data_manager.get_daily_calories()
        remaining = self.data_manager.get_daily_target() - consumed
        target = self.data_manager.get_daily_target()
        
        # Update target value (usually doesn't change, but just in case)
        self.target_value.text = f'{target} kcal'
        
        # Calculate progress percentage and get color for consumed calories
        consumed_percentage = (consumed / target * 100) if target > 0 else 0
        consumed_color = UIUtils.get_color_based_on_progress(consumed_percentage)
        self.consumed_value.text = f'{consumed} kcal'
        self.consumed_value.color = consumed_color
        self.consumed_title.color = consumed_color  # Update title color too
        
        # Calculate progress percentage and get color for remaining calories
        remaining_percentage = (consumed / target * 100) if target > 0 else 0
        remaining_color = UIUtils.get_color_based_on_progress(remaining_percentage)
        self.remaining_value.text = f'{remaining} kcal'
        self.remaining_value.color = remaining_color
        self.remaining_title.color = remaining_color  # Update title color too
