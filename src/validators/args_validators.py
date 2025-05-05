"""
Validators for command-line argument structure before further operations.

These functions check the number and presence of CLI arguments.
"""

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
