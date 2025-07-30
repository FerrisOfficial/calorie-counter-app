from abc import ABC, abstractmethod
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.factory import Factory
from src.consts import Colors


class BaseSettingsOptionMeta(type(BoxLayout), type(ABC)):
    """Metaclass to resolve conflict between Kivy and ABC metaclasses"""
    pass


class BaseSettingsOption(BoxLayout, ABC, metaclass=BaseSettingsOptionMeta):
    """
    Abstrakcyjna klasa bazowa dla wszystkich opcji w ustawieniach.
    Definiuje wspólny interfejs i styl dla opcji konfiguracyjnych.
    """
    
    def __init__(self, option_name: str, **kwargs):
        super().__init__(**kwargs)
        self.option_name = option_name
        self.setup_layout()
        self.apply_styling()
        self.create_option_content()
    
    def setup_layout(self):
        """Konfiguruje podstawowy layout opcji."""
        self.orientation = 'horizontal'
        self.spacing = 10
        self.size_hint_y = None
        self.height = 60
        self.padding = [15, 10]
    
    @abstractmethod
    def create_option_content(self):
        """
        Metoda abstrakcyjna do tworzenia zawartości opcji.
        Musi być zaimplementowana przez klasy dziedziczące.
        """
        pass
    
    @abstractmethod
    def get_option_value(self):
        """
        Metoda abstrakcyjna do pobierania wartości opcji.
        Musi być zaimplementowana przez klasy dziedziczące.
        """
        pass
    
    @abstractmethod
    def set_option_value(self, value):
        """
        Metoda abstrakcyjna do ustawiania wartości opcji.
        Musi być zaimplementowana przez klasy dziedziczące.
        """
        pass
    
    def create_option_label(self, text: str) -> Label:
        """Tworzy wystandaryzowaną etykietę dla opcji."""
        label = Label(
            text=text,
            size_hint_x=0.6,
            text_size=(None, None),
            halign='left',
            valign='middle',
            color=Colors.LIGHT_GRAY,  # Example background color
        )
        return label
    
    @abstractmethod
    def apply_styling(self):
        """
        Metoda abstrakcyjna do aplikowania stylowania opcji.
        Musi być zaimplementowana przez klasy dziedziczące.
        """
        pass
