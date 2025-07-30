# Your code goes here.
# You can delete these comments, but do not change the name of this file
# Write your code to expect a terminal of 80 characters wide and 24 rows high

import json

def welcome_message():
    """
    Introduce user to the project
    """
    print("\nWelcome to the Family Shopping List")

def main_menu():
    """
    Provide user with options to select how they will use the program
    """ 
    while True:
        print("\nMain Menu")
        print("1. Generate Shopping List")
        print("2. View Stock")
        print("3. Exit")

        choice = input("Enter your choice(1-3):")

        if choice == "1":
            generate_shopping_list()
            break
        elif choice == "2":
            view_stock()
            break
        elif choice == "3":
            print("Goodbye!")
            break
        else:
            print("Invalid input. Please enter 1, 2, or 3.")

# Placeholder functions to make main menu function
def generate_shopping_list():
    print("Generating shopping list...")

def view_stock():
    print("Viewing stock...")


def load_stock():
    """
    Load stock from the json file so user has access to 
    what stock is available.
    """
    with open("stock.json", "r") as file:
        stock = json.load(file)
        return stock

stock_data = load_stock()

for item, info in stock_data.items():
    print(f"{item}: {info['quantity']} {info['unit']}")


def load_recipes():
    """
    Load recipes from the json file so they are ready to be 
    compared to the stock list.
    """
    with open("recipes.json", "r") as file:
        stock = json.load(file)
        return stock

recipes_data = load_recipes()

for recipe_name, ingredients in recipes_data.items():
    print(f"\nRecipe: {recipe_name}")
    for item, info in ingredients.items():
        print(f"  {item}: {info['quantity']} {info['unit']}")

meal_plan = ["Greek Chicken", "Hummus and egg on toast"]

shopping_list = {}

for recipe_name in meal_plan:
   ingredients = recipes[recipe_name]

   for item, needed_info in ingredients.items():
        needed_qty = needed_info["quantity"]
        needed_unit = needed_info["unit"]

        if item in stock:
            stock_qty = stock[item]["quantity"]
            stock_unit = stock[item]["unit"]

             if stock_unit == needed_unit:
                if stock_qty < needed_qty:
                    # Not enough stock. Calculate how much more is needed.
                    extra_needed = needed_qty - stock_qty
                    shopping_list[item] = {"quantity": extra_needed, "unit": needed_unit}
            else:
                # Units are wrong. Add full amount to shopping list just in case
                shopping_list[item] = {"quantity": needed_qty, "unit": needed_unit}
        else:
            # Out of stock. Add full amount
            shopping_list[item] = {"quantity": needed_qty, "unit": needed_unit}


# Start program
load_stock()
load_recipes()
"""welcome_message()
main_menu()"""
