# Your code goes here.
# You can delete these comments, but do not change the name of this file
# Write your code to expect a terminal of 80 characters wide and 24 rows high
import json
import difflib

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
 
    while True:
        print("\nMain Menu")
        print("1. Generate Shopping List")
        print("2. View Stock")
        print("3. Exit")

        choice = input("Enter your choice(1-3):")

        if choice == "1":
            print("\n Available Recipes")
            for recipe in recipes_data:
                print(f"- {recipe}")
            meal_input = input("\n What do you want to eat? \nChoose your meal plan (separate by commas): \n")
            meal_plan = []
            for meal in meal_input.split(","):
                meal = meal.strip()
                match = get_closest_match(meal, recipes_data.keys())
                if match:
                    print(f"Matched '{meal}' to '{match}'")
                    meal_plan.append(match)
                else:
                    print(f"'{meal}' not found and was skipped.")
            if not meal_plan:
                print("No valid meals entered. Returning to main menu.")
                continue 

            shopping_list = generate_shopping_list(meal_plan, recipes_data, stock_data)
            print("\nShopping List:")
            for item, info in shopping_list.items():
                print(f"- {item}: {info['quantity']} {info['unit']}")
        elif choice == "2":
            view_stock(stock_data)
        elif choice == "3":
            print("Goodbye!")
            break
        else:
            print("Invalid input. Please enter 1, 2, or 3.")


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
    
def get_closest_match(user_input, recipe_names, cutoff=0.6):
    """
    Allow user to make small mistakes when inputting their meal plan
    """
    matches = difflib.get_close_matches(user_input, recipe_names, n = 1, cutoff=0.6)

    return matches[0] if matches else None

    
def generate_shopping_list(meal_plan, recipes_data, stock): 
    """
    Function takes into account already stocked ingredients to formulate a shopping list
    """
    shopping_list = {}

    for recipe_name in meal_plan:
        ingredients = recipes_data[recipe_name]

        for item, needed_info in ingredients.items():
            needed_qty = needed_info["quantity"]
            needed_unit = needed_info["unit"]

            if item in stock:
                stock_qty = stock[item]["quantity"]
                stock_unit = stock[item]["unit"]

                if stock_unit == needed_unit:
                    if stock_qty < needed_qty:
                        extra_needed = needed_qty - stock_qty
                    else:
                        continue  # Enough stock, no need to add
                else:
                    # Unit mismatch so add full amount
                    extra_needed = needed_qty
            else:
                # Item not in stock at all
                extra_needed = needed_qty

            # Add to shopping list
            if item in shopping_list:
                shopping_list[item]["quantity"] += extra_needed
            else:
                shopping_list[item] = {"quantity": extra_needed, "unit": needed_unit}

    return shopping_list


# Start program
welcome_message()
main_menu()
