from fastapi import APIRouter
from sql_app import seeder, models
from sql_app.database import get_db_sesh

# class that allows for separate routers (like Blueprints in Flask)
user_routes = APIRouter(
    prefix="/users",
    tags=["users"],
    responses={404: {"description": "Not found"}}
)

# Users route
# Seeds users and returns all records in users table
@user_routes.get("/")
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