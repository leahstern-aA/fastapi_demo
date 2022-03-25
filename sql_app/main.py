from fastapi import FastAPI
from sql_app.routers import user_routes

# create all DB tables
# now commented out because this is done with Alembic
# models.Base.metadata.create_all(bind=engine)

# instantiate FastAPI
app = FastAPI()

# register routers with main application
app.include_router(user_routes)

# Root route
@app.get("/")
def index():
    return {"Hello": "World"}