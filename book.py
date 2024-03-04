# Fine for managing books in the library

from storage import Storage, Book, User, BookCheckout
from sqlalchemy import text
from sqlalchemy.orm import Session
from prettytable import PrettyTable
from utils import print_green, print_red


class BooksManager:
    def __init__(self, database: Storage):
        self.database = database

    def add_book(self, title, author, isbn):
        """
        Adds a new book to the database.

        Args:
            title (str): The title of the book.
            author (str): The author of the book.
            isbn (str): The ISBN of the book.

        Returns:
            bool: True if the book was successfully added, False otherwise.
        """

        with Session(self.database.get_engine()) as session:
            existing_book = session.query(Book).filter(Book.isbn == isbn).one_or_none()

            if existing_book is not None:
                print_red("\nBook with this ISBN already exists.")
                return False

            new_book = Book(title=title, author=author, isbn=isbn)
            session.add(new_book)
            session.commit()

        print_green("\nBook added.")
        return True

    def delete_book(self, isbn):
        """
        Deletes a book from the database based on the provided ISBN.

        Args:
            isbn (str): The ISBN of the book to be deleted.

        Returns:
            bool: True if the book is successfully deleted, False otherwise.
        """

        with Session(self.database.get_engine()) as session:
            
            book_checked_out = session.query(BookCheckout).filter(BookCheckout.isbn == isbn, BookCheckout.checked_in_at == None).count()
            if book_checked_out > 0:
                print_red("\nBook is checked out, cannot be deleted.")
                return False

            book = session.query(Book).filter_by(isbn=isbn).first()
            session.delete(book)
            session.commit()
        print_green("\nBook deleted.")
        return True
    
    def update_book(self, isbn, title, author):
        """
        Updates the title and author of a book based on the provided ISBN.

        Args:
            isbn (str): The ISBN of the book to be updated.
            title (str): The new title of the book.
            author (str): The new author of the book.

        Returns:
            bool: True if the book is successfully updated, False otherwise.
        """

        with Session(self.database.get_engine()) as session:
            book = session.query(Book).filter_by(isbn=isbn).one_or_none()
            if book is None:
                print_red("\nBook not found.")
                return False
            book.title = title
            book.author = author
            session.commit()
        print_green("\nBook updated.")
        return True

    def list_books(self, colored=False):
        """
        Retrieves all books from the database and prints them in a formatted table.

        Args:
            self: The instance of the Book class.
            colored (bool, optional): Whether to use colored output. Defaults to False.
        Returns:
            None
        """

        with Session(self.database.get_engine()) as session:
            result = session.query(Book.title, Book.author, Book.isbn).all()

        table = PrettyTable()

        table.field_names = ["Title", "Author", "ISBN"]
        for row in result:
                table.add_row(row)

        if colored:
            print_green(table)
        else:
            print(table)
