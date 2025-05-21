"""
This module defines static messages, prompts, and configuration constants
used across the assistant bot application. These constants include UI strings,
user guidance text, validation rules, and formatting hints.

Usage:
    Import any constant directly from this module to ensure consistency and
    maintainability.

Example:
    from utils.constants import WELCOME_MESSAGE_TITLE, NAME_MIN_LENGTH
"""

# UI messages and prompts
WELCOME_MESSAGE_TITLE = "Welcome to the assistant bot!"
WELCOME_MESSAGE_SUBTITLE = "Here you have the list of available options for you"
HELLO_MESSAGE = "How can I help you?"
APP_PURPOSE_MESSAGE = "If you'd like, I can help you manage your phone contacts"
EXIT_MESSAGE = "Good bye!"

# Menu and help text
MENU_HELP_STR = """hello                                 - Greet the user
all                                   - Display all contacts
add <name> <phone>                    - Add a new contact or add phone to the existing one
change <name> <old_phone> <new_phone> - Update contact's phone number
phone <name>                          - Show contact's phone number
add-birthday <name> <birthday_date>   - Add a birthday to the specified contact
show-birthday <name>                  - Show the birthday of the specified contact
birthdays                             - Show upcoming birthdays within the next 7 days
help                                  - Show available commands
exit (or close)                       - Exit the app"""
HELP_AWARE_TIP = "type 'help' for the available list of commands"
INPUT_PROMPT = f"Enter a command (or {HELP_AWARE_TIP})"

# Error and validation messages
INVALID_COMMAND_MESSAGE = "Invalid command"
INVALID_EMPTY_COMMAND_MESSAGE = "You entered an empty command. Please try again"

# Validation constraints
NAME_MIN_LENGTH = 2
NAME_MAX_LENGTH = 50
MAX_DISPLAY_NAME_LEN = 15
PHONE_FORMAT_DESC_STR = "10 digits, optionally starting with '+'"
DATE_FORMAT = "%d.%m.%Y"
DATE_FORMAT_STR_REPRESENTATION = "DD.MM.YYYY"

# Messages
MSG_HAVE_CONTACTS = "You have {0} contact{1}"
