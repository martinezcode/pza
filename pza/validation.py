from pza.prints import (
    print_error,
    print_footer,
    print_header,
    print_label,
    print_line,
    print_separator,
    print_subheader,
    print_with_label,
)

from typing import Any

# --- Validation Helpers ---

def get_valid_boolean(original_value: Any) -> bool:
    """
    Returns a valid boolean value.
    """
    valid_value = original_value
    if not isinstance(valid_value, bool):
        print(f"Invalid boolean (converting to True or False)")
        valid_value = bool(valid_value)
    return valid_value

def get_valid_list(original_value: Any) -> list:
    """
    Returns a valid list.
    """
    valid_list = original_value
    if not isinstance(valid_list, list):
        print(f"Invalid list (defaulting to empty list)")
        valid_list = []
    return valid_list

def get_valid_dictionary(original_value: Any) -> dict:
    """
    Returns a valid dictionary.
    """
    valid_dictionary = original_value
    if not isinstance(valid_dictionary, dict):
        print(f"Invalid dictionary (defaulting to empty dictionary)")
        valid_dictionary = {}
    return valid_dictionary


if __name__ == "__main__":

    print_header(f"{__file__}")

    print_separator()

    print()

    print_separator()

    print_footer()
