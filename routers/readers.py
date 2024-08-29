# Import des modules FastAPI pour la création des routes
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..db import models, database
from ..schemas import schemas
# Pour la gestion des mots de passe
from ..db.hash import get_password_hash
from typing import List

# Création d'un routeur pour regrouper les routes liées aux lecteurs (readers)
router = APIRouter(
    prefix="/readers",
    tags=["Readers"]
)


def get_db():
    # Création d'une nouvelle session
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close() # Fermeture de la session après la fin de la requête  # noqa


# CREATE
# Route pour la création d'un nouveau lecteur
@router.post("/", response_model=schemas.Reader)
def create_reader(reader: schemas.ReaderCreate, db: Session = Depends(get_db)):
    hashed_password = get_password_hash(reader.password)  # Hash du mdp
    db_reader = models.Reader(
        first_name=reader.first_name,
        last_name=reader.last_name,
        email=reader.email,
        password=hashed_password.password
    )  # Création d'une instance du modèle Reader
    db.add(db_reader)  # Ajout du lecteur à la session
    db.commit()  # Enregistrement des changements en BDD
    db.refresh(db_reader)
    return db_reader


# READ
# Obtenir la liste de tous les lecteurs
@router.get("/", response_model=List[schemas.Reader])
def get_readers(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    readers = db.query(models.Reader).offset(skip).limit(limit).all()
    return readers


# UPDATE
# Modification
@router.get("/{reader_id}", response_model=schemas.Reader)
def get_reader(reader_id: int, db: Session = Depends(get_db)):
    db_reader = db.query(models.Reader).filter(models.Reader.id == reader_id).first()  # Recherche du lecteur par ID  # noqa
    if db_reader is None:
        raise HTTPException(status_code=404, detail="Lecteur non référencé")  # Erreur 404 si le lecteur n'existe pas  # noqa
    return db_reader  # Retourne le lecteur trouvé


# DELETE
# Suppression d'un lecteur
@router.delete("/{reader_id}", response_model=schemas.Reader)
def delete_reader(reader_id: int, db: Session = Depends(get_db)):
    db_reader = db.query(models.Reader).filter(models.Reader.id == reader_id).first()  # noqa
    if db_reader is None:
        raise HTTPException(status_code=404, detail="Lecteur non référencé")
    db.delete(db_reader)  # Suppression du lecteur de la session de base de données  # noqa
    db.commit()  # Enregistrement des changements
    return db_reader
