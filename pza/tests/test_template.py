"""
Tests
"""

from pza.prints import (
    print_error,
    print_footer,
    print_header,
    print_label,
    print_separator,
    print_subheader,
    print_with_label,
)
from pza.tests.test_helpers import *

import time

if __name__ == "__main__":

    # Set delay time between commands for viewing the output
    sleep_time = 1.5

    print_header(f"{__file__}")

    print_separator()

    # Test
    print_subheader(f"Testing")

    pass
    print()

    print_separator()
    time.sleep(sleep_time)

    # Test
    print_subheader(f"Testing")

    pass
    print()

    print_separator()
    time.sleep(sleep_time)

    print_footer()
