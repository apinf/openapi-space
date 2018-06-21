# Copyright 2017 Apinf Oy
# This file is covered by the EUPL license.
# You may obtain a copy of the licence at
# https://joinup.ec.europa.eu/community/eupl/og_page/european-union-public-licence-eupl-v11
from sqlalchemy import desc, asc, or_
from flask import Response
from connexion import request
import yaml
import json
from datetime import datetime

from space.models import API
from .auth import check_token


def get_owner(token, request_owner):
    if token and (request_owner == 'me' or request_owner == token.username):
        return (token.username, True)
    return (request_owner, False)


def serialize_api_meta_list(api_list, show_private=False):
    return [
        api_meta.serialize(swagger=False) for api_meta in api_list
        if show_private or not api_meta.private
    ]


def parse_order(order, sort):
    if order == "DESC":
        order = desc
    else:
        order = asc

    if sort == "NAME":
        sort = API.name
    elif sort == "CREATED":
        sort = API.created
    elif sort == "UPDATED":
        sort = API.updated
    elif sort == "OWNER":
        sort = API.owner

    return order(sort)


def delete_api(owner, api):
    (owner, is_own) = get_owner(check_token(), owner)
    if not is_own:
        return Response(status=403)

    deleted = []
    for version in API.query.filter_by(owner=owner, name=api):
        deleted.push(version.serialize())
        version.delete()
    return deleted


def delete_api_version(owner, api, version):
    (owner, is_own) = get_owner(check_token(), owner)
    if not is_own:
        return Response(status=403)

    num_of_versions = API.query.filter_by(owner=owner, name=api).count()
    if num_of_versions == 0:
        return Response(status=404)
    elif num_of_versions < 2:
        return Response(status=409)
    api = API.query.get((owner, api, version))
    if not api:
        return Response(status=404)
    api.delete()
    return api.serialize()


def get_api_versions(owner, api):
    token = check_token()
    (owner, show_private) = get_owner(token, owner)

    versions = API.query.filter_by(owner=owner, name=api).all()
    return serialize_api_meta_list(versions)


def get_json_definition(owner, api, version):
    token = check_token()
    (owner, show_private) = get_owner(token, owner)
    api = API.query.get((owner, api, version))
    if not api:
        return Response(status=404)
    elif api.private and not show_private:
        return Response(status=403)
    return Response(content_type="application/json", response=api.swagger)


def get_yaml_definition(owner, api, version):
    token = check_token()
    (owner, show_private) = get_owner(token, owner)
    api = API.query.get((owner, api, version))
    if not api:
        return Response(status=404)
    elif api.private and not show_private:
        return Response(status=403)
    try:
        swagger = json.loads(api.swagger)
        swagger_yaml = yaml.dump(swagger)
    except ValueError:
        return Response(status=500)
    return Response(content_type="text/vnd.yaml", response=swagger_yaml)


def get_owner_apis(owner, sort, order):
    token = check_token()
    (owner, show_private) = get_owner(token, owner)

    query = API.query.filter_by(owner=owner).order_by(parse_order(order, sort))

    return serialize_api_meta_list(query.all(), show_private)


def publish_api_version(owner, api, version):
    (owner, is_own) = get_owner(check_token(), owner)
    if not is_own:
        return Response(status=403)

    api = API.query.get((owner, api, version))
    if not api:
        return Response(status=404)
    elif api.published:
        return Response(status=409)
    api.published = True
    api.update()
    return Response(status=200)


def save_definition(owner, api, private, force):
    (owner, is_own) = get_owner(check_token(), owner)
    if not is_own:
        return Response(status=403)

    swagger = request.json
    if (not swagger or "info" not in swagger or
            "version" not in swagger["info"]):
        return Response(status=400)

    swagger_str = json.dumps(swagger)
    name = api
    version = swagger["info"]["version"]
    now = datetime.now()
    api = API.query.get((owner, api, version))
    if not api:
        api = API(
            owner=owner,
            name=name,
            version=version,
            created=now,
            modified=now,
            private=private,
            published=False,
            swagger=swagger_str)
        api.insert()
        return api.serialize(), 201
    else:
        if api.published and not force:
            return Response(status=409)
        api.swagger = swagger_str
        api.modified = now
        if type(private) == bool:
            api.private = private
        api.update()
    return api.serialize()


def search_apis(query, limit, offset, sort, order):
    searchterm = '%{0}%'.format(query)
    query = API.query \
        .filter(or_(API.owner.like(searchterm), API.name.like(searchterm))) \
        .order_by(parse_order(order, sort)) \
        .offset(offset) \
        .limit(limit).all()
    return serialize_api_meta_list(query)
