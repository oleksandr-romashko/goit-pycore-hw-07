"""
Phone field for storing and validating phone numbers.

This module defines the `Phone` class which extends `Field` and ensures
the phone number is valid on assignment or update.
"""

from field import Field
from validators.field_validators import validate_phone_number
from validators.errors import ValidationError


class Phone(Field):
    """
    Class for storing and validating phone numbers.

    Ensures the phone number matches expected format during initialization and
    value changes.
    """

    def __init__(self, phone_number: str):
        self._validate_phone(phone_number)
        super().__init__(phone_number)

    def update_phone(self, phone_number: str):
        """Sets a new validated phone value."""
        self._validate_phone(phone_number)
        self.value = phone_number

    def _validate_phone(self, phone_number: str):
        validate_phone_number(phone_number)


if __name__ == "__main__":
    PHONE_NUMBER_STR = "1234567890"
    phone_1 = Phone(PHONE_NUMBER_STR)
    assert phone_1.value == PHONE_NUMBER_STR

    try:
        phone_2 = Phone("123")
    except ValidationError as exc:
        error_msg = (
            "Invalid phone number '123'. "
            "Expected 10 digits, optionally starting with '+'."
        )
        assert str(exc) == error_msg
    else:
        cause = (
            "Should raise Validation error "
            "when creating Phone object with invalid phone number value"
        )
        assert False, cause

    print("Phone tests passed.")
