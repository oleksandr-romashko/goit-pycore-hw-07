"""
Module for managing an address book of contact records.

This module defines the AddressBook class, which serves as a container
and manager for multiple contact records. It supports adding, retrieving,
searching, and displaying records. Each record typically includes a name
and a list of associated phone numbers.
"""
from datetime import date, timedelta
from collections import UserDict

from utils.date_utils import is_leap_year, parse_date, format_date_str
from validators.errors import ValidationError
from validators.args_validators import validate_argument_type
from validators.contact_validators import (
    validate_contacts_not_empty,
    validate_contact_not_in_contacts,
    validate_contact_is_in_contacts,
)

from .record import Record

MSG_CONTACT_ADDED = "Contact added."
MSG_CONTACT_DELETED = "Contact deleted."
MSG_NO_MATCHES = "No matches found."
MSG_HAVE_CONTACTS = "You have {0} contact{1}"
MSG_FOUND_MATCHES = "Found {0} match{1}"


class AddressBook(UserDict):
    """
    A class for storing and managing contact records.

    Attributes:
        data (dict): A dictionary where keys are contact names and values are Record objects.

    Functionality:
        - Add new contacts
        - Find contacts by name or phone
        - Delete contacts
        - Display all records in aligned output
    """

    def __str__(self) -> str:
        """
        Returns a nicely formatted string listing all contacts with aligned phone numbers.

        Raises:
            ValidationError: If the address book is empty.
        """
        validate_contacts_not_empty(self.data)

        # Format output with title
        count = len(self.data)
        suffix = "" if count == 1 else "s"
        title = f"{MSG_HAVE_CONTACTS.format(count, suffix)}"
        contact_lines = self._format_records(self.data.values())
        output = f"{title}:\n{'\n'.join(contact_lines)}"

        return output

    def add_record(self, contact: Record) -> str:
        """
        Adds a new contact record to the address book.

        Args:
            contact (Record): The contact to add.

        Raises:
            ValidationError: If the contact already exists.

        Returns:
            str: A message confirming the addition.
        """
        validate_argument_type(contact, Record)

        # Prevent from overwriting existing entities
        validate_contact_not_in_contacts(contact.name.value, self.data)

        self.data[contact.name.value] = contact
        return MSG_CONTACT_ADDED

    def find(self, username: str) -> Record:
        """
        Finds a contact by name.

        Args:
            username (str): Partial or full name to search for (case-insensitive).

        Raises:
            ValidationError: If no contacts are found or the name is not found.

        Returns:
            Record: The matching contact.
        """
        validate_contacts_not_empty(self.data)
        contact = validate_contact_is_in_contacts(username, self.data)
        return contact

    def find_match(self, search_term: str = "") -> str:
        """
        Searches for contacts by name or phone number.

        Args:
            search_term (str): The term to search for (partial, case-insensitive match).

        Raises:
            ValidationError: If address book is empty.

        Returns:
            str: A formatted list of matches or a no matches message.
        """
        validate_contacts_not_empty(self)

        matches = []

        if not search_term:
            matches = list(self.data.values())
        else:
            for username, record in self.data.items():
                if search_term.lower() in username.lower():
                    matches.append(record)
                else:
                    if any(search_term in phone.value for phone in record.phones):
                        matches.append(record)

        if not matches:
            return MSG_NO_MATCHES

        # Sort found matches alphabetically by name
        matches.sort(key=lambda record: record.name.value.lower())

        # Create aligned contacts output
        contact_lines = self._format_records(matches)

        # Format output with title
        count = len(matches)
        suffix = "" if count == 1 else "es"
        search_prompt = f"'{search_term}'" if search_term else "empty search"
        title = f"{MSG_FOUND_MATCHES.format(count, suffix)} for {search_prompt}"
        output = f"{title}:\n{'\n'.join(contact_lines)}"

        return output

    def delete(self, username: str) -> str:
        """
        Deletes a contact from the address book.

        Args:
            username (str): Name of the contact to delete.

        Raises:
            ValidationError: If the contact does not exist.

        Returns:
            str: A message confirming deletion.
        """
        validate_contact_is_in_contacts(username, self.data)

        self.data.pop(username)
        return MSG_CONTACT_DELETED

    def get_upcoming_birthdays(
        self, today: str = None, upcoming_period_days: int = 7
    ) -> list[dict[str, str]]:
        """
        Returns a list of users who have birthdays within the upcoming period from today.

        Each user is a dict with keys "name" and "birthday" in format "YYYY.MM.DD".
        The returned list contains dicts with "name" and the upcoming
        "congratulation_date" in string format (YYYY-MM-DD).

        :param users: List of users with "name" and "birthday" keys.
        :param today: The date to start checking from (default: current date).
        :param upcoming_period_days: Number of days ahead to check for birthdays (default: 7).
        :return: List of users with upcoming birthdays sorted by date.
        """
        # Assign today each time function is called, not once during function definition
        if today is None:
            today_obj = date.today()
        else:
            today_obj = parse_date(today)

        # Empty data guard
        if not self.data:
            return []

        user_congratulations = []

        for record in self.data.values():
            # Retrieve birthday object
            birthday = record.birthday

            # Guard records without birthdays assigned
            if not birthday:
                continue

            # Handle the case if birthday is today or upcoming
            # Handle the case for February 29 birthday
            if birthday.value.month == 2 and birthday.value.day == 29:
                if is_leap_year(today_obj.year):
                    # For leap years, keep February 29
                    congratulation_date = birthday.value.replace(year=today_obj.year)
                else:
                    # For non-leap years, set birthday to March 1
                    congratulation_date = birthday.value.replace(
                        year=today_obj.year, month=3, day=1
                    )
            else:
                # For other birthdays, just replace the year
                congratulation_date = birthday.value.replace(year=today_obj.year)

            # Handle the case if birthday has passed, adjust to next year
            if congratulation_date < today_obj:
                # If it's a February 29 birthday in a non-leap year, adjust it to March 1 of next year
                if congratulation_date.month == 2 and congratulation_date.day == 29:
                    if not is_leap_year(today_obj.year + 1):
                        congratulation_date = congratulation_date.replace(
                            year=today_obj.year + 1, month=3, day=1
                        )
                    else:
                        congratulation_date = congratulation_date.replace(
                            year=today_obj.year + 1
                        )
                else:
                    # Otherwise just move it to the next year
                    congratulation_date = congratulation_date.replace(
                        year=today_obj.year + 1
                    )

            # Filter dates in upcoming period range and add them to the congratulations list
            if (
                today_obj
                <= congratulation_date
                <= today_obj + timedelta(upcoming_period_days)
            ):

                # Shift weekend congratulation to the following Monday
                if congratulation_date.weekday() == 5:  # Saturday
                    congratulation_date += timedelta(days=2)
                elif congratulation_date.weekday() == 6:  # Sunday
                    congratulation_date += timedelta(days=1)

                # Add congratulation to the list
                user_congratulations.append(
                    {
                        "name": record.name.value,
                        "congratulation_date": congratulation_date,
                    }
                )

        # Sort congratulations by date
        user_congratulations.sort(key=lambda user: user["congratulation_date"])

        # Convert congratulations date to string date representation
        for user in user_congratulations:
            user["congratulation_date"] = format_date_str(user["congratulation_date"])

        return user_congratulations

    def _format_records(self, records: list[Record], offset: str = "  ") -> list[str]:
        max_len = max(len(record.name.value) for record in records)
        return [
            (
                f"{offset}{record.name.value.ljust(max_len)} : "
                f"{'; '.join(phone.value for phone in record.phones)}"
            )
            for record in records
        ]


