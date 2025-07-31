# Your code goes here.
# You can delete these comments, but do not change the name of this file
# Write your code to expect a terminal of 80 characters wide and 24 rows high

import json

def welcome_message():
    """
    Introduce user to the project
    """
    print("\nWelcome to the Family Shopping List")

def view_stock(stock_data):
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
            meal_plan = ["Greek Chicken", "Hummus and egg on toast", "Lasagne", "Burgers"]
            shopping_list = generate_shopping_list(meal_plan, recipes_data, stock_data)
            print("\nShopping List:")
            for item, info in shopping_list.items():
                print(f"- {item}: {info['quantity']} {info['unit']}")
            break
        elif choice == "2":
            view_stock(stock_data)
            break
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

def generate_shopping_list(meal_plan, recipes_data, stock): 
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
                        # Not enough stock. Calculate how much more is needed.
                        extra_needed = needed_qty - stock_qty
                    else:
                        continue
                else: extra_needed = needed_qty
                
                    # Units are wrong. Add full amount to shopping list just in case
                if item in shopping_list:
                    shopping_list[item]["quantity"] += needed_qty
                else:
                    shopping_list[item] = {"quantity": needed_qty, "unit": needed_unit}
                
    return shopping_list

# Start program
welcome_message()
main_menu()
