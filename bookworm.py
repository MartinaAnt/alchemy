from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String, DateTime, Boolean, VARCHAR
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
import click
from sqlalchemy import delete

db = create_engine("sqlite:///book_worm.sqlite")
Base = declarative_base()


class Bookcase(Base):
    __tablename__ = "bookcase"

    id = Column(Integer, primary_key=True)
    title = Column(String)
    author = Column(String)
    date = Column(DateTime)
    # TODO jde vytvořit instance False/True, pokud ano, jak na to? - dokumentace sql, python class?
    # unread = Column(Boolean(), nullable=False, default=True)
    read = Column(Boolean, nullable=False, default=False
    # rating = Column(Integer)
    # note = Column(VARCHAR(1000))

    def __repr__(self):
        return f"<Bookcase(id = {self.id}, title='{self.title}', author='{self.author}', date={self.date}, " \
               f"read='{self.read}')> "


def connection():
    Base.metadata.create_all(db)
    Session = sessionmaker(bind=db)
    return Session()


# book = Bookcase(title='title', date='datetime.now()')
# print(book)

# TODO F&Q How to describe command for other users?

@click.group()
def librarian():
    pass

@librarian.command()
def report():
    session = connection()
    database = session.query(Bookcase)
    # query returns the instances of the class Bookcase
    books = database.all()
    # print(books)

    for book in books:
        print("\n")
        print(f"{book.id}. {book.title} by {book.author}, {book.date}, status: {book.read}")


@librarian.command()
@click.option('--title', prompt='Add new title ')
@click.option('--author', prompt='Written by ')
def add(title, author):
    session = connection()
    book = Bookcase(title=title, author=author, date=datetime.now())

    session.add(book)
    session.commit()

    print(f"Add title: {book.title} by {book.author}")


@librarian.command()
@click.option('--id', prompt='Which record would you like remove')
# TODO F&Q clean_id does not work, how come, syntax error?
def clean(id):
    session = connection()
    record = (delete(Bookcase).where(Bookcase.id == id).execution_options(synchronize_session="fetch"))

    session.execute(record)
    session.commit()


@librarian.command()
# TODO F&Q delete_database does not work, how come, syntax error?
def delete():
    session = connection()
    session.query(Bookcase).delete()
    session.commit()


if __name__ == "__main__":
    librarian()
