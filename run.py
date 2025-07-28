# Your code goes here.
# You can delete these comments, but do not change the name of this file
# Write your code to expect a terminal of 80 characters wide and 24 rows high


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

# Start program
welcome_message()
main_menu()
