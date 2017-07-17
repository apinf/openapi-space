def delete_api(owner, api):
    raise NotImplementedError('Handler delete_api not implemented')


def delete_api_version(owner, api, version):
    raise NotImplementedError('Handler delete_api_version not implemented')


def get_api_versions(owner, api):
    raise NotImplementedError('Handler get_api_versions not implemented')


def get_json_definition(owner, api, version):
    raise NotImplementedError('Handler get_json_definition not implemented')


def get_owner_apis(owner, sort, order):
    raise NotImplementedError('Handler get_owner_apis not implemented')


def get_yaml_definition(owner, api, version):
    raise NotImplementedError('Handler get_yaml_definition not implemented')


def publish_api_version(owner, api, version):
    raise NotImplementedError('Handler publish_api_version not implemented')


def save_definition(owner, api, isPrivate, definition, force):
    raise NotImplementedError('Handler save_definition not implemented')


def search_apis(query, limit, offset, sort, order):
    raise NotImplementedError('Handler search_apis not implemented')
