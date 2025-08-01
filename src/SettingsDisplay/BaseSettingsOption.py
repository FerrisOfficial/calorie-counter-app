from kivy.uix.boxlayout import BoxLayout
from kivy.metrics import dp

from src.Styled.StyledLabel import StyledLabel
from src.Styled.StyledButton import StyledButton


class BaseSettingsOption(BoxLayout):
    """
    Bazowa klasa dla opcji w ustawieniach.
    Zawiera strukturę: tytuł opcji, pole z wartością, przycisk akcji.
    """

    def __init__(self, option_title="", **kwargs):
        super().__init__(orientation='vertical', size_hint_y=None, **kwargs)
        self.option_title = option_title
        self.bind(minimum_height=self.setter('height'))
        self.create_option_layout()

    def create_option_layout(self):
        """Tworzy podstawową strukturę opcji: tytuł + wartość + przycisk"""
        # Kontener dla tytułu opcji
        self.title_container = self.create_title_section()
        self.add_widget(self.title_container)

        # Kontener dla wartości i przycisku
        self.value_container = self.create_value_section()
        self.add_widget(self.value_container)

    def create_title_section(self):
        """Tworzy sekcję z tytułem opcji"""
        title_container = BoxLayout(
            size_hint_y=None,
            height=dp(40),
            padding=[dp(8), dp(8)],
            orientation='vertical'
        )
        
        self.title_label = StyledLabel(
            text=self.option_title,
            halign='center',
            valign='middle',
            size_hint_y=None,
            height=dp(24)
        )
        title_container.add_widget(self.title_label)
        return title_container

    def create_value_section(self):
        """Tworzy sekcję z polem wartości i przyciskiem"""
        value_container = BoxLayout(
            orientation='horizontal',
            size_hint_y=None,
            height=dp(40),
            spacing=dp(10)
        )

        # Pole z aktualną wartością (implementowane w klasie pochodnej)
        self.value_display = self.create_value_display()
        value_container.add_widget(self.value_display)

        # Przycisk akcji (implementowany w klasie pochodnej)
        self.action_button = self.create_action_button()
        value_container.add_widget(self.action_button)

        return value_container

    def create_value_display(self):
        """
        Tworzy widget wyświetlający aktualną wartość opcji.
        Powinno być nadpisane w klasie pochodnej.
        """
        raise NotImplementedError("Subclass must implement create_value_display")

    def create_action_button(self):
        """
        Tworzy przycisk akcji dla opcji.
        Powinno być nadpisane w klasie pochodnej.
        """
        raise NotImplementedError("Subclass must implement create_action_button")

    def get_option_value(self):
        """
        Zwraca aktualną wartość opcji.
        Powinno być nadpisane w klasie pochodnej.
        """
        raise NotImplementedError("Subclass must implement get_option_value")

    def set_option_value(self, value):
        """
        Ustawia nową wartość opcji.
        Powinno być nadpisane w klasie pochodnej.
        """
        raise NotImplementedError("Subclass must implement set_option_value")

    def update_value_display(self):
        """
        Aktualizuje wyświetlaną wartość.
        Może być nadpisane w klasie pochodnej.
        """
        pass
