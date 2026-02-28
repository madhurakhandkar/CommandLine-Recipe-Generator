import requests
from config import API_KEY, DEFAULT_RECIPE_COUNT

BASE_URL = "https://api.spoonacular.com"


def get_recipes(query, cuisine, diet, include_ingredients, exclude_ingredients="", max_ready_time=None):
    """Search for recipes using the Spoonacular complex search endpoint."""
    url = f"{BASE_URL}/recipes/complexSearch"

    # Non-Vegetarian is not a Spoonacular diet — just omit it
    spoonacular_diet = diet if diet != "Non-Vegetarian" else ""

    params = {
        "apiKey": API_KEY,
        "query": query,
        "cuisine": cuisine,
        "diet": spoonacular_diet,
        "includeIngredients": include_ingredients,
        "excludeIngredients": exclude_ingredients,
        "number": DEFAULT_RECIPE_COUNT,
    }

    if max_ready_time:
        params["maxReadyTime"] = max_ready_time

    # Remove empty params to keep the request clean
    params = {k: v for k, v in params.items() if v != "" and v is not None}

    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        return data.get("results", [])
    except requests.exceptions.ConnectionError:
        print("\n[Error] No internet connection. Please check your network and try again.")
    except requests.exceptions.Timeout:
        print("\n[Error] The request timed out. Spoonacular may be slow — try again shortly.")
    except requests.exceptions.HTTPError as e:
        if response.status_code == 401:
            print("\n[Error] Invalid API key. Check your .env file.")
        elif response.status_code == 402:
            print("\n[Error] You've hit your Spoonacular API quota for today.")
        else:
            print(f"\n[Error] HTTP error occurred: {e}")
    except Exception as e:
        print(f"\n[Error] Something unexpected happened: {e}")

    return []


def get_recipe_instructions(recipe_id):
    """Fetch full recipe details including instructions."""
    url = f"{BASE_URL}/recipes/{recipe_id}/information"
    params = {
        "apiKey": API_KEY,
        "includeNutrition": False,
    }

    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        return {
            "instructions": data.get("instructions") or "No instructions available.",
            "ready_in": data.get("readyInMinutes"),
            "servings": data.get("servings"),
            "source_url": data.get("sourceUrl", ""),
        }
    except requests.exceptions.ConnectionError:
        print("\n[Error] No internet connection.")
    except requests.exceptions.Timeout:
        print("\n[Error] Request timed out fetching instructions.")
    except requests.exceptions.HTTPError as e:
        print(f"\n[Error] Could not fetch instructions: {e}")
    except Exception as e:
        print(f"\n[Error] Unexpected error: {e}")

    return {"instructions": "Could not retrieve instructions.", "ready_in": None, "servings": None, "source_url": ""}