from collections import UserDict

from record import Record

from validators.errors import ValidationError
from validators.contact_validators import (
    validate_contacts_not_empty,
    validate_contact_not_in_contacts,
    validate_contact_is_in_contacts,
)

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

    print("AddressBook tests passed.")
