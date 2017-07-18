from flask import Response
from connexion import request
from space.models import User, AuthToken


def login():
    body = request.json
    if not body["username"] or not body["password"]:
        return Response(status=400)

    user = User.query.get(body["username"])
    if not user:
        return Response(status=404)
    elif not user.check_password(body["password"]):
        return Response(status=401)
    return {"token": user.generate_auth_token()}


def logout():
    token = check_token()
    if not token:
        return Response(status=403)
    token.invalidate()
    return Response(status=200)


def check_token():
    if "Authorization" not in request.headers:
        return None
    encoded_token = request.headers["Authorization"]
    if not encoded_token:
        return None
    token = AuthToken.decode_token(encoded_token)
    if not token or token.expired():
        return None
    token.refresh()
    return token


def ping():
    if not check_token():
        return Response(status=403)
    return Response(status=200)


def register():
    body = request.json
    if not body["username"] or not body["email"] or not body["password"]:
        return Response(status=400)

    user = User(name=body["username"], email=body["email"])
    user.set_password(body["password"])
    user.insert()
    return {"token": user.generate_auth_token()}
