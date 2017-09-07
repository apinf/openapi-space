# Copyright 2017 Apinf Oy
# This file is covered by the EUPL license.
# You may obtain a copy of the licence at
# https://joinup.ec.europa.eu/community/eupl/og_page/european-union-public-licence-eupl-v11
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# Imports for shorter import paths in other places
from .user import User, AuthToken
from .api import API
