from fastapi import FastAPI
from routers import readers, books, borrows
from db import models, database


# Création d'une instance de FastAPI
app = FastAPI()


# Création des tables de la BDD
models.Base.metadata.create_all(bind=database.engine)


app.include_router(readers.router)
app.include_router(books.router)
app.include_router(borrows.router)


# Route Page d'Accueil pour éviter erreur NOT FOUND
@app.get("/")
def read_root():
    return {"message": "Bienvenue !"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
