import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("SPOONACULAR_API_KEY")

if not API_KEY:
    raise EnvironmentError("Missing SPOONACULAR_API_KEY in your .env file. Please add it before running.")

DIET_OPTIONS = [
    "Vegetarian",
    "Vegan",
    "Gluten Free",
    "Ketogenic",
    "Paleo",
    "Whole30",
    "Pescetarian",
    "Non-Vegetarian"
]

DIET_MAP = {str(i + 1): diet for i, diet in enumerate(DIET_OPTIONS)}
DIET_MAP.update({diet.lower(): diet for diet in DIET_OPTIONS})
DIET_MAP["non-veg"] = "Non-Vegetarian"
DIET_MAP["keto"] = "Ketogenic"

DEFAULT_RECIPE_COUNT = 5
FAVOURITES_FILE = "favourites.json"