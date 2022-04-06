from fastapi import APIRouter, Form, Request, Depends

from fastapi_csrf_protect import CsrfProtect
from fastapi_csrf_protect.exceptions import CsrfProtectError

from sql_app import models
from sql_app.database import get_db_sesh

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
def signup(request: Request, first: str = Form(...), last: str = Form(...), csrf_protect: CsrfProtect = Depends()):
    # try to get CSRF token from request header and validate it. Otherwise raise CsrfProtectError to be handled by
    # the csrf_protection_handler route
    try:
        csrf_token = csrf_protect.get_csrf_from_headers(request)
        csrf_protect.validate_csrf(csrf_token)
    except:
        raise CsrfProtectError(status_code=500, message="Could not validate CSRF token!")

    # get database session
    db = next(get_db_sesh())

    # add new user to databse
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