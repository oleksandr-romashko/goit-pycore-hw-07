"""
This module defines the Record class for managing a contact's name and associated phone numbers.
"""
from name import Name
from phone import Phone

from validators.errors import ValidationError
from validators.contact_validators import MSG_PHONE_EXISTS

MSG_PHONE_ADDED = "Phone added."
MSG_PHONE_DELETED = "Phone deleted."
MSG_PHONE_UPDATED = "Phone updated."


class Record:
    """
    A class for storing contact information, including the contact's name and a list of phones.

    Attributes:
        name (Name): The contact's name (required).
        phones (list[Phone]): A list of phones associated with the contact.

    Functionality:
        - Add phone numbers.
        - Remove phone numbers.
        - Edit existing phone numbers.
        - Search for a phone number.
    """

    def __init__(self, username: str):
        self.name = Name(username)
        self.phones: list[Phone] = []

    def __str__(self):
        return (
            f"Contact name: {self.name.value}, "
            f"phones: {'; '.join(phone.value for phone in self.phones)}"
        )

    def add_phone(self, phone_number: str) -> str:
        """
        Adds a phone number to the record.

        Raises:
            ValidationError: If the phone number already exists.
        """
        if self._find_phone_with_index(phone_number):
            raise ValidationError(
                MSG_PHONE_EXISTS.format(self.name.value, phone_number)
            )

        self.phones.append(Phone(phone_number))
        return MSG_PHONE_ADDED

    def remove_phone(self, phone_number: str) -> str:
        """
        Removes a phone from the record.

        Raises:
            ValidationError: If the phone number does not exist.
        """
        search_result = self._find_phone_with_index(phone_number)
        if not search_result:
            raise ValidationError(f"Phone '{phone_number}' not found.")

        idx, _ = search_result
        self.phones.pop(idx)
        return MSG_PHONE_DELETED

    def edit_phone(self, prev_phone_number: str, new_phone_number: str) -> str:
        """
        Updates an existing phone with a new phone number.

        Raises:
            ValidationError: If the new phone number already exists
            or if the old phone number is not found.
        """
        if self._find_phone_with_index(new_phone_number):
            raise ValidationError(f"Phone '{new_phone_number}' already exists.")

        search_result = self._find_phone_with_index(prev_phone_number)
        if not search_result:
            raise ValidationError(f"Phone '{prev_phone_number}' not found.")

        _, phone = search_result
        phone.update_phone(new_phone_number)
        return MSG_PHONE_UPDATED

    def find_phone(self, phone_number: str) -> Phone | None:
        """
        Finds and returns a phone number object from the record.

        Returns:
            Phone: The phone object if found, otherwise None.
        """
        result = self._find_phone_with_index(phone_number)
        return result[1] if result else None

    def _find_phone_with_index(self, phone_number: str) -> tuple[int, Phone]:
        """
        Searches for a phone number and returns its index and object.

        Returns:
            tuple[int, Phone]: A tuple of the index and phone object if found, otherwise None.
        """
        if not self.phones:
            return None

        for idx, phone in enumerate(self.phones):
            if phone.value == phone_number:
                return idx, phone


if __name__ == "__main__":
    # TESTS

    # Create a Record instance
    record = Record("Alice")
    assert record.name.value == "Alice"
    assert len(record.phones) == 0
    assert str(record) == "Contact name: Alice, phones: "

    # Try to create Record instance with empty name
    try:
        record = Record("")
    except ValidationError as exc:
        assert str(exc) == "Username cannot be empty or just whitespace."
    else:
        assert False, "Should raise Validation error"

    # Add a phone number
    result_add = record.add_phone("1234567890")
    assert result_add == MSG_PHONE_ADDED
    assert len(record.phones) == 1
    assert record.phones[0].value == "1234567890"
    assert str(record) == "Contact name: Alice, phones: 1234567890"

    # Add another phone number
    record.add_phone("0987654321")
    assert len(record.phones) == 2
    assert record.phones[0].value == "1234567890"
    assert record.phones[1].value == "0987654321"
    assert str(record) == "Contact name: Alice, phones: 1234567890; 0987654321"

    # Find a phone
    found_phone = record.find_phone("1234567890")
    assert found_phone is not None
    assert found_phone.value == "1234567890"

    assert record.find_phone("9999999999") is None

    # Edit a phone
    result_edit = record.edit_phone("1234567890", "1122334455")
    assert result_edit == MSG_PHONE_UPDATED
    assert record.find_phone("1234567890") is None
    assert record.find_phone("1122334455") is not None
    assert record.find_phone("1122334455").value == "1122334455"

    try:
        record.edit_phone("1234567890", "8888888888")
    except ValidationError as exc:
        assert str(exc) == "Phone '1234567890' not found."
    else:
        assert False, "Should raise Validation error"

    try:
        record.edit_phone("1122334455", "0987654321")
    except ValidationError as exc:
        assert str(exc) == "Phone '0987654321' already exists."
    else:
        assert False, "Should raise Validation error"

    # Remove a phone
    result_remove_1 = record.remove_phone("0987654321")
    assert result_remove_1 == MSG_PHONE_DELETED
    assert len(record.phones) == 1
    assert record.phones[0].value == "1122334455"
    assert str(record) == "Contact name: Alice, phones: 1122334455"

    try:
        record.remove_phone("0000000000")
    except ValidationError as exc:
        assert str(exc) == "Phone '0000000000' not found."
    else:
        assert False, "Should raise Validation error"

    # Find phone with index
    phone_1 = "1234567890"
    phone_2 = "0987654321"

    record_2 = Record("Alex")
    record_2.add_phone(phone_1)
    record_2.add_phone(phone_2)
    assert record_2.phones[0].value == phone_1
    assert record_2.phones[1].value == phone_2
    record_2_find_1 = record_2._find_phone_with_index(phone_1)
    assert record_2_find_1[0] == 0
    assert record_2_find_1[1].value == phone_1
    record_2_find_2 = record_2._find_phone_with_index(phone_2)
    assert record_2_find_2[0] == 1
    assert record_2_find_2[1].value == phone_2

    print("Record tests passed.")
