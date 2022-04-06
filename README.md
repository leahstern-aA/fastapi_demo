## FastAPI Demo
This is a basic FastAPI app built by Leah Stern while researching the framework
and its capabilities.

The app is very simple and currently just seeds a SQLite database and retrieves the
data in a route.

## Basic usage

1. `pipenv install` to set up virtual environment with dependencies in the Pipfile
2. Create a .env file with a SQLite DATABASE_URL (based on .env.example)
3. `pipenv run alembic upgrade head` to create SQLite database and tables
and apply the existing migration
4. `pipenv run uvicorn sql_app.main:app --reload` to run the application
    - You can view the application in your browser at localhost:8000

## Filesystem
```
.
└── alembic
    ├── versions       ->    Folder containing all migration version files
    ├── env.py         ->    Alembic configuration script
    ├── README         ->    Alembic README
    └── script.py.mako ->    Template for migration version files

└── sql_app
    ├── __init__.py    ->    empty
    ├── database.py    ->    SQLAlchemy setup and configuration
    ├── main.py        ->    FastAPI instantiation and routes
    ├── models.py      ->    SQLAlchemy model classes
    ├── schemas.py     ->    Pydantic schemas for data validation with models
    ├── seeder.py      ->    Seeds database
    └── sql_app.db     ->    SQLite database location, will be created automatically by Alembic

└── .env               ->    Environment variables (currently just DATABASE_URL)
└── alembic.ini        ->    Alembic's database configuration script
└── Pipfile            ->    Virtual environment dependencies
└── Pipfile.lock       ->    Metadata for virtual environment dependencies
```

## CSRF protection
CSRF protection for this app was set up using the FastAPI CSRF Protect extension:
https://github.com/aekasitt/fastapi-csrf-protect.

This is a third-party package and needs to be installed before importing. I followed
the set up instructions in the README for the FastAPI CSRF Protect project.

## SQLite and SQLAlchemy setup
The SQLite database lives here: fastapi_demo/sql_app/sql_app.db. The database URL is
specified in the .env file in the parent folder.

Boilerplate setup for integrating SQLAlchemy into this application was taken from 
the FastAPI documentation: https://fastapi.tiangolo.com/tutorial/sql-databases/

## Alembic integration
Alembic integration was made possible thanks to this tutorial: https://ahmed-nafies.medium.com/fastapi-with-sqlalchemy-postgresql-and-alembic-and-of-course-docker-f2b7411ee396

These were the steps I followed to get Alembic set up with this FastAPI application:
1. `pipenv install alembic` to install Alembic in this project's virtual environment
2. `alembic init alembic` in top level directory to initialize files/folders necessary
for migrations
3. Removed dummy value for `sqlalchemy.url` in `alembic.ini` file
4. Created .env file with DATABASE_URL inidcating path to SQLite database
5. Modified fastapi_demo/alembic/env.py file as follows:
    - Set `sqlalchemy.url` in `alembic.ini` file to DATABASE_URL from .env file:
      `config.set_main_option("sqlalchemy.url", os.environ.get("DATABASE_URL"))`
    - Assigned `target_metadata` to Base.metadata:
      `from sql_app.database import Base`
      `target_metadata = Base.metadata`
6. Ran `alembic revision —autogenerate -m “message”` in top level directory to generate
initial migration
    - Had to modify the `upgrade()` and `downgrade()` functions with the correct Alembic
      operation methods
7. Ran `alembic upgrade head` to apply the migration to the database

## Notes and issues
I ran into one issue with migrations, which is not an Alembic problem but rather an issue
with SQLite databases in general. I attempted to modify an existing column with the Alembic
`alter_column` method, but SQLite threw a syntax error when I tried applying this migration.
SQLite databases cannot alter existing columns or tables (https://www.sqlite.org/lang_altertable.html). In order to make a change like this, one must create a new table with the required change, copy all the data over from the current table, and drop the current table.