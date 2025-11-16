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

import pride.__main__

if __name__ == "__main__":

    print_header(f"{__file__}")

    print_separator()

    # Test
    print_subheader(f"Testing Main")

    pride.__main__.main()

    print_separator()

    print_footer()
