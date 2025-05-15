"""
Simple contact management module.

This module provides functions to manage a contact list using an AddressBook
instance.
It includes functionality to add new contacts, update phone numbers, and
retrieve contact details.

Functions:
- add_contact(username, phone_number, book): Adds a new contact or appends phone
  if contact exists.
- change_contact(username, prev_phone_number, new_phone_number, book): Changes
  an existing contact's phone number.
- show_phone(search_term, book): Shows the phone number(s) of a matching contact.
- show_all(book): Shows all saved contacts.
"""
from services.address_book.address_book import AddressBook
from services.address_book.record import Record


def add_contact(username: str, phone_number: str, book: AddressBook) -> str:
    """
    Add a new contact with a phone number, or append the phone if the contact already exists.

    Args:
        username (str): Name of the contact.
        phone_number (str): Phone number to add.
        book (AddressBook): The address book instance to update.

    Returns:
        str: Result message indicating success or duplication.
    """
    record: Record = book.get(username)

    if not record:
        record = Record(username)
        record.add_phone(phone_number)
        return book.add_record(record)

    return record.add_phone(phone_number)


def change_contact(
    username: str, prev_phone_number: str, new_phone_number: str, book: AddressBook
) -> str:
    """
    Update an existing contact's phone number.

    Args:
        username (str): Contact's name.
        prev_phone_number (str): Old phone number to replace.
        new_phone_number (str): New phone number to set.
        book (AddressBook): The address book instance containing the contact.

    Returns:
        str: Result message from the phone update operation.
    """
    record = book.find(username)
    return record.edit_phone(prev_phone_number, new_phone_number)


def show_phone(search_term: str, book: AddressBook) -> str:
    """
    Retrieve the phone number(s) for a contact matching the search term.

    Partial and case-insensitive matching is supported.

    Args:
        search_term (str): Search keyword (full or partial contact name).
        book (AddressBook): The address book instance to search.

    Returns:
        str: Matching contact(s) and phone number(s) as string.
    """
    return book.find_match(search_term)


def add_birthday(username: str, date: str, book: AddressBook) -> str:
    """
    Add a birthday to the specified contact.

    Args:
        username (str): Contact's name.
        date (str): Birthday in string format.
        book (AddressBook): Address book instance.

    Returns:
        str: Result message indicating success on add or update operation.
    """
    # TODO: Implement logic to parse date and assign birthday to contact
    pass


def show_birthday(username: str, book: AddressBook) -> str:
    """
    Retrieve the birthday of the specified contact.

    Args:
        username (str): Contact's name.
        book (AddressBook): Address book instance.

    Returns:
        str: Birthday string.
    """
    # TODO: Implement logic to fetch and return birthday
    pass


def show_upcoming_birthday(book: AddressBook) -> str:
    """
    Retrieve birthdays occurring in the next 7 days.

    Args:
        book (AddressBook): Address book instance.

    Returns:
        str: Formatted list of upcoming birthdays.
    """
    # TODO: Implement logic to find and display upcoming birthdays
    pass


def show_all(book: AddressBook) -> str:
    """
    Return all contacts in the address book with their phone numbers.

    Args:
        book (AddressBook): The address book instance.

    Returns:
        str: All contacts as a formatted string.
    """
    return str(book)
