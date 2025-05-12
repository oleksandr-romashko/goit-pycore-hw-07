"""
Birthday field for storing and validating birth dates.

This module defines the `Birthday` class which extends `Field` and ensures
the birth date is valid on assignment or update, following the expected format.
"""

from field import Field
from validators.errors import ValidationError
from validators.field_validators import validate_birthday_date
from utils.constants import BIRTHDAY_FORMAT_MSG


class Birthday(Field):
    """
    Class for storing and validating birth dates.

    Ensures the date matches the expected birthday format during initialization and
    on value changes.
    """

    def __init__(self, value: str):
        date = validate_birthday_date(value)
        super().__init__(date)


if __name__ == "__main__":
    # TESTS

    valid_date = "02.03.2000"
    date_with_invalid_format = "2000-03-02"

    valid_birthday = Birthday(valid_date)

    date_invalid_format_result = None
    try:
        date_invalid_format_result = Birthday(date_with_invalid_format)
    except ValidationError as exc:
        cause = f"Invalid provided date format '{date_with_invalid_format}'."
        tip = f"Use {BIRTHDAY_FORMAT_MSG} format."
        error_msg = f"{cause} {tip}"
        assert str(exc) == error_msg
    else:
        cause = "Should raise Validation error when birthday date has invalid format"
        assert False, cause

    print("Birthday tests passed.")
