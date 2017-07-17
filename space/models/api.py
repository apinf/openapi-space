from . import db


class API(db.Model):
    __tablename__ = "APIs"
    owner = db.Column(db.String, db.ForeignKey("Users.name"), primary_key=True)
    name = db.Column(db.String, primary_key=True)
    version = db.Column(db.String)
    created = db.Column(db.DateTime)
    modified = db.Column(db.DateTime)
    swagger = db.Column(db.Text)
