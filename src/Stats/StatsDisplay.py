"""
Statistics display components for the Calorie Counter app
"""

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.graphics import Color, RoundedRectangle
from kivy.utils import get_color_from_hex
from kivy.metrics import dp

from src.Styled.BaseDisplayStyle import BaseDisplayStyle
from src.UIUtils import UIUtils
from src.consts import Colors


class StatsDisplay(BaseDisplayStyle):
    """Handles statistics display and formatting"""
    
    def __init__(self, data_manager):
        super().__init__(data_manager)
        
    @property
    def title_text(self):
        """Title for the statistics display"""
        return 'Stats'
    
    def create_content(self):
        """Creates the main content for statistics display"""
        stats = self.data_manager.get_weekly_stats()
        
        # Create content container
        content_container = BoxLayout(orientation='vertical', spacing=dp(10))
        
        # Header with statistics
        stats_header = self._create_stats_header(stats)
        
        # Additional information
        avg_daily = stats['avg_daily']
        extra_info = Label(
            text='[color=666666]Daily average: {} kcal[/color]'.format(int(avg_daily)),
            font_size=dp(14),
            size_hint_y=None,
            height=dp(30),
            markup=True
        )
        
        # Daily details with progress
        details_scroll = ScrollView()
        details_layout = BoxLayout(
            orientation='vertical',
            size_hint_y=None,
            spacing=dp(8)
        )
        details_layout.bind(minimum_height=details_layout.setter('height'))
        
        for day_data in stats['daily_data']:
            day_card = self._create_day_card(day_data)
            details_layout.add_widget(day_card)
        
        details_scroll.add_widget(details_layout)
        
        content_container.add_widget(stats_header)
        content_container.add_widget(extra_info)
        content_container.add_widget(details_scroll)
        
        return content_container
    
    def show_weekly_stats(self):
        """Displays beautiful weekly statistics using base display style"""
        self.show_display()
    
    def _create_stats_header(self, stats):
        """Creates the header section with main statistics"""
        stats_header = BoxLayout(
            orientation='vertical',
            size_hint_y=None,
            height=dp(90),
            spacing=dp(5)
        )
        
        # Main statistics with colors
        main_stats = BoxLayout(orientation='horizontal', size_hint_y=None, height=dp(80))
        
        # Consumed calories
        consumed_box = self._create_stat_box(
            'Consumed', 
            f'{stats["total_calories"]}', 
            'kcal', 
            Colors.GREEN
        )
        
        # Weekly target
        target_box = self._create_stat_box(
            'Target', 
            f'{stats["target_weekly"]}', 
            'kcal', 
            Colors.BLUE
        )
        
        # Progress percentage
        percent_color = UIUtils.get_color_based_on_progress(stats['weekly_percentage'])
        percent_status = 'TARGET' if stats['weekly_percentage'] >= 90 else 'GOOD' if stats['weekly_percentage'] >= 70 else 'LOW'
        
        percent_box = self._create_stat_box(
            'Progress', 
            f'{stats["weekly_percentage"]:.0f}%', 
            percent_status, 
            percent_color
        )
        
        main_stats.add_widget(consumed_box)
        main_stats.add_widget(target_box)
        main_stats.add_widget(percent_box)
        
        stats_header.add_widget(main_stats)
        
        return stats_header
    
    def _create_stat_box(self, title, value, unit, color):
        """Creates a statistics box widget"""
        box = BoxLayout(orientation='vertical', size_hint_x=0.33)
        
        title_label = Label(text=title, font_size=dp(12), color=Colors.GRAY)
        value_label = Label(
            text=value,
            font_size=dp(18),
            bold=True,
            color=color
        )
        unit_label = Label(
            text=f'[color={Colors.to_hex(color).replace("#", "")}]{unit}[/color]',
            font_size=dp(12),
            markup=True
        )
        
        box.add_widget(title_label)
        box.add_widget(value_label)
        box.add_widget(unit_label)
        
        return box
    
    def _create_day_card(self, day_data):
        """Creates a card for a single day in statistics"""
        card = BoxLayout(
            orientation='horizontal',
            size_hint_y=None,
            height=dp(60),
            padding=dp(15),
            spacing=dp(15)
        )
        
        # Card background with color based on goal achievement
        goal_percentage = day_data['progress_percentage']
        bg_color = UIUtils.get_background_color_based_on_progress(goal_percentage)
        progress_color = UIUtils.get_color_based_on_progress(goal_percentage)
        
        # Use base class method to create card background
        self.create_card_background(card, bg_color)
        
        # Date
        day_name = day_data['date'].strftime('%a')  # Day abbreviation
        day_date = day_data['date'].strftime('%d.%m')
        
        date_layout = BoxLayout(orientation='vertical', size_hint_x=0.25)
        date_layout.add_widget(Label(
            text=day_name,
            font_size=dp(12),
            bold=True,
            color=Colors.GRAYER
        ))
        date_layout.add_widget(Label(
            text=day_date,
            font_size=dp(10),
            color=Colors.GRAY,
        ))
        
        # Meal and calorie information
        info_layout = BoxLayout(orientation='vertical', size_hint_x=0.5)
        info_layout.add_widget(Label(
            text='{} kcal'.format(day_data['calories']),
            font_size=dp(16),
            bold=True,
            color=progress_color,
            halign='left'
        ))
        
        meals_text = '{} meals'.format(day_data['meals_count']) if day_data['meals_count'] != 1 else '1 meal'
        info_layout.add_widget(Label(
            text=meals_text,
            font_size=dp(12),
            color=Colors.GRAY,
            halign='left'
        ))
        
        # Achievement percentage
        percent_label = Label(
            text='{}%'.format(int(goal_percentage)),
            font_size=dp(14),
            bold=True,
            color=progress_color,
            size_hint_x=0.25
        )
        
        card.add_widget(date_layout)
        card.add_widget(info_layout)
        card.add_widget(percent_label)
        
        return card
