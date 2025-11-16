"""
Tests

Note: This test demonstrates the minimum requirements to launch an app.
(App Name + Entry Point Function)
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
from pza import interface

if __name__ == "__main__":

    print_header(f"{__file__}")

    print_separator()

    # Test
    print_subheader(f"Testing interface")

    test_recipe = get_test_app_recipe()
    verbose = True
    if not isinstance(test_recipe, dict):
        print(f"Invalid test recipe")
    interface.run(
        test_recipe,
        verbose
    )
    print()

    print_separator()

    print_footer()
