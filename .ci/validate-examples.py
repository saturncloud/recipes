import json
from pathlib import Path
from typing import Any, Dict

from jsonschema import RefResolver, Validator
from jsonschema.validators import validator_for


schemas: Dict[str, Any] = {}
examples: Dict[str, Any] = {}

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
    resolver = RefResolver(f"{r}/schema.json", s)
    # 'resource-sets' needs a relative import, which jsonschema doesn't natively support
    if r == "resource-sets":
        resolver.store["/resources/schema.json"] = schemas["resources"]
    validator: Validator = validator_for(s)(s, resolver)
    validator.validate(examples[r])
    print("success!")

