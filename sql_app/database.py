from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

# SQLite DB, .db file located in current directory
# Get from .env file
SQLALCHEMY_DATABASE_URL = os.environ.get("DATABASE_URL")

"""
Create SQLAlchemy engine

`check_same_thread` only required for SQLite dbs. By default only one
thread can communicate with a SQLite db. We need to turn this default
off so that FastAPI can use multithreaded DB connections.
"""
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

# Each instance of this class will be a db session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# DB models will inherit from this class to produce Table objects
# and appropriate mapper() calls
Base = declarative_base()

# instantiate DB connection session
def get_db_sesh():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()