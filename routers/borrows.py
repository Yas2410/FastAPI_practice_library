from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..db import models, database
from ..schemas import schemas
from typing import List


router = APIRouter(
    prefix="/borrows",
    tags=["Borrows"]
)


def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()


# CREATE
# Route pour créer un nouvel emprunt
@router.post("/", response_model=schemas.Borrow)
def create_borrow(borrow: schemas.BorrowCreate, db: Session = Depends(get_db)):
    db_borrow = models.Borrow(
        reader_id=borrow.reader_id,
        book_id=borrow.book_id,
        borrow_date=borrow.borrow_date,
        return_date=borrow.return_date
    )
    db.add(db_borrow)
    db.commit()
    db.refresh(db_borrow)
    return db_borrow


# READ
# Obtenir la liste de tous les emprunts
@router.get("/", response_model=List[schemas.Borrow])
def get_borrows(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    borrows = db.query(models.Borrow).offset(skip).limit(limit).all()
    return borrows


# READ by ID
# Route pour obtenir un emprunt par son ID
@router.get("/{borrow_id}", response_model=schemas.Borrow)
def get_borrow(borrow_id: int, db: Session = Depends(get_db)):
    db_borrow = db.query(models.Borrow).filter(models.Borrow.id == borrow_id).first()  # noqa
    if db_borrow is None:
        raise HTTPException(status_code=404, detail="Erreur")
    return db_borrow  # Retourne l'emprunt trouvé


# DELETE
# Suppression d'un emprunt
@router.delete("/{borrow_id}", response_model=schemas.Borrow)
def delete_borrow(borrow_id: int, db: Session = Depends(get_db)):
    db_borrow = db.query(models.Borrow).filter(models.Borrow.id == borrow_id).first()  # noqa
    if db_borrow is None:
        raise HTTPException(status_code=404, detail="Erreur")
    db.delete(db_borrow)
    db.commit()
    return db_borrow
