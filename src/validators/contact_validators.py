"""
Validators for contact management commands.

Each function validates input arguments or contact data before executing a command
by calling appropriate validation function.

Called validators may raise ValidationError with descriptive messages if
validation fails.
"""
from typing import Any

from validators.field_validators import validate_username_length, validate_phone_number
from validators.errors import ValidationError

from utils.deprecation_warning import transition_warning

MSG_CONTACT_EXISTS = "Contact with username '{0}' already exists"
MSG_CONTACT_NOT_FOUND = "Contact '{0}' not found"
MSG_NO_CONTACTS = "You don't have any contacts yet, but you can add one anytime."
MSG_PHONE_EXISTS = "Contact '{0}' has '{1}' phone number already."


def validate_contact_not_in_contacts(username: str, contacts: dict) -> None:
    """
    Ensures the contact with the given username does not already exist (case-insensitive).

    Args:
        username (str): username key to be checked.
        records (dict): Existing contacts dictionary.

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
    Ensures there is at least one contact in the contacts book.

    Args:
        book (dict): Address Book dictionary.

    Raises:
        ValidationError: If no contacts exist.
    """
    if not contacts:
        raise ValidationError(MSG_NO_CONTACTS)


def validate_contact_is_in_contacts(username: str, contacts: dict) -> Any:
    """
    Ensures a contact with the provided username exists, case-insensitively.

    Args:
        username (str): username to check.
        contacts (dict): Address Book dictionary.

    Raises:
        ValidationError: If contact doesn't exist or name differs by case.
    """
    match = None
    for contact in contacts:
        if contact.lower() == username.lower():
            match = contact
            break

    if not match:
        raise ValidationError(f"{MSG_CONTACT_NOT_FOUND.format(username)}.")

    # If there's a match with a different case, let the user know
    if match != username:
        raise ValidationError(
            f"{MSG_CONTACT_NOT_FOUND.format(username)}, "
            f"but a contact exists under '{match}'. "
            f"Did you mean '{match}'?"
        )

    return contacts.get(username)


# --- Transitional functional wrappers (deprecated) ---


@transition_warning("Use 'validate_book_not_empty' from contact_validators.py instead.")
def validate_contact_not_in_contacts_wrapper(args: list[str], contacts: dict) -> None:
    """
    Transitional wrapper for ensuring the contact with the given username
    does not already exist.

    Args:
        args (list[str]): args[0] = username to be checked.
        contacts (dict): Existing contacts dictionary.
    """
    username = args[0]
    validate_contact_not_in_contacts(username, contacts)


@transition_warning(
    "Use 'validate_contact_not_in_contacts_dict' from contact_validators.py instead."
)
def validate_contacts_not_empty_wrapper(_, contacts: dict) -> None:
    """
    Transitional wrapper for ensuring there is at least one contact.

    Args:
        _ (Any): Placeholder for args, not used.
        contacts (dict): Contacts dictionary.
    """
    validate_contacts_not_empty(contacts)


@transition_warning(
    "Use 'validate_contact_is_in_contacts' from contact_validators.py instead."
)
def validate_contact_is_in_contacts_wrapper(args: list[str], contacts: dict) -> None:
    """
    Ensures a contact with the provided username exists, case-insensitively.

    Args:
        args (list[str]): args[0] = username.
        contacts (dict): Contacts dictionary.

    Raises:
        ValidationError: If contact doesn't exist or name differs by case.
    """
    username = args[0]

    # Check case-insensitive match by converting both stored and input names to lowercase
    match = None
    for contact in contacts:
        if contact.lower() == username.lower():
            match = contact
            break

    if not match:
        raise ValidationError(f"{MSG_CONTACT_NOT_FOUND.format(username)}.")

    # If there's a match with a different case, let the user know
    if match != username:
        raise ValidationError(
            f"{MSG_CONTACT_NOT_FOUND.format(username)}, "
            f"but a contact exists under '{match}'. "
            f"Did you mean '{match}'?"
        )


@transition_warning("Use 'validate_username_length' from field_validators.py instead.")
def validate_contact_username_length(args: list[str], _) -> None:
    """
    Transitional wrapper for username validation.

    Args:
        args (list[str]): args[0] = username.
        _ (Any): Placeholder for contact data (unused).
    """
    username = args[0]
    validate_username_length(username)


@transition_warning(
    "Handling of phones changed to have a list of phone objects per contact in 'Record' class"
)
def validate_not_phone_duplicate(args: list[str], contacts: dict) -> None:
    """
    Ensures the new phone number is different from the existing one.

    Args:
        args (list[str]): args[0] = username, args[1] = new phone number.
        contacts (dict): Contacts dictionary.

    Raises:
        ValidationError: If phone number hasn't changed.
    """
    username, phone_number = args
    if contacts.get(username) == phone_number:
        raise ValidationError(MSG_PHONE_EXISTS.format(username, phone_number))


@transition_warning("Use 'validate_phone_number' from field_validators.py instead.")
def validate_contact_phone_number(args: list[str], _) -> None:
    """
    Transitional wrapper for phone number validation.

    Args:
        args (list[str]): args[1] = phone number.
        _ (Any): Placeholder for contact data (unused).
    """
    phone_number = args[1]
    validate_phone_number(phone_number)
