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

# --- Recipe definitions ---

def get_app_recipe(app_name: str, app_display_name: str, app_version: str) -> dict:
    """
    Defines app specifications.
    """
    recipe = {
        "name": app_name,
        "display_name": app_display_name,
        "version": app_version,
        "entry_point": "pride.commands.entry_point",
        "test_entry_point": "pride.commands.test_entry_point",
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
        "onboarding_required": True, # Same as framwork default
        "log_level": "info", # Same as framwork default
        "allow_downloads": None, # App specific default
    }
    return recipe

def get_onboarding_recipe() -> dict:
    """
    Defines app setup wizard specifications.
    """
    recipe = {
        "allow_downloads": {
            "display":"Allow Downloads",
            "description": "Would you like to allow downloading of pride flag data?",
            "type": bool,
            "choices": ["yes", "no"],
            "required": True,
            "validator": "pride.recipe.validate_allow_downloads",
        },
    }
    return recipe

def get_database_recipe() -> dict:
    """
    Defines app database schema.
    """
    recipe = {
        "schema_version": "0.4.6",
        "Colors": {
            "color_id": "INTEGER PRIMARY KEY AUTOINCREMENT",
            "color_name": "TEXT",
        },
        "Flags": {
            "flag_id": "INTEGER PRIMARY KEY AUTOINCREMENT",
            "flag_name": "TEXT",
            "filename": "TEXT",
            "stripes": "INTEGER",
            "shapes": "BOOLEAN",
            "src": "TEXT",
            "citation_text": "TEXT",
            "citation_sources": "TEXT",
            "citation_image": "TEXT",
            "citation_author": "TEXT",
        },
        "ColorMap": {
            "color_id": "INTEGER",
            "flag_id": "INTEGER",
        },
    }
    return recipe

def get_command_recipe() -> dict:
    """
    Defines command line interface commands and arguments.
    """
    recipe = {
        "export": {
            "callback": "pride.commands.export",
            "help": "Export flag images and data",
            "args": [
                {
                    "name": "--out-folder",
                    "type": str,
                    "default": "",
                    "help": "Folder to save exported images and data"
                },
            ],
        },
        "search": {
            "callback": "pride.commands.search",
            "help": "Search for a flag",
            "args": [
                {
                    "name": "--term",
                    "type": str,
                    "default": "",
                    "help": "Text to search for"
                },
            ],
        },
    }
    return recipe

# --- Onboarding validation functions ---

def validate_allow_downloads(input: str) -> str | None:
    """
    Requires download of sample data to be allowed.
    """
    if not input or input.strip().lower() != "yes":
        return "Allowing downloads is required. Enter 'yes' to continue."
    return None

if __name__ == "__main__":

    print_header(f"{__file__}")

    print_separator()

    print()

    print_separator()

    print_footer()
