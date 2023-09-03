# psqldb.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import toml

secrets = toml.load(".streamlit/secrets.toml")
# DATABASE_URI = (f"{secrets['postgresql']['dialect']}://{secrets['postgresql']['user']}:{secrets['postgresql']['password']}@"
#                 f"{secrets['postgresql']['host']}:{secrets['postgresql']['port']}/{secrets['postgresql']['database']}")
# DATABASE_URI =  "postgres://radhakrishnan:Smo1k1H9nUNsFn7TxNj1d97M6B0QgLCv@dpg-ciqhei59aq0dcpts1ij0-a.oregon-postgres.render.com:5432/demao"
DATABASE_URI =  "postgresql://radhakrishnan:Smo1k1H9nUNsFn7TxNj1d97M6B0QgLCv@dpg-ciqhei59aq0dcpts1ij0-a.oregon-postgres.render.com:5432/demao"

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
