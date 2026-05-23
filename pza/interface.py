from pza.prints import (
    print_error,
    print_footer,
    print_header,
    print_separator,
    print_subheader,
    print_with_label,
)
from pza import pie
from pza import settings

import argparse
import os

def run(
    app_recipe: dict,
    verbose: bool = False
):
    """
    Command line interface entry point.
    """
    app_name = app_recipe.get("name", None)
    app_display_name = app_recipe.get("display_name", None)
    app_version = app_recipe.get("version", None)
    app_onboarding_recipe = app_recipe.get("onboarding_recipe", None)
    app_command_recipe = app_recipe.get("command_recipe", None)
    app_entry_point_path = app_recipe.get("entry_point", None)
    app_test_entry_point_path = app_recipe.get("test_entry_point", None)

    app_entry_point_function = None
    if app_entry_point_path:
        app_entry_point_function = pie.get_function(app_entry_point_path)
    app_test_entry_point_function = None
    if app_test_entry_point_path:
        app_test_entry_point_function = pie.get_function(app_test_entry_point_path)

    if not app_name:
        print(f"App name is required")
        return

    if not app_display_name:
        app_display_name = app_name

    if verbose:
        print()
        if app_version:
            print(f"Launching {app_display_name} version {app_version}")
        else:
            print(f"Launching {app_display_name}")
        print()

    # --- Set Up the Argument Parser ---

    # Specify the program name that will start the app from the command line
    app_parser = argparse.ArgumentParser(
        prog=app_name,
        description=f"{app_name} command-line interface"
    )

    # --- Add Universal Arguments ---

    app_parser.add_argument(
        # Settings profile for the current session
        "--profile",
        default="default",
        help="Profile name"
    )
    app_parser.add_argument(
        # Override log level for the current session
        "--debug",
        action="store_true",
        help="Override log level for session"
    )
    app_parser.add_argument(
        # Override any settings for the current session
        "--override",
        nargs=2,
        metavar=("KEY", "VALUE"),
        action="append",
        help="Override settings for session"
    )

    # Set up the command subparsers
    # The command specifies which feature of the program to run
    # Built-in commands available with all apps are: 'config', 'test'
    # The 'app_entry_point_function' will be used by default if no command is given

    # Add subparsers for commands and arguments
    app_subparsers = app_parser.add_subparsers(dest="command", required=False)

    # --- Add Command: 'test' ---

    _ = app_subparsers.add_parser("test", help="Run test mode")

    # Add test command arguments
    # If the test entry point required any arguments, they would be added here

    # --- Add Command: 'config' ---

    config_subparser = app_subparsers.add_parser(
        "config",
        help="Manage settings profiles"
    )

    # Add 'config' command arguments
    # Only accept one other argument for a config session (mutually exclusive)
    group_subparser = config_subparser.add_mutually_exclusive_group()
    group_subparser.add_argument(
        # Run initial onboarding setup wizard
        "--setup",
        action="store_true",
        help="Run initial setup wizrd"
    )
    group_subparser.add_argument(
        # List profile settings
        "--list",
        action="store_true",
        help="List current settings"
    )
    group_subparser.add_argument(
        # Set profile setting
        "--set",
        nargs=2,
        metavar=(
            "KEY",
            "VALUE"
        ),
        action="append",
        help="Set a setting"
    )
    group_subparser.add_argument(
        # Get profile setting
        "--get",
        metavar="KEY",
        help="Get a setting"
    )
    group_subparser.add_argument(
        # Reset all profile settings to default values
        "--reset",
        action="store_true",
        help="Reset profile to defaults"
    )
    group_subparser.add_argument(
        # Delete profile settings
        "--delete-profile",
        metavar="NAME",
        help="Delete a profile"
    )
    group_subparser.add_argument(
        # Copy profile settings
        "--copy-profile",
        nargs=2,
        metavar=(
            "SRC",
            "DEST"
        ),
        help="Copy one profile to another"
    )
    group_subparser.add_argument(
        # Edit profile settings
        "--edit",
        action="store_true",
        help="Edit settings file manually"
    )

    # --- Add Custom Commands ---

    if app_command_recipe:
        if verbose:
            print(f"Adding commands from recipe")
            print()
        register_commands_from_recipe(app_subparsers, app_command_recipe, verbose)

    # Parse the arguments
    args = app_parser.parse_args()

    if verbose:
        formatted_args = str(args)
        formatted_args = formatted_args.replace("Namespace(","Arguments:\n\n  ")
        formatted_args = formatted_args.replace(")","")
        formatted_args = formatted_args.replace(", ","\n  ")
        print(f"{formatted_args}")
        print()

    # Prepare for arguments that override settings
    setting_overrides = None

    # --- Handle Universal Arguments ---

    # Get the profile passed in or use default
    active_profile = "default"
    if args.profile and args.profile.strip():
        active_profile = args.profile

    # Get the log level override with flag --debug or command test
    if args.debug or args.command == 'test':
        if not setting_overrides:
            setting_overrides = {}
        setting_overrides["log_level"] = "debug"

    # Get any additional setting overrides passed in with --override
    if args.override:
        if not setting_overrides:
            setting_overrides = {}
        for key, value in args.override:
            setting_overrides[key] = value

    # --- Load Properties, Settings, And Logger ---

    # Load the framework environment for app features
    #
    # THIS STEP IS ESSENTIAL
    #
    # Do this after the profile and setting override args are processed
    # Do this before running app commands
    # Do this before running any operations that use settings, database, or logging
    #
    # This enables the app to rely on the established hubs for settings, database, and logging
    CurrentAppHub = pie.AppHub(app_recipe, active_profile, setting_overrides, args)

    if not CurrentAppHub.folders_created or not CurrentAppHub.settings_created:
        print(f"Unable to load app hub")
        return

    # Settings, database, and logging are now available
    CurrentAppHub.logger.info(f"{app_name} launched")
    print()

    # --- Entry Point Command ---

    # Specify which command runs when the app is called by name
    if not args.command:
        # Run app
        if not app_entry_point_function:
            print(f"Invalid entry point")
            return
        app_entry_point_function(CurrentAppHub)
        return

    # --- Handle Command: test ---

    if args.command == "test":
        # Test app
        if not app_test_entry_point_function:
            # App test entry point is optional
            # Run a basic test if no entry point callback function is given
            print(CurrentAppHub)
            print()
            CurrentAppHub.list()
            print_subheader(f"Testing Logging")
            CurrentAppHub.logger.info("test")
            print_subheader(f"Testing Settings")
            current_settings = CurrentAppHub.settings.get_settings()
            settings.list_settings(current_settings, f"Current settings for {active_profile} profile:")
            print_subheader(f"Testing Database")
            conn = CurrentAppHub.database.connect()
            print(f"Database connected" if conn else f"Unable to connect to database")
            print()
            return
        app_test_entry_point_function(CurrentAppHub)
        return

    # --- Handle Command: config ---

    if args.command == "config":
        # Run setup wizard
        if args.setup:
            if not isinstance(app_onboarding_recipe, dict):
                print(f"No onboarding recipe is available")
                print()
                return
            force_setup = True
            _ = settings.perform_onboarding(app_onboarding_recipe, force_setup)
            return

        # List current settings
        if args.list:
            # Get settings without overrides
            current_settings = CurrentAppHub.settings.get_settings(False)
            settings.list_settings(current_settings, f"Current settings for {active_profile} profile:")
            print()
            if args.debug or args.override:
                settings.list_settings(setting_overrides, f"Setting overrides for current session:")
                print()
            return

        # Get current setting
        if args.get:
            # Get setting without overrides
            current_setting = CurrentAppHub.settings.get(args.get, False)
            print(f"{args.get}: {current_setting}")
            print()
            return

        # Reset settings to default
        if args.reset:
            confirm = input(f"Reset all settings for {active_profile} profile? (y/N): ")
            if confirm.lower().startswith("y"):
                if settings.reset_settings(CurrentAppHub.profile_settings_file, CurrentAppHub.defaults):
                    print(f"Settings for {active_profile} profile reset to defaults")
                else:
                    print(f"Unable to reset {active_profile} profile to defaults")
            else:
                print(f"Reset cancelled")
            print()
            return

        # Update settings
        if args.set:
            # Handle multiple instances of --set
            for setting_name, setting_value in args.set:
                # Clean and convert data type
                if isinstance(setting_value, str):
                    setting_value_clean = setting_value.lower().strip()
                    if setting_value_clean == "true":
                        _ = CurrentAppHub.settings.set(setting_name, True)
                    elif setting_value_clean == "false":
                        _ = CurrentAppHub.settings.set(setting_name, False)
                    elif setting_value_clean in ["none", "null"]:
                        _ = CurrentAppHub.settings.set(setting_name, None)
                    else:
                        _ = CurrentAppHub.settings.set(setting_name, setting_value)

            # Reload and display the updated setting
            print(f"Updated {active_profile} profile")
            print()
            # Get settings without overrides
            current_settings = CurrentAppHub.settings.get_settings(False)
            settings.list_settings(current_settings, f"Current settings for {active_profile} profile:")
            print()
            if args.debug or args.override:
                settings.list_settings(setting_overrides, f"Setting overrides for current session:")
                print()
            return

        # Delete profile
        if args.delete_profile:
            confirm = input(f"Are you sure you want to delete {args.delete_profile} profile? This cannot be undone! (y/N): ")
            if confirm.lower().startswith("y"):
                profile_folder = os.path.join(CurrentAppHub.settings_folder, args.delete_profile)
                _ = pie.delete_folder(profile_folder)
            else:
                print(f"Delete cancelled")
            print()
            return

        # Copy profile
        if args.copy_profile:
            source_name, destination_name = args.copy_profile
            source_folder = os.path.join(CurrentAppHub.settings_folder, source_name)
            destination_folder = os.path.join(CurrentAppHub.settings_folder, destination_name)
            _ = pie.copy_folder(source_folder, destination_folder)
            print()
            return

        # Edit profile
        if args.edit:
            pie.open_file_with_editor(CurrentAppHub.profile_settings_file)
            return

    # --- Handle Custom Command ---

    if hasattr(args, "_handler"):
        # Defer to custom handler in the app
        kwargs = args._get_kwargs()
        kwargs = kwargs[4:-1]
        args._handler(CurrentAppHub, **{k.replace("-", "_"): v for k, v in kwargs})
        return

    # Just print help if no handler was run
    app_parser.print_help()
    print()
    return

