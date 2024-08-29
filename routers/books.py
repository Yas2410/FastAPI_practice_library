from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db import models, database
from schemas import schemas
from typing import List

router = APIRouter(
    prefix="/books",
    tags=["Books"]
)


def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()


# CREATE
# Route pour la création d'un nouveau livre
@router.post("/", response_model=schemas.Book)
def create_book(book: schemas.BookCreate, db: Session = Depends(get_db)):
    db_book = models.Book(
        title=book.title,
        author=book.author,
        isbn=book.isbn
    )  # Création d'une instance du modèle Book
    db.add(db_book)  # Ajout du livre à la session
    db.commit()  # Enregistrement des changements en BDD
    db.refresh(db_book)  # Rafraîchissement de l'instance avec les données de la BDD  # noqa
    return db_book  # Retourne le livre créé


# READ
# Obtenir la liste de tous les livres
@router.get("/", response_model=List[schemas.Book])
def get_books(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    books = db.query(models.Book).offset(skip).limit(limit).all()
    return books


# READ by ID
# Route pour obtenir un livre par son ID
@router.get("/{book_id}", response_model=schemas.Book)
def get_book(book_id: int, db: Session = Depends(get_db)):
    db_book = db.query(models.Book).filter(models.Book.id == book_id).first()
    if db_book is None:
        raise HTTPException(status_code=404, detail="Livre non référencé")
    return db_book

# DELETE
# Suppression d'un livre
@router.delete("/{book_id}", response_model=schemas.Book)
def delete_book(book_id: int, db: Session = Depends(get_db)):
    db_book = db.query(models.Book).filter(models.Book.id == book_id).first()
    if db_book is None:
        raise HTTPException(status_code=404, detail="Livre non référencé")
    db.delete(db_book)
    db.commit()
    return db_book
