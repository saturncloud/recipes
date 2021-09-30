# Object schemas

With our customers increasingly interested in infrastructure-as-code and not having to use the UI, it's become apparent that
.Dockerfile-like ways of specifying objects in Saturn Cloud would be useful. This repo is to store the specifications of those

## Resources

For resources, they can be specified with one or more files:

* `saturn-resource.json` (required) - a json file that specifies how the resource should be created. This should fully encapsulate all of the parameters you can set in the UI.
* `saturn-resource-start.sh` (optional) - if easier, rather then putting the startup script in the json file it can be uploaded separately

Here is how you would validate the example using the schema for resources in Python:

```python
from jsonschema import validate
import json

with open('resources/resource-schema.json',) as f:
    schema = json.load(f)

with open('resources/example.json',) as f:
    instance = json.load(f)

validate(instance = instance, schema = schema)
```