def register_commands_from_recipe(subparsers, command_recipe, verbose = False):
    """
    Processes command recipe.
    """
    for cmd_name, cmd_spec in command_recipe.items():
        if not cmd_spec:
            if verbose:
                print(f"Skipping unmapped command: {cmd_name}")
        else:
            if verbose:
                print(f"Enabling command: {cmd_name}")

            # Get valid command specification
            cmd_callback = cmd_spec.get("callback", None) or ""
            cmd_callback = cmd_callback.strip()
            cmd_help = cmd_spec.get("help", None) or ""
            cmd_help = cmd_help.strip()
            cmd_args = cmd_spec.get("args", []) or []

            if not cmd_callback:
                if verbose:
                    print(f"Skipping command: {cmd_name} (missing callback)")
                    continue

            # Convert callback string to actual function object
            cmd_callback_function = pie.get_function(cmd_callback)
            if not cmd_callback_function:
                if verbose:
                    print(f"Skipping command: {cmd_name} (invalid callback function)")
                    continue

            # Add subparser for the current command
            cmd_subparser = subparsers.add_parser(cmd_name, help=cmd_help)

            # Check for mutually exclusive group arguments
            for arg in cmd_args:
                if "exclusive" in arg.keys() and arg["exclusive"]:
                    # Create subparser for group
                    group_subparser = cmd_subparser.add_mutually_exclusive_group()
                    break

            # Process arguments for the current command
            for arg in cmd_args:
                try:
                    if "exclusive" in arg.keys() and arg["exclusive"]:
                        # Add group argument
                        group_subparser.add_argument(
                            arg["name"],
                            **{k: v for k, v in arg.items() if k != "name" and k != "exclusive"}
                        )
                    else:
                        # Add standard argument
                        cmd_subparser.add_argument(
                            arg["name"],
                            **{k: v for k, v in arg.items() if k != "name" and k != "exclusive"}
                        )
                except Exception as e:
                    print_error(e, f"Unable to parse arguments '{arg}'")
                    return None

            # Add the callback function to the current command parser
            cmd_subparser.set_defaults(_handler=cmd_callback_function)
    if verbose:
        print()

def get_test_command_recipe() -> dict:
    """
    Defines test example command line interface commands and their arguments.
    """
    command_recipe = {
        "echo": {
            "callback": "pza.prints.print_header",
            "help": "Echo input",
            "exclusive": False,
            "args": [
                {
                    "name": "--input",
                    "type": str,
                    "default": "",
                    "help": "Text to echo"
                },
            ],
        },
        "info": {
            "callback": "pza.prints.print_footer",
            "help": "Display app info",
        },
    }
    return command_recipe

if __name__ == "__main__":

    print_header(f"{__file__}")

    print_separator()

    print_subheader("Testing")
    app_name = "test_app"
    command_recipe = get_test_command_recipe()
    app_parser = argparse.ArgumentParser(
        prog=app_name,
        description=f"{app_name} command-line interface"
    )
    app_subparsers = app_parser.add_subparsers(dest="command", required=False)
    print()
    register_commands_from_recipe(app_subparsers, command_recipe)
    print()
    print(f"{app_subparsers}")
    print()

    print_separator()

    print_footer()
