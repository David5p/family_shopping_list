# Your code goes here.
# You can delete these comments, but do not change the name of this file
# Write your code to expect a terminal of 80 characters wide and 24 rows high
import json
import difflib
from collections import Counter
from colorama import init, Fore, Style

init(autoreset=True)  # Automatically reset colors after each print


def view_stock(stock_data):
    """
    When user wants to see current stock
    """
    print("\nCurrent Stock:")
    print(f'{"Item":<28} | {"Quantity":<10} | {"Unit":<15}')
    print('-' * 53)
    for item, info in stock_data.items():
        print(f'{item:<28} | {info["quantity"]:<10} | {info["unit"]:<15}')


def main_menu():
    """
    Introduce user to the project and provide
    user with options to select how they will
    use the program
    """
    print(Style.BRIGHT + Fore.CYAN + "\nWelcome to the Family Shopping List")
    stock_data = load_stock()
    recipes_data = load_recipes()
    flat_recipes = flatten_recipes(recipes_data)

    while True:
        print(Style.BRIGHT + Fore.MAGENTA + "\nMain Menu")
        print("1. View Recipes")
        print("2. Edit Recipes")
        print("3. Generate Shopping List")
        print("4. View Stock")
        print("5. Edit Stock")
        print("6. Exit")

        choice = input(Style.BRIGHT + Fore.YELLOW + "Enter your choice(1-6):")
        if choice == "1":
            view_recipes(flat_recipes)

        elif choice == "2":
            view_recipes(flat_recipes)
            edit_recipes(recipes_data)

        elif choice == "3":
            while True:
                print(
                    Style.BRIGHT + Fore.CYAN +
                    "Would you like to plan meals for"
                    " the weekend(2 days) or a full week (7 days)?")
                days_input = input(
                    Style.BRIGHT + Fore.YELLOW +
                    "Enter your choice (2 or 7): "
                    ).strip()

                if days_input in ["2", "7"]:
                    break  # valid input, so break out of the loop
                else:
                    print(
                        Style.BRIGHT + Fore.RED +
                        "Invalid input. Please enter 2 or 7.")

            meal_plan = get_meal_plan_from_user(flat_recipes)
            if not meal_plan:
                print(
                    Style.BRIGHT + Fore.RED +
                    "No valid meals entered. Returning to main menu.")
                continue

            shopping_list = generate_shopping_list(
                meal_plan, flat_recipes, stock_data)
            print("\nShopping List:")
            for item, info in shopping_list.items():
                print(f"- {item}: {info['quantity']} {info['unit']}")

        elif choice == "4":
            view_stock(stock_data)

        elif choice == "5":
            view_stock(stock_data)
            edit_stock(stock_data)

        elif choice == "6":
            print(
                Style.BRIGHT + Fore.CYAN + "Goodbye!")
            break
        else:
            print(
                Style.BRIGHT + Fore.RED +
                "Invalid input. Please enter 1, 2, 3, 4, 5 or 6.")


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
    Allow the user to update or add items in the stock list,
    then save the changes.
    """
    while True:
        item_name = input(
            Style.BRIGHT + Fore.YELLOW +
            "Enter the name of the item to update"
            "(or type 'done' to finish): "
            ).strip().lower()

        if item_name == "done":
            break

        existing_item = get_existing_item_key(item_name, stock_data)

        if not existing_item:
            match = get_closest_match(
                item_name.title(),
                list(stock_data.keys()))
            if match:
                confirm = input(
                    Fore.LIGHTYELLOW_EX +
                    f"Did you mean'{match}'? (y/n): "
                    ).strip().lower()
                if confirm == "y":
                    existing_item = match
        if existing_item:
            item_name = existing_item
            print(
                Style.BRIGHT + Fore.GREEN +
                f"{item_name} found in stock. Updating...")
        else:
            print(
                Style.BRIGHT + Fore.GREEN +
                f"{item_name} not found. Adding as a new item.")

        try:
            quantity = float(input(
                Style.BRIGHT + Fore.YELLOW +
                f"Enter the quantity for '{item_name}': "))
            unit = input(
                Style.BRIGHT + Fore.YELLOW +
                f"Enter the unit for '{item_name}' "
                "(e.g., grams, packs, servings or pieces): "
            ).strip().lower()

            stock_data[item_name.title()] = {
                "quantity": quantity,
                "unit": unit
            }
            print(
                Style.BRIGHT + Fore.GREEN +
                f"Updated '{item_name.title()}' in stock.")

        except ValueError:
            print(
                Style.BRIGHT + Fore.RED +
                "Invalid quantity. Please enter a number.")

    # Save the updated stock data
    with open("stock.json", "w") as file:
        json.dump(stock_data, file, indent=4)

    print(
        Style.BRIGHT + Fore.GREEN +
        "Stock list updated and saved.")


def get_existing_item_key(user_input, stock_data):
    for item in stock_data:
        if item.lower() == user_input.lower():
            return item
    return None


def flatten_recipes(recipes_data):
    flat_recipes = {}
    for category in recipes_data.values():
        for recipe_name, ingredients in category.items():
            fixed_ingredients = {}
            for ing, info in ingredients.items():
                try:
                    qty = float(info["quantity"])
                except ValueError:
                    qty = 0  # Or handle error appropriately
                fixed_ingredients[ing] = {
                    "quantity": qty,
                    "unit": info["unit"]
                }
            flat_recipes[recipe_name] = fixed_ingredients
    return flat_recipes


def view_recipes(flat_recipes):
    print("\nAvailable Recipes:")
    for index, recipe_name in enumerate(flat_recipes, 1):
        print(f"{index}. {recipe_name}")


def category_choices():
    categories = ["Breakfast", "Meals", "Snacks"]
    while True:
        print(
            Style.BRIGHT + Fore.YELLOW +
            "\nSelect a category:")
        for index, category in enumerate(categories, start=1):
            print(f"{index}. {category}")
        choice = input(
            Style.BRIGHT + Fore.YELLOW + "Enter your choice (1-3): "
            ).strip()

        if choice.isdigit() and 1 <= int(choice) <= len(categories):
            return categories[int(choice) - 1]
        else:
            print(
                Style.BRIGHT + Fore.RED +
                "Invalid input. Please choose a valid number from the list.")


def input_ingredients():
    ingredients = {}
    while True:
        ingredient = input(
            Style.BRIGHT + Fore.YELLOW +
            "Enter ingredient name (or type 'done' to finish): "
            ).strip().lower()
        if ingredient == "done":
            break
        try:
            quantity = float(input(
                Style.BRIGHT + Fore.YELLOW +
                f"Enter the quantity for '{ingredient}': "))
            unit = input(
                Style.BRIGHT + Fore.YELLOW +
                f"Enter the unit for '{ingredient}' "
                "(e.g., grams, packs, servings or pieces): "
                ).strip().lower()
            ingredients[ingredient] = {"quantity": quantity, "unit": unit}
        except ValueError:
            print(
                Style.BRIGHT + Fore.RED +
                "Invalid quantity. Please enter a number.")
    return ingredients


def display_ingredients(ingredients):
    """
    Display all current ingredients with quantities and units.
    """
    print("\nCurrent ingredients:")
    for i, (ingredient, details) in enumerate(ingredients.items(), 1):
        print(f"{i}. {ingredient}: {details['quantity']} {details['unit']}")
    print(f"{len(ingredients) + 1}. Add new ingredient")
    print(f"{len(ingredients) + 2}. Finish editing")


def edit_existing_ingredient(ingredients, index):
    """
    Allow the user to edit or remove an existing ingredient.
    """
    ingd_name = list(ingredients.keys())[index]
    print(
        Fore.LIGHTYELLOW_EX + f"Editing '{ingd_name}'")

    # Ask user what they want to do with this ingredient
    sub_action = input(
        Style.BRIGHT + Fore.YELLOW +
        "Type 'edit' to change quantity/unit, "
        "'remove' to delete ingredient, or 'cancel' to go back: "
        ).strip().lower()
    if sub_action == 'edit':
        # Get new quantity and unit, if provided, update ingredient details
        while True:
            new_unit = input(
                Style.BRIGHT + Fore.YELLOW +
                f"Enter new unit for '{ingd_name}' "
                f"(current: {ingredients[ingd_name]['unit']}): "
                ).strip()

            # Check if it's a number (not allowed)
            if new_unit.replace('.', '', 1).isdigit():
                print(
                    Style.BRIGHT + Fore.RED +
                    "Unit cannot be a number."
                    "Please enter a valid unit (e.g., grams, packs).")
            elif not new_unit:
                print(
                    Style.BRIGHT + Fore.RED + "Unit cannot be empty.")
            else:
                break

        new_qty = input(
            Style.BRIGHT + Fore.YELLOW +
            f"Enter new quantity for '{ingd_name}' "
            f"(current: {ingredients[ingd_name]['quantity']}): "
            ).strip()
        if new_qty:
            ingredients[ingd_name]['quantity'] = float(new_qty)
        if new_unit:
            ingredients[ingd_name]['unit'] = new_unit
            print(f"Updated '{ingd_name}'")
    elif sub_action == 'remove':
        # Remove the ingredient from the recipe
        del ingredients[ingd_name]
        print(
            Style.BRIGHT + Fore.GREEN +
            f"Removed '{ingd_name}' from the recipe.")
    elif sub_action == 'cancel':
        print(
            Style.BRIGHT + Fore.GREEN +
            "Cancelled editing")
    else:
        print(
            Style.BRIGHT + Fore.RED +
            "Invalid action.")


def add_new_ingredient(ingredients):
    """
    Add a new ingredient to the list.
    """
    new_ingd = input(
        Style.BRIGHT + Fore.YELLOW +
        "Enter new ingredient name: "
        ).strip()
    new_qty = input(
        Style.BRIGHT + Fore.YELLOW +
        "Enter quantity: "
        ).strip()
    new_unit = input(
        Style.BRIGHT + Fore.YELLOW +
        "Enter unit: "
        ).strip()
    if new_ingd:
        ingredients[new_ingd] = {"quantity": new_qty, "unit": new_unit}
        print(
            Style.BRIGHT + Fore.GREEN +
            f"Added '{new_ingd}'.")
    else:
        print(
            Style.BRIGHT + Fore.RED +
            "Ingredient name cannot be empty.")


def edit_ingredients(ingredients):
    """
    Orchestrates editing of recipe ingredients by calling helper functions.
    """
    while True:
        display_ingredients(ingredients)
        choice = input(
            Style.BRIGHT + Fore.YELLOW +
            "Select an ingredient number to edit/remove, "
            "or choose to add/finish: "
            ).strip()
        if not choice.isdigit():
            print(
                Style.BRIGHT + Fore.RED +
                "Please enter a valid number")
            continue

        choice_num = int(choice)
        if 1 <= choice_num <= len(ingredients):
            edit_existing_ingredient(ingredients, choice_num - 1)
        elif choice_num == len(ingredients) + 1:
            add_new_ingredient(ingredients)
        elif choice_num == len(ingredients) + 2:
            print(
                Style.BRIGHT + Fore.GREEN +
                "Finished editing ingredients.")
            break
        else:
            print(
                Style.BRIGHT + Fore.RED +
                "Invalid selection.")


def list_recipes(flat_recipes):
    """
    Refresh the recipe list each time in case it changes
    """
    recipe_list = list(flat_recipes.keys())
    print("\nAvailable Recipes:")
    for index, recipe in enumerate(recipe_list, 1):
        print(f"{index}. {recipe}")
    return recipe_list


def handle_new_recipe(recipes_data):
    """
    Prompts the user to create a new recipe by entering
    its name, category, and ingredients.
    Adds the new recipe to the recipes_data dictionary
    under the selected category.
    """
    recipe_name = input(
        Style.BRIGHT + Fore.YELLOW +
        "Enter new recipe name: "
        ).strip().title()
    selected_category = category_choices()
    new_ingredients = input_ingredients()

    if selected_category not in recipes_data:
        recipes_data[selected_category] = {}

    recipes_data[selected_category][recipe_name] = new_ingredients
    print(
        Style.BRIGHT + Fore.GREEN +
        f"Added '{recipe_name}' to category '{selected_category}'.")


def get_recipe_selection(recipe_list):
    """
    Prompts the user to select an existing recipe by number,
    add a new recipe, or finish editing.
    """
    selection = input(
        Style.BRIGHT + Fore.YELLOW +
        "\nEnter the number of the recipe to edit/delete "
        "or type 'new' to add a recipe, or 'done' to finish: "
        ).strip().lower()
    if selection == "done":
        return "done", None
    elif selection == "new":
        return "new", None

    elif selection.isdigit():
        index = int(selection) - 1
        if 0 <= index < len(recipe_list):
            return "existing", recipe_list[index]

    print(
        Style.BRIGHT + Fore.RED +
        "Invalid selection.")
    return "invalid", None


def get_recipe_category(recipes_data, recipe_name):
    """
    Finds and returns the category to which a given recipe belongs.
    """
    for category, recipes in recipes_data.items():
        if recipe_name in recipes:
            return category
    return None


def handle_existing_recipe_action(recipes_data, category, recipe_name):
    """
    Allows the user to either edit or delete an existing recipe.
    """

    print(
        Style.BRIGHT + Fore.GREEN +
        f"\n'{recipe_name}' found in category '{category}'.")
    action = input(
        Style.BRIGHT + Fore.YELLOW +
        "Type 'edit' to update or 'delete' to remove it: "
        ).strip().lower()

    if action == "delete":
        del recipes_data[category][recipe_name]
        print(
            Style.BRIGHT + Fore.GREEN +
            f"'{recipe_name}' has been deleted.")
    elif action == "edit":
        edit_ingredients(recipes_data[category][recipe_name])
    else:
        print(
            Style.BRIGHT + Fore.RED +
            "Invalid action. Please type 'edit' or 'delete'.")


def edit_recipes(recipes_data):

    """
    Allow the user to update or add items to the recipes,
    then save the changes.
    """
    while True:
        flat_recipes = flatten_recipes(recipes_data)
        recipe_list = list_recipes(flat_recipes)

        selection_type, recipe_name = get_recipe_selection(recipe_list)

        if selection_type == "done":
            break
        elif selection_type == "new":
            handle_new_recipe(recipes_data)
            continue
        elif selection_type == "existing":
            category = get_recipe_category(
                recipes_data, recipe_name)

        # Find the category of the selected recipe
            if not category:
                print(
                    Style.BRIGHT + Fore.RED +
                    f"\nCould not find the category for "
                    f"{recipe_name}. Skipping.")
                continue
            handle_existing_recipe_action(recipes_data, category, recipe_name)
        else:
            continue

    # Save the updated recipes data
    with open("recipes.json", "w") as file:
        json.dump(recipes_data, file, indent=4)

    print(
        Style.BRIGHT + Fore.GREEN +
        "Recipes list updated and saved.")


def get_closest_match(user_input, recipe_names, cutoff=0.5):
    """
    Allow user to make small mistakes when inputting their meal plan
    """
    matches = difflib.get_close_matches(
        user_input, recipe_names, n=1, cutoff=0.6)

    return matches[0] if matches else None


def get_meal_plan_from_user(flat_recipes):
    recipe_list = list(flat_recipes.keys())
    print("\nAvailable Recipes:")
    for index, recipe in enumerate(flat_recipes, 1):
        print(f"{index}. {recipe}")

    meal_input = input(
        Style.BRIGHT + Fore.YELLOW +
        "\nEnter the recipe numbers for your meal plan "
        "(comma-separated):\n")

    meal_plan = []
    for value in meal_input.split(","):
        value = value.strip()
        if value.isdigit():
            index = int(value) - 1
            if 0 <= index < len(recipe_list):
                selected_recipe = recipe_list[index]
                meal_plan.append(selected_recipe)
                print(
                    Style.BRIGHT + Fore.GREEN +
                    f"Added: {selected_recipe}")
            else:
                print(
                    Style.BRIGHT + Fore.RED +
                    f"Invalid number: {value}. Skipped.")

        else:
            print(
                Style.BRIGHT + Fore.RED +
                f"'{value}' is not a valid number. Skipped.")
    return meal_plan


def generate_shopping_list(meal_plan, flat_recipes, stock):
    """
    Calculates ingredient needs by summing all required quantities first,
    then comparing to stock to produce an accurate shopping list.
    """
    total_needed = {}
    # Count how many times each meal is selected
    recipe_counts = Counter(meal_plan)

    # Step 1: Aggregate total needed quantities
    for recipe_name, count in recipe_counts.items():
        ingredients = flat_recipes[recipe_name]
        for item, needed_info in ingredients.items():
            needed_qty = needed_info["quantity"] * count
            needed_unit = needed_info["unit"]

            if item in total_needed:
                total_needed[item]["quantity"] += needed_qty
            else:
                total_needed[item] = {
                    "quantity": needed_qty, "unit": needed_unit}

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
if __name__ == "__main__":
    main_menu()
