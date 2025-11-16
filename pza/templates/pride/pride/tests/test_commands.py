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

import pride.commands
import pride.properties

import time

if __name__ == "__main__":

    # Set delay time between commands for viewing the output
    sleep_time = 1.5

    print_header(f"{__file__}")

    print_separator()

    # Test
    print_subheader(f"Testing Initialization")

    profile = "test"
    overrides = None
    TestHub = pride.properties.initialize_app(profile, overrides)
    TestHub.list()
    print()

    print_separator()
    time.sleep(sleep_time)

    # Test
    print_subheader(f"Testing Entry Point")

    pride.commands.entry_point(TestHub)
    print()

    print_separator()
    time.sleep(sleep_time)

    print_footer()