from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from . import seeder, models, schemas
from .database import SessionLocal, engine

# create all DB tables
# now commented out because this is done with Alembic
# models.Base.metadata.create_all(bind=engine)

# instantiate FastAPI
app = FastAPI()

# instantiate DB connection session
def get_db_sesh():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()

# Root route
@app.get("/")
def index():
    return {"Hello": "World"}

# Users route
# Seeds users and returns all records in users table
@app.get("/users/")
def get_all_users():
    # We need next() to get return value from Python functions that `yield`
    # rather than `return`. This gets the actual value from the yielded
    # generator object.
    db = next(get_db_sesh())

    if db:
        seeder.seed(db)
        return db.query(models.User).all()
    else:
        return {"error": "There was a problem retrieving users"}