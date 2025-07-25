from backend.utils.config import DIET_API_KEY,EXERCISE_API_KEY
import random
import requests
from langchain_core.tools import tool
from typing import Annotated



class FitnessData:

    def __init__(self):
        self.base_url = "https://api.api-ninjas.com/v1/exercises"
        self.api_key = EXERCISE_API_KEY
       
    
    def get_muscle_groups_and_types(self):
     
        muscle_targets = {
                'full_body': ["abdominals", "biceps", "calves", "chest", "forearms", "glutes",
                    "hamstrings", "lower_back", "middle_back", "quadriceps",
                    "traps", "triceps", "adductors"
                    ],
                'upper_body': ["biceps", "chest", "forearms", "lats", "lower_back", "middle_back", "neck", "traps", "triceps" ],
                'lower_body': ["adductors", "calves", "glutes", "hamstrings", "quadriceps"]
            }
        exercise_types = {'types':["powerlifting","strength", "stretching", "strongman"]}

        return muscle_targets, exercise_types


    def fetch_exercises(self, type, muscle, difficulty):
        headers = {
            'X-Api-Key':self.api_key
        }
        params= {
            'type': type,
            'muscle': muscle,
            'difficulty': difficulty
            }
        try:
            response = requests.get(self.base_url, headers=headers,params=params)
            result = response.json()
            if not result:
                print(f"No exercises found for {muscle}")
            return result
        except requests.RequestException as e:
            print(f"Request failed: {e}")
            return []
        
       

    def generate_workout_plan(self, query='full_body', difficulty='intermediate'):
        output=[]
        muscle_targets, exercise_types = self.get_muscle_groups_and_types()
        muscle = random.choice(muscle_targets.get(query))
        type = random.choice(exercise_types.get('types'))
        result = self.fetch_exercises('stretching', muscle, difficulty)
        print(result)
        limit_plan = result[:3]
        for i, data in enumerate(limit_plan):
            if data not in output:
                output.append(f"Exercise {i+1}: {data['name']}")
                output.append(f"Muscle: {data['muscle']}")
                output.append(f"Instructions: {data['instructions']}")
              
        return output
    
@tool
def fitness_data_tool(query: Annotated[str, "This input will either be full_body, upper_body \
                                        or lower_body exercise plan"]):
    """use this tool to get fitness or workout plan for a user.
    The workout name provided serves as your input  \
                                        """
    fitness_tool = FitnessData()
    result = fitness_tool.generate_workout_plan(query)

    return result