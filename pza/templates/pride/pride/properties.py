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
from pza.pie import AppHub

from pride import recipe

# --- Constant app properties ---

APP_NAME = "pride"
APP_DISPLAY_NAME = "Capture the Pride Flag"
APP_VERSION = "0.4.6"

# --- App functions ---

def initialize_app(profile: str = "default", setting_overrides: dict | None = None) -> AppHub:
    """
    Loads the framework environment.
    This step enables settings, database, and logging.

    Apps launched with 'pza.interface.run()' do not need to call this
    because 'run()' performs the initialization automatically.

    Call this function to initialize an environment for testing the app or running
    standalone components that do not use the command line interface.
    """
    PrideHub = AppHub(
        recipe.get_app_recipe(APP_NAME, APP_DISPLAY_NAME, APP_VERSION),
        profile,
        setting_overrides
    )
    return PrideHub

def list_properties() -> None:
    """
    Prints a list of app properties.
    """
    print_with_label("Application Name", APP_NAME)
    print_with_label("Application Display Name", APP_DISPLAY_NAME)
    print_with_label("Application Version", APP_VERSION)
    return

if __name__ == "__main__":

    print_header(f"{__file__}")

    print_separator()

    print()

    print_separator()

    print_footer()