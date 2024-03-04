# This file contains the database schema and the Storage class, which is used to interact with the database.

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, UUID
from sqlalchemy.orm import relationship  # Add for relationships
import datetime
import uuid

Base = declarative_base()

class User(Base):  
    __tablename__ = "users"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4) # This user's raw ID, which cannot be changed for one user
    user_id = Column(String, unique=True, nullable=False) # This user's ID, which can be changed for one user, based on users choice
    name = Column(String, nullable=False) # This user's name
    created_at = Column(DateTime, default=datetime.datetime.now, nullable=False) # This user's creation date

    books_checked_out = relationship("Book", secondary="books_checkout", back_populates="user")  # Relationships 

class Book(Base):
    __tablename__ = "books"
    isbn = Column(String, primary_key=True) # This book's ISBN
    title = Column(String, nullable=False) # This book's title
    author = Column(String, nullable=False) # This book's author
    created_at = Column(DateTime, default=datetime.datetime.now, nullable=False) # This book's creation date

    user = relationship("User", secondary="books_checkout", back_populates="books_checked_out") # Relationships

class BookCheckout(Base):

    # for due date and other functionality extension we can just add a new columns 
    # Eg: For due date, add new column, due_date and then check if the book is checked in after the due date

    __tablename__ = "books_checkout"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4) # This checkout's raw ID, which cannot be changed for one checkout
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False) # This checkout's user raw ID
    isbn = Column(String, ForeignKey("books.isbn"), nullable=False,) # This checkout's book ISBN
    checked_in_at = Column(DateTime, nullable=True) # This checkout's check-in date, and is NULL if the book is not checked in
    created_at = Column(DateTime, default=datetime.datetime.now, nullable=False) # This checkout's creation date

class Storage:
    def __init__(self, database_name):
        self.engine = create_engine(f"sqlite:///{database_name}")
        Base.metadata.create_all(self.engine)  # Metadata from Base

    def get_engine(self):
        return self.engine
