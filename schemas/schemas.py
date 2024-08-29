from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime


class ReaderBase(BaseModel):
    first_name: str
    last_name: str
    email: str


class ReaderCreate(ReaderBase):
    password: str


class Reader(ReaderBase):
    id: int
    borrows: List["Borrow"] = []  # Liste des livres empruntés associés au lecteur  # noqa

    class Config:
        orm_mode = True


class BookBase(BaseModel):
    title: str
    author: str
    isbn: str


class BookCreate(BookBase):
    pass


class Book(BookBase):
    id: int
    borrows: List["Borrow"] = []  # Liste des emprunts associés au livre

    class Config:
        orm_mode = True


class BorrowBase(BaseModel):
    borrow_date: datetime
    return_date: Optional[datetime]


class BorrowCreate(BorrowBase):
    reader_id: int
    book_id: int


class Borrow(BorrowBase):
    id: int
    reader: Reader
    book: Book


class Config:
    orm_mode = True
