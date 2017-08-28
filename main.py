#!/usr/bin/python3
# Copyright 2017 Apinf Oy
# This file is covered by the EUPL license.
# You may obtain a copy of the licence at
# https://joinup.ec.europa.eu/community/eupl/og_page/european-union-public-licence-eupl-v11
from space.app import space
from space.models import db

db.init_app(space)
with space.test_request_context():
    db.create_all()
print("Initialization complete")

if __name__ == "__main__":
    # Not running in uWSGI, run in debug mode.
    space.run(debug=True, port=8080)
