"""
Field base class for storing values in contact records.

This module defines the base `Field` class used for contact fields.
It provides basic storage and string conversion behavior.
"""

from dataclasses import dataclass
from typing import Any


@dataclass(repr=False)
class Field:
    """
    Base class for contact record fields.

    Stores a single value and provides a default string representation.
    """

    _value: Any

    def __str__(self):
        return str(self.value)

    def __repr__(self):
        return f"{self.__class__.__name__}(value='{str(self.value)}')"

    @property
    def value(self):
        """
        Retrieves the stored value of the field.

        This property provides read access to the internal `_value` attribute,
        which represents the field's content. It is used by subclasses to access
        or override the behavior of getting a field's value.

        Returns:
            Any: The current value stored in the field.
        """
        return self._value

    @value.setter
    def value(self, new_value):
        self._value = new_value


if __name__ == "__main__":
    # TESTS

    TEST_VALUE_1 = "value1"
    TEST_VALUE_2 = "value2"

    field_1 = Field(TEST_VALUE_1)
    field_2 = Field(TEST_VALUE_2)

    assert str(field_1) == TEST_VALUE_1
    assert str(field_2) == TEST_VALUE_2

    assert field_1 == Field(TEST_VALUE_1)

    print("Field tests passed.")
