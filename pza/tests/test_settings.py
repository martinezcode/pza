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
from pza.pie import get_pza_folder, get_framework_settings_recipe
from pza import settings

import os
import time

if __name__ == "__main__":

    # Set delay time between commands for viewing the output
    sleep_time = 2

    print_header(f"{__file__}")

    print_separator()

    # Load test environment
    print_subheader(f"Testing Write")

    temp_folder = get_pza_folder()
    temp_file = os.path.join(temp_folder, "test.json")
    test_settings = get_framework_settings_recipe()
    settings_created = settings.write_settings_file(temp_file, test_settings)
    print_with_label("Settings created", temp_file)
    print()

    print_separator()
    time.sleep(sleep_time)

    # Load and display the real settings
    print_subheader(f"Testing Read")

    current_settings = settings.read_settings_file(temp_file)
    settings.list_settings(current_settings, f"Active Settings")
    print()

    print_separator()
    time.sleep(sleep_time)

    # Change a specific setting to new value
    print_subheader(f"Testing Edit and Read")

    setting_name = f"log_level"
    changed_setting = settings.change_setting(temp_file, setting_name, f"debug")
    print_with_label(f"Changed {setting_name}", settings.get_setting(temp_file, setting_name, test_settings))
    print()

    print_separator()
    time.sleep(sleep_time)

    # Reset a specific setting to default
    print_subheader(f"Testing Reset One")

    setting_name = f"log_level"
    restored_setting = settings.reset_setting(temp_file, setting_name, test_settings)
    print_with_label(f"Restored {setting_name}", settings.get_setting(temp_file, setting_name, test_settings))
    print()

    print_separator()
    time.sleep(sleep_time)

    # Reset all settings to defaults
    print_subheader(f"Testing Reset All")

    settings_reset = settings.reset_settings(temp_file, test_settings)
    print_with_label(f"Settings Reset", f"{settings_reset}")
    print()
    current_settings = settings.read_settings_file(temp_file)
    settings.list_settings(current_settings, f"Restored Settings")

    print_separator()
    time.sleep(sleep_time)

    print_footer()
