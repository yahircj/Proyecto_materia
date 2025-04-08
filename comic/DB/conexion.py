import os
from sqlalchemy import create_engine
from sqlalchemy.orm.session import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# Nombre de la base de datos
dbName = "usuarios.sqlite"

# Ruta absoluta del directorio actual (DB/)
base_dir = os.path.dirname(os.path.realpath(__file__))

# URL completa del archivo SQLite
dbURL = f"sqlite:///{os.path.join(base_dir, dbName)}"

# Crear motor de conexión con SQLAlchemy
engine = create_engine(dbURL, echo=True)  # echo=True muestra las consultas SQL en consola

# Crear sesión
Session = sessionmaker(bind=engine)

# Base declarativa para modelos ORM
Base = declarative_base()