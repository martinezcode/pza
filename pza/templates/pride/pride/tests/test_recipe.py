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

import pride.recipe

if __name__ == "__main__":

    print_header(f"{__file__}")

    print_separator()

    # Test
    print_subheader(f"Testing Settings Recipe")

    default_settings = pride.recipe.get_settings_recipe()
    print(f"Default App Settings: {default_settings}")
    print()

    print_separator()

    print_footer()