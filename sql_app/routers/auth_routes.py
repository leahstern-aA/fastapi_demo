from fastapi import APIRouter, Form, Request
from sql_app import seeder, models
from sql_app.database import get_db_sesh
from fastapi.responses import HTMLResponse

# class that allows for separate routers (like Blueprints in Flask)
auth_routes = APIRouter(
    prefix="/auth",
    tags=["auth"],
    responses={404: {"description": "Not found"}}
)

"""
POST route for signup. Posts signup form and adds the new user to the database.

Uses the Form class from FastAPI. Note that the form fields are parameters to
the view function.

NOTE: currently, this app does not include a frontend nor SSR, so you'll need
to use Postman or a similar platform to send this POST request
"""
@auth_routes.post("/signup/")
def signup(first: str = Form(...), last: str = Form(...)):
    db = next(get_db_sesh())

    if db:
        new_user = models.User(
            first_name=first,
            last_name=last
        )

        db.add(new_user)
        db.commit()

        return new_user.to_dict()
    else:
        return {"error": "There was a problem creating this user."}