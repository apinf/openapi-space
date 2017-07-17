#!/usr/bin/python3
from space.app import space
from space.models import db

db.init_app(space)
print("Initialization complete")

if __name__ == "__main__":
    # Not running in uWSGI, run in debug mode.
    space.run(debug=True, port=8080)
