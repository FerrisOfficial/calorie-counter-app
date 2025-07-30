from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.spinner import Spinner
from kivy.metrics import dp

from src.Styled.BaseSettingsOption import BaseSettingsOption
from src.Styled.StyledButton import StyledButton
from src.Styled.StyledTextInput import StyledTextInput
from src.Styled.StyledLabel import StyledLabel
from src.Styled.BaseDisplayStyle import BaseDisplayStyle
from src.consts import Colors


class SetTargetOption(BaseSettingsOption, BaseDisplayStyle):
    """
    Opcja ustawienia celu kalorycznego (z ręcznym lub automatycznym obliczeniem).
    Korzysta ze wspólnego stylu popupów (BaseDisplayStyle).
    """

    def __init__(self, on_value_change=None, **kwargs):
        self.current_target = 2000
        self.on_value_change = on_value_change
        BaseSettingsOption.__init__(self, option_name="Target", **kwargs)
        BaseDisplayStyle.__init__(self)

    def create_option_content(self):
        self.option_label = self.create_option_label("Kcal Target")
        self.add_widget(self.option_label)

        value_container = BoxLayout(
            orientation='horizontal',
            size_hint_x=0.4,
            spacing=10
        )

        self.target_label = StyledLabel(
            text=f"{self.current_target}",
            size_hint_x=0.6,
            halign='center'
        )
        value_container.add_widget(self.target_label)

        self.set_button = StyledButton(
            text="Set",
            size_hint_x=0.4,
            height=dp(40),
            bg_color=Colors.ORANGE
        )
        self.set_button.bind(on_press=lambda *_: self.show_display())
        value_container.add_widget(self.set_button)

        self.add_widget(value_container)

    # === Właściwości z BaseDisplayStyle ===

    @property
    def title_text(self):
        return "Set Daily Calorie Target"

    @property
    def title_color(self):
        return Colors.ORANGE

    def create_content(self):
        return self.create_popup_content()

    # === Zawartość popupu ===

    def create_popup_content(self):
        from kivy.uix.scrollview import ScrollView

        scroll = ScrollView()

        main_layout = BoxLayout(
            orientation='vertical',
            spacing=15,
            padding=20,
            size_hint_y=None
        )
        main_layout.bind(minimum_height=main_layout.setter('height'))

        manual_section = self.create_manual_section()
        main_layout.add_widget(manual_section)

        separator = StyledLabel(
            text="OR",
            size_hint_y=None,
            height=dp(30),
            color=Colors.GRAY,
            halign='center',
            valign='middle'
        )
        main_layout.add_widget(separator)

        auto_section = self.create_auto_section()
        main_layout.add_widget(auto_section)

        scroll.add_widget(main_layout)

        root_layout = BoxLayout(orientation='vertical')
        root_layout.add_widget(scroll)

        button_layout = BoxLayout(
            orientation='horizontal',
            size_hint_y=None,
            height=dp(50),
            spacing=dp(10),
            padding=[dp(20), dp(10), dp(20), dp(10)]
        )

        cancel_btn = StyledButton(text="Cancel", bg_color=Colors.GRAY)
        cancel_btn.bind(on_press=self.dismiss_display)
        button_layout.add_widget(cancel_btn)

        save_btn = StyledButton(text="Save", bg_color=Colors.ORANGE)
        save_btn.bind(on_press=self.save_target)
        button_layout.add_widget(save_btn)

        root_layout.add_widget(button_layout)

        return root_layout

    # === Sekcje ===

    def create_manual_section(self):
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
        section = BoxLayout(
            orientation='vertical',
            size_hint_y=None,
            spacing=dp(10)
        )
        section.bind(minimum_height=section.setter('height'))

        form_layout = BoxLayout(orientation='vertical', spacing=dp(8), size_hint_y=None)
        form_layout.bind(minimum_height=form_layout.setter('height'))

        # Age
        age_row = self.create_form_row("Age:", "years")
        self.age_input = age_row['input']
        form_layout.add_widget(age_row['layout'])

        # Gender
        gender_row = BoxLayout(orientation='horizontal', size_hint_y=None, height=dp(40), spacing=dp(10))
        gender_row.add_widget(StyledLabel(text="Gender:", size_hint_x=0.35, height=dp(40)))
        self.gender_spinner = Spinner(
            text='Male',
            values=['Male', 'Female'],
            size_hint_x=0.45,
            height=dp(40)
        )
        gender_row.add_widget(self.gender_spinner)
        gender_row.add_widget(StyledLabel(text="", size_hint_x=0.2, height=dp(40)))
        form_layout.add_widget(gender_row)

        # Height
        height_row = self.create_form_row("Height:", "cm")
        self.height_input = height_row['input']
        form_layout.add_widget(height_row['layout'])

        # Weight
        weight_row = self.create_form_row("Weight:", "kg")
        self.weight_input = weight_row['input']
        form_layout.add_widget(weight_row['layout'])

        # Activity
        activity_row = BoxLayout(orientation='horizontal', size_hint_y=None, height=dp(40), spacing=dp(10))
        activity_row.add_widget(StyledLabel(text="Activity:", size_hint_x=0.35, height=dp(40)))
        self.activity_spinner = Spinner(
            text='Moderate',
            values=['Sedentary', 'Light', 'Moderate', 'Active', 'Very Active'],
            size_hint_x=0.45,
            height=dp(40)
        )
        activity_row.add_widget(self.activity_spinner)
        activity_row.add_widget(StyledLabel(text="", size_hint_x=0.2, height=dp(40)))
        form_layout.add_widget(activity_row)

        # Weight loss
        weight_loss_row = self.create_weight_loss_row("Loss:", "kg/week")
        self.weight_loss_input = weight_loss_row['input']
        self.weight_loss_input.text = "0.5"
        form_layout.add_widget(weight_loss_row['layout'])

        # Calculate button
        calculate_btn = StyledButton(text="Calculate Target", size_hint_y=None, height=dp(40), bg_color=Colors.BLUE)
        calculate_btn.bind(on_press=self.calculate_target)
        form_layout.add_widget(calculate_btn)

        # Result
        self.calculated_result = StyledLabel(
            text="Fill the form and click Calculate",
            size_hint_y=None,
            height=dp(50),
            halign='center',
            valign='middle'
        )
        form_layout.add_widget(self.calculated_result)

        section.add_widget(StyledLabel(
            text="Calculate Based on Personal Data",
            size_hint_y=None,
            height=dp(30),
            font_size='16sp',
            bold=True
        ))
        section.add_widget(form_layout)
        return section

    def create_form_row(self, label_text, unit_text):
        layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=dp(40), spacing=dp(10))
        layout.add_widget(StyledLabel(text=label_text, size_hint_x=0.35, height=dp(40)))
        input = StyledTextInput(input_filter='int', multiline=False, size_hint_x=0.45, height=dp(40), halign='center')
        layout.add_widget(input)
        layout.add_widget(StyledLabel(text=unit_text, size_hint_x=0.2, height=dp(40)))
        return {'layout': layout, 'input': input}

    def create_weight_loss_row(self, label_text, unit_text):
        layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=dp(40), spacing=dp(10))
        layout.add_widget(StyledLabel(text=label_text, size_hint_x=0.35, height=dp(40)))
        input = StyledTextInput(input_filter='float', multiline=False, size_hint_x=0.35, height=dp(40), halign='center')
        layout.add_widget(input)
        layout.add_widget(StyledLabel(text=unit_text, size_hint_x=0.3, height=dp(40)))
        return {'layout': layout, 'input': input}

    def calculate_target(self, instance):
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

            bmr = 10 * weight + 6.25 * height - 5 * age + (5 if gender == 'Male' else -161)
            activity_multipliers = {
                'Sedentary': 1.2,
                'Light': 1.375,
                'Moderate': 1.55,
                'Active': 1.725,
                'Very Active': 1.9
            }
            tdee = bmr * activity_multipliers[activity]
            daily_deficit = weight_loss_goal * 7700 / 7
            calculated_target = int(tdee - daily_deficit)
            min_calories = 1500 if gender == 'Male' else 1200

            if calculated_target < min_calories:
                self.calculated_result.text = f"Warning: Target too low! Minimum recommended: {min_calories} kcal/day"
                calculated_target = min_calories
            else:
                self.calculated_result.text = f"Calculated target: {calculated_target} kcal/day\n(For {weight_loss_goal} kg/week loss)"

            self.manual_input.text = str(calculated_target)

        except ValueError:
            self.calculated_result.text = "Please enter valid numbers"

    def save_target(self, instance):
        try:
            new_target = int(self.manual_input.text)
            if new_target > 0:
                self.current_target = new_target
                self.target_label.text = f"{self.current_target}"
                if self.on_value_change:
                    self.on_value_change(new_target)
                self.dismiss_display()
        except ValueError:
            pass

    def get_option_value(self):
        return self.current_target

    def set_option_value(self, value):
        if isinstance(value, (int, float)) and value > 0:
            self.current_target = int(value)
            self.target_label.text = f"{self.current_target} kcal"

    def apply_styling(self):
        pass