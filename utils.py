# FIle for utility functions

from termcolor import colored
import re
import uuid


def print_green(text):
    print(colored(text, 'green'))

def print_red(text):
    print(colored(text, 'red'))

def validate_user_id(user_id):
    """
    Check if the user ID only has numbers, lowercase letters, and hyphens, underscores and periods only.

    Args:
        user_id (str): The user ID to be checked.

    Returns:
        bool: True if the user ID is valid, False otherwise.
    """
    # check if the userID only has numbers, lowercase letters, and hyphens, underscores and periods only
    # return bool(re.match(r'^[a-z0-9_-]+$', user_id))
    if not re.match(r'^[a-z0-9_-]+$', user_id):
        print_red("User ID must only contain numbers, lowercase letters, hyphens, underscores, and periods")
        return False
    else:
        return True
    
def validate_isbn(isbn):
    """
    Check if the ISBN is a number.

    Args:
        isbn (str): The ISBN to be checked.

    Returns:
        bool: True if the ISBN is a number, False otherwise.
    """
    try:
        _ = int(isbn) # check if the ISBN is a number, because ISBN MUST be a number according to the international standards
    except ValueError:
        print_red("ISBN must be a number")
        return False
    else:
        return True

def validate_uuid(uuid_str):
    """
    Check if the UUID is a valid UUID format.

    Args:
        uuid_str (str): The UUID to be checked.

    Returns:
        bool: True if the UUID is a valid UUID format, False otherwise.
    """
    try:
        uuid_str = uuid.UUID(uuid_str)
    except ValueError:
        print_red("UUID must be a valid UUID format")
        return False
    else:
        return uuid_str
