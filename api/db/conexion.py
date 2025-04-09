import os
from sqlalchemy import create_engine
from sqlalchemy.orm.session import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# Nombre de la base de datos
dbHost = os.getenv("DB_HOST")
dbPort = os.getenv("DB_PORT", 3306)
dbUser = os.getenv("DB_USER")
dbPassword = os.getenv("DB_PASSWORD")
dbName = os.getenv("DB_NAME")

# URL completa del archivo SQLite
dbURL = f"mysql+mysqlconnector://{dbUser}:{dbPassword}@{dbHost}:{dbPort}/{dbName}"

# Crear motor de conexión con SQLAlchemy
engine = create_engine(dbURL, echo=True)  # echo=True muestra las consultas SQL en consola

# Crear sesión
Session = sessionmaker(bind=engine)

# Base declarativa para modelos ORM
Base = declarative_base()