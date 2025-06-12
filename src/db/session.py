from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from ..config import settings

        # src/db/session.py
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from ..utils import logging  # Importer le module de journalisation


# engine = create_engine(
#     settings.DATABASE_URL, 
#     connect_args={"check_same_thread": False} if settings.DATABASE_URL.startswith("sqlite") else {}
# )
# SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base = declarative_base()

# # Dependency to get the database session
# def get_db():
#     db = SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()


# Création du moteur SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from ..config import settings  # ya lo habías corregido 👌
from ..utils import logging  # por si ya tienes el logging de las queries

# Crear el motor SQLAlchemy con la URL de la base de datos desde config.py
engine = create_engine(
    settings.DATABASE_URL,
    connect_args={"check_same_thread": False} if settings.DATABASE_URL.startswith("sqlite") else {},
    echo=settings.SQL_ECHO  # activamos el echo SQL según el config
)

# Crear la sesión local para interactuar con la BD
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Clase base para los modelos declarativos
Base = declarative_base()

# Dependencia para obtener la sesión de la BD (FastAPI usa este get_db en los endpoints)
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
