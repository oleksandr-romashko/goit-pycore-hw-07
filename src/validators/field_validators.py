"""
Validators for field values (name, phone, etc.).

Validators raise ValidationError with descriptive messages if validation fails.
"""
import re
from datetime import date

from utils.constants import (
    NAME_MIN_LENGTH,
    NAME_MAX_LENGTH,
    MAX_DISPLAY_NAME_LEN,
    PHONE_FORMAT_DESC_STR,
    BIRTHDAY_FORMAT_MSG,
)
from utils.text_utils import truncate_string
from date_utils import parse_date, format_date_str

from validators.errors import ValidationError


def validate_username_length(username: str) -> None:
    """
    Validates username against minimum and maximum allowed lengths.

    Args:
        username (str): name to validate.

    Raises:
        ValidationError: If username is too short or too long.
    """
    username = username.strip()

    if not username:
        raise ValidationError("Username cannot be empty or just whitespace.")

    if len(username) < NAME_MIN_LENGTH:
        message_too_short = (
            f"Username '{username}' is too short "
            f"and should have at least {NAME_MIN_LENGTH} symbols."
        )
        raise ValidationError(message_too_short)

    if len(username) > NAME_MAX_LENGTH:
        truncated_username = truncate_string(
            username, max_length=MAX_DISPLAY_NAME_LEN, include_suffix_in_max_length=True
        )
        message_too_long = (
            f"Username '{truncated_username}' is too long "
            f"and should have not more than {NAME_MAX_LENGTH} symbols."
        )
        raise ValidationError(message_too_long)


def validate_phone_number(phone: str) -> None:
    """
    Validates phone number format: 10 digits, optionally prefixed with '+'.

    Args:
        phone (str): phone number to validate.

    Raises:
        ValidationError: If phone number format is invalid.
    """
    phone = phone.strip()

    if not phone:
        raise ValidationError("Phone cannot be empty or just whitespace.")

    # Remove all non-digit characters for counting digits, incl. "+" symbol
    digits_only = re.sub(r"\D", "", phone)

    if not len(digits_only) == 10:
        raise ValidationError(
            f"Invalid phone number '{phone}'. Expected {PHONE_FORMAT_DESC_STR}."
        )


def validate_birthday_format(value: str) -> date:
    """
    Validates and parses a birthday string into a date object.

    Args:
        value (str): The birthday string to validate, expected in the defined format.

    Returns:
        date: A `datetime.date` object representing the validated birthday.

    Raises:
        ValidationError: If the input does not match the expected format.
    """
    try:
        birth_date = parse_date(value)
        return birth_date
    except ValueError as exc:
        cause = f"Invalid provided date format '{value}'."
        tip = f"Use {BIRTHDAY_FORMAT_MSG} format."
        raise ValidationError(f"{cause} {tip}") from exc


def validate_birthday_is_in_the_past(birthday: date) -> None:
    """
    Validates that the given birthday date passed or today.

    Args:
        birthday (date): A `datetime.date` object representing the birthday.

    Raises:
        ValidationError: If the birthday is in the future.
    """
    today = date.today()
    if birthday > today:
        birthday_str = format_date_str(birthday)
        raise ValidationError(
            f"Given birthday date '{birthday_str}' can't be in the future."
        )
