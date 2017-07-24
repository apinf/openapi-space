import yaml
from swagger_spec_validator.validator20 import validate_spec


def test_validate_spec():
    with open("swagger.yaml", "r") as stream:
        specification = yaml.load(stream)
    swagger_resolver = validate_spec(specification)
    assert swagger_resolver.referrer['info']['title'] == 'OpenAPI space'
