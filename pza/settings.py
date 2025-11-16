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

import os
import json
import importlib
from typing import Any
from pathlib import Path

def write_settings_file(settings_file: str, current_settings: dict) -> bool:
    """
    Saves settings to .json file.
    Returns True if the file is written successfully.
    Returns False if the file is not written.
    """
    if not current_settings:
        print(f"Invalid settings")
        return False
    # Create the settings folder if it doesn't exist
    settings_folder = os.path.dirname(settings_file)
    try:
        os.makedirs(settings_folder, exist_ok=True)
    except Exception as e:
        print_error(e, f"Unable to create folder: {settings_folder}")
        return False
    # Open the file for writing
    try:
        with open(settings_file, "w", encoding="utf-8") as settings_file_io:
            # Save the dictionary to file in json format
            json.dump(current_settings, settings_file_io, indent=4)
    except FileNotFoundError as e:
        print_error(e, f"Unable to load settings file")
        return False
    except Exception as e:
        print_error(e, f"Unable to load settings file: {settings_file}")
        return False
    return True

def read_settings_file(settings_file: str) -> dict | None:
    """
    Reads settings from .json file.
    Returns a dictionary with the loaded settings or None if the load fails.
    """
    current_settings = None
    # Load the settings from the given file
    try:
        with open(settings_file, "r", encoding="utf-8") as settings_file_io:
            current_settings = json.load(settings_file_io)
    except FileNotFoundError as e:
        print_error(e, f"Unable to load settings file:")
        return None
    except json.JSONDecodeError as e:
        print_error(e, f"Unable to load settings file: {settings_file}")
        return None
    except Exception as e:
        print_error(e, f"Unable to load settings file: {settings_file}")
        return None
    return current_settings

def list_settings(given_settings: dict | None = None, title: str = "") -> None:
    """
    Prints the given settings.
    """
    if given_settings is None:
        print(f"Invalid settings")
        print()
        return
    if title:
        print_label(title)
        print()
    for setting_name, setting_value in given_settings.items():
        print_with_label(setting_name, setting_value)
    return

def reset_settings(settings_file: str, default_settings: dict) -> bool:
    """
    Resets all setting to default values.
    Deletes the settings file and recreates with defaults.
    Creates a new settings file if current settings file doesn't exist.
    Returns True if the file is created successfully.
    Returns False if the file is not created.
    """
    # Delete the existing settings
    if settings_file and os.path.exists(settings_file):
        try:
            os.remove(settings_file)
        except Exception as e:
            print_error(e, f"Unable to delete existing settings")
            return False
    # Create new settings file with defaults
    if not isinstance(default_settings, dict):
        print(f"Invalid default settings")
        return False
    write_settings_file(settings_file, default_settings)
    if not settings_file or not os.path.exists(settings_file):
        return False
    return True

def reset_setting(settings_file: str, setting_name: str, default_settings: dict) -> Any:
    """
    Resets a setting to default value and update saved settings file.
    Returns the updated value.
    """
    # Load settings without overrides
    if not default_settings:
        print(f"Invalid default settings")
        return None
    if setting_name not in default_settings.keys():
        # Default to None if setting is not pre-defined in defaults
        default_value = None
    else:
        default_value = default_settings.get(setting_name)
    # Update the setting
    updated_setting = change_setting(settings_file, setting_name, default_value)
    return updated_setting

def change_setting(settings_file: str, setting_name: str, new_value: Any) -> Any:
    """
    Changes setting to new value and update saved settings file.
    Creates the setting with the new value if it doesn't already exist.
    Returns the updated value.
    """
    if not settings_file:
        print(f"Invalid settings file")
        return None
    # Load settings without overrides
    current_settings = read_settings_file(settings_file)
    if not current_settings:
        print(f"Unable to load settings")
        return None
    # Update and save the setting
    current_settings[setting_name] = new_value
    _ = write_settings_file(settings_file, current_settings)
    return current_settings.get(setting_name)

