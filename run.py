# Your code goes here.
# You can delete these comments, but do not change the name of this file
# Write your code to expect a terminal of 80 characters wide and 24 rows high
import json
import difflib
from collections import Counter

def welcome_message():
    """
    Introduce user to the project
    """
    print("\nWelcome to the Family Shopping List")

def view_stock(stock_data):
    """
    When user wants to see current stock
    """
    print("\nCurrent Stock:")
    for item, info in stock_data.items():
        print(f"- {item}: {info['quantity']} {info['unit']}")

def main_menu():
    """
    Provide user with options to select how they will use the program
    """
    stock_data = load_stock()
    recipes_data = load_recipes()
    flat_recipes = flatten_recipes(recipes_data)
 
    while True:
        print("\nMain Menu")
        print("1. View Recipes")
        print("2. Edit Recipes")
        print("3. Generate Shopping List")
        print("4. View Stock")
        print("5. Edit Stock")
        print("6. Exit")

        choice = input("Enter your choice(1-6):")
        if choice == "1":
            view_recipes(flat_recipes)
        
        elif choice == "2":
            print("Edit Recipes not implemented yet.")

        elif choice == "3":
            while True:
                print("Would you like to plan meals for the weekend(2 days) or a full week (7 days)?")
                days_input = input("Enter your choice (2 or 7): ").strip()
                
                if days_input in ["2", "7"]:
                    number_of_days = int(days_input)
                    break  # valid input, so break out of the loop
                else:
                    print("Invalid input. Please enter 2 or 7.")

            meal_plan = get_meal_plan_from_user(flat_recipes)
            if not meal_plan:
                print("No valid meals entered. Returning to main menu.")
                continue 

            shopping_list = generate_shopping_list(meal_plan, flat_recipes, stock_data)
            print("\nShopping List:")
            for item, info in shopping_list.items():
                print(f"- {item}: {info['quantity']} {info['unit']}")

        elif choice == "4":
            view_stock(stock_data)

        elif choice == "5":
            while True:
                edit_stock(stock_data)

        elif choice == "6":
            print("Goodbye!")
            break
        else:
            print("Invalid input. Please enter 1, 2, 3, 4, 5 or 6.")


def load_stock():
    """
    Load stock from the json file so user has access to 
    what stock is available.
    """
    with open("stock.json", "r") as file:
        stock = json.load(file)
        return stock


def load_recipes():
    """
    Load recipes from the json file so they are ready to be 
    compared to the stock list.
    """
    with open("recipes.json", "r") as file:
        recipes = json.load(file)
        return recipes

def edit_stock(stock_data):
    """
    Allow the user to update or add items in the stock list, then save the changes.
    """
    while True:
        item_name = input("Enter the name of the item to update (or type 'done' to finish): ").strip().lower()
        
        if item_name == "done":
            break

        existing_item = get_existing_item_key(item_name, stock_data)

        if existing_item:
            item_name = existing_item
            print(f"{item_name} found in stock. Updating...")
        else:
            print(f"{item_name} not found. Adding as a new item.")


        try:
            quantity = float(input(f"Enter the quantity for '{item_name}': "))
            unit = input(f"Enter the unit for '{item_name}' (e.g., grams, packs, servings or pieces): ").strip().lower()
            stock_data[item_name.title()] = {"quantity": quantity, "unit": unit}
            print(f"Updated '{item_name.title()}' in stock.")
        except ValueError:
            print("Invalid quantity. Please enter a number.")

    # Save the updated stock data
    with open("stock.json", "w") as file:
        json.dump(stock_data, file, indent=4)

    print("Stock list updated and saved.")

def get_existing_item_key(user_input, stock_data):
    for item in stock_data:
        if item.lower() == user_input.lower():
            return item
    return None


def flatten_recipes(recipes_data):
    """
    Condense nested recipe categories into a single dictionary.
    """
    flat_recipes = {}
    for category in recipes_data.values():
        flat_recipes.update(category)
    return flat_recipes

def view_recipes(flat_recipes):
    print("\nAvailable Recipes:")
    for recipe_name in flat_recipes:
        print(f"- {recipe_name}")
    
def get_closest_match(user_input, recipe_names, cutoff=0.5):
    """
    Allow user to make small mistakes when inputting their meal plan
    """
    matches = difflib.get_close_matches(user_input, recipe_names, n = 1, cutoff=0.6)

    return matches[0] if matches else None

def get_meal_plan_from_user(flat_recipes):
    print("\n Available Recipes")
    for recipe in flat_recipes:
        print(f"- {recipe}")

    meal_input = input("\n What do you want to eat? \nChoose your meal plan (separate by commas): \n")
           
    meal_plan = []
    for meal in meal_input.split(","):
        meal = meal.strip()
        match = get_closest_match(meal, flat_recipes.keys(), cutoff = 0.5)
        if match:
            print(f"Matched '{meal}' to '{match}'")
            meal_plan.append(match)
        else:
            print(f"'{meal}' not found and was skipped.")
    return meal_plan

def generate_shopping_list(meal_plan, flat_recipes, stock): 
    """
    Calculates ingredient needs by summing all required quantities first,
    then comparing to stock to produce an accurate shopping list.
    """
    total_needed = {}
    recipe_counts = Counter(meal_plan)  # Count how many times each meal is selected

    # Step 1: Aggregate total needed quantities
    for recipe_name, count in recipe_counts.items():
        ingredients = flat_recipes[recipe_name]
        for item, needed_info in ingredients.items():
            needed_qty = needed_info["quantity"] * count
            needed_unit = needed_info["unit"]

            if item in total_needed:
                total_needed[item]["quantity"] += needed_qty
            else:
                total_needed[item] = {"quantity": needed_qty, "unit": needed_unit}

    # Step 2: Compare with stock
    shopping_list = {}
    for item, need_info in total_needed.items():
        needed_qty = need_info["quantity"]
        needed_unit = need_info["unit"]

        if item in stock:
            stock_qty = stock[item]["quantity"]
            stock_unit = stock[item]["unit"]

            if stock_unit == needed_unit:
                if stock_qty < needed_qty:
                    shopping_list[item] = {
                        "quantity": round(needed_qty - stock_qty, 2),
                        "unit": needed_unit
                    }
                # else: enough stock, do nothing
            else:
                # Unit mismatch – assume we need to buy all
                shopping_list[item] = {
                    "quantity": round(needed_qty, 2),
                    "unit": needed_unit
                }
        else:
            # Not in stock at all
            shopping_list[item] = {
                "quantity": round(needed_qty, 2),
                "unit": needed_unit
            }

    return shopping_list



# Start program
welcome_message()
main_menu()
