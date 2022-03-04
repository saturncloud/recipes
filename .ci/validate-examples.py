import json
import requests

from pathlib import Path
from typing import Any, Dict

from jsonschema import RefResolver, Validator, ValidationError
from jsonschema.validators import validator_for
from ruamel import yaml


INSTANCE_TYPE_OPTIONS_URL = "https://saturncloud.io/static/constants.yaml"

res = requests.get(url=INSTANCE_TYPE_OPTIONS_URL)
instance_type_options = yaml.safe_load(res.text)["tiers"]

schemas: Dict[str, Any] = {}
examples: Dict[str, Any] = {}


def mandatoryAdditionalProperties(schema, name):
    if "properties" not in schema:
        return
    if schema.get("additionalProperties", True):
        raise ValueError(
            "Please set additionalProperties=false everwhere! \n"
            f"* Missing in schema: {name}"
        )
    for field, value in schema["properties"].items():     
        if value.get("type") == "array":
            for item in value["items"]:
                mandatoryAdditionalProperties(item, f"{name}.{field}")
        else:
            mandatoryAdditionalProperties(value, f"{name}.{field}")

# load files
root = Path(__file__).parent.parent
for d in root.iterdir():
    if d.is_dir() and not str(d).startswith("."):
        with open(root / d / "schema.json") as f:
            schemas[str(d)] = json.load(f)
        with open(root / d / "example.json") as f:
            examples[str(d)] = json.load(f)

# validate files
for r, s in schemas.items():
    print(f"validating '{r}'...")
    mandatoryAdditionalProperties(s, r)
    resolver = RefResolver(f"{r}/schema.json", s)
    # 'sets' needs a relative import, which jsonschema doesn't natively support
    resolver.store["/resources/schema.json"] = schemas["resources"]
    resolver.store["/templates/schema.json"] = schemas["templates"]
    resolver.store["/images/schema.json"] = schemas["images"]
    validator: Validator = validator_for(s)(s, resolver)
    validator.validate(examples[r])

    # check that instance_types are valid
    recipe = examples[r]
    for resource in [
        recipe.get("jupyter_server"),
        recipe.get("deployment"),
        recipe.get("job"),
        recipe.get("rstudio_server"),
        recipe.get("dask_cluster", {}).get("worker"),
        recipe.get("dask_cluster", {}).get("scheduler")
    ]:
        if resource is not None and resource["instance_type"] not in instance_type_options:
            raise ValidationError(
                f"instance_type ('{resource['instance_type']}') is not a valid option. "
                f"Look at {INSTANCE_TYPE_OPTIONS_URL} for valid options."
            )
    print("success!")


