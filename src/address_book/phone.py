"""
Phone field for storing and validating phone numbers.

This module defines the `Phone` class which extends `Field` and ensures
the phone number is valid on assignment or update.
"""

from field import Field
from validators.field_validators import validate_phone_number


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
