import bcrypt
import hashlib
from Crypto.Random import random
import datetime
import json
import base64

from . import db


class User(db.Model):
    __tablename__ = "Users"
    name = db.Column(db.String(32), primary_key=True)
    email = db.Column(db.String, unique=True)
    hashed_password = db.Column(db.String)

    def set_password(self, password):
        self.hashed_password = bcrypt.hashpw(
            password.encode("utf-8"), bcrypt.gensalt())

    def check_password(self, password):
        return self.hashed_password == bcrypt.hashpw(
            password.encode("utf-8"), self.hashed_password)

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def check_auth_token(self, token):
        tokenObj = AuthToken.get_token(self.name, token)
        if tokenObj.expired():
            return False
        tokenObj.refresh()
        return tokenObj

    # Source: https://stackoverflow.com/a/33191626
    def generate_auth_token(self,
                            length=64,
                            expiry=datetime.timedelta(days=14)):
        alnum = ''.join(c for c in map(chr, range(256)) if c.isalnum())
        token = ''.join(random.choice(alnum) for _ in range(length))
        hasher = hashlib.sha256()
        non_hashed_token = token.encode(encoding="utf-8")
        hasher.update(non_hashed_token)
        hashed_token = hasher.digest()

        tokenObj = AuthToken(username=self.name, hashed_token=hashed_token)
        tokenObj.refresh(expiry, update=False)
        tokenObj.insert()
        return tokenObj.encode_token(non_hashed_token)


class AuthToken(db.Model):
    __tablename__ = "AuthTokens"
    username = db.Column(
        db.String, db.ForeignKey("Users.name"), primary_key=True)
    hashed_token = db.Column(db.String(64), primary_key=True)
    best_before = db.Column(db.DateTime)

    @classmethod
    def get_token(cls, username, token):
        hasher = hashlib.sha256()
        hasher.update(token.encode("utf-8"))
        return cls.query.get((username, hasher.digest()))

    def expired(self):
        if datetime.datetime.now() > self.best_before:
            self.invalidate()
            return True
        return False

    def refresh(self, new_time=datetime.timedelta(days=14), update=True):
        self.best_before = datetime.datetime.now() + new_time
        if update:
            db.session.commit()

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def invalidate(self):
        db.session.delete(self)
        db.session.commit()

    def encode_token(self, non_hashed_token):
        return base64.b64encode(
            json.dumps({
                "token": non_hashed_token.decode("utf-8"),
                "user": self.username,
                #                "best_before": self.best_before
            }).encode("utf-8")).decode("utf-8")

    @classmethod
    def decode_token(cls, encoded_token):
        raw_json = base64.b64decode(encoded_token).decode("utf-8")
        token_data = json.loads(raw_json)
        token = cls.get_token(token_data["user"], token_data["token"])
        return token
