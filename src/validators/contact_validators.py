"""
Validators for contact management commands.

Each function validates input arguments or contact data before executing a command
by calling appropriate validation function.

Called validators may raise ValidationError with descriptive messages if
validation fails.
"""

from datetime import date

from services.address_book.phone import Phone
from validators.errors import ValidationError
from utils.date_utils import format_date_str

MSG_CONTACT_EXISTS = "Contact with username '{0}' already exists"
MSG_NO_CONTACTS = "You don't have contacts yet, but you can add one anytime."
MSG_CONTACT_NOT_FOUND = "Contact '{0}' not found"
MSG_PHONE_EXISTS = "Contact '{0}' has '{1}' phone number already."
MSG_BIRTHDAY_DUPLICATE = "Birthday for '{0}' is already set to '{1}'."


def validate_contact_not_in_contacts(username: str, contacts: dict) -> None:
    """
    Ensures the contact with the given username does not already exist (case-insensitive).

    Args:
        username (str): username key to be checked.
        contacts (dict): Existing contacts dictionary.

    Raises:
        ValidationError: If contact already exists or is in a different case.
    """
    for contact in contacts.values():
        contact_name = contact.name.value
        # Check for exact match
        if contact_name == username:
            raise ValidationError(f"{MSG_CONTACT_EXISTS.format(username)}.")

        # Check for case-insensitive match
        if contact_name.lower() == username.lower():
            raise ValidationError(
                f"{MSG_CONTACT_EXISTS.format(username)}, "
                f"but under a different name: '{contact_name}'."
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


def validate_contact_is_in_contacts(username: str, contacts: dict[str, any]) -> any:
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


def validate_phone_not_in_contact(phone_number: str, record) -> None:
    for phone_obj in record.phones:
        # Check for exact match
        if phone_obj.value == phone_number:
            raise ValidationError(MSG_PHONE_EXISTS.format(record.name, phone_number))


def validate_phone_is_in_contact(phone_number: str, record) -> tuple[int, Phone]:
    if not record.phones:
        return None

    for idx, phone in enumerate(record.phones):
        if phone.value == phone_number:
            return idx, phone

    raise ValidationError(f"Phone '{phone_number}' not found.")


def validate_birthday_duplicate(birthday: date, record):
    if birthday == record.birthday.value:
        username = record.name
        date_str = format_date_str(record.birthday.value)
        raise ValidationError(MSG_BIRTHDAY_DUPLICATE.format(username, date_str))
