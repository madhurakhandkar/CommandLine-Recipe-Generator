import json
import os
from config import FAVOURITES_FILE


def load_favourites():
    """Load favourites from the JSON file."""
    if not os.path.exists(FAVOURITES_FILE):
        return []
    try:
        with open(FAVOURITES_FILE, "r") as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError):
        print("[Warning] Could not read favourites file. Starting fresh.")
        return []


def save_favourites(favourites):
    """Write favourites list to the JSON file."""
    try:
        with open(FAVOURITES_FILE, "w") as f:
            json.dump(favourites, f, indent=2)
    except IOError as e:
        print(f"[Error] Could not save favourites: {e}")


def add_favourite(recipe):
    """Add a recipe to favourites if it's not already there."""
    favourites = load_favourites()
    if any(f["id"] == recipe["id"] for f in favourites):
        print(f"  '{recipe['title']}' is already in your favourites.")
        return
    favourites.append({"id": recipe["id"], "title": recipe["title"]})
    save_favourites(favourites)
    print(f"  ✓ '{recipe['title']}' saved to favourites!")


def remove_favourite(recipe_id):
    """Remove a recipe from favourites by ID."""
    favourites = load_favourites()
    updated = [f for f in favourites if f["id"] != recipe_id]
    if len(updated) == len(favourites):
        print("  Recipe not found in favourites.")
    else:
        save_favourites(updated)
        print("  ✓ Removed from favourites.")


def display_favourites():
    """Print all saved favourites."""
    favourites = load_favourites()
    if not favourites:
        print("\n  You have no saved favourites yet.")
        return

    print("\n--- Your Favourite Recipes ---")
    for i, recipe in enumerate(favourites, start=1):
        print(f"  {i}. {recipe['title']}  (ID: {recipe['id']})")
    print()

    while True:
        action = input("Enter a number to remove a favourite, or press Enter to go back: ").strip()
        if action == "":
            break
        if action.isdigit():
            index = int(action) - 1
            if 0 <= index < len(favourites):
                remove_favourite(favourites[index]["id"])
                display_favourites()
                return
            else:
                print("  Invalid number.")
        else:
            print("  Please enter a valid number or press Enter.")