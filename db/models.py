from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base


class Reader(Base):
    # Nom de la table
    __tablename__ = "readers"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String, index=True)
    last_name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String)

    # Relationship = Relations entre les tables
    # Ici par exemple, un lecteur peut avoir plusieurs emprunts
    borrows = relationship("Borrow", back_populates="reader")


class Book(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    author = Column(String, index=True)
    isbn = Column(String, unique=True, index=True)

    borrows = relationship("Borrow", back_populates="book")


# Table supplémentaire pour simplifier la gestion des relations
class Borrow(Base):
    __tablename__ = "borrows"

    id = Column(Integer, primary_key=True, index=True)
    reader_id = Column(Integer, ForeignKey("readers.id")) # Ajout d'une clé étrangère pour identifier le lecteur  # noqa
    book_id = Column(Integer, ForeignKey("books.id"))  # Idem pour identifier le livre  # noqa
    borrow_date = Column(DateTime)
    return_date = Column(DateTime)

    reader = relationship("Reader", back_populates="borrows")  # Relation avec Reader  # noqa
    book = relationship("Book", back_populates="borrows")  # Relation avec Book
