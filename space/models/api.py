import json

from . import db


class API(db.Model):
    __tablename__ = "APIs"
    owner = db.Column(db.String, db.ForeignKey("Users.name"), primary_key=True)
    name = db.Column(db.String, primary_key=True)
    version = db.Column(db.String, primary_key=True)
    created = db.Column(db.DateTime)
    modified = db.Column(db.DateTime)
    private = db.Column(db.Boolean)
    published = db.Column(db.Boolean)
    swagger = db.Column(db.Text)

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def serialize(self):
        data = {
            "owner": self.owner,
            "name": self.name,
            "version": self.version,
            "created": self.created.isoformat(),
            "modified": self.modified.isoformat(),
            "private": self.private,
            "published": self.published
        }
        if len(self.swagger) > 0:
            data["swagger"] = json.loads(self.swagger)
        return data
