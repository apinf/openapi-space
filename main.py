#!/usr/bin/python3
import connexion
from space.models import db

space = connexion.App("OpenAPI space", specification_dir='./')
space.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:////space.db"
space.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
space.config["SECRET_KEY"] = "Highly secret secret key"
space.add_api('swagger.yaml')
db.init_app(space)
print("Initialization complete")

if __name__ == "__main__":
    # Not running in uWSGI, run in debug mode.
    space.run(debug=True, port=8080)
