import bcrypt
import hashlib
from Crypto.Random import random
from datetime import datetime

from . import db


class User(db.Model):
    name = db.Column(db.String(32), primary_key=True)
    email = db.Column(db.String)
    hashed_password = db.Column(db.String)

    def set_password(self, password):
        self.hashed_password = bcrypt.hashpw(password, bcrypt.gensalt())

    def check_password(self, password):
        return self.hashed_password == bcrypt.hashpw(password,
                                                     self.hashed_password)

    def check_auth_token(self, token):
        tokenObj = AuthToken.get_token(self.name, token)
        if tokenObj.expired():
            return False
        tokenObj.refresh()
        db.session.update(tokenObj)
        return tokenObj

    # Source: https://stackoverflow.com/a/33191626
    def generate_auth_token(self,
                            length=64,
                            expiry=datetime.timedelta(days=14)):
        alnum = ''.join(c for c in map(chr, range(256)) if c.isalnum())
        token = ''.join(random.choice(alnum) for _ in range(length))
        hasher = hashlib.sha256()
        hasher.update(token)

        tokenObj = AuthToken(self.name, hasher.digest())
        tokenObj.refresh(expiry)
        db.session.add(tokenObj)


class AuthToken(db.Model):
    username = db.Column(
        db.String, db.ForeignKey("user.name"), primary_key=True)
    hashed_token = db.Column(db.String(64), primary_key=True)
    best_before = db.Column(db.DateTime)

    @classmethod
    def get_token(cls, username, token):
        hasher = hashlib.sha256()
        hasher.update(token)
        return cls.query.get(
            username=username, hashed_token=hasher.digest()).first()

    def has_expired(self):
        if datetime.now() > self.best_before:
            db.session.delete(self)
            db.session.commit()
            return True
        return False

    def refresh(self, new_time=datetime.timedelta(days=14)):
        self.best_before = datetime.now() + new_time
