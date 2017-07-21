import yaml
from swagger_spec_validator.validator20 import validate_spec
with open("swagger.yaml", "r") as stream:
    specification = yaml.load(stream)
validate_spec(specification)
