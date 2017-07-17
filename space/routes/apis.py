def delete_api(request, owner, api):
    raise NotImplementedError('Handler delete_api not implemented')


def delete_api_version(request, owner, api, version):
    raise NotImplementedError('Handler delete_api_version not implemented')


def get_api_versions(request, owner, api):
    raise NotImplementedError('Handler get_api_versions not implemented')


def get_json_definition(request, owner, api, version):
    raise NotImplementedError('Handler get_json_definition not implemented')


def get_owner_apis(request, owner, sort, order):
    raise NotImplementedError('Handler get_owner_apis not implemented')


def get_yaml_definition(request, owner, api, version):
    raise NotImplementedError('Handler get_yaml_definition not implemented')


def publish_api_version(request, owner, api, version):
    raise NotImplementedError('Handler publish_api_version not implemented')


def save_definition(request, owner, api, isPrivate, definition, force):
    raise NotImplementedError('Handler save_definition not implemented')


def search_apis(request, query, limit, offset, sort, order):
    raise NotImplementedError('Handler search_apis not implemented')
