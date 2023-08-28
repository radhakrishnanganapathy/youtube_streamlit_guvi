# psqldb.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import toml

secrets = toml.load(".streamlit/secrets.toml")
DATABASE_URI = (f"{secrets['postgresql']['dialect']}://{secrets['postgresql']['user']}:{secrets['postgresql']['password']}@"
                f"{secrets['postgresql']['host']}:{secrets['postgresql']['port']}/{secrets['postgresql']['database']}")
engine = create_engine(DATABASE_URI)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def CreateTables():
    Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
