"""
Phone field for storing and validating phone numbers.

This module defines the `Phone` class which extends `Field` and ensures
the phone number is valid on assignment or update.
"""

from validators.errors import ValidationError
from validators.field_validators import validate_phone_number

from .field import Field


class Phone(Field):
    """
    Class for storing and validating phone numbers.

    Ensures the phone number matches expected format during initialization and
    value changes.
    """

    def __init__(self, phone_number: str):
        self._validate_phone_number(phone_number)
        super().__init__(phone_number)

    def update_phone(self, phone_number: str):
        """Sets a new validated phone value."""
        self._validate_phone_number(phone_number)
        self.value = phone_number

    @Field.value.setter
    def value(self, new_value: str):
        self._validate_phone_number(new_value)
        self._value = new_value

    def _validate_phone_number(self, phone_number: str):
        validate_phone_number(phone_number)


if __name__ == "__main__":
    # TESTS

    # Test data
    phone_valid_number_str_1 = "1234567890"
    phone_valid_number_str_2 = "0987654321"
    phone_invalid_number_value = "123"

    # Create instance with valid phone number
    phone_test_1 = Phone(phone_valid_number_str_1)
    assert phone_test_1.value == phone_valid_number_str_1

    # Create instance with invalid phone number
    try:
        Phone(phone_invalid_number_value)
    except ValidationError as exc:
        error_msg = (
            f"Invalid phone number '{phone_invalid_number_value}'. "
            "Expected 10 digits, optionally starting with '+'."
        )
        assert str(exc) == error_msg
    else:
        cause = (
            "Should raise Validation error "
            "when creating Phone instance with invalid phone number value"
        )
        assert False, cause

    # Direct assignment to Phone instance value a valid phone number
    phone_test_2 = Phone(phone_valid_number_str_1)
    phone_test_2.value = phone_valid_number_str_2
    assert phone_test_2.value == phone_valid_number_str_2

    # Direct assignment to Phone instance value an invalid phone number
    phone_test_3 = Phone(phone_valid_number_str_1)
    try:
        phone_test_3.value = phone_invalid_number_value
    except ValidationError as exc:
        error_msg = (
            f"Invalid phone number '{phone_invalid_number_value}'. "
            "Expected 10 digits, optionally starting with '+'."
        )
        assert str(exc) == error_msg
    else:
        cause = (
            "Should raise Validation error "
            "when updating Phone instance value directly "
            "with invalid phone number value"
        )
        assert False, cause
    assert phone_test_3.value == phone_valid_number_str_1

    # Update instance with valid phone number
    phone_test_4 = Phone(phone_valid_number_str_1)
    phone_test_4.update_phone(phone_valid_number_str_2)
    assert phone_test_4.value == phone_valid_number_str_2

    # Update instance with invalid phone number
    phone_test_5 = Phone(phone_valid_number_str_1)
    try:
        phone_test_5.update_phone(phone_invalid_number_value)
    except ValidationError as exc:
        error_msg = (
            f"Invalid phone number '{phone_invalid_number_value}'. "
            "Expected 10 digits, optionally starting with '+'."
        )
        assert str(exc) == error_msg
    else:
        cause = (
            "Should raise Validation error "
            "when updating Phone instance with invalid phone number value"
        )
        assert False, cause

    print("Phone tests passed.")
