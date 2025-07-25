import requests
import random
from backend.utils.config import DIET_API_KEY
from langchain_core.tools import tool
from typing import Annotated

class Dietitian:

    def __init__(self):
        self.base_url = "https://api.spoonacular.com"
        self.api_key = DIET_API_KEY
    
    def fetch_meal(self, time_frame="day", diet="None"):

        url = f"{self.base_url}/mealplanner/generate"
        params = {
            "timeFrame":time_frame,
            "diet": diet,
            "apiKey":self.api_key
        }

        response = requests.get(url, params=params)
        if not response:
            print('Meal Plan not found')
        return response.json()
    
    def get_recipe_information(self, recipe_id):

        url = f"{self.base_url}/recipes/{recipe_id}/information"
        params = {"apiKey": self.api_key}
        response = requests.get(url, params=params)
        if not response:
            print("Recipe not found")
        return response.json()


    def generate_meal_plan(self, query):
        meals_processed = []
        meal_plan = self.fetch_meal(query)
        print(meal_plan)
        
        meals = meal_plan.get('meals')
        nutrients = meal_plan.get('nutrients')

        for i, meal in enumerate(meals):
            recipe_info = self.get_recipe_information(meal.get('id'))
            ingredients = [ingredient['original'] for ingredient in recipe_info.get('extendedIngredients')]

            meals_processed.append(f"🍽️ Meal {i+1}: {meal.get('title')}")
            meals_processed.append(f"Prep Time: {meal.get('readyInMinutes')}")
            meals_processed.append(f"Servings: {meal.get('servings')}")
            
    
            meals_processed.append("📝 Ingredients:\n" + "\n".join(ingredients))
            meals_processed.append(f"📋 Instructions:\n {recipe_info.get('instructions')}")
            

        
        meals_processed.append( 
        "\n🔢 Daily Nutrients:\n"
        f"Protein: {nutrients.get('protein', 'N/A')} kcal\n"
        f"Fat: {nutrients.get('fat', 'N/A')} g\n"
        f"Carbohydrates: {nutrients.get('carbohydrates', 'N/A')} g"
        )


        return meals_processed
    
@tool
def diet_tool(query: Annotated[str, "This input will either be None, vegetarian, and vegan"]):
    """use this tool to get diet plan for the user.
    The diet type provided serves as your input  \
                                        """
    dietitian_tool = Dietitian()
    result = dietitian_tool.generate_meal_plan(query)

    return result