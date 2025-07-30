"""
Settings display components for the Calorie Counter app
"""

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.metrics import dp

from src.Styled.BaseDisplayStyle import BaseDisplayStyle
from src.consts import Colors
from src.SettingsDisplay.SetTargetOption.SetTargetOption import SetTargetOption


class SettingsDisplay(BaseDisplayStyle):
    """Handles settings display using base display style"""
    
    def __init__(self, data_manager=None):
        super().__init__(data_manager)
        
    @property
    def title_text(self):
        """Title for the settings display"""
        return 'Settings'
    
    @property
    def title_color(self):
        """Color for the settings title"""
        return Colors.ORANGE
    
    @property
    def close_button_color(self):
        """Background color for the close button"""
        return Colors.ORANGE
    
    def create_content(self):
        """Creates the main content for settings display"""
        # Główny kontener z scrollview dla ustawień
        scroll = ScrollView()
        
        content_container = BoxLayout(
            orientation='vertical',
            spacing=dp(15),
            size_hint_y=None,
            padding=[dp(20), dp(10)]
        )
        content_container.bind(minimum_height=content_container.setter('height'))
        
        # Nagłówek sekcji
        settings_header = Label(
            text='Application Settings',
            font_size=dp(18),
            color=Colors.ORANGE,
            size_hint_y=None,
            height=dp(40),
            text_size=(None, None),
            halign='left',
            bold=True
        )
        content_container.add_widget(settings_header)
        
        # Opcja ustawienia celu kalorycznego
        self.target_option = SetTargetOption(on_value_change=self.on_target_changed)
        content_container.add_widget(self.target_option)
        
        # Separator dla przyszłych opcji
        separator = Label(
            text='',
            size_hint_y=None,
            height=dp(20)
        )
        content_container.add_widget(separator)
        
        # Placeholder dla przyszłych ustawień
        future_settings_label = Label(
            text='[color=666666]More settings coming soon:\n• Theme preferences\n• Data export options\n• Notification settings[/color]',
            font_size=dp(14),
            markup=True,
            size_hint_y=None,
            height=dp(100),
            text_size=(None, None),
            halign='left',
            valign='top'
        )
        content_container.add_widget(future_settings_label)
        
        scroll.add_widget(content_container)
        return scroll
    
    def show_settings(self):
        """Shows the settings display"""
        # Załaduj aktualne ustawienia przed pokazaniem
        self.load_current_settings()
        self.show_display()
    
    def load_current_settings(self):
        """Ładuje aktualne ustawienia z data managera"""
        if self.data_manager and hasattr(self, 'target_option'):
            # Pobierz aktualny cel kaloryczny z data managera
            current_target = self.data_manager.get_daily_target()
            if current_target:
                self.target_option.set_option_value(current_target)
    
    def on_target_changed(self, new_target):
        """Callback wywoływany gdy zmieni się cel kaloryczny"""
        if self.data_manager:
            self.data_manager.set_daily_target(new_target)
    
    def save_settings(self):
        """Zapisuje ustawienia do data managera"""
        if self.data_manager and hasattr(self, 'target_option'):
            # Zapisz cel kaloryczny
            target_value = self.target_option.get_option_value()
            self.data_manager.set_daily_target(target_value)
