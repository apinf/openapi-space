from flask import Response
from connexion import request

from space.integration import apinf
from space.models import User, AuthToken


def login():
    body = request.json
    user = User.query.get(body["username"])
    if not user:
        return Response(status=404)
    elif not user.check_password(body["password"]):
        return Response(status=401)
    return {"token": user.generate_auth_token(), "username": user.name}


def login_apinf_token():
    body = request.json
    return check_apinf_token(body["user_id"], body["auth_token"])


def login_apinf():
    body = request.json
    (user_id, auth_token) = apinf.login(body["username"], body["password"])
    if not user_id:
        return Response(status=401)
    return check_apinf_token(user_id, auth_token)


def check_apinf_token(user_id, auth_token):
    (username, email) = apinf.check_token(user_id, auth_token)
    if not username:
        return Response(status=401)

    username = "apinf:%s" % username
    user = User.query.get(username)
    if not user:
        # Email left out because of uniqueness problems
        user = User(
            name=username,
            hashed_password="",
            email="%s@remote_login/apinf" % username)
        user.insert()
    return {"token": user.generate_auth_token(), "username": user.name}


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
    username = body["username"]
    if ":" in username:
        return Response(status=400)
    email = body["email"]
    if "@" not in email:
        return Response(status=400)

    user = User(name=username, email=email)
    user.set_password(body["password"])
    user.insert()
    return {"token": user.generate_auth_token(), "username": user.name}
