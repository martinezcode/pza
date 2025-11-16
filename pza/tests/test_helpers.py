"""
Test helper library
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
from pza.pie import get_pza_folder, create_folder, get_framework_settings_recipe

import os

# --- Sample Recipes ---

def get_test_app_recipe() -> dict:
    """
    Defines app specifications.
    """
    recipe = {
        "name": "test_app",
        "display_name": "Test App",
        "version": "0.4.2",
        "entry_point": "pza.tests.test_helpers.test_entry_point_a",
        "test_entry_point": "pza.tests.test_helpers.test_entry_point_b",
        "settings_recipe": get_test_settings_recipe(),
        "command_recipe": get_test_command_recipe(),
        "onboarding_recipe": get_test_onboarding_recipe(),
        "database_recipe": get_test_database_recipe(),
    }
    return recipe

def get_test_settings_recipe() -> dict:
    """
    Defines app default setting specifications.
    """
    recipe = {
        "onboarding_required": False, # Override framwork default
        "log_level": "debug", # Override framwork default
        "profile_data_file": os.path.join("[default_profile_documents_folder]", "[app_name].db"),
    }
    return recipe

def get_test_onboarding_recipe() -> dict:
    """
    Defines app setup wizard specifications.
    """
    recipe = {
        "app_documents_folder": {
            "display": f"App Documents Folder",
            "description": f"Folder where app documents will be saved",
            "type": str,
            "required": True,
        },
        "profile_documents_folder": {
            "display": f"Profile Documents Folder",
            "description": f"Folder where profile specific documents will be saved",
            "type": str,
            "required": True,
        },
        "profile_data_file": {
            "display": f"Profile Data File",
            "description": f"Database file where profile specific data will be saved",
            "type": str,
            "required": False,
        },
    }
    return recipe

def get_test_database_recipe() -> dict:
    """
    Defines app database schema.
    """
    recipe = {
        "schema_version": "0.1.1",
        "Teams": {
            "team_id": "INTEGER PRIMARY KEY AUTOINCREMENT",
            "team_name": "TEXT",
            "is_ranked": "BOOLEAN DEFAULT 0",
        },
        "Players": {
            "player_id": "INTEGER PRIMARY KEY AUTOINCREMENT",
            "player_name": "TEXT",
            "jersey_number": "INTEGER",
        }
    }
    return recipe

def get_test_command_recipe() -> dict:
    """
    Defines command line interface commands and their arguments.
    """
    recipe = {
        "c": {
            "callback": "pza.tests.test_helpers.test_entry_point_c",
            "help": "Entry point c",
            "exclusive": False,
            "args": [
                {
                    "name": "--input",
                    "type": str,
                    "default": "",
                    "help": "Input text"
                },
            ],
        },
        "d": {
            "callback": "pza.tests.test_helpers.test_entry_point_d",
            "help": "Entry point d",
        },
    }
    return recipe

# --- Test Command Entry Points ---

def test_entry_point_a(CurrentAppHub, args = None) -> None:
    print(f"Entry Point Reached: a")
    return

def test_entry_point_b(CurrentAppHub, args = None) -> None:
    print(f"Entry Point Reached: b")
    return

def test_entry_point_c(CurrentAppHub, args = None) -> None:
    print(f"Entry Point Reached: c")
    if not args or not args.input:
        print(f"No Input")
    else:
        print()
        print(f"Input: {args.input}")
    return

def test_entry_point_d(CurrentAppHub, args = None) -> None:
    print(f"Entry Point Reached: d")
    return

# --- Test Folders and Files ---

def get_test_folder() -> str:
    pza_folder = get_pza_folder()
    test_folder = os.path.join(pza_folder, "test")
    _ = create_folder(test_folder)
    return test_folder

def get_test_settings_file() -> str:
    test_folder = get_test_folder()
    test_file = os.path.join(test_folder, "test.json")
    return test_file

def get_test_database_file() -> str:
    test_folder = get_test_folder()
    test_file = os.path.join(test_folder, "test.db")
    return test_file

def get_test_log_file() -> str:
    test_folder = get_test_folder()
    test_file = os.path.join(test_folder, "test.log")
    return test_file

if __name__ == "__main__":

    print_header(f"{__file__}")

    print_separator()

    print()

    print_separator()

    print_footer()