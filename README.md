# Object schemas

With our customers increasingly interested in infrastructure-as-code and not having to use the UI, it's become apparent that
.Dockerfile-like ways of specifying objects in Saturn Cloud would be useful. This repo is to store the specifications of those

## Resources

For resources, they can be specified with one or more files:

* `recipe.json` (required) - a json file that specifies how the resource should be created. This should fully encapsulate all of the parameters you can set in the UI.

Here is how you would validate the example using the schema for resources in Python:

```python
import json
from jsonschema import validate

with open('resources/schema.json') as f:
    schema = json.load(f)

with open('resources/example.json') as f:
    instance = json.load(f)

validate(instance=instance, schema=schema)
```