if __name__ == "__main__":
    # Basic tests to verify AddressBook logic

    # Setup
    record_1 = Record("Alice")
    record_1.add_phone("1234567890")

    record_2 = Record("Bob")
    record_2.add_phone("9876543210")
    record_2.add_phone("7233232321")

    record_3 = Record("Alex")
    record_3.add_phone("9875554446")

    record_empty = Record("NoPhone")

    # Create book instance
    book = AddressBook()
    assert len(book.data) == 0

    # Test __str__ with 0 records
    book_str_0_contacts_msg = (
        "You don't have any contacts yet, but you can add one anytime."
    )
    try:
        str(book)
    except ValidationError as exc:
        assert str(exc) == book_str_0_contacts_msg
    else:
        assert False, "Should raise Validation error"

    # Test add contact - incorrect type
    try:
        result_add_incorrect_type = book.add_record(object())
    except TypeError as exc:
        incorrect_type_msg = "Expected type 'Record', but received type 'object'."
        assert str(exc) == incorrect_type_msg
    else:
        assert False, "Should raise TypeError error when incorrect type"
    assert len(book.data) == 0

    # Test add contact - first contact
    result_add_1 = book.add_record(record_1)
    assert result_add_1 == MSG_CONTACT_ADDED
    assert len(book.data) == 1

    # Test __str__ with 1 record
    book_str_1_contact_msg = "You have 1 contact:\n" "  Alice : 1234567890"
    assert str(book) == book_str_1_contact_msg

    # Test add contact - second contact
    book.add_record(record_2)
    assert len(book.data) == 2

    # Test __str__ with 2 records
    book_str_2_contacts_msg = (
        "You have 2 contacts:\n"
        "  Alice : 1234567890\n"
        "  Bob   : 9876543210; 7233232321"
    )
    assert str(book) == book_str_2_contacts_msg

    # Test add contact - record with empty phones as third contact
    book.add_record(record_empty)
    assert len(book.data) == 3

    # Test __str__ with 3 records
    book_str_3_contacts_msg = (
        "You have 3 contacts:\n"
        "  Alice   : 1234567890\n"
        "  Bob     : 9876543210; 7233232321\n"
        "  NoPhone : "
    )

    # Test add contact - add existing contact
    try:
        book.add_record(record_2)
    except ValidationError as exc:
        contact_already_exists_msg = "Contact with username 'Bob' already exists."
        assert str(exc) == contact_already_exists_msg
    else:
        assert False, "Should raise Validation error"
    assert len(book.data) == 3

    # Test find - found contact
    found_contact = book.find("Alice")
    assert found_contact.name.value == "Alice"
    assert found_contact.phones == record_1.phones

    # Test find - contact not found
    try:
        book.find("Unknown_name")
    except ValidationError as exc:
        not_found_msg = "Contact 'Unknown_name' not found."
        assert str(exc) == not_found_msg
    else:
        assert False, "Should raise Validation error"

    # Test find match - search for username match
    # single result
    match_username_term = "Al"
    match_username_msg = (
        f"{MSG_FOUND_MATCHES.format(1, '')} for '{match_username_term}':\n"
        "  Alice : 1234567890"
    )
    match_username_result = book.find_match(match_username_term)
    assert match_username_result == match_username_msg
    # multiple results
    book.add_record(record_3)
    match_username_msg = (
        f"{MSG_FOUND_MATCHES.format(2, 'es')} for '{match_username_term}':\n"
        "  Alex  : 9875554446\n"
        "  Alice : 1234567890"
    )
    match_username_result = book.find_match(match_username_term)
    assert match_username_result == match_username_msg

    # Test find match - search for phone number match
    # single result
    match_phone_single_term = "876"
    match_phone_number_msg_1 = (
        f"{MSG_FOUND_MATCHES.format(1, '')} for '{match_phone_single_term}':\n"
        "  Bob : 9876543210; 7233232321"
    )
    match_phone_result = book.find_match(match_phone_single_term)
    assert match_phone_result == match_phone_number_msg_1
    # multiple results
    match_phone_multiple_term = "987"
    match_phone_number_msg_2 = (
        f"{MSG_FOUND_MATCHES.format(2, 'es')} for '{match_phone_multiple_term}':\n"
        "  Alex : 9875554446\n"
        "  Bob  : 9876543210; 7233232321"
    )
    match_phone_result = book.find_match(match_phone_multiple_term)
    assert match_phone_result == match_phone_number_msg_2

    # Test find match - no matches
    match_unknown_term = "unknown"
    match_unknown_number_msg = MSG_NO_MATCHES
    match_unknown_result = book.find_match(match_unknown_term)
    assert match_unknown_result == match_unknown_number_msg

    # Test find match - empty term
    match_empty_term = ""
    match_empty_term_msg = (
        "Found 4 matches for empty search:\n"
        "  Alex    : 9875554446\n"
        "  Alice   : 1234567890\n"
        "  Bob     : 9876543210; 7233232321\n"
        "  NoPhone : "
    )
    match_empty_result = book.find_match(match_empty_term)
    assert match_empty_result == match_empty_term_msg

    # Test delete contact
    assert len(book.data) == 4
    try:
        book.delete("unknown_when_with_contacts")
    except ValidationError as exc:
        assert str(exc) == "Contact 'unknown_when_with_contacts' not found."
    else:
        assert False, "Should raise Validation error"
    assert len(book.data) == 4

    try:
        book.delete("alex")
    except ValidationError as exc:
        assert (
            str(exc)
            == "Contact 'alex' not found, but a contact exists under 'Alex'. Did you mean 'Alex'?"
        )
    else:
        assert False, "Should raise Validation error"
    assert len(book.data) == 4

    try:
        book.delete("     Alex   ")
    except ValidationError as exc:
        assert str(exc) == "Contact '     Alex   ' not found."
    else:
        assert False, "Should raise Validation error"
    assert len(book.data) == 4

    result_delete_1 = book.delete("Alex")
    assert result_delete_1 == MSG_CONTACT_DELETED
    assert "Alex" not in book.data
    assert len(book.data) == 3

    result_delete_2 = book.delete("Alice")
    assert result_delete_2 == MSG_CONTACT_DELETED
    assert "Alice" not in book.data
    assert len(book.data) == 2

    result_delete_3 = book.delete("Bob")
    assert result_delete_3 == MSG_CONTACT_DELETED
    assert "Bob" not in book.data
    assert len(book.data) == 1

    result_delete_4 = book.delete("NoPhone")
    assert result_delete_4 == MSG_CONTACT_DELETED
    assert "NoPhone" not in book.data
    assert len(book.data) == 0

    try:
        book.delete("unknown_when_no_contacts")
    except ValidationError as exc:
        assert str(exc) == "Contact 'unknown_when_no_contacts' not found."
    else:
        assert False, "Should raise Validation error"
    assert len(book.data) == 0

    # Test __str__ with 0 records after all have been deleted
    book_str_0_contacts_after_deletion_msg = (
        "You don't have any contacts yet, but you can add one anytime."
    )
    try:
        str(book)
    except ValidationError as exc:
        assert str(exc) == book_str_0_contacts_after_deletion_msg
    else:
        assert False, "Should raise Validation error"

    # Test birthdays
    book_birthdays = AddressBook()

    birthday_record_no_birthday = Record("David")

    birthday_record_1 = Record("Alice")
    birthday_record_1.add_birthday("04.01.2001")

    birthday_record_2 = Record("Bob")
    birthday_record_2.add_birthday("01.01.2002")

    birthday_record_3 = Record("Charlie")
    birthday_record_3.add_birthday("31.12.2003")

    # birthdays - test no records ends up empty list
    birthdays_empty_expected = []
    birthdays_empty_result = book_birthdays.get_upcoming_birthdays()
    assert birthdays_empty_expected == birthdays_empty_result

    # birthdays - test record with no birthday are ignored
    book_birthdays.add_record(birthday_record_no_birthday)
    birthdays_no_birthday_expected = []
    birthdays_no_birthday_result = book_birthdays.get_upcoming_birthdays()
    assert birthdays_no_birthday_expected == birthdays_no_birthday_result

    # birthdays - test single record + move birthday from weekend to closest weekday
    book_birthdays.add_record(birthday_record_1)
    birthdays_one_expected = [{"name": "Alice", "congratulation_date": "06.01.2025"}]
    birthdays_one_result = book_birthdays.get_upcoming_birthdays(today="01.01.2025")
    assert birthdays_one_expected == birthdays_one_result

    # birthdays - test two records + sort elements by date
    book_birthdays.add_record(birthday_record_2)
    birthdays_two_expected = [
        {"name": "Bob", "congratulation_date": "01.01.2025"},
        {"name": "Alice", "congratulation_date": "06.01.2025"},
    ]
    birthdays_two_result = book_birthdays.get_upcoming_birthdays(today="01.01.2025")
    assert birthdays_two_expected == birthdays_two_result

    # birthdays - test three records when birthdays out of upcoming period are ignored
    book_birthdays.add_record(birthday_record_3)
    birthdays_three_expected = [
        {"name": "Bob", "congratulation_date": "01.01.2025"},
        {"name": "Alice", "congratulation_date": "06.01.2025"},
    ]
    birthdays_three_result = book_birthdays.get_upcoming_birthdays(today="01.01.2025")
    assert birthdays_three_expected == birthdays_three_result

    # birthdays - test three records when upcoming passes new year + adding year to upcoming
    # Note: for "Alice" closest work day after weekend in 2026 is 05.01, not like in 2025 06.01
    birthdays_passing_new_year_expected = [
        {"name": "Charlie", "congratulation_date": "31.12.2025"},
        {"name": "Bob", "congratulation_date": "01.01.2026"},
        {"name": "Alice", "congratulation_date": "05.01.2026"},
    ]
    birthdays_passing_new_year_result = book_birthdays.get_upcoming_birthdays(
        today="30.12.2025"
    )
    assert birthdays_passing_new_year_expected == birthdays_passing_new_year_result

    # birthdays - additional test of upcoming period of whole year
    birthdays_upcoming_period_1_expected = [
        {"name": "Bob", "congratulation_date": "01.01.2025"},
        {"name": "Alice", "congratulation_date": "06.01.2025"},
        {"name": "Charlie", "congratulation_date": "31.12.2025"},
    ]
    birthdays_upcoming_period_1_result = book_birthdays.get_upcoming_birthdays(
        today="01.01.2025", upcoming_period_days=365
    )
    assert birthdays_upcoming_period_1_expected == birthdays_upcoming_period_1_result

    # birthdays - additional test of upcoming period of whole year with correct sorting
    birthdays_upcoming_period_2_expected = [
        {"name": "Alice", "congratulation_date": "06.01.2025"},
        {"name": "Charlie", "congratulation_date": "31.12.2025"},
        {"name": "Bob", "congratulation_date": "01.01.2026"},
    ]
    birthdays_upcoming_period_2_result = book_birthdays.get_upcoming_birthdays(
        today="03.01.2025", upcoming_period_days=365
    )
    assert birthdays_upcoming_period_2_expected == birthdays_upcoming_period_2_result

    print("AddressBook tests passed.")