def get_setting(settings_file: str, setting_name: str, default_settings: dict | None = None) -> Any:
    """
    Loads settings from file and return the value for setting_name.
    Creates the setting with a default value if it doesn't exist.
    """
    # Load settings
    if not settings_file:
        print(f"Invalid settings file")
        return None
    current_settings = read_settings_file(settings_file)
    if not current_settings:
        print(f"Unable to load settings")
        return None
    if setting_name not in current_settings.keys():
        # Assign default value if setting doesn't exist
        if not default_settings:
            # Default to None if defaults not provided
            default_setting = None
        else:
            # Use pre-defined defaults or fallback to None
            default_setting = default_settings.get(setting_name, None)
        # Merge the default into the current_settings
        current_settings[setting_name] = default_setting
        # Save the new setting to file
        _ = write_settings_file(settings_file, current_settings)
    current_setting = current_settings.get(setting_name)
    return current_setting

def get_setting_path(settings_file: str, setting_name: str) -> Path | None:
    """
    Returns a pathlib Path for setting_name.
    """
    file_setting = get_setting(settings_file, setting_name)
    if not isinstance(file_setting, str):
        print(f"Invalid path setting: {setting_name}")
        return None
    return Path(file_setting)

def get_setting_parent_path(settings_file: str, setting_name: str) -> Path | None:
    """
    Returns a pathlib Path for parent folder of setting_name.
    """
    file_setting = get_setting_path(settings_file, setting_name)
    if not file_setting:
        return None
    file_setting_parent = file_setting.parent
    return file_setting_parent

