"""
Command handlers for the Assistant Bot.

Each handler corresponds to a user command and includes input validation,
business logic, and response generation.
"""

import sys

from utils.constants import (
    HELLO_MESSAGE,
    APP_PURPOSE_MESSAGE,
    INVALID_COMMAND_MESSAGE,
    MENU_HELP_STR,
    HELP_AWARE_TIP,
    EXIT_MESSAGE,
)
from decorators.input_error import input_error
from validators.args_validators import (
    validate_are_two_arguments,
    validate_is_one_argument_username,
)
from validators.contact_validators import (
    validate_contact_not_in_contacts_wrapper,
    validate_contact_is_in_contacts_wrapper,
    validate_contact_username_length,
    validate_contact_phone_number,
    validate_not_phone_duplicate,
    validate_contacts_not_empty_wrapper,
)
from contacts.contacts_manager import add_contact, change_contact, show_phone, show_all


def handle_hello() -> str:
    """Returns a hello message to the user."""
    # No validation checks here
    return f"{HELLO_MESSAGE}\n{APP_PURPOSE_MESSAGE}."


@input_error
def handle_add(args: list[str], contacts: dict[str, str]) -> str:
    """Adds a new contact after validation."""
    validate_are_two_arguments(args, contacts)
    validate_contact_username_length(args, contacts)
    validate_contact_phone_number(args, contacts)
    validate_contact_not_in_contacts_wrapper(args, contacts)
    return add_contact(args, contacts)


@input_error
def handle_change(args: list[str], contacts: dict[str, str]) -> str:
    """Changes an existing contact's number after validation."""
    validate_are_two_arguments(args, contacts)
    validate_contact_phone_number(args, contacts)
    validate_contact_is_in_contacts_wrapper(args, contacts)
    validate_not_phone_duplicate(args, contacts)
    return change_contact(args, contacts)


@input_error
def handle_phone(args: list[str], contacts: dict[str, str]) -> str:
    """Returns phone numbers matching the username (partial match supported)."""
    validate_is_one_argument_username(args, contacts)
    # Partial match is supported - the check if username is in the
    # contacts list (with partial match) is not checked by validator and
    # postponed further to the handler function
    return show_phone(args, contacts)


@input_error
def handle_all(args: list[str], contacts: dict[str, str]) -> str:
    """Displays all saved contacts after validation."""
    validate_contacts_not_empty_wrapper(args, contacts)
    return show_all(args, contacts)


def handle_help() -> str:
    """Returns the help menu."""
    # No validation here
    return MENU_HELP_STR


def handle_exit(prefix="", suffix="") -> None:
    """Prints exit message and exits the program."""
    # No validation here
    print(f"{prefix}{EXIT_MESSAGE}{f' {suffix}' if suffix else ''}")
    sys.exit(0)


def handle_unknown() -> str:
    """Handles unknown commands by showing a fallback message."""
    # No validation here
    return f"{INVALID_COMMAND_MESSAGE}. {HELP_AWARE_TIP.capitalize()}."
