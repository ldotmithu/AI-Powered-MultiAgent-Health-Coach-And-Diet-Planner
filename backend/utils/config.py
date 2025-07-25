from dotenv import load_dotenv
import os
load_dotenv()


GROQ_API_KEY = os.getenv("GROQ_API_KEY")
EXERCISE_API_KEY = os.getenv("EXERCISE_API_KEY")
DIET_API_KEY = os.getenv("DIET_API_KEY")

LLM_MODEL = "gemma2-9b-it"
TEMPERATURE = 0.3
