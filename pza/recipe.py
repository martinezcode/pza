from pza.prints import (
    print_error,
    print_footer,
    print_header,
    print_label,
    print_separator,
    print_subheader,
    print_with_label,
)

# --- Recipe definitions ---

def get_app_recipe(app_name: str, app_display_name: str, app_version: str) -> dict:
    """
    Defines app specifications.
    """
    recipe = {
        "name": app_name,
        "display_name": app_display_name,
        "version": app_version,
        "entry_point": "pza.pie.main",
        "entry_args": None,
        "test_entry_point": "pza.tests.test_helpers.test_entry_point_a",
        "test_args": None,
        "settings_recipe": get_settings_recipe(),
        "command_recipe": get_command_recipe(),
        "onboarding_recipe": get_onboarding_recipe(),
        "database_recipe": get_database_recipe(),
    }
    return recipe

def get_settings_recipe() -> dict:
    """
    Defines app default setting specifications.
    """
    recipe = {
        "onboarding_required": False,
        "log_level": "info",
        "app_documents_folder": "[default_app_documents_folder]",
        "profile_documents_folder": "[default_profile_documents_folder]",
    }
    return recipe

def get_onboarding_recipe() -> dict:
    """
    Defines app setup wizard specifications.
    """
    recipe = None
    return recipe

def get_database_recipe() -> dict:
    """
    Defines app database schema.
    """
    recipe = None
    return recipe

def get_command_recipe() -> dict:
    """
    Defines command line interface commands and their arguments.
    """
    recipe = {
        "pride": {
            "callback": "pza.commands.pride",
            "help": "Generates a modular project app template.",
            "args": [
                {
                    "name": "--out-folder",
                    "type": str,
                    "default": "",
                    "help": "Path to folder where template folder will be created.",
                },
            ],
        },
        "solo": {
            "callback": "pza.commands.solo",
            "help": "Generates a single file app template.",
            "args": [
                {
                    "name": "--out-file",
                    "type": str,
                    "default": "",
                    "help": "Path to file where template will be created.",
                },
            ],
        },
        "recipe": {
            "callback": "pza.commands.recipe",
            "help": "Generates a recipe dictionary.",
            "args": [
                {
                    "name": "--py",
                    "type": str,
                    "default": "",
                    "help": "Path to python file for generating app recipe.",
                    "exclusive": True,
                },
                {
                    "name": "--folder",
                    "type": str,
                    "default": "",
                    "help": "Path to python package folder for generating app recipe.",
                    "exclusive": True,
                },
                {
                    "name": "--db",
                    "type": str,
                    "default": "",
                    "help": "Path to sqlite file for generating database recipe.",
                    "exclusive": True,
                },
            ],
        },
        "sql": {
            "callback": "pza.commands.sql",
            "help": "Generates a sql statement.",
            "args": [
                {
                    "name": "--recipe",
                    "type": str,
                    "default": "",
                    "help": "Recipe for generating sql statement.",
                    "exclusive": True,
                },
                {
                    "name": "--json",
                    "type": str,
                    "default": "",
                    "help": "JSON string recipe for generating sql statement.",
                    "exclusive": True,
                },
                {
                    "name": "--json-file",
                    "type": str,
                    "default": "",
                    "help": "Path to file containing JSON recipe for generating sql statement.",
                    "exclusive": True,
                },
                {
                    "name": "--out-file",
                    "type": str,
                    "default": "",
                    "help": "Path to file where sql will be saved.",
                    "exclusive": False,
                },
                {
                    "name": "--run",
                    "type": str,
                    "default": "",
                    "help": "Command line program to run with sql as input.",
                    "exclusive": False,
                },
            ],
        },
    }
    return recipe

if __name__ == "__main__":

    print_header(f"{__file__}")

    print_separator()

    print()

    print_separator()

    print_footer()