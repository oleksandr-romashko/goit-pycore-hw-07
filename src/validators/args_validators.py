"""
Validators for command-line argument structure before further operations.

These functions check the number and presence of CLI arguments.
"""

from typing import Any
from datetime import date

from validators.errors import ValidationError


def validate_are_two_arguments(args: list[str], _) -> None:
    """
    Ensures two non-empty arguments are provided: username and phone number.

    Args:
        args (list[str]): args[0] = username, args[1] = phone number.
        _ (Any): Placeholder for contacts dictionary, unused here.

    Raises:
        ValidationError: If arguments are missing or empty.
    """
    if len(args) != 2 or len(args[0].strip()) == 0 or len(args[1].strip()) == 0:
        raise ValidationError(
            "You must provide two arguments, username and a phone number."
        )


def validate_is_one_argument_username(args: list[str], _) -> None:
    """
    Ensures a single non-empty argument (username) is provided.

    Args:
        args (list[str]): args[0] = username.
        _ (Any): Placeholder for contacts dictionary, unused here.

    Raises:
        ValidationError: If username is missing or empty.
    """
    if len(args) != 1 or len(args[0].strip()) == 0:
        raise ValidationError("You must provide username as a single argument.")


def validate_argument_type(obj: object, obj_type: Any | tuple) -> None:
    """
    Ensures that the provided object is of the expected type.

    Args:
        obj: The object to check.
        obj_type: The expected type or tuple of types.

    Raises:
        ValidationError: If the object's type is incorrect.
    """
    if not isinstance(obj, obj_type):
        if isinstance(obj_type, tuple):
            message = (
                f"Expected type '{', '.join([o_type.__name__ for o_type in obj_type])}', "
                f"but received type '{type(obj).__name__}'."
            )
            raise TypeError(message)

        message = f"Expected type '{obj_type.__name__}', but received type '{type(obj).__name__}'."
        raise TypeError(message)


if __name__ == "__main__":
    assert not validate_argument_type("string", str)
    assert not validate_argument_type("string", (str, date))
    assert not validate_argument_type(date(2025, 5, 13), (str, date))

    try:
        validate_argument_type({}, str)
    except TypeError as exc:
        error_msg = "Expected type 'str', but received type 'dict'."
        assert str(exc) == error_msg
    else:
        cause = "Should raise TypeError error when type is not of expected type."
        assert False, cause

    try:
        validate_argument_type([], (str, date))
    except TypeError as exc:
        error_msg = "Expected type 'str, date', but received type 'list'."
        assert str(exc) == error_msg
    else:
        cause = "Should raise TypeError error when type is not of expected types."
        assert False, cause
