"""
Validators for contact management commands.

Each function validates input arguments or contact data before executing a command
by calling appropriate validation function.

Called validators may raise ValidationError with descriptive messages if
validation fails.
"""

from typing import Any

from validators.errors import ValidationError

MSG_CONTACT_EXISTS = "Contact with username '{0}' already exists"
MSG_NO_CONTACTS = "You don't have contacts yet, but you can add one anytime."
MSG_CONTACT_NOT_FOUND = "Contact '{0}' not found"


def validate_contact_not_in_contacts(username: str, contacts: dict) -> None:
    """
    Ensures the contact with the given username does not already exist (case-insensitive).

    Args:
        username (str): username key to be checked.
        contacts (dict): Existing contacts dictionary.

    Raises:
        ValidationError: If contact already exists or is in a different case.
    """
    # Check for exact match (avoid unnecessary iteration if an exact match is found early)
    if username in contacts:
        raise ValidationError(f"{MSG_CONTACT_EXISTS.format(username)}.")

    # Check for case-insensitive match
    for existing_username in contacts:
        if existing_username.lower() == username.lower():
            raise ValidationError(
                f"{MSG_CONTACT_EXISTS.format(username)}, "
                f"but under a different name: '{existing_username}'."
            )


def validate_contacts_not_empty(contacts: dict) -> None:
    """
    Ensures that the contacts dictionary is not empty.

    Args:
        contacts (dict): Dictionary of contacts.

    Raises:
        ValidationError: If no contacts exist.
    """
    if not contacts:
        raise ValidationError(MSG_NO_CONTACTS)


def validate_contact_is_in_contacts(username: str, contacts: dict[str, Any]) -> Any:
    """
    Ensures a contact with the provided username exists, case-insensitively.

    Args:
        username (str): username to check.
        contacts (dict): Dictionary of contacts.

    Raises:
        ValidationError: If contact doesn't exist or name differs by case.
    """
    match = next((c for c in contacts if c.lower() == username.lower()), None)

    if not match:
        raise ValidationError(f"{MSG_CONTACT_NOT_FOUND.format(username)}.")

    # If there's a match with a different case, let the user know
    if match != username:
        raise ValidationError(
            f"{MSG_CONTACT_NOT_FOUND.format(username)}. "
            f"However, a contact with a similar name exists as '{match}'. "
            f"Did you mean '{match}'?"
        )

    return contacts[match]
