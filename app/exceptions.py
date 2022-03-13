from pydantic.errors import PydanticValueError


class FieldNotFoundError(PydanticValueError):
    code = "not_found.field"
    msg_template = "{msg}"

class InvalidFilterError(PydanticValueError):
    code = "invalid.filter"
    msg_template = "{msg}"
