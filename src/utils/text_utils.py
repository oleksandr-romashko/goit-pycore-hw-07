"""
Reusable string utilities for formatting, truncation, and other text operations.
"""


def truncate_string(
    string: str,
    max_length: int = 8,
    suffix: str = "...",
    include_suffix_in_max_length: bool = False,
) -> str:
    """
    Truncates the provided string with an optional suffix.

    Args:
        string (str): The original string to truncate.
        max_length (int): The maximum allowed length for the final output string.
        suffix (str): The suffix to append after truncation (default is "...").
        include_suffix_in_max_length (bool): Whether the suffix should count toward the max_length.

    Returns:
        str: The truncated string with suffix if truncation occurred.

    Examples:
        truncate_string("Hello world", 5) => "Hello..."
        truncate_string("Hello world", 5, include_suffix_in_max_length=True) => "He..."
    """
    if not isinstance(string, str):
        raise TypeError(
            f"During truncation expected 'string' to be of type 'str', but was '{type(string)}'"
        )

    if not isinstance(max_length, int):
        raise TypeError(
            f"During truncation expected 'max_length' to be of type 'int' but was '{type(max_length)}'"
        )

    if not isinstance(suffix, str):
        raise TypeError(
            f"During truncation expected 'suffix' to be of type 'str' but was '{type(suffix)}'"
        )

    # Guard empty values
    if not string and not suffix:
        return ""

    string_length = len(string)

    # Nothing to truncate -> return original string
    if string_length <= max_length:
        return string

    # Case whe suffix has no influence on result and just added to the end of the truncated string
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


if __name__ == "__main__":
    # TESTS
    TEST_STRING = "Hello world!"
    # tweaking string value
    assert truncate_string(TEST_STRING) == "Hello wo..."
    assert truncate_string(TEST_STRING, include_suffix_in_max_length=True) == "Hello..."
    assert truncate_string("12345678") == "12345678"
    assert truncate_string("12345678", include_suffix_in_max_length=True) == "12345678"
    assert truncate_string("abc") == "abc"
    assert truncate_string("abc", include_suffix_in_max_length=True) == "abc"
    assert truncate_string("") == ""
    assert truncate_string("", include_suffix_in_max_length=True) == ""
    # tweaking max_length value
    assert truncate_string(TEST_STRING, max_length=13) == TEST_STRING
    assert (
        truncate_string(TEST_STRING, max_length=13, include_suffix_in_max_length=True)
        == TEST_STRING
    )
    assert truncate_string(TEST_STRING, max_length=12) == TEST_STRING
    assert (
        truncate_string(TEST_STRING, max_length=12, include_suffix_in_max_length=True)
        == TEST_STRING
    )
    assert truncate_string(TEST_STRING, max_length=9) == "Hello wor..."
    assert (
        truncate_string(TEST_STRING, max_length=9, include_suffix_in_max_length=True)
        == "Hello ..."
    )
    assert truncate_string(TEST_STRING, max_length=3) == "Hel..."
    assert (
        truncate_string(TEST_STRING, max_length=3, include_suffix_in_max_length=True)
        == "..."
    )
    assert truncate_string(TEST_STRING, max_length=2) == "He..."
    assert (
        truncate_string(TEST_STRING, max_length=2, include_suffix_in_max_length=True)
        == ".."
    )
    assert truncate_string(TEST_STRING, max_length=1) == "H..."
    assert (
        truncate_string(TEST_STRING, max_length=1, include_suffix_in_max_length=True)
        == "."
    )
    assert truncate_string(TEST_STRING, max_length=0) == "..."
    assert (
        truncate_string(TEST_STRING, max_length=0, include_suffix_in_max_length=True)
        == ""
    )
    assert truncate_string(TEST_STRING, max_length=-1) == "..."
    assert (
        truncate_string(TEST_STRING, max_length=-1, include_suffix_in_max_length=True)
        == ""
    )
    # tweaking suffix value
    assert truncate_string(TEST_STRING, suffix="###") == "Hello wo###"
    assert (
        truncate_string(TEST_STRING, suffix="###", include_suffix_in_max_length=True)
        == "Hello###"
    )
    assert truncate_string(TEST_STRING, suffix="123") == "Hello wo123"
    assert (
        truncate_string(TEST_STRING, suffix="123", include_suffix_in_max_length=True)
        == "Hello123"
    )
    assert truncate_string(TEST_STRING, suffix="") == "Hello wo"
    assert (
        truncate_string(TEST_STRING, suffix="", include_suffix_in_max_length=True)
        == "Hello wo"
    )
    assert truncate_string(TEST_STRING, suffix="12345678") == "Hello wo12345678"
    assert (
        truncate_string(
            TEST_STRING, suffix="12345678", include_suffix_in_max_length=True
        )
        == "12345678"
    )
    assert truncate_string(TEST_STRING, suffix="123456789") == "Hello wo123456789"
    assert (
        truncate_string(
            TEST_STRING, suffix="123456789", include_suffix_in_max_length=True
        )
        == "23456789"
    )
    assert truncate_string(TEST_STRING, suffix="1234567890") == "Hello wo1234567890"
    assert (
        truncate_string(
            TEST_STRING, suffix="1234567890", include_suffix_in_max_length=True
        )
        == "34567890"
    )
    assert truncate_string("", suffix="") == ""
    assert truncate_string("", suffix="", include_suffix_in_max_length=True) == ""
