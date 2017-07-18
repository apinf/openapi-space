from sqlalchemy import desc, asc
from flask import Response
from connexion import request
import yaml
import json
from datetime import datetime

from space.models import API
from .auth import check_token


def delete_api(owner, api):
    raise NotImplementedError('Handler delete_api not implemented')


def delete_api_version(owner, api, version):
    raise NotImplementedError('Handler delete_api_version not implemented')


def get_api_versions(owner, api):
    raise NotImplementedError('Handler get_api_versions not implemented')


def get_json_definition(owner, api, version):
    api = API.query.filter_by(owner=owner, name=api, version=version).first()
    if not api:
        return Response(status=404)
    token = check_token()
    if api.private and (not token or token.username != api.owner):
        return Response(status=403)
    return Response(content_type="application/json", response=api.swagger)


def get_yaml_definition(owner, api, version):
    api = API.query.filter_by(owner=owner, name=api, version=version).first()
    if not api:
        return Response(status=404)
    token = check_token()
    if api.private and (not token or token.username != api.owner):
        return Response(status=403)
    swagger = json.loads(api.swagger)
    swagger_yaml = yaml.dump(swagger)
    return Response(content_type="text/vnd.yaml", response=swagger_yaml)


def get_owner_apis(owner, sort, order):
    query = API.query.filter_by(owner=owner)
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

    query = query.order_by(order(sort))
    return [result.serialize(swagger=False) for result in query.all()]


def publish_api_version(owner, api, version):
    raise NotImplementedError('Handler publish_api_version not implemented')


def save_definition(owner, api, private, definition, force):
    token = check_token()
    if not token:
        return Response(status=403)
    if owner == 'me':
        owner = token.username
    elif token.username != owner:
        return Response(status=403)

    swagger = request.json
    if (not swagger or "info" not in swagger or
            "version" not in swagger["info"]):
        return Response(status=400)

    swagger_str = json.dumps(swagger)
    name = api
    version = swagger["info"]["version"]
    now = datetime.now()
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
    return api.serialize()


def search_apis(query, limit, offset, sort, order):
    raise NotImplementedError('Handler search_apis not implemented')
