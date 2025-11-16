from pza import interface

from pride.properties import APP_NAME, APP_DISPLAY_NAME, APP_VERSION
from pride import recipe

# --- Main app interface launcher ---

def main():
    """
    Launches the interface with 'interface.run()'.

    'interface.run()' will:
        - load logging
        - load settings
        - load database
        - create app folders
        - create app settings file
        - create app database
        - process terminal commands and arguments using recipe definition
        - run callbackback function for main entry point, test entry point or command handler

    Terminal commands built-in are:
        - 'test'
        - 'config'
            --setup, --list, --set, --get, --reset,
            --delete-profile, --copy-profile

    Terminal launch will perform one of the following:
        - APP_NAME: Run 'entry_point' callback without arguments.
        - Command 'config': Run built-in settings management task with arguments.
        - Command 'test': Activate '--debug' logging mode and
            run 'test_entry_point' callback without arguments.
        - Custom Command: Run command handler callback with arguments
            as specified in the app recipe.
    """
    interface.run(
        app_recipe=recipe.get_app_recipe(APP_NAME, APP_DISPLAY_NAME, APP_VERSION),
        verbose=False
    )
    return

if __name__ == "__main__":

    # Run the main function to launch the interface
    main()
