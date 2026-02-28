from api import get_recipe_instructions
from favourites import add_favourite

DIVIDER = "-" * 50


def display_welcome():
    print("\n" + "=" * 50)
    print("   Welcome to CommandLine Recipe Generator!")
    print("=" * 50)
    print("Find recipes based on your diet, ingredients,")
    print("cuisine preferences, and more.\n")


def display_menu():
    print("\nWhat would you like to do?")
    print("  1. Search for recipes")
    print("  2. View favourite recipes")
    print("  3. Quit")
    print()


def show_options(options, title="Options"):
    print(f"\n{title}:")
    for i, option in enumerate(options, start=1):
        print(f"  {i}. {option}")
    print()


def prompt_optional(label):
    """Prompt for an optional input, returning empty string if skipped."""
    return input(f"{label} (press Enter to skip): ").strip()


def gather_search_filters():
    """Collect all search filters from the user."""
    print(f"\n{DIVIDER}")
    print("Let's narrow down your search.\n")

    query = prompt_optional("Main ingredient or dish you're looking for")
    include_ingredients = prompt_optional("Ingredients to include (comma-separated)")
    exclude_ingredients = prompt_optional("Ingredients to exclude (comma-separated)")
    cuisine = prompt_optional("Preferred cuisine (e.g. Italian, Mexican, Thai)")

    max_time = prompt_optional("Max cooking time in minutes")
    max_ready_time = int(max_time) if max_time.isdigit() else None

    show_instructions = input("\nShow full instructions for each recipe? (yes/no): ").strip().lower()
    show_instructions = show_instructions in ("yes", "y")

    return {
        "query": query,
        "include_ingredients": include_ingredients,
        "exclude_ingredients": exclude_ingredients,
        "cuisine": cuisine,
        "max_ready_time": max_ready_time,
        "show_instructions": show_instructions,
    }


def display_recipe(index, recipe, show_instructions=False):
    """Print a single recipe with optional instructions."""
    print(f"\n{DIVIDER}")
    print(f"  {index}. {recipe['title']}")

    if show_instructions:
        details = get_recipe_instructions(recipe["id"])
        if details["ready_in"]:
            print(f"     Ready in: {details['ready_in']} minutes | Servings: {details['servings']}")
        print(f"\n  Instructions:\n")
        # Strip HTML tags simply if present
        instructions = details["instructions"]
        import re
        instructions = re.sub(r"<[^>]+>", "", instructions)
        print(f"  {instructions}")
        if details["source_url"]:
            print(f"\n  Full recipe: {details['source_url']}")


def display_recipes(recipes, show_instructions=False):
    """Display all recipes and offer save-to-favourites option."""
    print(f"\n{'=' * 50}")
    print(f"  Found {len(recipes)} recipe(s):")

    for i, recipe in enumerate(recipes, start=1):
        display_recipe(i, recipe, show_instructions)

    print(f"\n{DIVIDER}")
    save_prompt = input("\nWould you like to save any recipe to favourites? Enter the number(s) (e.g. 1,3) or press Enter to skip: ").strip()

    if save_prompt:
        selections = [s.strip() for s in save_prompt.split(",")]
        for sel in selections:
            if sel.isdigit():
                index = int(sel) - 1
                if 0 <= index < len(recipes):
                    add_favourite(recipes[index])
                else:
                    print(f"  No recipe at position {sel}.")
            else:
                print(f"  '{sel}' is not a valid number.")


def select_diet(diet_options, diet_map):
    """Handle diet selection loop."""
    show_options(diet_options, title="Select your diet")

    while True:
        user_input = input("Enter diet name or number: ").strip().lower()
        selected = diet_map.get(user_input)

        if selected:
            confirm = input(f"\nYou selected '{selected}'. Confirm? (yes/no): ").strip().lower()
            if confirm in ("yes", "y"):
                return selected
            else:
                print("No problem, let's pick again.")
                show_options(diet_options, title="Select your diet")
        else:
            print("  Invalid option. Please try again.")
            show_options(diet_options, title="Select your diet")