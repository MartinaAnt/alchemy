from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String, DateTime, Boolean
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker

db = create_engine("sqlite:///book_worm.sqlite")
Base = declarative_base()

# tvorba nové databáze
# engine = create_engine("mysql+pymysql://root:root@/")
# engine.execute("CREATE DATABASE book_worm") #create db
# engine.execute("USE book_work") #select new db
# eng = create_engine("mysql+pymysql://root:root@/book_worm", echo = True)


class Bookcase(Base):

    __tablename__ = "bookcase"

    name = Column(String)
    author = Column(String)
    date = Column(DateTime)
    unread = Column(Boolean, default=True)
    read = Column(Boolean, default=False)
    rating = Column(Integer)
    note = Column(String)

    def __repr__(self):
        return f"<Bookcase(title='{self.name}', date={self.date})"


book = Bookcase(text='title', date='datetime.now()')

Session = sessionmaker(bind=db)
session = Session()

query = session.query(Bookcase)
print(query.all())
