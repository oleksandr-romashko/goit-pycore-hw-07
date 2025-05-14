"""
Name field for storing and validating contact names.

This module defines the `Name` class which extends `Field` and ensures
the contact name is valid on assignment.
"""

from validators.errors import ValidationError
from validators.field_validators import validate_username_length

from .field import Field


class Name(Field):
    """
    Class for storing and validating contact names.

    Ensures the name is validated on initialization.
    """

    def __init__(self, username: str):
        username = username.strip()
        validate_username_length(username)
        super().__init__(username)


if __name__ == "__main__":
    # TESTS

    name_valid_str = "Alice"
    name_too_short_str = "A"
    name_too_long_str = "A" * 51

    name_valid = Name(name_valid_str)

    try:
        Name(name_too_short_str)
    except ValidationError as exc:
        cause = f"Username '{name_too_short_str}' is too short and should have at least 2 symbols."
        assert str(exc) == cause
    else:
        cause = "Should raise Validation error when name is too short"
        assert False, cause

    try:
        Name(name_too_long_str)
    except ValidationError as exc:
        cause = "Username 'AAAAAAAAAAAA...' is too long and should have not more than 50 symbols."
        assert str(exc) == cause
    else:
        cause = "Should raise Validation error when name is too short"
        assert False, cause

    print("Name tests passed.")
