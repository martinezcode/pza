"""
Tests
"""

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

import pride.properties
import pride.library

if __name__ == "__main__":

    print_header(f"{__file__}")

    print_separator()

    # Test
    print_subheader(f"Testing Random Flag")

    profile = "test"
    overrides = None
    TestHub = pride.properties.initialize_app(profile, overrides)
    database_populated = pride.library.import_sample_data(TestHub)
    if database_populated:
        flag_row = pride.library.get_random_flag(TestHub)
        print(flag_row["flag_name"])
        print()

    print_separator()

    print_footer()
