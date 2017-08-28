# Copyright 2017 Apinf Oy
# This file is covered by the EUPL license.
# You may obtain a copy of the licence at
# https://joinup.ec.europa.eu/community/eupl/og_page/european-union-public-licence-eupl-v11
import requests
from space.app import config


def login(username, password):
    payload = {"username": username, "password": password}
    r = requests.post("%s/login" % (config["apinf_base_url"]), data=payload)
    response = r.json()
    if ("data" in response and response.get("status", "error") == "success"):
        data = response["data"]
        if "userId" in data and "authToken" in data:
            return (data["userId"], data["authToken"])
    return (None, None)


def check_token(userID, authToken):
    headers = {"X-User-Id": userID, "X-Auth-Token": authToken}
    r = requests.get("%s/users" % (config["apinf_base_url"]), headers=headers)
    response = r.json()
    if ("data" in response and response.get("status", "error") == "success" and
            len(response["data"]) > 0):
        user = response["data"][0]
        if "username" not in user or "emails" not in user:
            return None
        email = ""
        for emailObj in user["emails"]:
            if emailObj.get("verified", False):
                email = emailObj.get("address", "")
                break
        return (user["username"], email)
    return (None, None)
