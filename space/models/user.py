import bcrypt
from itsdangerous import (TimedJSONWebSignatureSerializer as Serializer,
                          BadSignature, SignatureExpired)
from . import db

SECRET_KEY = "replaceme"


class User(db.Model):
    name = db.Column(db.String(32), primary_key=True)
    email = db.Column(db.String)
    hashed_password = db.Column(db.String)

    def set_password(self, password):
        self.hashed_password = bcrypt.hashpw(password, bcrypt.gensalt())

    def check_password(self, password):
        return self.hashed_password == bcrypt.hashpw(password,
                                                     self.hashed_password)

    def generate_auth_token(self, expiration=600):
        s = Serializer(SECRET_KEY, expires_in=expiration)
        return s.dumps({'username': self.name})

    @staticmethod
    def read_auth_token(token):
        s = Serializer(SECRET_KEY)
        try:
            data = s.loads(token)
        except SignatureExpired:
            # Token expired
            return None
        except BadSignature:
            # Invalid token
            return None
        return User.query.get(name=data['username']).first()
