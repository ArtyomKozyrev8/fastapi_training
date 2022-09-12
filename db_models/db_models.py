from sqlalchemy.orm import relationship, backref, declarative_base
from sqlalchemy import Column, Integer, String, Sequence, ForeignKey, Table

Base = declarative_base()


book_publisher_link = Table(
    'book_publisher_link',
    Base.metadata,
    Column('book_id', Integer, ForeignKey('books.id'), primary_key=True),
    Column('publisher_id', Integer, ForeignKey('publishers.id'), primary_key=True),
)


class Publisher(Base):
    __tablename__ = "publishers"
    id = Column(Integer, primary_key=True)
    name = Column(String(100), unique=True)
    books = relationship('Book', secondary=book_publisher_link, back_populates='publishers')

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return f"Publisher({self.name})"


class Author(Base):
    __tablename__ = "authors"
    id = Column(Integer, primary_key=True)
    name = Column(String(100), unique=True)
    books = relationship("Book", back_populates="author")  # back_populates is field in Book table (author in Book)

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return f"Author({self.name})"


class Book(Base):
    __tablename__ = "books"
    id = Column(Integer, primary_key=True)
    title = Column(String(100))
    description = Column(String(255))
    author_id = Column(Integer, ForeignKey('authors.id'))
    publishers = relationship('Publisher', secondary=book_publisher_link, back_populates='books')
    author = relationship("Author", back_populates="books")

    def __init__(self, title, description=None):
        self.title = title
        self.description = description

    def __repr__(self):
        return f"Book({self.title})"
