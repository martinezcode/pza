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
from pza import logger

if __name__ == "__main__":

    print_header(f"{__file__}")

    print_separator()

    # Test
    print_subheader(f"Testing logger")

    app_name = "test_app"
    app_logger = logger.get_logger(app_name, "debug")
    print(app_logger)
    print()
    app_logger.info(f"test")
    print()

    print_separator()

    print_footer()
