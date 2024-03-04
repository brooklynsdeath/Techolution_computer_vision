# Techolution_computer_vision
For the `Redesigning Poor Code` assessment.

# Redesigning Poor Code

## Problem Statement
Your task is to reformat a poorly designed code for a Library Management System with the following functionalities
1. Manage books (add, update, delete, list, and search by various attributes like title, author, or ISBN)
2. Manage users (add, update, delete, list, and search by attributes like name, user ID)
3. Check out and check-in books
4. Track book availability
5. Simple logging of operations

### Task for the Candidate
1. The application should utilize classes and objects more effectively, with clear relationships and responsibilities among them with Object Oriented Design.
2. Implement or refactor the storage.py for reliable storage and retrieval using file-based storage (JSON, CSV, etc.)
3. Obtain input from the user using CLI to access information from the user in a friendly and intuitive manner.
4. Implement error handling and input validation throughout the application.
5. The application's design doesn't facilitate easy extension or modification.
6. Ensure that the application is modular and scalable, allowing for future expansions such as new types of items to manage or additional features like due dates for books, late fees, etc.
7. Include document action and comments to explain the design decisions, architecture, and usage of classes and methods.

## Solution

Code folder structure:
```
.
├── README.md
├── book.py
├── check.py
├── library.db
├── main.py
├── requirements.txt
├── storage.py
├── user.py
└── utils.py
```
### How to run the code
1. Clone the repository
2. Install the requirements using `pip install -r requirements.txt`
3. Run the code using `python3 main.py`
4. Follow the instructions on the terminal to use the application <br>

### Conclusion
The application has undergone a redesign to enhance its utilization of classes and objects, ensuring clear delineation of relationships and responsibilities through Object-Oriented Design principles. It now employs file-based storage for robust data storage and retrieval via a SQLite database. User interaction is facilitated through a Command-Line Interface (CLI), providing a user-friendly and intuitive experience. Comprehensive error handling and input validation mechanisms have been integrated throughout the application. Its design emphasizes ease of extension and modification, characterized by modularity and scalability, paving the way for future enhancements such as managing new item types or introducing additional features like due dates for books and late fees. Additionally, the application incorporates documentation detailing design decisions, architecture, and usage of classes and methods, including actionable comments for clarity and comprehension.
