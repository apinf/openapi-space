from . import db


class API(db.Model):
    owner = db.Column(db.String, db.ForeignKey("user.name"))
    name = db.Column(db.String)
    version = db.Column(db.String)
    created = db.Column(db.DateTime)
    modified = db.Column(db.DateTime)
    swagger = db.Column(db.Text)
