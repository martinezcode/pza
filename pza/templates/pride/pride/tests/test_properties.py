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
from pza.pie import AppHub

import pride.properties

if __name__ == "__main__":

    print_header(f"{__file__}")

    print_separator()

    # Test
    print_subheader(f"Testing Properties")

    pride.properties.list_properties()
    print()
    profile = "test"
    overrides = None
    TestHub = pride.properties.initialize_app(profile, overrides)
    TestHub.list()
    print()

    print_separator()

    print_footer()
