"""
UI utility functions for the Calorie Counter app
"""

from kivy.uix.popup import Popup
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.utils import get_color_from_hex
from kivy.metrics import dp
from src.StyledButton import StyledButton
from src.consts import Colors


class UIUtils:
    """Utility functions for UI operations"""
    
    @staticmethod
    def show_popup(title, message, size_hint=(0.8, 0.6), confirm_callback=None, 
                   confirm_text='OK', cancel_text='Cancel'):
        """Displays stylized popup with message"""
        content = BoxLayout(orientation='vertical', padding=dp(20), spacing=dp(15))
        
        # Icon depending on message type
        if 'Success' in title or 'success' in title.lower():
            icon = 'OK'
            title_color = '#4CAF50'
        elif 'Error' in title or 'error' in title.lower():
            icon = 'ERROR'
            title_color = '#F44336'
        elif 'Confirmation' in title or confirm_callback:
            icon = 'WARNING'
            title_color = '#FF9800'
        else:
            icon = 'INFO'
            title_color = '#2196F3'
        
        # Title with icon
        title_label = Label(
            text='[color={}][b]{} {}[/b][/color]'.format(title_color.replace('#', ''), icon, title),
            font_size=dp(30),
            size_hint_y=None,
            height=dp(40),
            markup=True
        )
        
        # Message
        msg_label = Label(
            text=message,
            font_size=dp(25),
            color=get_color_from_hex("#898989"),
            text_size=(None, None),
            halign='center',
            valign='middle'
        )
        
        content.add_widget(title_label)
        content.add_widget(msg_label)
        
        # Buttons - one or two depending on whether there's a confirm_callback
        if confirm_callback:
            # Two buttons for confirmation
            buttons_layout = BoxLayout(orientation='horizontal', spacing=dp(10), size_hint_y=None, height=dp(50))
            
            cancel_btn = StyledButton(
                text=cancel_text,
                size_hint_y=None,
                height=dp(50),
                bg_color=title_color,
                font_size=dp(16),
                color=get_color_from_hex('#000000')
            )
            
            confirm_btn = StyledButton(
                text=confirm_text,
                size_hint_y=None,
                height=dp(50),
                bg_color=title_color,
                font_size=dp(16),
                color=get_color_from_hex('#000000')
            )
            
            buttons_layout.add_widget(cancel_btn)
            buttons_layout.add_widget(confirm_btn)
            content.add_widget(buttons_layout)
        else:
            # Single OK button
            close_btn = StyledButton(
                text='OK',
                size_hint_y=None,
                height=dp(50),
                bg_color=title_color,
                font_size=dp(16),
                color=get_color_from_hex('#000000')
            )
            content.add_widget(close_btn)
        
        popup = Popup(
            title='',
            content=content,
            size_hint=size_hint,
            separator_height=0,
            auto_dismiss=False if confirm_callback else True
        )
        
        if confirm_callback:
            def on_confirm(instance):
                popup.dismiss()
                confirm_callback()
            
            confirm_btn.bind(on_press=on_confirm)
            cancel_btn.bind(on_press=popup.dismiss)
        else:
            close_btn.bind(on_press=popup.dismiss)
        
        popup.open()
        return popup
    
    @staticmethod
    def get_color_based_on_progress(percentage):
        """Returns color based on progress percentage"""
        if percentage >= 90:
            return Colors.RED  
        elif percentage >= 70:
            return Colors.ORANGE  
        else:
            return Colors.GREEN

    @staticmethod
    def get_background_color_based_on_progress(percentage):
        """Returns background color based on progress percentage"""
        if percentage >= 90:
            return '#E8F5E8'  # Light green
        elif percentage >= 70:
            return '#FFF3E0'  # Light orange
        else:
            return '#FFEBEE'  # Light red
