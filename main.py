#!/usr/bin/python3
from flask import Flask
from space.models import db

space = Flask("OpenAPI space")
space.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:////space.db"
space.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
space.config["SECRET_KEY"] = "Highly secret secret key"
db.init_app(space)
print("Initialization complete")

if __name__ == "__main__":
    # Not running in uWSGI, run in debug mode.
    space.run(debug=True, port=8080)