def perform_onboarding(settings_file: str, app_name: str, onboarding_recipe: dict, force_setup: bool = False) -> bool:
    """
    Runs the onboarding setup wizard.
    """
    if not settings_file:
        print(f"Invalid settings file")
        return False

    onboarding_required = get_setting(settings_file, "onboarding_required") or force_setup

    if not onboarding_required:
        # Onboarding is already completed or not required
        return True

    if not onboarding_recipe:
        print(f"Unable to load onboarding prompts")
        return False

    # Welcome message
    print_line()
    print(f"Initial Setup Wizard")
    print_line()
    print()
    print(f"Default settings have been created for the active profile:")
    print()

    # Load and display current environment and settings
    current_settings = read_settings_file(settings_file)
    list_settings(current_settings)
    print()

    # Show help info
    config_change_command = f"    {app_name} config --set setting_name new_value"
    print(f"Settings can be changed at any time by running:")
    print()
    print(config_change_command)
    print()
    print_line()
    print("Settings Review")
    print_line()
    print()

    # Prompt for each setting in the onboarding map
    for setting_name, prompt_options in onboarding_recipe.items():

        # Display the current value and description
        current_value = get_setting(settings_file, setting_name)
        setting_display_name = prompt_options["display"]
        setting_description = prompt_options["description"]
        setting_type = prompt_options["type"]
        setting_required = prompt_options["required"]
        validator_function = None
        if "validator" in prompt_options.keys() and isinstance(prompt_options["validator"], str):
            module_name, function_name = prompt_options["validator"].rsplit(".", 1)
            if not module_name:
                print(f"Invalid module name (use module_name.function_name)")
                return False
            try:
                validator_function = getattr(importlib.import_module(module_name), function_name)
            except Exception as e:
                print_error(e, f"Unable to discover function {prompt_options["validator"]}")
                return False
        choices = []
        if "choices" in prompt_options.keys() and isinstance(prompt_options["choices"], list):
            if setting_type != bool or len(prompt_options["choices"]) == 2:
                choices = prompt_options["choices"]
        prompt = ""
        prompt += f"Setting: {setting_display_name}{' *' if setting_required else ''}\n"
        prompt += f"Description: {setting_description}\n"
        prompt += f"Current Value: {current_value}\n"

        if setting_required:
            # Build prompt for required setting value
            prompt += f"* The {setting_display_name} setting is required\n\n"
            if prompt_options["type"] == bool:
                if choices:
                    prompt += (
                        f"Enter a setting value of "
                        f"'{choices[0]}' or '{choices[1]}' "
                        f"or type 'quit' to cancel: "
                    )
                else:
                    prompt += f"Enter a setting value of 'true' or 'false' or type 'quit' to cancel: "
            else:
                if choices:
                    prompt += (
                        f"Enter a choice from the list or type 'quit' to cancel:\n"
                        f"{choices}\n"
                        f"Choice: "
                    )
                else:
                    prompt += f"Enter a setting value or type 'quit' to cancel: "
        else:
            # Build and present prompt for user option
            prompt += f"Would you like to change the {setting_display_name} setting?\n"
            prompt += f"Enter 'y' to change the value\n"
            prompt += f"Enter 'n' to keep the default value\n"
            prompt += f"Enter 'quit' to cancel\n"
            prompt += f"(y/N/quit): "
            user_input = input(prompt).strip().lower()
            if user_input == 'quit':
                # User cancelled onboarding
                print()
                return False
            if not user_input.startswith("y"):
                # User did not enter a 'yes' response
                # Skip this non-required setting
                print()
                print(f"Keeping current value for: {setting_display_name}")
                print()
                continue
            # Build prompt for new setting value
            if setting_type == bool:
                if choices:
                    prompt = (
                        f"Enter "
                        f"'{choices[0]}' or '{choices[1]}' "
                        f"or type 'quit' to cancel: "
                    )
                else:
                    prompt = f"Enter 'true' or 'false' or type 'quit' to cancel: "

            else:
                if choices:
                    prompt = (
                        f"Enter a choice from the list or type 'quit' to cancel:\n"
                        f"{choices}\n"
                        f"Choice: "
                    )
                else:
                    prompt = f"Enter the new setting value or type 'quit' to cancel: "

        # Display the value input prompt
        input_value = input(prompt).strip()

        if input_value.lower() == 'quit':
            # User cancelled onboarding
            print()
            return False

        if setting_required or choices:
            # Loop until we have a valid input or user quits
            while True:
                input_value_valid = (
                    (choices and input_value.lower() in [x.lower() for x in choices])
                    or
                    (not choices and setting_type == bool and input_value.lower() in ["true", "false"])
                    or
                    (not choices and setting_type != bool and input_value.lower() not in ["", "none", "null"])
                )
                if input_value_valid and validator_function:
                    validation_message = validator_function(input_value)
                    if validation_message:
                        print(validation_message)
                        input_value_valid = False
                if not input_value_valid:
                    prompt = f"Enter the required setting value or type 'quit' to cancel: "
                    input_value = input(prompt).strip()
                    if input_value == 'quit':
                        # User cancelled onboarding
                        print()
                        return False
                    # Continue loop to validate new input
                    continue
                else:
                    # End loop with valid value
                    break

        if input_value == "":
            print(f"No value was entered.")
            print()
            print(f"Keeping current value for: {setting_display_name}")
            print()
            print(f"Use the config command to change it later:")
            print()
            print(config_change_command.replace("setting_name", setting_name))
            print()
            continue

        # Handle settings with special data types
        if setting_type == bool:
            setting_value = input_value.lower()
            if setting_value == "true" or (choices and setting_value == choices[0].lower()):
                setting_value = True
            elif setting_value == "false" or (choices and setting_value == choices[1].lower()):
                setting_value = False
            else:
                print(f"Invalid value")
                print()
                print(f"Use the config command to change {setting_display_name} to 'true' or 'false' later:")
                print()
                print(f"{config_change_command.replace("setting_name", setting_name).replace("new_value", "true")}")
                print()
                continue
        elif input_value.lower() in ["none", "null"]:
            setting_value = None
        else:
            # Save string setting without changing case
            setting_value = input_value
        # Change the setting to the new value
        change_setting(settings_file, setting_name, setting_value)
        print()

    print_line()
    print(f"Setup Completed")
    print_line()
    print()
    # Change the setting flag to indicate onboarding is completed
    change_setting(settings_file, "onboarding_required", False)

    # Return true after all required settings have been entered and user did not quit
    return True

if __name__ == "__main__":

    print_header(f"{__file__}")

    print_separator()

    print()

    print_separator()

    print_footer()
