# Task: create an application that will store the content of our library. I chose children's books.
# more info about task is in the file "zadani_ukolu.txt"

import click
from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, Integer, String, DateTime, Boolean

db = create_engine("sqlite:///books.sqlite")
Base = declarative_base()

## Create empty database
def connect_to():
    Base.metadata.create_all(db)
    Session = sessionmaker(bind=db)
    return Session()
connect_to()       ## zavoláno pro vytvoreni databaze


class Book(Base):
    __tablename__ = "kids_books"
    id = Column(Integer, primary_key=True)
    book_name = Column(String)
    author = Column(String)
    number_of_pages = Column(Integer)
    date_added = Column(DateTime)
    read_yes_no = Column(Boolean, default=False)
    partially_read = Column(Boolean, default=False)
    lent_to = Column(String)        # name of person or None
    date_of_borrowing = Column(DateTime)
    notes = Column(String)

    def __repr__(self):
        return f"<Kniha(id={self.id}, book_name='{self.book_name}', author = '{self.author}', date_added={self.date_added})>"


@click.group()
def kids_library():
    pass


## ADD book into the library
@kids_library.command()
# @click.option("--adding", prompt="Add a book")
@click.option("--name", prompt="Name of the book")
@click.option("--author", prompt="Author of the book")
@click.option("--pages", prompt="Number of pages")
def add_book(name, author, pages):
    book_session = connect_to()
    book = Book(book_name=name, author=author, number_of_pages=pages, date_added=datetime.now())
    book_session.add(book)  
    book_session.commit()
    print(f"Added: {book.book_name}, {book.author}, {book.number_of_pages}")


## SUMMARY, write out the content of the library, dump file
@kids_library.command()
# @click.option("--read", default=False, is_flag=True)
def dump_file():
    book_session = connect_to()
    qu = book_session.query(Book)   #qu (=query)
    books = qu.all()
    for book in books:
        print(f"{book.id}.) Název: {book.book_name}, autor: {book.author}, počet stran: {book.number_of_pages} (přidáno do knihovny: {book.date_added})")


## READ, the books that we have already read
@kids_library.command()
@click.option("--book_id", prompt="Insert ID of the book")
def already_read(book_id):
    book_session = connect_to()
    qu = book_session.query(Book)
    read_book = qu.filter_by(id=book_id).one()
    read_book.read_yes_no = True
    book_session.add(read_book)
    book_session.commit()
    print(f"Kniha s ID {book_id} byla přečtena")



if __name__ == "__main__":
    kids_library()