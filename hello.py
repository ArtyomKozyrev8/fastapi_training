from typing import Optional, List

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

from db_models import Base, Book, Publisher, Author

from random import randint

DB_URL = "postgresql+psycopg2://some_user:some_pswd@127.0.0.1:9798/fastapi_training_db"


f = lambda: randint(10000, 99999)


def create_book(
        db: Session,
        title: str,
        description: Optional[str] = None,
) -> Book:
    book = Book(title=title, description=description)
    db.add(book)
    db.commit()
    db.refresh(book)
    return book


def update_book(
    db: Session,
    book_id: int,
    author_id: Optional[str] = None,
    publisher_ids: Optional[List[int]] = None,
    title: Optional[str] = None,
    description: Optional[str] = None,
) -> Book:
    book = db.query(Book).filter(Book.id == book_id).one_or_none()
    if book is None:
        raise Exception("Oh no! No such book!")

    if author_id is not None:
        book.author_id = author_id

    if title is not None:
        book.title = title

    if description is not None:
        book.description = description

    if publisher_ids is not None:
        publishers = []
        for i in publisher_ids:
            publisher = db.query(Publisher).filter(Publisher.id == i).one_or_none()
            if publisher is None:
                raise Exception("Oh no! No such publisher!")
            publishers.append(publisher)

        book.publishers = publishers

    db.commit()
    db.refresh(book)
    return book


def get_books_all(db: Session) -> List:
    res = db.query(Book).all()

    res = [
        {
            "id": i.id,
            "title": i.title,
            "description": i.description,
            "author": (lambda x: {"id": x.id, "name": x.name} if x is not None else x)(i.author),
            "publishers": [{"id": p.id, "name": p.name} for p in i.publishers]
        } for i in res
    ]
    return res

def create_author(db: Session, name: str) -> Author:
    author = Author(name=name)
    db.add(author)
    db.commit()
    db.refresh(author)
    return author


def create_publisher(db: Session, name: str) -> Publisher:
    publisher = Publisher(name=name)
    db.add(publisher)
    db.commit()
    db.refresh(publisher)
    return publisher


def update_publisher(db: Session, publisher_id: int, name: Optional[str] = None) -> Publisher:
    publisher = db.query(Publisher).filter(Publisher.id == publisher_id).one_or_none()
    if publisher is None:
        raise Exception("Oh no! No such publisher!")

    if name is not None:
        publisher.name = name

    db.commit()
    db.refresh(publisher)
    return publisher


def update_author(db: Session, author_id: int, name: Optional[str] = None) -> Author:
    author = db.query(Author).filter(Author.id == author_id).one_or_none()

    if author is None:
        raise Exception("Oh no! No such author!")

    if name is not None:
        author.name = name

    db.commit()
    db.refresh(author)
    return author


if __name__ == '__main__':
    engine = create_engine(DB_URL, echo=False)
    SessionLocal: Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)()
    Base.metadata.create_all(bind=engine)

    # SessionLocal.add(x)
    # SessionLocal.commit()
    # SessionLocal.refresh(x)
    # print(x.id)

    author = create_author(SessionLocal, f"Sam-{f()}")
    print(author.books, author.id)
    book = create_book(SessionLocal, f"The Book-{f()}")
    print(book.id, book.publishers, book.author)
    publisher_1 = create_publisher(SessionLocal, f"The Publisher-{f()}")
    print(publisher_1.id, publisher_1.books, publisher_1.name)
    publisher_2 = create_publisher(SessionLocal, f"The Publisher-{f()}")
    print(publisher_2.id, publisher_2.books, publisher_2.name)

    new_book = update_book(
        SessionLocal,
        book_id=book.id,
        author_id=author.id,
        title="Title!",
        description="Title ! Desc !",
        publisher_ids=[publisher_1.id, publisher_2.id],
    )
    print(new_book.author, new_book.author_id, new_book.description)

    r = get_books_all(SessionLocal)

    print("*" * 100)
    for i in r:
        print(i)

    SessionLocal.execute("DROP TABLE IF EXISTS users ;")
    SessionLocal.commit()
