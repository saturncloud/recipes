import json
from pathlib import Path

from jsonschema import validate


root = Path(__file__).parent.parent

for d in root.iterdir():
    if d.is_dir() and not str(d).startswith("."):
        print(f"validating '{d}'...")
        with open(root / d / "schema.json") as f:
            schema = json.load(f)
        with open(root / d / "example.json") as f:
            instance = json.load(f)

        validate(instance=instance, schema=schema)
        print("success!")

