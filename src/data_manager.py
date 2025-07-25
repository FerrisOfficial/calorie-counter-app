"""
Data management for the Calorie Counter app
Handles storing and retrieving meal data
"""

from kivy.storage.jsonstore import JsonStore
from datetime import datetime, timedelta


class CalorieDataManager:
    """Manages calorie data storage and retrieval"""
    
    def __init__(self, filename='calorie_data.json'):
        self.store = JsonStore(filename)
        self.daily_target = 2000  # Default daily target
        
    def get_today_string(self):
        """Returns today's date as string"""
        return datetime.now().strftime('%Y-%m-%d')
    
    def add_meal(self, name, calories, date=None):
        """Adds a new meal to the specified date (or today)"""
        if date is None:
            date = self.get_today_string()
            
        # Validate input
        if not name or not isinstance(calories, int) or calories <= 0:
            raise ValueError("Invalid meal data")
            
        # Initialize day if it doesn't exist
        if not self.store.exists(date):
            self.store.put(date, meals=[])
        
        # Get existing meals
        meals = self.store.get(date)['meals']
        
        # Create new meal
        meal = {
            'name': name,
            'calories': calories,
            'time': datetime.now().strftime('%H:%M')
        }
        
        # Add to meals list
        meals.append(meal)
        self.store.put(date, meals=meals)
        
        return meal
    
    def get_meals_for_date(self, date):
        """Returns list of meals for specific date"""
        if self.store.exists(date):
            return self.store.get(date)['meals']
        return []
    
    def get_today_meals(self):
        """Returns today's meals"""
        return self.get_meals_for_date(self.get_today_string())
    
    def delete_meal(self, meal_index, date=None):
        """Deletes meal at specified index for given date"""
        if date is None:
            date = self.get_today_string()
            
        if not self.store.exists(date):
            return False
            
        meals = self.store.get(date)['meals']
        
        if 0 <= meal_index < len(meals):
            deleted_meal = meals.pop(meal_index)
            self.store.put(date, meals=meals)
            return deleted_meal
        
        return False
    
    def clear_all_meals(self, date=None):
        """Clears all meals for specified date"""
        if date is None:
            date = self.get_today_string()
            
        self.store.put(date, meals=[])
    
    def get_daily_calories(self, date=None):
        """Returns total calories consumed for specified date"""
        if date is None:
            date = self.get_today_string()
            
        meals = self.get_meals_for_date(date)
        return sum(meal['calories'] for meal in meals)
    
    def get_weekly_stats(self):
        """Returns weekly statistics for the last 7 days"""
        today = datetime.now()
        weekly_data = []
        total_calories = 0
        
        for i in range(7):
            day = today - timedelta(days=i)
            day_str = day.strftime('%Y-%m-%d')
            
            meals = self.get_meals_for_date(day_str)
            daily_calories = sum(meal['calories'] for meal in meals)
            total_calories += daily_calories
            
            weekly_data.append({
                'date': day,
                'date_str': day_str,
                'calories': daily_calories,
                'meals_count': len(meals),
                'progress_percentage': (daily_calories / self.daily_target * 100) if self.daily_target > 0 else 0
            })
        
        target_weekly = 7 * self.daily_target
        weekly_percentage = (total_calories / target_weekly * 100) if target_weekly > 0 else 0
        avg_daily = total_calories / 7
        
        return {
            'daily_data': list(reversed(weekly_data)),  # Oldest to newest
            'total_calories': total_calories,
            'target_weekly': target_weekly,
            'weekly_percentage': weekly_percentage,
            'avg_daily': avg_daily
        }
    
    def set_daily_target(self, target):
        """Sets daily calorie target"""
        if target > 0:
            self.daily_target = target
    
    def get_daily_target(self):
        """Returns daily calorie target"""
        return self.daily_target
