"""
Reusable string utilities for formatting, truncation, and other text operations.
"""

DEFAULT_TRUNCATE_LENGTH = 8
MSG_FORMATTED_LINE = "{offset}{title} : {value}"
MSG_DEFAULT_LINE_OFFSET = "  "


def truncate_string(
    string: str,
    max_length: int = DEFAULT_TRUNCATE_LENGTH,
    suffix: str = "...",
    include_suffix_in_max_length: bool = False,
) -> str:
    """
    Truncates the given string to a maximum length and optionally appends a suffix.

    Args:
        string (str): The input string to truncate.
        max_length (int): The maximum allowed total length of the result string.
        suffix (str): The suffix to append (e.g. "...").
        include_suffix_in_max_length (bool): Whether the suffix length counts toward max_length.

    Returns:
        str: The truncated string with or without suffix as specified.

    Raises:
        TypeError: If input types are invalid.

    Examples:
        >>> truncate_string("Hello world", 5)
        'Hello...'
        >>> truncate_string("Hello world", 5, include_suffix_in_max_length=True)
        'He...'
    """
    if not isinstance(string, str):
        raise TypeError(
            f"During truncation expected 'string' to be of type 'str', "
            f"but was '{type(string).__name__}'"
        )

    if not isinstance(max_length, int):
        raise TypeError(
            f"During truncation expected 'max_length' to be of type 'int', "
            f"but was '{type(max_length).__name__}'"
        )

    if not isinstance(suffix, str):
        raise TypeError(
            f"During truncation expected 'suffix' to be of type 'str', "
            f"but was '{type(suffix).__name__}'"
        )

    # Guard empty values
    if not string and not suffix:
        return ""

    string_length = len(string)

    # Nothing to truncate -> return original string
    if string_length <= max_length:
        return string

    # Case where suffix has no influence on result and just added to the end of the truncated string
    if not include_suffix_in_max_length:
        return f"{string[:max_length]}{suffix}"

    # Following is a case when suffix length matters

    if max_length <= 0:
        return ""

    suffix_length = len(suffix)

    # Truncate suffix only
    if suffix_length >= max_length:
        return suffix[-max_length:]

    # There is at least one symbol in the string
    string_slice_end = max_length - suffix_length
    sliced_string = string[:string_slice_end]
    return f"{sliced_string}{suffix}"


def format_text_output(
    header: str, items: list, offset: str = MSG_DEFAULT_LINE_OFFSET
) -> str:
    """
    Formats a header and a list of (key, value) pairs into aligned output.

    Args:
        header (str): The header/title line.
        items (list of tuple[str, str]): The items to format.
        offset (str): Optional string for indentation.

    Returns:
        str: Formatted multi-line string starting with header.
    """
    return f"{header}:\n{format_columns_output(items, offset)}"


def format_columns_output(
    items: list[tuple[str, str]], offset: str = MSG_DEFAULT_LINE_OFFSET
) -> str:
    """
    Formats a list of (title, value) pairs into aligned columns.

    Args:
        items (list of tuple[str, str]): The data to format.
        offset (str): String used for indentation (default: 2 spaces).

    Returns:
        str: Multi-line string with aligned output.
    """
    max_title_len = max((len(item[0]) for item in items), default=0)
    str_lines = [format_line_output(item, max_title_len, offset) for item in items]
    return "\n".join(str_lines)


def format_line_output(
    item: tuple[str, str], max_title_len=0, offset: str = MSG_DEFAULT_LINE_OFFSET
) -> str:
    """
    Formats a single (title, value) pair into an aligned string line.

    Args:
        item (tuple[str, str]): A pair where the first element is the title,
                                and the second is the value.
        max_title_len (int): The length to pad the title to for alignment.
        offset (str): String to prepend for indentation (default is two spaces).

    Returns:
        str: A formatted string like '  Title : Value', with aligned titles
             based on max_title_len.
    """
    return MSG_FORMATTED_LINE.format(
        offset=offset, title=item[0].ljust(max_title_len), value=item[1]
    )


