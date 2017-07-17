import connexion

connexionSpace = connexion.App("OpenAPI space", specification_dir='./')
space = connexionSpace.app
space.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:////space.db"
space.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
space.config["SECRET_KEY"] = "Highly secret secret key"
connexionSpace.add_api('swagger.yaml')
