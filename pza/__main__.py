from pza.pie import FRAMEWORK_NAME, FRAMEWORK_DISPLAY_NAME, FRAMEWORK_VERSION
from pza.interface import run
from pza.recipe import get_app_recipe

# --- Main interface launcher ---

def main():
    """
    Launches the interface with 'run()'.

    'run()' will:
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

    run(
        app_recipe=get_app_recipe(FRAMEWORK_NAME, FRAMEWORK_DISPLAY_NAME, FRAMEWORK_VERSION),
        verbose=False
    )
    return

if __name__ == "__main__":

    # Run the main function
    main()
