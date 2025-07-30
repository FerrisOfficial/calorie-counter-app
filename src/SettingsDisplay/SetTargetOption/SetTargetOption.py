from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.spinner import Spinner
from kivy.uix.popup import Popup
from kivy.uix.scrollview import ScrollView
from kivy.metrics import dp
from src.Styled.BaseSettingsOption import BaseSettingsOption
from src.Styled.StyledButton import StyledButton
from src.Styled.StyledTextInput import StyledTextInput
from src.Styled.StyledLabel import StyledLabel
from src.consts import Colors


class SetTargetOption(BaseSettingsOption):
    """
    Opcja ustawienia celu kalorycznego - automatycznie na podstawie parametrów
    fizycznych lub ręcznie przez wprowadzenie wartości.
    """
    
    def __init__(self, on_value_change=None, **kwargs):
        self.current_target = 2000  # Domyślny cel kaloryczny
        self.popup = None
        self.on_value_change = on_value_change  # Callback dla zmiany wartości
        super().__init__(option_name="Target", **kwargs)
    
    def create_option_content(self):
        """Tworzy zawartość opcji ustawienia celu kalorycznego."""
        # Etykieta opcji
        self.option_label = self.create_option_label("Kcal Target")
        self.add_widget(self.option_label)
        
        # Kontener na wartość i przycisk
        value_container = BoxLayout(
            orientation='horizontal',
            size_hint_x=0.4,
            spacing=10
        )
        
        # Wyświetlanie aktualnej wartości
        self.target_label = StyledLabel(
            text=f"{self.current_target}",
            size_hint_x=0.6,
            halign='center'
        )
        value_container.add_widget(self.target_label)
        
        # Przycisk do otwierania okna ustawień
        self.set_button = StyledButton(
            text="Set",
            size_hint_x=0.4,
            height=dp(40),
            bg_color=Colors.ORANGE
        )
        self.set_button.bind(on_press=self.open_target_popup)
        value_container.add_widget(self.set_button)
        
        self.add_widget(value_container)
    
    def open_target_popup(self, instance):
        """Otwiera popup do ustawienia celu kalorycznego."""
        if self.popup:
            self.popup.dismiss()
        
        content = self.create_popup_content()
        
        self.popup = Popup(
            title="Set Daily Calorie Target",
            content=content,
            size_hint=(0.95, 0.9),
            auto_dismiss=False
        )
        # Ustaw styl tytułu popupu
        self.popup.title_font = 'Roboto'  # lub inna dostępna czcionka
        self.popup.title_size = 18
        self.popup.title_color = Colors.ORANGE
        self.popup.title_bold = True
        self.popup.open()
    
    def create_popup_content(self):
        """Tworzy zawartość popup'a z opcjami ustawienia celu."""
        # ScrollView dla głównej zawartości
        scroll = ScrollView()

        main_layout = BoxLayout(
            orientation='vertical',
            spacing=15,
            padding=20,
            size_hint_y=None
        )
        main_layout.bind(minimum_height=main_layout.setter('height'))

        # Sekcja 1: Ręczne ustawienie
        manual_section = self.create_manual_section()
        main_layout.add_widget(manual_section)

        # Separator
        separator = StyledLabel(
            text="OR",
            size_hint_y=None,
            height=dp(30),
            color=Colors.GRAY,
            text_size=(None, None),
            halign='center',
            valign='middle',
            bg_color='#00000000'  # Przezroczyste tło
        )
        main_layout.add_widget(separator)

        # Sekcja 2: Automatyczne obliczenie
        auto_section = self.create_auto_section()
        main_layout.add_widget(auto_section)

        scroll.add_widget(main_layout)

        # Główny kontener z przyciskami na dole
        root_layout = BoxLayout(
            orientation='vertical'
        )

        # Usunięto dodatkowy header
        root_layout.add_widget(scroll)

        # Przyciski akcji na dole
        button_layout = BoxLayout(
            orientation='horizontal',
            size_hint_y=None,
            height=dp(50),
            spacing=dp(10),
            padding=[dp(20), dp(10), dp(20), dp(10)]  # taki sam padding z góry i z dołu
        )

        cancel_btn = StyledButton(text="Cancel", bg_color=Colors.GRAY)
        cancel_btn.bind(on_press=self.close_popup)
        button_layout.add_widget(cancel_btn)

        save_btn = StyledButton(text="Save", bg_color=Colors.ORANGE)
        save_btn.bind(on_press=self.save_target)
        button_layout.add_widget(save_btn)

        root_layout.add_widget(button_layout)

        return root_layout
    
    def create_manual_section(self):
        """Tworzy sekcję ręcznego ustawienia celu."""
        section = BoxLayout(
            orientation='vertical',
            size_hint_y=None,
            height=dp(100),
            spacing=dp(10)
        )
        
        title = StyledLabel(
            text="Manual Target Setting",
            size_hint_y=None,
            height=dp(30),
            font_size='16sp',
            bold=True
        )
        section.add_widget(title)
        
        input_layout = BoxLayout(
            orientation='horizontal',
            size_hint_y=None,
            height=dp(40),
            spacing=dp(10)
        )
        
        input_layout.add_widget(StyledLabel(text="Target:", size_hint_x=0.3, height=dp(40)))
        
        self.manual_input = StyledTextInput(
            text=str(self.current_target),
            input_filter='int',
            multiline=False,
            size_hint_x=0.5,
            halign='center',
            height=dp(40)
        )
        input_layout.add_widget(self.manual_input)
        
        input_layout.add_widget(StyledLabel(text="kcal", size_hint_x=0.2, height=dp(40)))
        
        section.add_widget(input_layout)
        
        return section
    
    def create_auto_section(self):
        """Tworzy sekcję automatycznego obliczenia celu."""
        section = BoxLayout(
            orientation='vertical',
            size_hint_y=None,
            spacing=dp(10),
            padding=[0, 0, 0, 0]  # Dodany padding dla spójności
        )
        section.bind(minimum_height=section.setter('height'))
        
        title = StyledLabel(
            text="Calculate Based on Personal Data",
            size_hint_y=None,
            height=dp(30),
            font_size='16sp',
            bold=True,
            text_size=(None, None),
            halign='left',
            valign='middle'
        )
        section.add_widget(title)
        
        # Formularz z danymi osobowymi
        form_layout = BoxLayout(
            orientation='vertical',
            spacing=dp(8),
            size_hint_y=None
        )
        form_layout.bind(minimum_height=form_layout.setter('height'))
        
        # Wiek
        age_row = self.create_form_row("Age:", "years")
        self.age_input = age_row['input']
        form_layout.add_widget(age_row['layout'])
        
        # Płeć
        gender_row = BoxLayout(orientation='horizontal', size_hint_y=None, height=dp(40), spacing=dp(10))
        gender_label = StyledLabel(
            text="Gender:", 
            size_hint_x=0.35,  # Ujednolicone z 0.3 do 0.35
            size_hint_y=None,
            height=dp(40),
            text_size=(None, None),
            halign='left',
            valign='middle'
        )
        gender_row.add_widget(gender_label)
        
        self.gender_spinner = Spinner(
            text='Male',
            values=['Male', 'Female'],
            size_hint_x=0.45,  # Zmniejszone z 0.65 do 0.45 (tak jak pola tekstowe)
            size_hint_y=None,
            height=dp(40)
        )
        gender_row.add_widget(self.gender_spinner)
        
        # Puste miejsce dla wyrównania z innymi polami
        gender_spacer = StyledLabel(
            text="", 
            size_hint_x=0.2,  # Tak jak jednostki w innych polach
            size_hint_y=None,
            height=dp(40),
            bg_color='#00000000'  # Przezroczyste tło
        )
        gender_row.add_widget(gender_spacer)
        form_layout.add_widget(gender_row)
        
        # Wzrost
        height_row = self.create_form_row("Height:", "cm")
        self.height_input = height_row['input']
        form_layout.add_widget(height_row['layout'])
        
        # Waga
        weight_row = self.create_form_row("Weight:", "kg")
        self.weight_input = weight_row['input']
        form_layout.add_widget(weight_row['layout'])
        
        # Poziom aktywności
        activity_row = BoxLayout(orientation='horizontal', size_hint_y=None, height=dp(40), spacing=dp(10))
        activity_label = StyledLabel(
            text="Activity:", 
            size_hint_x=0.35,  # Ujednolicone z 0.3 do 0.35
            size_hint_y=None,
            height=dp(40),
            text_size=(None, None),
            halign='left',
            valign='middle'
        )
        activity_row.add_widget(activity_label)
        
        self.activity_spinner = Spinner(
            text='Moderate',
            values=['Sedentary', 'Light', 'Moderate', 'Active', 'Very Active'],
            size_hint_x=0.45,  # Zmniejszone z 0.65 do 0.45 (tak jak pola tekstowe)
            size_hint_y=None,
            height=dp(40)
        )
        activity_row.add_widget(self.activity_spinner)
        
        # Puste miejsce dla wyrównania z innymi polami
        activity_spacer = StyledLabel(
            text="", 
            size_hint_x=0.2,  # Tak jak jednostki w innych polach
            size_hint_y=None,
            height=dp(40),
            bg_color='#00000000'  # Przezroczyste tło
        )
        activity_row.add_widget(activity_spacer)
        form_layout.add_widget(activity_row)
        
        # Cel zrzucenia wagi
        weight_loss_row = self.create_weight_loss_row("Loss:", "kg/week")
        self.weight_loss_input = weight_loss_row['input']
        self.weight_loss_input.text = "0.5"  # Domyślna wartość 0.5 kg/tydzień
        form_layout.add_widget(weight_loss_row['layout'])
        
        # Przycisk oblicz
        calculate_btn = StyledButton(
            text="Calculate Target",
            size_hint_y=None,
            height=dp(40),
            bg_color=Colors.BLUE
        )
        calculate_btn.bind(on_press=self.calculate_target)
        form_layout.add_widget(calculate_btn)
        
        # Wynik obliczeń
        self.calculated_result = StyledLabel(
            text="Fill the form and click Calculate",
            size_hint_y=None,
            height=dp(50),  # Zwiększona wysokość dla większego tekstu
            text_size=(None, None),
            halign='center',
            valign='middle'
        )
        form_layout.add_widget(self.calculated_result)
        
        section.add_widget(form_layout)
        
        return section
    
    def create_form_row(self, label_text, unit_text):
        """Tworzy wiersz formularza z etykietą, polem tekstowym i jednostką."""
        row_layout = BoxLayout(
            orientation='horizontal',
            size_hint_y=None,
            height=dp(40),
            spacing=dp(10)
        )
        
        label = StyledLabel(
            text=label_text, 
            size_hint_x=0.35,  # Ujednolicone z 0.3 do 0.35
            size_hint_y=None,
            height=dp(40),
            text_size=(None, None),
            halign='left',
            valign='middle'
        )
        row_layout.add_widget(label)
        
        text_input = StyledTextInput(
            input_filter='int',
            multiline=False,
            size_hint_x=0.45,
            size_hint_y=None,
            height=dp(40),
            halign='center'
        )
        row_layout.add_widget(text_input)
        
        unit_label = StyledLabel(
            text=unit_text, 
            size_hint_x=0.2,  # Pozostaje 0.2
            size_hint_y=None,
            height=dp(40),
            text_size=(None, None),
            halign='left',
            valign='middle'
        )
        row_layout.add_widget(unit_label)
        
        return {'layout': row_layout, 'input': text_input}
    
    def create_weight_loss_row(self, label_text, unit_text):
        """Tworzy wiersz formularza dla celu zrzucenia wagi (akceptuje liczby dziesiętne)."""
        row_layout = BoxLayout(
            orientation='horizontal',
            size_hint_y=None,
            height=dp(40),
            spacing=dp(10)
        )
        
        label = StyledLabel(
            text=label_text, 
            size_hint_x=0.35,  # Zmienione z 0.4 do 0.35 dla ujednolicenia
            size_hint_y=None,
            height=dp(40),
            text_size=(None, None),
            halign='left',
            valign='middle'
        )
        row_layout.add_widget(label)
        
        text_input = StyledTextInput(
            input_filter='float',  # Akceptuje liczby dziesiętne
            multiline=False,
            size_hint_x=0.35,
            size_hint_y=None,
            height=dp(40),
            halign='center'
        )
        row_layout.add_widget(text_input)
        
        unit_label = StyledLabel(
            text=unit_text, 
            size_hint_x=0.3,  # Pozostaje 0.3
            size_hint_y=None,
            height=dp(40),
            text_size=(None, None),
            halign='left',
            valign='middle'
        )
        row_layout.add_widget(unit_label)
        
        return {'layout': row_layout, 'input': text_input}
    
    def calculate_target(self, instance):
        """Oblicza cel kaloryczny na podstawie wprowadzonych danych."""
        try:
            age = int(self.age_input.text or 0)
            height = int(self.height_input.text or 0)
            weight = int(self.weight_input.text or 0)
            weight_loss_goal = float(self.weight_loss_input.text or 0)
            gender = self.gender_spinner.text
            activity = self.activity_spinner.text
            
            if age <= 0 or height <= 0 or weight <= 0:
                self.calculated_result.text = "Please fill all fields with valid values"
                return
            
            # Obliczenie BMR (Basal Metabolic Rate) używając wzoru Mifflin-St Jeor
            if gender == 'Male':
                bmr = 10 * weight + 6.25 * height - 5 * age + 5
            else:
                bmr = 10 * weight + 6.25 * height - 5 * age - 161
            
            # Mnożniki dla poziomów aktywności
            activity_multipliers = {
                'Sedentary': 1.2,
                'Light': 1.375,
                'Moderate': 1.55,
                'Active': 1.725,
                'Very Active': 1.9
            }
            
            # Obliczenie TDEE (Total Daily Energy Expenditure)
            tdee = bmr * activity_multipliers[activity]
            
            # Obliczenie deficytu kalorycznego dla celu zrzucenia wagi
            # 1 kg tłuszczu = około 7700 kcal
            weekly_deficit = weight_loss_goal * 7700  # Całkowity deficyt na tydzień
            daily_deficit = weekly_deficit / 7  # Dzienny deficyt
            
            # Cel kaloryczny = TDEE - dzienny deficyt
            calculated_target = int(tdee - daily_deficit)
            
            # Sprawdzenie czy cel nie jest zbyt niski (minimum 1200 kcal dla kobiet, 1500 dla mężczyzn)
            min_calories = 1500 if gender == 'Male' else 1200
            if calculated_target < min_calories:
                self.calculated_result.text = f"Warning: Target too low! Minimum recommended: {min_calories} kcal/day"
                calculated_target = min_calories
            
            result_text = f"Calculated target: {calculated_target} kcal/day"
            if weight_loss_goal > 0:
                result_text += f"\n(For {weight_loss_goal} kg/week loss)"
            
            self.calculated_result.text = result_text
            self.manual_input.text = str(calculated_target)
            
        except ValueError:
            self.calculated_result.text = "Please enter valid numbers"
    
    def save_target(self, instance):
        """Zapisuje ustawiony cel kaloryczny."""
        try:
            new_target = int(self.manual_input.text)
            if new_target > 0:
                self.current_target = new_target
                self.target_label.text = f"{self.current_target}"
                
                # Powiadom o zmianie wartości
                if self.on_value_change:
                    self.on_value_change(new_target)
                    
                self.close_popup(instance)
            else:
                # Można dodać komunikat o błędzie
                pass
        except ValueError:
            # Można dodać komunikat o błędzie
            pass
    
    def close_popup(self, instance):
        """Zamyka popup."""
        if self.popup:
            self.popup.dismiss()
            self.popup = None
    
    def get_option_value(self):
        """Zwraca aktualną wartość celu kalorycznego."""
        return self.current_target
    
    def set_option_value(self, value):
        """Ustawia wartość celu kalorycznego."""
        if isinstance(value, (int, float)) and value > 0:
            self.current_target = int(value)
            self.target_label.text = f"{self.current_target} kcal"
    
    def apply_styling(self):
        """Aplikuje stylowanie zgodne z motywem aplikacji."""
        self.canvas.before.clear()
        with self.canvas.before:
            from kivy.graphics import Color, RoundedRectangle
            Color(*Colors.LIGHT_GRAY)
            RoundedRectangle(
                pos=self.pos,
                size=self.size,
                radius=[10]
            )
        
        self.bind(pos=self.update_graphics, size=self.update_graphics)
    
    def update_graphics(self, *args):
        """Aktualizuje grafikę po zmianie pozycji lub rozmiaru."""
        self.canvas.before.clear()
        with self.canvas.before:
            from kivy.graphics import Color, RoundedRectangle
            Color(*Colors.LIGHT_GRAY)
            RoundedRectangle(
                pos=self.pos,
                size=self.size,
                radius=[10]
            )
