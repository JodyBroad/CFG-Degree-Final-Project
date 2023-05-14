# db is initialised seperately here to avoid circular imports as so many other modules depend on it

# SQLAlchemy is how we link to the db
from flask_sqlalchemy import SQLAlchemy

# creating a db accessible via the app
db = SQLAlchemy()
