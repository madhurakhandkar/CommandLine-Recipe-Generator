import requests

API_KEY = 'e2620fe78e704f7b9cf5350182e2e7c7'

def get_recipes(query, cuisine, diet, includeIngredients):
    url = "https://api.spoonacular.com/recipes/complexSearch"
    params = {
        'apiKey': API_KEY,
        'cuisine': cuisine,
        'includeIngredients': includeIngredients,
        'query': query,
        'diet': diet,
        'number': 5  # Number of recipes to fetch
    }
    response = requests.get(url, params=params)
    data = response.json()
    return data.get('results', [])

def get_recipe_instructions(recipe_id):
    url = f"https://api.spoonacular.com/recipes/{recipe_id}/information"
    params = {
        'apiKey': API_KEY,
        'includeNutrition': False
    }
    response = requests.get(url, params=params)
    data = response.json()
    return data.get('instructions', "No instructions available.")

def display_recipes(recipes, show_instructions=False):
    for i, recipe in enumerate(recipes, start=1):
        print(f"{i}. {recipe['title']}")
        if show_instructions:
            instructions = get_recipe_instructions(recipe['id'])
            print("Instructions:")
            print(instructions)
            print()

def display_welcome():
    print("Welcome to your personalized recipe maker!")
    print()
    print("Please select below what diet you follow.")

def show(dietOptions):
    for index, diet in enumerate(dietOptions, start=1):
        print(f"{index}. {diet}")
    print()

def confirm_selection(diet):
    while True:
        confirmation = input(f"You selected {diet}. Are you sure? (yes/no): ").strip().lower()
        print()
        print("Right now it will print about 5 recipes by default, to change that edit the number under get_recipes")
        if confirmation in ("y", "yes"):
            query = input("Enter the MAIN ingredient or dish you want to include in your recipe search (leave blank if you don't want any): ").strip()
            includeIngredients = input("Enter specific ingredients to include (comma-separated, leave blank if you don't want any): ").strip()
            cuisine = input("Enter a specific cuisine you want to include in your recipe search (leave blank if you don't want any): ").strip()
            show_instructions = input("Enter 'true' if you want instructions for the recipe provided or enter 'false' if you don't: ").strip().lower() == 'true'
            print("Great! Gathering the best recipes for you")
            recipes = get_recipes(query, cuisine, diet, includeIngredients)
            if recipes:
                display_recipes(recipes, show_instructions)
            else:
                print("Sorry no recipes were found :'(. Try again with different items.")
            return True
        elif confirmation in ("n", "no"):
            print("Alright, please select your diet again.")
            return False
        else:
            print("Invalid input. Please respond with 'yes' or 'no'.")

def main():
    display_welcome()
    dietOptions = ["Vegetarian", "Vegan", "Non-Vegetarian"]
    show(dietOptions)
    
    dietMap = {
        "1": "Vegetarian",
        "2": "Vegan",
        "3": "Non-Vegetarian",
        "vegetarian": "Vegetarian",
        "vegan": "Vegan",
        "non-vegetarian": "Non-Vegetarian",
        "non-veg": "Non-Vegetarian"
    }
    
    while True:
        userInput = input("Input your diet (Vegetarian/Vegan/Non-Vegetarian): ").strip().lower()
        selectedDiet = dietMap.get(userInput)
        
        if selectedDiet:
            if confirm_selection(selectedDiet):
                break
            else:
                display_welcome()
                show(dietOptions)
        else:
            print("Invalid input. Please enter a valid diet option.")
            show(dietOptions)

if __name__ == "__main__":
    main()
