"""
Meal management logic for the Calorie Counter app
"""

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.graphics import Color, RoundedRectangle
from kivy.utils import get_color_from_hex
from kivy.metrics import dp

from src.MealManager.MealCard.MealCard import MealCard
from src.UIUtils import UIUtils


class MealManager:
    """Handles all meal-related operations and display logic"""
    
    def __init__(self, data_manager, meals_layout, meal_name_input, calories_input, update_daily_info_callback):
        self.data_manager = data_manager
        self.meals_layout = meals_layout
        self.meal_name_input = meal_name_input
        self.calories_input = calories_input
        self.update_daily_info_callback = update_daily_info_callback
    
    def add_meal(self, instance):
        """Adds a new meal"""
        meal_name = self.meal_name_input.text.strip()
        calories_text = self.calories_input.text.strip()
        
        if not meal_name or not calories_text:
            UIUtils.show_popup('Error', 'Please fill in all fields!')
            return
            
        try:
            calories = int(calories_text)
            if calories <= 0:
                raise ValueError("Calories must be greater than 0")
        except ValueError:
            UIUtils.show_popup('Error', 'Please enter a valid number of calories!')
            return
        
        try:
            # Add meal using data manager
            meal = self.data_manager.add_meal(meal_name, calories)
            
            # Clear input fields
            self.meal_name_input.text = ''
            self.calories_input.text = ''
            
            # Refresh display
            self.load_today_meals()
            self.update_daily_info_callback()
            
            UIUtils.show_popup('Success', f'Added meal: {meal_name} ({calories} kcal)')
            
        except ValueError as e:
            UIUtils.show_popup('Error', str(e))
    
    def load_today_meals(self):
        """Loads and displays today's meals as beautiful cards"""
        self.meals_layout.clear_widgets()
        
        meals = self.data_manager.get_today_meals()
        
        if not meals:
            # Message when no meals
            empty_card = self._create_empty_meals_card()
            self.meals_layout.add_widget(empty_card)
        else:
            for i, meal in enumerate(meals):
                # Use inner function to properly close the index
                def create_meal_card(index, meal_data):
                    meal_card = MealCard(
                        meal_data=meal_data,
                        delete_callback=lambda x: self.delete_meal(index)
                    )
                    return meal_card
                
                meal_card = create_meal_card(i, meal)
                self.meals_layout.add_widget(meal_card)
    
    def _create_empty_meals_card(self):
        """Creates empty meals message card"""
        empty_card = BoxLayout(
            orientation='vertical',
            size_hint_y=None,
            height=dp(80),
            padding=dp(20)
        )
        
        with empty_card.canvas.before:
            Color(*get_color_from_hex('#F5F5F5'))
            empty_rect = RoundedRectangle(
                pos=empty_card.pos, 
                size=empty_card.size, 
                radius=[dp(15)]
            )
        empty_card.bind(
            size=lambda x, *args: setattr(empty_rect, 'size', x.size),
            pos=lambda x, *args: setattr(empty_rect, 'pos', x.pos)
        )
        
        empty_label = Label(
            text='[color=999999]No meals for today\nAdd your first meal![/color]',
            font_size=dp(14),
            halign='center',
            markup=True
        )
        empty_label.bind(size=empty_label.setter('text_size'))
        
        empty_card.add_widget(empty_label)
        return empty_card
    
    def clear_all_meals(self, instance):
        """Deletes all meals from today"""
        def confirm_clear():
            self.data_manager.clear_all_meals()
            self.load_today_meals()
            self.update_daily_info_callback()
        
        UIUtils.show_popup(
            'Confirmation', 
            'Are you sure you want to delete\nall today\'s meals?',
            size_hint=(0.8, 0.4),
            confirm_callback=confirm_clear,
            confirm_text='Delete all',
            cancel_text='Cancel'
        )
    
    def delete_meal(self, meal_index):
        """Deletes meal from list with confirmation"""
        meals = self.data_manager.get_today_meals()
        
        if 0 <= meal_index < len(meals):
            meal_to_delete = meals[meal_index]
            
            def confirm_delete():
                deleted_meal = self.data_manager.delete_meal(meal_index)
                if deleted_meal:
                    self.load_today_meals()
                    self.update_daily_info_callback()
            
            UIUtils.show_popup(
                'Confirmation',
                f'Are you sure you want to delete meal:\n"{meal_to_delete["name"]}" ({meal_to_delete["calories"]} kcal)?',
                size_hint=(0.8, 0.4),
                confirm_callback=confirm_delete,
                confirm_text='YES - Delete',
                cancel_text='Cancel'
            )
