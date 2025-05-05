"""
Field base class for storing values in contact records.

This module defines the base `Field` class used for contact fields.
It provides basic storage and string conversion behavior.
"""

from dataclasses import dataclass
from typing import Any


@dataclass
class Field:
    """
    Base class for contact record fields.

    Stores a single value and provides a default string representation.
    """

    _value: Any

    def __str__(self):
        return str(self.value)

    def __repr__(self):
        return str(self.value)

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, new_value):
        self._value = new_value


if __name__ == "__main__":
    # TESTS

    value_1 = "value1"
    value_2 = "value2"

    field_1 = Field(value_1)
    field_2 = Field(value_2)

    assert str(field_1) == value_1
    assert str(field_2) == value_2

    print("All tests passed.")
