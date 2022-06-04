import jsonschema
from jsonschema import validate

schema = {
    "type": "object",
    "properties": {
        "name": {"type": "string", "blank": False, "minLength": 4},
        "description": {"type": "string", "blank": False, "minlenght": 4}
    },

    "required": ["name", "description"]
}


def validate_json(data):
    try:
        validate(instance=data, schema=schema)
        return True
    except jsonschema.exceptions.ValidationError as e:
        print("well-formed but invalid JSON:", e)
        return False
