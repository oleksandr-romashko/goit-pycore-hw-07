"""
Command handlers for CLI application.

Each handler corresponds to a specific user command and includes input validation,
invokes business logic, and generates an appropriate response.
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
from validators.args_validators import validate_args_have_n_arguments
from contacts.contacts_manager import add_contact, change_contact, show_phone, show_all


def handle_hello() -> str:
    """Returns a greeting message to the user."""
    # No validation checks here
    return f"{HELLO_MESSAGE}\n{APP_PURPOSE_MESSAGE}."


@input_error
def handle_add(args: list[str], book: dict) -> str:
    """
    Add a new contact.

    Expected args: [username, phone_number]
    """
    validate_args_have_n_arguments(args, 2, "username and a phone number")
    username, phone_number = args
    return add_contact(username, phone_number, book)


@input_error
def handle_change(args: list[str], book: dict) -> str:
    """
    Change an existing contact's phone number.

    Expected args: [username, old_phone_number, new_phone_number]
    """
    validate_args_have_n_arguments(
        args, 3, "username, old phone number and new phone number"
    )
    username, prev_phone_number, new_phone_number = args
    return change_contact(username, prev_phone_number, new_phone_number, book)


@input_error
def handle_phone(args: list[str], book: dict) -> str:
    """
    Return phone numbers for contacts matching the search term (partial match supported).

    Expected args: [search_term]
    """
    validate_args_have_n_arguments(args, 1, "username")
    # Partial match is supported - the check if username is in the
    # contacts list (with partial match) is not checked by validator and
    # postponed further to the handler
    search_term = args[0]
    return show_phone(search_term, book)


@input_error
def handle_all(_, book: dict) -> str:
    """Return a string listing all saved contacts and their phone numbers."""
    return show_all(book)


def handle_help() -> str:
    """Returns the help menu."""
    # No validation here
    return MENU_HELP_STR


def handle_exit(prefix="", suffix="") -> None:
    """Print a farewell message and terminate the program."""
    # No validation here
    print(f"{prefix}{EXIT_MESSAGE}{f' {suffix}' if suffix else ''}")
    sys.exit(0)


def handle_unknown() -> str:
    """Handles unknown commands by showing a fallback message."""
    # No validation here
    return f"{INVALID_COMMAND_MESSAGE}. {HELP_AWARE_TIP.capitalize()}."
