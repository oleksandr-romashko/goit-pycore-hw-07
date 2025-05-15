"""
Birthday field for storing and validating birth dates.

This module defines the `Birthday` class which extends `Field` and ensures
the birth date is valid on assignment or update, following the expected format.
"""

from datetime import date

from services.address_book.field import Field

from utils.constants import BIRTHDAY_FORMAT_MSG
from utils.date_utils import format_date_str
from validators.args_validators import validate_argument_type
from validators.errors import ValidationError
from validators.field_validators import (
    validate_birthday_format,
    validate_birthday_is_in_the_past,
)


class Birthday(Field):
    """
    Class for storing and validating birth dates.

    Ensures the date matches the expected birthday format during initialization
    and on value changes.
    """

    def __init__(self, value: str | date):
        birth_date = self.__validate_date_value(value)
        super().__init__(birth_date)

    def __str__(self):
        return format_date_str(self.value)

    def __repr__(self):
        return f"{self.__class__.__name__}(value='{format_date_str(self.value)}')"

    @Field.value.setter
    def value(self, new_value: str | date):
        birth_date = self.__validate_date_value(new_value)
        self._value = birth_date

    def __validate_date_value(self, value: str | date) -> date:
        validate_argument_type(value, (str, date))
        birth_date = value
        if not isinstance(value, date):
            birth_date = validate_birthday_format(value)
        validate_birthday_is_in_the_past(birth_date)
        return birth_date


if __name__ == "__main__":
    # TESTS

    # Test data
    date_str_valid = "02.03.2000"
    date_str_with_invalid_format = "2000-03-02"
    date_str_in_the_future = "01.01.2200"

    date_obj_valid = date(2000, 3, 2)
    date_obj_in_the_future = date(2200, 1, 1)

    # Create instance with valid date string
    birthday_test_1 = Birthday(date_str_valid)
    assert isinstance(birthday_test_1.value, date)
    assert format_date_str(birthday_test_1.value) == date_str_valid

    # Create instance with invalid date format string
    try:
        Birthday(date_str_with_invalid_format)
    except ValidationError as exc:
        cause = f"Invalid provided date format '{date_str_with_invalid_format}'."
        tip = f"Use {BIRTHDAY_FORMAT_MSG} format."
        error_msg = f"{cause} {tip}"
        assert str(exc) == error_msg
    else:
        cause = "Should raise Validation error when birthday date has invalid format"
        assert False, cause

    # Create instance with invalid date string in the future
    try:
        Birthday(date_str_in_the_future)
    except ValidationError as exc:
        cause = (
            f"Given birthday date '{date_str_in_the_future}' can't be in the future."
        )
        assert str(exc) == cause
    else:
        cause = "Should raise Validation error when birthday date is in the future"
        assert False, cause

    # Direct assignment to Birthday instance value a valid date string
    birthday_test_2 = Birthday(date_str_valid)
    birthday_test_2.value = date_str_valid
    assert isinstance(birthday_test_2.value, date)
    assert format_date_str(birthday_test_2.value) == date_str_valid

    # Direct assignment to Birthday instance value an invalid date format string
    birthday_test_3 = Birthday(date_str_valid)
    try:
        birthday_test_3.value = date_str_with_invalid_format
    except ValidationError as exc:
        error_msg = (
            f"Invalid provided date format '{date_str_with_invalid_format}'. "
            f"Use {BIRTHDAY_FORMAT_MSG} format."
        )
        assert str(exc) == error_msg
    else:
        cause = (
            "Should raise Validation error "
            "when updating Birthday instance value directly with invalid date string value"
        )
        assert False, cause
    assert isinstance(birthday_test_3.value, date)
    assert format_date_str(birthday_test_3.value) == date_str_valid

    # Direct assignment to Birthday instance value an invalid date string in the future
    birthday_test_4 = Birthday(date_str_valid)
    try:
        birthday_test_4.value = date_str_in_the_future
    except ValidationError as exc:
        error_msg = (
            f"Given birthday date '{date_str_in_the_future}' can't be in the future."
        )
        assert str(exc) == error_msg
    else:
        cause = (
            "Should raise Validation error "
            "when updating Birthday instance value directly "
            "with invalid date in the future string value"
        )
        assert False, cause
    assert isinstance(birthday_test_4.value, date)
    assert format_date_str(birthday_test_4.value) == date_str_valid

    # Create instance with valid date object
    birthday_test_5 = Birthday(date_obj_valid)
    assert isinstance(birthday_test_5.value, date)
    assert format_date_str(birthday_test_5.value) == "02.03.2000"

    # Create instance with invalid date object in the future
    try:
        Birthday(date_obj_in_the_future)
    except ValidationError as exc:
        cause = "Given birthday date '01.01.2200' can't be in the future."
        assert str(exc) == cause
    else:
        cause = "Should raise Validation error when birthday date is in the future"
        assert False, cause

    # Direct assignment to Birthday instance value a valid date object
    birthday_test_6 = Birthday(date_obj_valid)
    birthday_test_6.value = "02.03.2000"
    assert isinstance(birthday_test_6.value, date)
    assert format_date_str(birthday_test_6.value) == "02.03.2000"

    # Direct assignment to Birthday instance value an invalid date object in the future
    birthday_test_7 = Birthday(date_obj_valid)
    try:
        birthday_test_7.value = date_obj_in_the_future
    except ValidationError as exc:
        error_msg = "Given birthday date '01.01.2200' can't be in the future."
        assert str(exc) == error_msg
    else:
        cause = (
            "Should raise Validation error "
            "when updating Birthday instance value directly "
            "with invalid date in the future object value"
        )
        assert False, cause
    assert isinstance(birthday_test_7.value, date)
    assert format_date_str(birthday_test_7.value) == "02.03.2000"

    print("Birthday tests passed.")
