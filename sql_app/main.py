from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from fastapi_csrf_protect import CsrfProtect
from fastapi_csrf_protect.exceptions import CsrfProtectError
from pydantic import BaseModel

from sql_app.routers import user_routes, auth_routes

import os

# create all DB tables
# now commented out because this is done with Alembic
# models.Base.metadata.create_all(bind=engine)

# instantiate FastAPI
app = FastAPI()

# register routers with main application
app.include_router(user_routes)
app.include_router(auth_routes)

# CSRF settings class, loads secret key from .env
class CsrfSettings(BaseModel):
    secret_key : str = os.environ.get("SECRET_KEY")

# loads CsrfSettings class into CsrfProtect configuration
@CsrfProtect.load_config
def get_csrf_config():
    return CsrfSettings()

# Root route
@app.get("/")
def index():
    return {"Hello": "World"}

"""
Route for custom CSRF protection exception handling.

If a CSRF exception is encountered in another route, that route simply needs
to raise a CsrfProtectError with a status_code and message, for example:

if condition:
    raise CsrfProtectError(status_code=404, message="Something went wrong!")

and it will be rerouted to and handled by this exception handler route.
"""
@app.exception_handler(CsrfProtectError)
def csrf_exception_handler(request: Request, exception: CsrfProtectError):
    return JSONResponse(
        status_code=exception.status_code,
        content={"error": exception.message}
    )