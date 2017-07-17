import bcrypt
import hashlib
from Crypto.Random import random
import datetime
import json
import base64

from . import db

DEFAULT_EXPIRY = datetime.timedelta(days=14)


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

    # Source: https://stackoverflow.com/a/33191626
    def generate_auth_token(self, length=64, expiry=DEFAULT_EXPIRY):
        alnum = ''.join(c for c in map(chr, range(256)) if c.isalnum())
        token = (''.join(random.choice(alnum) for _ in range(length)))
        hasher = hashlib.sha256()
        hasher.update(token.encode("utf-8"))
        hashed_token = hasher.digest()

        tokenObj = AuthToken(username=self.name, hashed_token=hashed_token)
        tokenObj.refresh(expiry, update=False)
        tokenObj.insert()
        return tokenObj.encode_token(non_hashed_token=token)


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
        hashed_token = hasher.digest()
        return cls.query.get((username, hashed_token))

    def expired(self):
        if datetime.datetime.now() > self.best_before:
            self.invalidate()
            return True
        return False

    def refresh(self, new_time=DEFAULT_EXPIRY, update=True):
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
        client_token_data = {
            "token": non_hashed_token,
            "user": self.username,
        }
        client_token_json = json.dumps(client_token_data)
        # json.dumps outputs a string, but base64 wants bytes.
        client_token_json = client_token_json.encode("utf-8")
        # Encode JSON with Base64
        client_token = base64.b64encode(client_token_json)
        # We don't want to use bytes for strings, so turn the base64 bytes into
        # a string.
        client_token = client_token.decode("utf-8")
        return client_token

    @classmethod
    def decode_token(cls, encoded_token):
        # Decode base64
        raw_json = base64.b64decode(encoded_token)
        # Turn decoded bytes object into a string
        raw_json = raw_json.decode("utf-8")
        # Parse the string
        token_data = json.loads(raw_json)
        # Read the data and get the token
        token = cls.get_token(token_data["user"], token_data["token"])
        return token
