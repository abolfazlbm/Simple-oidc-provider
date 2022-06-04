import sys

import jsonschema
from jsonschema import validate

schema = {
    "type": "object",
    "properties": {
        "username": {"type": "string", "blank": False, "minLength": 2},
        "password": {"type": "string", "blank": False, "minLength": 8, "maxLength": 32},
        "email": {"type": "string", "format": "email", "pattern": "\"?([-a-zA-Z0-9.`?{}]+@\w+\.\w+)\"?",
                  "blank": False},
        "firstname": {"type": "string", "blank": False},
        "lastname": {"type": "string", "blank": False},
        "roles": {"type": "array", "items": [{"type": "string"}]}
    },
    "required": ["username", "password", "email", "firstname", "lastname", "roles"]
}


def validate_json(data):
    try:
        validate(instance=data, schema=schema)
        return True
    except jsonschema.exceptions.ValidationError as e:
        print("well-formed but invalid JSON:", e)
        return False

