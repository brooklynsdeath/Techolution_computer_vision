# File for the check-in and check-out of books

from storage import Storage
from sqlalchemy.orm import Session
from sqlalchemy import text
import datetime

from storage import BookCheckout, Book, User
from prettytable import PrettyTable
from utils import print_green, print_red
import uuid


class BooksCheckoutManager:
    def __init__(self, database: Storage):
        self.database = database

    def checkout_book(self, user_id, isbn):
        """
        Checkout a book for a user.

        Args:
            user_id (str): The ID of the user.
            isbn (str): The ISBN of the book.

        Returns:
            bool: True if the book is successfully checked out, False otherwise.
        """
        with Session(self.database.get_engine()) as session:
            checkout = session.query(BookCheckout).filter(BookCheckout.isbn == isbn, BookCheckout.checked_in_at == None).count()
            if checkout > 0:
                print_red("\nBook already checked out.")
                return False
            
            user_raw_id = session.query(User.id).filter(User.user_id == user_id).first()

            if user_raw_id is None:
                print_red("\nUser does not exist.")
                return False

            user_raw_id = user_raw_id[0]

            new_checkout = BookCheckout(user_id=user_raw_id, isbn=isbn)
            session.add(new_checkout)
            session.commit()

        print_green("\nBook checked out.")
        return True

    def checkin_book(self, isbn):
            """
            Check in a book with the given ISBN.

            Args:
                isbn (str): The ISBN of the book to be checked in.

            Returns:
                bool: True if the book was successfully checked in, False otherwise.
            """
            with Session(self.database.get_engine()) as session:
                checkout = session.query(BookCheckout).filter_by(isbn=isbn, checked_in_at=None).first()
                if checkout is None:
                    print_red("\nBook not checked out.")
                    return False
                checkout.checked_in_at = datetime.datetime.now()
                session.commit()
            print_green("Book checked in.")
            return True
    
    def trace_book(self, isbn):
        """
        Retrieves the user who has checked out the book with the provided ISBN.

        Args:
            isbn (str): The ISBN of the book to be traced.

        Returns:
            None
        """

        with Session(self.database.get_engine()) as session:
            result = session.query(Book.isbn).filter(Book.isbn == isbn).one_or_none()

            if result is None:
                print_red("\nBook does not exist.")
                return

            result = session.query(Book.title, Book.author, Book.isbn, User.name, User.user_id)\
                .join(BookCheckout, BookCheckout.isbn == Book.isbn)\
                .join(User, User.id == BookCheckout.user_id)\
                .filter(Book.isbn == isbn, BookCheckout.checked_in_at == None)\
                .order_by(BookCheckout.created_at.desc()).first()
            session.commit()
            
        if result is None:
            print_green("\nBook is Available for checkout.")
            return

        table = PrettyTable()
        table.field_names = ["Title", "Author", "ISBN", "User Name", "User ID"]
        table.add_row(result)
        print_red("Book is checked out")
        print_red(table)

    def list_checked_out_books(self):
        """
        Retrieves all books that are currently checked out and prints them in a formatted table.

        Returns:
            None
        """

        with Session(self.database.get_engine()) as session:
            result = session.query(Book.title, Book.author, Book.isbn, User.name, User.user_id)\
                .join(BookCheckout, BookCheckout.isbn == Book.isbn)\
                .join(User, User.id == BookCheckout.user_id)\
                .filter(BookCheckout.checked_in_at == None)\
                .order_by(BookCheckout.created_at.desc()).all()
            session.commit()

        table = PrettyTable()
        table.field_names = ["Title", "Author", "ISBN", "User Name", "User ID"]
        for row in result:
            table.add_row(row)
        print_green(table)
