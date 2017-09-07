# Copyright 2017 Apinf Oy
# This file is covered by the EUPL license.
# You may obtain a copy of the licence at
# https://joinup.ec.europa.eu/community/eupl/og_page/european-union-public-licence-eupl-v11
import connexion
import yaml

with open("config.yaml", "r") as stream:
    config = yaml.load(stream)

connexionSpace = connexion.App("OpenAPI space", specification_dir="./")

space = connexionSpace.app
space.config["SQLALCHEMY_DATABASE_URI"] = config["database_uri"]
space.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
space.config["BASE_URL"] = config["base_url"]
space.config["SECRET_KEY"] = config["secret_key"]

connexionSpace.add_api("swagger.yaml")
