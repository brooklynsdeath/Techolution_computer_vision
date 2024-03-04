# This is a deliberately poorly implemented main script for a Library Management System.

# import book_management
# import user_management
# import checkout_management

# Main file for the library management system

from storage import Storage
from book import BooksManager
from user import UserManager
from check import BooksCheckoutManager
from utils import print_green, print_red, validate_user_id, validate_isbn, validate_uuid
import uuid
import re

from prettytable import PrettyTable

def main_menu():
    choice_table = PrettyTable()

    choice_table.field_names = ["Choice", "Description"]
    choice_table.add_row(["1", "Add Book"])
    choice_table.add_row(["2", "List Books"])
    choice_table.add_row(["3", "Update Book"])
    choice_table.add_row(["4", "Delete Book"])
    choice_table.add_row(["5", "Check Book Availability"])
    choice_table.add_row(["6", "Add User"])
    choice_table.add_row(["7", "List Users"])
    choice_table.add_row(["8", "Update User"])
    choice_table.add_row(["9", "Delete User"])
    choice_table.add_row(["10", "Checkout Book"])
    choice_table.add_row(["11", "Checkin Book"])
    choice_table.add_row(["12", "List Checked Out Books"])
    choice_table.add_row(["13", "Exit"])

    choice_table.align = "l"

    print("\n", choice_table)

    choice = input("Enter choice: ")
    return choice

def main():

    storage = Storage("library.db") # storage is traversed across the application to maintainer only single connection to the database, and avoid ghost connections
    books_manager = BooksManager(storage)
    user_manager = UserManager(storage)
    checkout_manager = BooksCheckoutManager(storage)


    while True:
        choice = main_menu()
        if choice == '1': # Add Book
            title = input("Enter title: ")
            author = input("Enter author: ")
            isbn = input("Enter ISBN: ")
            if not validate_isbn(isbn): # the checks itself print the error message
                continue
            books_manager.add_book(title, author, isbn)

        elif choice == '2': # List Books
            books_manager.list_books(colored=True)

        elif choice == '3': # Update Book
            books_manager.list_books()
            isbn = input("Enter ISBN: ")
            if not validate_isbn(isbn):
                continue
            title = input("Enter title: ")
            author = input("Enter author: ")
            books_manager.update_book(isbn, title, author)

        elif choice == '4': # Delete Book
            books_manager.list_books()
            isbn = input("Enter ISBN: ")
            if not validate_isbn(isbn):
                continue
            books_manager.delete_book(isbn)

        elif choice == '5': # Check Book Availability
            books_manager.list_books()
            isbn = input("Enter ISBN: ")
            if not validate_isbn(isbn):
                continue
            checkout_manager.trace_book(isbn)

        elif choice == '6': # Add User
            name = input("Enter name: ")
            user_id = input("Enter user ID: ")
            if not validate_user_id(user_id):
                continue
            user_manager.add_user(name, user_id)

        elif choice == '7': # List Users
            user_manager.list_users(colored=True)

        elif choice == '8': # Update User
            user_manager.list_users_raw_id()
            user_raw_id = input("Enter user Raw ID: ") # for updating the user, we need the raw ID, because the user ID can be changed when updating the user
            if not validate_uuid(user_raw_id):
                continue
            else:
                user_raw_id = uuid.UUID(user_raw_id)
            user_id = input("Enter user ID: ")
            if not validate_user_id(user_id):
                continue
            name = input("Enter name: ")
            user_manager.update_user(user_raw_id, user_id, name)

        elif choice == '9': # Delete User
            user_manager.list_users()
            user_id = input("Enter user ID: ")
            if not validate_user_id(user_id):
                continue
            user_manager.delete_user(user_id)

        elif choice == '10': # Checkout Book
            user_manager.list_users()
            user_id = input("Enter user ID: ")
            if not validate_user_id(user_id):
                continue
            books_manager.list_books()
            isbn = input("Enter ISBN: ")
            if not validate_isbn(isbn):
                continue
            checkout_manager.checkout_book(user_id, isbn)

        elif choice == '11': # Checkin Book
            isbn = input("Enter ISBN: ")
            if not validate_isbn(isbn):
                continue
            checkout_manager.checkin_book(isbn)

        elif choice == '12': # List Checked Out Books
            checkout_manager.list_checked_out_books()

        elif choice == '13': # Exit
            print("Exiting...")
            print("Goodbye!")
            break

        else: # Catch all other choices
            print(f"Choice: {choice}")
            print("Invalid choice, please try again.")

if __name__ == "__main__":
    main()
