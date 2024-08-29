# Créer une connexion à la BDD
from sqlalchemy import create_engine
# Va définir une classe de base pour les modèles ORM 
from sqlalchemy.ext.declarative import declarative_base
# Créer une session de BDD locale
from sqlalchemy.orm import sessionmaker

# Ma BDD stockée localement
SQLALCHEMY_DATABASE_URL = "sqlite:///./fastapi-practice-lib.db"

# Création d'un moteur de connexion à la BDD
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})  # noqa

# Session locale qui va permettre d'interagir avec la BDD dans les routes FastAPI  # noqa
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Classe de base. Tous les modèles hériteront de cete classe
Base = declarative_base()
