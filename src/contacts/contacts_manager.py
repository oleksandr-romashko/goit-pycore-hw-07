"""
Simple contact management module.

This module provides basic functions to manage a contact list,
including adding, updating, and displaying contact phone numbers.

Functions:
- add_contact(args, contacts): Adds a new contact.
- change_contact(args, contacts): Changes an existing contact's phone number.
- show_phone(args, contacts): Shows the phone number of a contact.
- show_all(_, contacts): Shows all saved contacts.
"""
from utils.deprecation_warning import transition_warning


@transition_warning("Use 'add_record' from address_book.py instead.")
def add_contact(args: list[str], contacts: dict[str, str]) -> str:
    """Add a new contact with username and phone number.

    args: [username, phone]
    """
    username, phone = args
    contacts[username] = phone
    return "Contact added."


@transition_warning("Use 'edit_phone' from record.py instead.")
def change_contact(args: list[str], contacts: dict[str, str]) -> str:
    """Update the phone number of an existing contact.

    args: [username, new_phone]
    """
    username, phone = args
    contacts[username] = phone
    return "Contact updated."


@transition_warning("Use 'find_with_partial_match' of address_book instance instead.")
def show_phone(args: list[str], contacts: dict[str, str]) -> str:
    """
    Display the phone number(s) for the specified contact
    (case-insensitive, partial match allowed).

    args: [search_term]
    """
    search_term = args[0].lower()
    matches = []

    for username, phone in contacts.items():
        # case-insensitive, partial match
        if search_term.lower() in username.lower():
            matches.append((username, phone))

    if not matches:
        return "No matches found."

    # Find length of the longest username for alignment
    max_len = max(len(username) for username, _ in matches)

    # Create aligned output
    output_lines = [
        f"  {username.ljust(max_len)} : {phone}" for username, phone in matches
    ]
    return (
        f"Found {len(matches)} match{'es' if len(matches) != 1 else ''}:\n"
        + "\n".join(output_lines)
    )


@transition_warning("Use string representation of address_book instance instead.")
def show_all(_: list[str], contacts: dict[str, str]) -> str:
    """Return all saved contacts with their phone numbers."""
    # Find length of the longest username for alignment
    max_len = max(len(username) for username in contacts)

    # Create aligned output
    output_lines = [
        f"  {username.ljust(max_len)} : {phone}" for username, phone in contacts.items()
    ]
    return (
        f"You have {len(contacts)} contact{'s' if len(contacts) != 1 else ''}:\n"
        + "\n".join(output_lines)
    )
