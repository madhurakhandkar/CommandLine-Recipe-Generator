from config import DIET_OPTIONS, DIET_MAP
from api import get_recipes
from display import display_welcome, display_menu, display_recipes, gather_search_filters, select_diet
from favourites import display_favourites


def search_flow():
    """Run the full recipe search flow."""
    diet = select_diet(DIET_OPTIONS, DIET_MAP)
    filters = gather_search_filters()

    print("\nSearching for recipes, please wait...")

    recipes = get_recipes(
        query=filters["query"],
        cuisine=filters["cuisine"],
        diet=diet,
        include_ingredients=filters["include_ingredients"],
        exclude_ingredients=filters["exclude_ingredients"],
        max_ready_time=filters["max_ready_time"],
    )

    if recipes:
        display_recipes(recipes, show_instructions=filters["show_instructions"])
    else:
        print("\n  No recipes found with those filters. Try adjusting your search.")


def main():
    display_welcome()

    while True:
        display_menu()
        choice = input("Enter your choice (1/2/3): ").strip()

        if choice == "1":
            search_flow()
        elif choice == "2":
            display_favourites()
        elif choice == "3":
            print("\nThanks for using CommandLine Recipe Generator. Happy cooking!\n")
            break
        else:
            print("  Invalid choice. Please enter 1, 2, or 3.")


if __name__ == "__main__":
    main()
