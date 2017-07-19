from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# Imports for shorter import paths in other places
from .user import User, AuthToken
from .api import API
