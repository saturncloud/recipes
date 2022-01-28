import json
from pathlib import Path

from jsonschema import validate


root = Path(__file__).parent.parent


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

for d in root.iterdir():
    if d.is_dir() and not str(d).startswith("."):
        print(f"validating '{d}'...")
        with open(root / d / "schema.json") as f:
            schema = json.load(f)
        with open(root / d / "example.json") as f:
            instance = json.load(f)

        mandatoryAdditionalProperties(schema, d)

        validate(instance=instance, schema=schema)
        print("success!")