if __name__ == "__main__":
    # TESTS

    # Truncate tests

    TEST_TRUNCATE_STRING = "Hello world!"
    # tweaking string value
    assert truncate_string(TEST_TRUNCATE_STRING) == "Hello wo..."
    assert (
        truncate_string(TEST_TRUNCATE_STRING, include_suffix_in_max_length=True)
        == "Hello..."
    )
    assert truncate_string("12345678") == "12345678"
    assert truncate_string("12345678", include_suffix_in_max_length=True) == "12345678"
    assert truncate_string("abc") == "abc"
    assert truncate_string("abc", include_suffix_in_max_length=True) == "abc"
    assert truncate_string("") == ""
    assert truncate_string("", include_suffix_in_max_length=True) == ""
    # tweaking max_length value
    assert truncate_string(TEST_TRUNCATE_STRING, max_length=13) == TEST_TRUNCATE_STRING
    assert (
        truncate_string(
            TEST_TRUNCATE_STRING, max_length=13, include_suffix_in_max_length=True
        )
        == TEST_TRUNCATE_STRING
    )
    assert truncate_string(TEST_TRUNCATE_STRING, max_length=12) == TEST_TRUNCATE_STRING
    assert (
        truncate_string(
            TEST_TRUNCATE_STRING, max_length=12, include_suffix_in_max_length=True
        )
        == TEST_TRUNCATE_STRING
    )
    assert truncate_string(TEST_TRUNCATE_STRING, max_length=9) == "Hello wor..."
    assert (
        truncate_string(
            TEST_TRUNCATE_STRING, max_length=9, include_suffix_in_max_length=True
        )
        == "Hello ..."
    )
    assert truncate_string(TEST_TRUNCATE_STRING, max_length=3) == "Hel..."
    assert (
        truncate_string(
            TEST_TRUNCATE_STRING, max_length=3, include_suffix_in_max_length=True
        )
        == "..."
    )
    assert truncate_string(TEST_TRUNCATE_STRING, max_length=2) == "He..."
    assert (
        truncate_string(
            TEST_TRUNCATE_STRING, max_length=2, include_suffix_in_max_length=True
        )
        == ".."
    )
    assert truncate_string(TEST_TRUNCATE_STRING, max_length=1) == "H..."
    assert (
        truncate_string(
            TEST_TRUNCATE_STRING, max_length=1, include_suffix_in_max_length=True
        )
        == "."
    )
    assert truncate_string(TEST_TRUNCATE_STRING, max_length=0) == "..."
    assert (
        truncate_string(
            TEST_TRUNCATE_STRING, max_length=0, include_suffix_in_max_length=True
        )
        == ""
    )
    assert truncate_string(TEST_TRUNCATE_STRING, max_length=-1) == "Hello world..."
    assert (
        truncate_string(
            TEST_TRUNCATE_STRING, max_length=-1, include_suffix_in_max_length=True
        )
        == ""
    )
    # tweaking suffix value
    assert truncate_string(TEST_TRUNCATE_STRING, suffix="###") == "Hello wo###"
    assert (
        truncate_string(
            TEST_TRUNCATE_STRING, suffix="###", include_suffix_in_max_length=True
        )
        == "Hello###"
    )
    assert truncate_string(TEST_TRUNCATE_STRING, suffix="123") == "Hello wo123"
    assert (
        truncate_string(
            TEST_TRUNCATE_STRING, suffix="123", include_suffix_in_max_length=True
        )
        == "Hello123"
    )
    assert truncate_string(TEST_TRUNCATE_STRING, suffix="") == "Hello wo"
    assert (
        truncate_string(
            TEST_TRUNCATE_STRING, suffix="", include_suffix_in_max_length=True
        )
        == "Hello wo"
    )
    assert (
        truncate_string(TEST_TRUNCATE_STRING, suffix="12345678") == "Hello wo12345678"
    )
    assert (
        truncate_string(
            TEST_TRUNCATE_STRING, suffix="12345678", include_suffix_in_max_length=True
        )
        == "12345678"
    )
    assert (
        truncate_string(TEST_TRUNCATE_STRING, suffix="123456789") == "Hello wo123456789"
    )
    assert (
        truncate_string(
            TEST_TRUNCATE_STRING, suffix="123456789", include_suffix_in_max_length=True
        )
        == "23456789"
    )
    assert (
        truncate_string(TEST_TRUNCATE_STRING, suffix="1234567890")
        == "Hello wo1234567890"
    )
    assert (
        truncate_string(
            TEST_TRUNCATE_STRING, suffix="1234567890", include_suffix_in_max_length=True
        )
        == "34567890"
    )
    assert truncate_string("", suffix="") == ""
    assert truncate_string("", suffix="", include_suffix_in_max_length=True) == ""

    # format_line_output test

    test_format_line_item = ("Alice", "1234567890")
    TEST_FORMAT_LINE_RESULT = format_line_output(
        test_format_line_item, max_title_len=5, offset="  "
    )
    assert TEST_FORMAT_LINE_RESULT == "  Alice : 1234567890"
    assert format_line_output(("Name", "Alice"), max_title_len=6) == "  Name   : Alice"

    # format_columns_output tests

    test_format_columns_items = [("Alice", "1234567890"), ("Bob", "0987654321")]
    TEST_FORMAT_COLUMNS_RESULT = format_columns_output(
        test_format_columns_items, offset="> "
    )
    assert TEST_FORMAT_COLUMNS_RESULT == (
        "> Alice : 1234567890\n" "> Bob   : 0987654321"
    )

    TEST_FORMAT_COLUMNS_ITEMS_EMPTY = format_columns_output([])
    assert TEST_FORMAT_COLUMNS_ITEMS_EMPTY == ""

    # format_text_output tests

    TEST_FORMAT_TEXT_TITLE = "Found contacts"
    test_format_text_items = [("Alice", "1234567890"), ("Bob", "0987654321")]
    TEST_FORMAT_TEXT_RESULT = format_text_output(
        TEST_FORMAT_TEXT_TITLE, test_format_text_items, offset="- "
    )
    assert TEST_FORMAT_TEXT_RESULT == (
        "Found contacts:\n" "- Alice : 1234567890\n" "- Bob   : 0987654321"
    )

    print("Test utils tests passed.")
