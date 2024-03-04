# File for managing users

from storage import Storage
from sqlalchemy import text
from sqlalchemy.orm import Session
from prettytable import PrettyTable
from storage import User, Book, BookCheckout
from utils import print_green, print_red
import uuid

class UserManager:
    def __init__(self, database: Storage):
        self.database = database

    def add_user(self, name, user_id):
        """
        Adds a new user to the database.

        Args:
            name (str): The name of the user.
            user_id (str): The ID of the user.

        Returns:
            None
        """
        with Session(self.database.get_engine()) as session:
            existing_user = session.query(User).filter(User.user_id == user_id).one_or_none()

            # Check if user already exists, and if so, do not add user
            if existing_user is not None:
                print_red("\nUser with this ID already exists.")
                return
            new_user = User(name=name, user_id=user_id)
            session.add(new_user)
            session.commit()
        print_green("\nUser added.")
    
    def delete_user(self, user_id):
        """
        Deletes a user from the database.

        Args:
            user_id (str): The ID of the user to be deleted.

        Returns:
            bool: True if the user is successfully deleted, False otherwise.
        """

        with Session(self.database.get_engine()) as session:
            
            user_checkedout_books = session.query(User)\
                .join(BookCheckout, User.id == BookCheckout.user_id)\
                .filter(User.user_id == user_id, BookCheckout.checked_in_at == None).count()
            
            # Check if user has books checked out, and if so, do not delete user
            if user_checkedout_books > 0:
                print_red("\nUser has books checked out, cannot delete user")
                return False

            user = session.query(User).filter_by(user_id=user_id).first()
            if user is None:
                print_red("\nUser not found.")
                return False
            session.delete(user)
            session.commit()
        print_green("\nUser deleted.")
        return True
    
    def update_user(self, user_raw_id, user_id, name):
        """
        Updates a user's information in the database.

        Args:
            user_raw_id (uuid): The raw ID of the user to be updated.
            user_id (str): The new ID of the user.
            name (str): The new name of the user.

        Returns:
            bool: True if the user is successfully updated, False otherwise.
        """

        with Session(self.database.get_engine()) as session:
        
            user = session.query(User).filter_by(id=user_raw_id).first()

            # Check if user exists, and if not, print User not found message
            if user is None:
                print_red("\nUser not found.")
                return False
            user.name = name
            user.user_id = user_id
            session.commit()
        print_green("\nUser updated.")
        return True
    
    def list_users(self, colored=False):
        """
        Retrieves a list of users from the database and prints them in a formatted table.

        Returns:
            bool: True if the operation is successful.
        """
        with Session(self.database.get_engine()) as session:
            result = session.query(User.name, User.user_id).all()
        table = PrettyTable()

        table.field_names = ["Name", "User ID"]
        for row in result:
            table.add_row(row)
        if colored:
            print_green(table)
        else:
            print(table)
        
        return True
    
    def list_users_raw_id(self):
        """
        Retrieves a list of users from the database and prints them in a formatted table.

        Returns:
            bool: True if the operation is successful.
        """
        with Session(self.database.get_engine()) as session:
            result = session.query(User.id, User.name, User.user_id).all()
        table = PrettyTable()

        table.field_names = ["Raw ID", "Name", "User ID"]
        for row in result:
            table.add_row(row)
        print(table)
        
        return True
