# Task: create an application that will store the content of our library. I chose children's books.
# more info about task is in the file "zadani_ukolu.txt"

import click
from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, Integer, String, DateTime

db = create_engine("sqlite:///books.sqlite")
Base = declarative_base()

# Create empty database
# def connect_to():
#     Base.metadata.create_all(db)
#     Session = sessionmaker(bind=db)
#     return Session
# connect()

Session = sessionmaker(bind=db)
book_session = Session()


class Book(Base):
    __tablename__ = "kids_books"

    id = Column(Integer, primary_key=True)
    book_name = Column(String)
    author = Column(String)
    number_of_pages = Column(Integer)
    #date_added = Column(DateTime)      # rozbíjí mi to -> vyřešit
    #read = Column(bool)        # bool nelze? -> vygooglit
    #partially_read = Column(bool)      # bool nelze? -> vygooglit
    lent_to = Column(String)        # name of person or None
    date_of_borrowing = Column(DateTime)

    def __repr__(self):
        return f"<Kniha(id='.{self.id}.', book_name='.{self.book_name}.', author = '.{self.author}.', date_of_borrowing={self.date_of_borrowing})"  # date_added={self.date_added}
    

@click.group()
def kids_library():
    pass

# ADD book into the library
@kids_library.command()
# @click.option("--adding", prompt="Add a book")
# @click.argument("name")
# @click.argument("author")
# @click.argument("pages")
@click.option("--name", prompt="Name of the book")
@click.option("--author", prompt="Author of the book")
@click.option("--pages", prompt="Number of pages")

def add_book(name, author, pages):
    # book_session = connect_to()
    book_session = Session()
    book = Book(book_name=name, author=author, number_of_pages=pages)       # , date_added=datetime.now()
    book_session.add(book)
    book_session.commit()
    print(f"Added: {book.book_name}, {book.author}, {book.number_of_pages}")    # , {book.date_added}

# write out the content of the library, dump file
@kids_library.command()
# @click.option
def dump_file():
    book_session = Session()
    qu = book_session.query(Book)   #qu (=query)
    books = qu.all()
    for book in books:
        print(f"{book.id}.) Název: {book.book_name}, autor: {book.author}, počet stran: {book.number_of_pages}")    #(zadáno: {book.date_added})


if __name__ == "__main__":
    kids_library()   










# book_session = connect()
# qu = book_session.query(Book)       # qu (=query)
# print(qu.all())