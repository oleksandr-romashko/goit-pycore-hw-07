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
    Instances of Field are compared based on their stored value.
    """

    _value: Any

    def __str__(self):
        return str(self.value)

    def __repr__(self):
        return f"{self.__class__.__name__}(value={repr(self.value)})"

    @property
    def value(self) -> Any:
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
    def value(self, new_value: Any) -> None:
        self._value = new_value


if __name__ == "__main__":
    # TESTS

    TEST_VALUE_STR = "some_value"
    TEST_VALUE_DATE = 42

    test_field_str = Field(TEST_VALUE_STR)
    assert isinstance(test_field_str.value, str)
    assert str(test_field_str) == TEST_VALUE_STR
    assert test_field_str == Field(TEST_VALUE_STR)  # __eq__ override test
    assert repr(test_field_str) == "Field(value='some_value')"  # __repr__ override test

    test_field_int = Field(TEST_VALUE_DATE)
    assert isinstance(test_field_int.value, int)
    assert str(test_field_int) == str(TEST_VALUE_DATE)
    assert test_field_int == Field(TEST_VALUE_DATE)  # __eq__ override test
    assert repr(test_field_int) == "Field(value=42)"  # __repr__ override test

    print("Field tests passed.")
