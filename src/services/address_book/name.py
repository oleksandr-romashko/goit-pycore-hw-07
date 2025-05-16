"""
Name field for storing and validating contact names.

This module defines the `Name` class which extends `Field` and ensures
the contact name is valid on assignment.
"""

from services.address_book.field import Field

from validators.errors import ValidationError
from validators.field_validators import validate_username_length


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

    TEST_NAME_VALID = "Alice"
    TEST_NAME_VALID_SHORTEST = "Bc"
    TEST_NAME_VALID_LONGEST = "D" * 50
    TEST_NAME_INVALID_TOO_SHORT = "A"
    TEST_NAME_INVALID_TOO_LONG = "E" * 51

    # Happy path
    name_valid_short = Name(TEST_NAME_VALID)

    # Shortest possible name
    name_valid_short = Name(TEST_NAME_VALID_SHORTEST)

    # Longest possible name
    name_valid_long = Name(TEST_NAME_VALID_LONGEST)

    # Too short name
    try:
        Name(TEST_NAME_INVALID_TOO_SHORT)
    except ValidationError as exc:
        TEST_TOO_SHORT_MSG = (
            f"Username '{TEST_NAME_INVALID_TOO_SHORT}' is too short "
            "and should have at least 2 symbols."
        )
        assert str(exc) == TEST_TOO_SHORT_MSG
    else:
        assert False, "Should raise Validation error when name is too short"

    # Too long name
    try:
        Name(TEST_NAME_INVALID_TOO_LONG)
    except ValidationError as exc:
        TEST_TOO_LONG_MSG = "Username 'EEEEEEEEEEEE...' is too long and should have not more than 50 symbols."
        assert str(exc) == TEST_TOO_LONG_MSG
    else:
        assert False, "Should raise Validation error when name is too short"

    print("Name tests passed.")
