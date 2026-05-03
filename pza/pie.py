# --- Framework Modules ---

from pza.prints import (
    print_error,
    print_footer,
    print_header,
    print_separator,
    print_subheader,
    print_with_label,
)
from pza.logger import get_logger
from pza import settings
from pza import database

# --- Built-in Modules ---

from typing import Any, List
from pathlib import Path
from logging import Logger
from importlib import resources
import os
import platform
import shutil
import subprocess
import json
import importlib
import sqlite3
import urllib.request
import ssl
import webbrowser

# --- External Modules ---

import certifi

# --- Framework Constants ---

FRAMEWORK_NAME = "pza"
FRAMEWORK_DISPLAY_NAME = "Pza"
FRAMEWORK_VERSION = "0.4.6"

# --- Hub for app features ---

class AppHub(object):
    """
    Provides framework features.

    Initializes the environment for an app:
       - Loads app properties
       - Creates all app folders
       - Creates settings file
       - Creates database file
       - Creates logging mechanism

    Minimum requirement is a recipe dictionary containing the app name.
    Everything else is optional.
    Example: {"app_name": "my_app"}.
    """
    def __init__(
            self,
            app_recipe: dict,
            active_profile: str = "default",
            setting_overrides: dict | None = None,
            runtime_arguments = None
        ) -> None:

        # Define constant attributes
        self.SETTINGS_FILENAME = f"settings.json"

        # Define all attributes with default values
        self.name = None
        self.display_name = None
        self.version = None
        self.settings_recipe = None
        self.command_recipe = None
        self.onboarding_recipe = None
        self.database_recipe = None
        self.folders_created = False
        self.settings_created = False

        # Define file and folder attributes
        self.settings_folder = None
        self.profile_settings_folder = None
        self.default_documents_folder = None
        self.default_profile_documents_folder = None
        self.log_folder = None
        self.profile_settings_file = None
        self.log_file = None
        self.database_file = None

        # Define pathlib Path attributes for convenience
        self.settings_folder_path = None
        self.profile_settings_folder_path = None
        self.default_documents_folder_path = None
        self.default_profile_documents_folder_path = None
        self.log_folder_path = None
        self.profile_settings_file_path = None
        self.log_file_path = None
        self.database_file_path = None

        # Define feature class attributes
        self.settings = None
        self.logger = None
        self.database = None

        # Save profile, recipe, overrides, and arguments
        self.profile = active_profile
        self.recipe = app_recipe
        self.overrides = setting_overrides
        self.arguments = runtime_arguments

        # Handle defaults
        self.framework_settings_recipe = get_framework_settings_recipe()
        self.defaults = None

        # Validate profile
        if (
            not self.profile
            or not isinstance(self.profile, str)
            or not self.profile.strip()
        ):
            self.profile = "default"
        else:
            self.profile = self.profile.strip()

        # Populate attributes from the recipe
        if isinstance(app_recipe, dict):
            self.name = app_recipe.get("name", None)
            self.display_name = app_recipe.get("display_name", self.name)
            self.version = app_recipe.get("version", None)
            self.settings_recipe = app_recipe.get("settings_recipe", None)
            self.command_recipe = app_recipe.get("command_recipe", None)
            self.onboarding_recipe = app_recipe.get("onboarding_recipe", None)
            self.database_recipe = app_recipe.get("database_recipe", None)

        # App name is required to continue
        if self.name:
            # Create critical folders populating attributes
            self.settings_folder, \
            self.profile_settings_folder, \
            self.default_documents_folder, \
            self.default_profile_documents_folder, \
            self.log_folder \
            = initialize_folders(self.name, self.profile)
            self.folders_created = (
                self.settings_folder and os.path.exists(self.settings_folder) and
                self.profile_settings_folder and os.path.exists(self.profile_settings_folder) and
                self.default_documents_folder and os.path.exists(self.default_documents_folder) and
                self.default_profile_documents_folder and os.path.exists(self.default_profile_documents_folder) and
                self.log_folder and os.path.exists(self.log_folder)
            )

            if self.folders_created:
                # Get defaults with placeholders replaced after loading folder attributes
                self.defaults = self.merge_defaults()

                # Create profile settings file after creating folders and merging defaults
                self.profile_settings_file = get_profile_settings_file(
                    self.name,
                    self.profile,
                    self.SETTINGS_FILENAME,
                    self.defaults
                )
                self.settings_created = self.profile_settings_file and os.path.exists(self.profile_settings_file)

                # Load the feature class attributes after loading the recipe, profile, folders, and files
                if self.settings_created:
                    self.settings = SettingsHub(
                        self.name,
                        self.profile,
                        self.SETTINGS_FILENAME,
                        self.defaults,
                        self.overrides
                    )

                # Load logger after loading settings to get the correct log level
                self.log_file = get_log_file(self.name, f"{self.name}.log")
                self.logger = self.load_logger()

                # Load the database
                self.database_file = get_database_file(self.name, f"{self.name}.db")
                self.database = DatabaseHub(self.name, f"{self.name}.db", self.database_recipe)

                # Geth pathlib paths
                self.settings_folder_path = Path(self.settings_folder)
                self.profile_settings_folder_path = Path(self.profile_settings_folder)
                self.default_documents_folder_path = Path(self.default_documents_folder)
                self.default_profile_documents_folder_path = Path(self.default_profile_documents_folder)
                self.log_folder_path = Path(self.log_folder)
                self.profile_settings_file_path = Path(self.profile_settings_file)
                self.log_file_path = Path(self.log_file)
                self.database_file_path = Path(self.database_file)

    def __str__(self):
        """
        Returns a string represenation of the class.
        """
        return f"AppHub: {self.display_name} ({FRAMEWORK_DISPLAY_NAME} version {FRAMEWORK_VERSION})"

    def list(self):
        """
        Prints a list of hub attributes.
        """
        print_with_label(f"Application Name", self.name)
        print_with_label(f"Application Display Name", self.display_name)
        print_with_label(f"Profile Name", self.profile)
        print_with_label(f"App Settings Folder", self.settings_folder)
        print_with_label(f"Profile Settings Folder", self.profile_settings_folder)
        print_with_label(f"Profile Settings File", self.profile_settings_file)
        print_with_label(f"App Database File", self.database_file)
        print_with_label(f"Log File", self.log_file)
        print_with_label(f"Logger", self.logger)

    def load_logger(self) -> Logger:
        """
        Loads app logging mechanism.
        """
        # Get the log level for the current session
        if isinstance(self.overrides, dict) and "log_level" in self.overrides.keys():
            # Use override log level
            log_level = self.overrides.get("log_level")
        else:
            # Use log level from saved settings file
            current_settings = read_json_file_to_dictionary(self.profile_settings_file)
            if isinstance(current_settings, dict):
                log_level = current_settings.get("log_level", "info")
            else:
                log_level = "info"
        return get_logger(self.name, log_level, self.log_file)

    def get_placeholder_recipe(self) -> dict:
        """
        Returns a find/replace mapping for setting placeholders.
        """
        replacements = {}
        replacements["[profile]"] = self.profile or ""
        replacements["[app_name]"] = self.name or ""
        replacements["[app_display_name]"] = self.display_name or ""
        replacements["[app_version]"] = self.version or ""
        replacements["[default_app_documents_folder]"] = get_default_app_documents_folder(self.name) or ""
        replacements["[default_profile_documents_folder]"] = get_default_profile_documents_folder(self.name, self.profile) or ""
        replacements["[app_settings_folder]"] = get_app_settings_folder(self.name) or ""
        replacements["[profile_settings_folder]"] = get_profile_settings_folder(self.name, self.profile) or ""
        replacements["[log_folder]"] = get_log_folder(self.name) or ""
        return replacements

    def merge_defaults(self, verbose: bool = False) -> dict:
        """
        Get a dictionary with the framwork default and app default settings merged.
        App defaults will override any settings that already exist in the framework.
        """
        # Validate framework defaults
        if not isinstance(self.framework_settings_recipe, dict):
            print(f"Invalid framwork default settings")
            return None
        # Merge app defaults
        merged_defaults = self.framework_settings_recipe.copy()
        if isinstance(self.settings_recipe, dict):
            merged_defaults.update(self.settings_recipe)
        # Replace placeholders
        replacements = self.get_placeholder_recipe()
        for find_text, replace_text in replacements.items():
            for setting_name, setting_value in merged_defaults.items():
                if not isinstance(setting_value, str):
                    # Skip non-string settings
                    continue
                merged_defaults[setting_name] = setting_value.replace(find_text, replace_text)
        if verbose:
            settings.list_settings(self.framework_settings_recipe, "Framework Defaults")
            print()
            settings.list_settings(self.settings_recipe, "App Defaults")
            print()
            settings.list_settings(merged_defaults, "Merged Defaults")
        return merged_defaults

    def get_profiles(self) -> list:
        """
        Return a list of existing profile folder names.
        """
        if not self.app_name:
            return None
        if not self.settings_folder or not os.path.exists(self.settings_folder):
            return None
        subfolders = get_subfolders(self.settings_folder)
        return subfolders

    def setup(self, force_setup: bool = False) -> bool:
        onboarding_completed = settings.perform_onboarding(
            self.profile_settings_file,
            self.name,
            self.onboarding_recipe,
            force_setup
        )
        return onboarding_completed

# --- Hub for settings features ---

class SettingsHub(object):
    """
    Provides app settings features.
    """
    def __init__(
            self,
            app_name: str,
            active_profile: str,
            settings_file_name: str,
            default_settings: dict | None = None,
            setting_overrides: dict | None = None
        ) -> None:
        self.app_name = app_name
        self.profile = active_profile
        self.overrides = setting_overrides
        self.defaults = default_settings
        self.settings_folder = get_app_settings_folder(self.app_name)
        self.profile_settings_folder = get_profile_settings_folder(self.app_name, self.profile)
        self.profile_settings_file_name = settings_file_name
        self.profile_settings_file = get_profile_settings_file(self.app_name, self.profile, self.profile_settings_file_name, self.defaults)
        self.settings_folder_path = Path(self.settings_folder)
        self.profile_settings_folder_path = Path(self.profile_settings_folder)
        self.profile_settings_file_path = Path(self.profile_settings_file)

    def get_settings(self, allow_overrides: bool = True) -> dict | None:
        """
        Reads settings from .json file for the active profile.
        Creates settings file with defaults if it doesn't exist.
        Overrides are injected if they exist and 'allow_overrides' is True.
        Use 'allow_overrides=False' if any settings will be updated and saved back to file.
        Returns a dictionary with the loaded settings.
        """
        if not self.profile_settings_file:
            print(f"Invalid profile settings file")
            return None
        # Create settings file with defaults if it doesn't exist
        if not os.path.exists(self.profile_settings_file):
            settings_written = settings.write_settings_file(self.profile_settings_file, self.defaults)
            if not settings_written:
                return None
        # Get current settings from file
        current_settings = settings.read_settings_file(self.profile_settings_file)
        # Merge in overrides
        if allow_overrides and isinstance(self.overrides, dict):
            current_settings.update(self.overrides)
        return current_settings

    def get(self, setting_name: str, allow_overrides: bool = True) -> Any:
        """
        Reads settings from file and returns the value for setting_name.
        Creates the setting with a default value if it doesn't exist.
        Override value will be returned if it exists and 'allow_overrides' is True.
        """
        # Use the override if allowed and found
        if (
            allow_overrides and
            isinstance(self.overrides, dict) and
            setting_name in self.overrides.keys()
        ):
            current_setting = self.overrides.get(setting_name)
            return current_setting

        # Load settings without overrides
        current_settings = self.get_settings(False)
        if not current_settings:
            print(f"Unable to load settings")
            return None
        if setting_name not in current_settings.keys():
            # Assign default value if setting doesn't exist
            if not self.defaults:
                print(f"Unable to load default settings")
                return None
            # Default to None if setting is not pre-defined in defaults
            default_setting = self.defaults.get(setting_name, None)
            # Merge the default into the current_settings
            current_settings[setting_name] = default_setting
            # Save the setting to file
            # This is safe because current settings do not include overrides
            settings_file = get_profile_settings_file(self.app_name, self.profile, self.profile_settings_file_name, self.defaults)
            _ = settings.write_settings_file(settings_file, current_settings)
        current_setting = current_settings.get(setting_name)
        return current_setting

    def get_path(self, setting_name: str, allow_overrides: bool = True) -> Path:
        """
        Assumes the setting value is file or folder path string.
        Returns a pathlib Path() for the setting value.
        """
        item = self.get(setting_name, allow_overrides)
        item_path = Path(item)
        return item_path

    def get_parent_path(self, setting_name: str, allow_overrides: bool = True) -> Path:
        """
        Assumes the setting value is file or folder path string.
        Finds the parent folder of the item specified by the setting value.
        Returns a pathlib Path() for the parent folder.
        """
        item = self.get(setting_name, allow_overrides)
        item_path = Path(item)
        parent_folder_path = item_path.parent
        return parent_folder_path

    def get_app_documents_folder(self, allow_overrides: bool = True) -> Path:
        """
        Returns path string for app documents folder setting.
        """
        folder = self.get("app_documents_folder", allow_overrides)
        return folder

    def get_profile_documents_folder(self, allow_overrides: bool = True) -> Path:
        """
        Returns path string for profile documents folder setting.
        """
        folder = self.get("profile_documents_folder", allow_overrides)
        return folder

    def get_app_documents_folder_path(self, allow_overrides: bool = True) -> Path:
        """
        Returns pathlib Path for app documents folder setting.
        """
        return Path(self.get_app_documents_folder(allow_overrides))

    def get_profile_documents_folder_path(self, allow_overrides: bool = True) -> Path:
        """
        Returns pathlib Path for profile documents folder setting.
        """
        return Path(self.get_profile_documents_folder(allow_overrides))

    def set(self, setting_name: str, setting_value: Any) -> Any:
        """
        Changes setting to new value and update saved settings file.
        Creates the setting with the new value if it doesn't already exist.
        Returns the updated value.
        """
        return settings.change_setting(self.profile_settings_file, setting_name, setting_value)

# --- Hub for database features ---

class DatabaseHub(object):
    """
    Provides app database features.
    """
    def __init__(
            self,
            app_name: str,
            database_file_name: str,
            database_recipe: dict | None = None
        ) -> None:
        self.app_name = app_name
        self.file = get_database_file(self.app_name, database_file_name)
        self.database_recipe = database_recipe
        self.database_created = False
        self.connection = None
        if self.file and self.database_recipe:
            self.database_created = self.create()

    def connect(self) -> sqlite3.Connection:
        return database.connect(self.file)

    def create(self) -> bool:
        return database.create_database_from_recipe(self.file, self.database_recipe)

# --- Framework Recipes ---

def get_framework_settings_recipe() -> dict:
    """
    Framework defaults that all apps will start with.
    The 'onboarding_required' flag can be used to enforce
    an initial user setup if needed by the app.

    Use placeholders defined in 'get_placeholder_recipe()'
    for settings to be filled in after APP_NAME and PROFILE are set:
    """
    recipe = {
        "onboarding_required": True,
        "log_level": "info",
        "app_documents_folder": "[default_app_documents_folder]",
        "profile_documents_folder": "[default_profile_documents_folder]",
    }
    return recipe

# --- Test Helpers ---

def load_test_app(log_level: str = "debug", setting_overrides: dict | None = None) -> bool:
    """
    Creates a dummy app for testing.
    """
    test_recipe = {"app_name": "test_app"}
    # Handle optional session overrides
    if setting_overrides or log_level:
        test_overrides = {}
        if isinstance(setting_overrides, dict):
            test_overrides.update(setting_overrides)
        if log_level:
            test_overrides["log_level"] = log_level
    else:
        test_overrides = None
    test_profile = None
    # Load the framework environment for the test app
    return AppHub(test_recipe, test_profile, test_overrides, None)

# --- Folder and File Operation Helpers ---

def create_folder(target_folder: str) -> bool:
    """
    Creates a folder.
    """
    if not target_folder:
        print(f"Invalid folder")
        return False
    if os.path.exists(target_folder):
        return True
    try:
        # Create the folder
        os.makedirs(target_folder, exist_ok=True)
    except Exception as e:
        print_error(e, f"Unable to create folder: {target_folder}")
        return False
    return os.path.exists(target_folder)

def delete_folder(target_folder: str) -> bool:
    """
    Deletes a folder.
    Does not move to trash.
    This cannot be undone.
    """
    if not target_folder or not os.path.exists(target_folder):
        print(f"Folder does not exist: {target_folder}")
        return False
    try:
        shutil.rmtree(target_folder)
        print(f"Deleted folder: {target_folder}")
    except Exception as e:
        print_error(e, f"Unable to delete folder: {target_folder}")
        return False
    return True

def copy_folder(source_folder: str, destination_folder: str) -> bool:
    """
    Copies a folder from source to destination.
    """
    if not source_folder or not os.path.exists(source_folder) or not os.path.isdir(source_folder):
        print(f"Invalid source folder: {source_folder}")
        return False
    if not destination_folder:
        print(f"Invalid destination folder: {destination_folder}")
        return False
    if os.path.exists(destination_folder):
        print(f"Folder already exists: {destination_folder}")
        return False
    try:
        shutil.copytree(source_folder, destination_folder)
        print(f"Copied folder from {source_folder} to {destination_folder}")
    except Exception as e:
        print(f"Unable to copy folder from {source_folder} to {destination_folder}")
        return False
    return True

def copy_folder_contents(
        source_folder: str,
        destination_folder: str,
        include_metadata: bool = False,
        exclude_names: List[str] = []
    ) -> bool:
    """
    Copies contents of a folder from source to destination.
    """
    if not source_folder or not os.path.exists(source_folder) or not os.path.isdir(source_folder):
        print(f"Invalid source folder: {source_folder}")
        return False
    if not destination_folder:
        print(f"Invalid destination folder: {destination_folder}")
        return False
    if not os.path.exists(destination_folder):
        folder_created = create_folder(destination_folder)
    else:
        folder_created = True
    if not folder_created:
        return False
    try:
        print()
        print(f"Copying folder: {source_folder}")
        contents = os.listdir(source_folder)
        for item_name in contents:
            if item_name.lower() in [x.lower() for x in exclude_names]:
                continue
            source = os.path.join(source_folder, item_name)
            destination = os.path.join(destination_folder, item_name)
            if os.path.isdir(source):
                copy_folder_contents(source, destination, include_metadata, exclude_names)
            elif include_metadata:
                shutil.copy2(source, destination)
            else:
                shutil.copy(source, destination)
        print()
        print(f"Copied folder contents\nFrom: {source_folder}\nTo: {destination_folder}")
    except Exception as e:
        print_error(e, f"Unable to copy folder contents\nFrom: {source_folder}\nTo: {destination_folder}")
        return False
    return True

def copy_file(source_file: str, destination_file: str) -> bool:
    """
    Copies a folder from source to destination.
    """
    if not source_file or not os.path.exists(source_file) or os.path.isdir(source_file):
        print(f"Invalid source file: {source_file}")
        return False
    if not destination_file:
        print(f"Invalid destination file: {destination_file}")
        return False
    if os.path.exists(destination_file):
        print(f"File already exists: {destination_file}")
        return False
    try:
        shutil.copyfile(source_file, destination_file)
        print(f"Copied file from {source_file} to {destination_file}")
    except Exception as e:
        print(f"Unable to copy file from {source_file} to {destination_file}")
        return False
    return True

def get_subfolders(target_folder: str, recursive: bool = False) -> list | None:
    """
    Generates a list of subfolders of the given folder.
    """
    if (
        not target_folder or
        not isinstance(target_folder, str) or
        not os.path.exists(target_folder) or
        not os.path.isdir(target_folder)
    ):
        print(f"Invalid folder")
        return None
    subfolders = []
    if recursive:
        # Traverse current folder and subfolders
        for root, folder_names, _ in os.walk(target_folder):
            for folder_name in folder_names:
                subfolders.append(os.path.join(root, folder_name))
    else:
        # Traverse current folder only
        for folder_item_name in os.listdir(target_folder):
            folder_item = os.path.join(target_folder, folder_item_name)
            if os.path.isdir(folder_item):
                subfolders.append(folder_item_name)
    return subfolders

def delete_file(target_file: str) -> bool:
    """
    Deletes a file.
    Does not move to trash.
    This cannot be undone.
    """
    if not target_file or not os.path.exists(target_file):
        print(f"File does not exist: {target_file}")
        return False
    try:
        os.remove(target_file)
        print(f"Deleted file: {target_file}")
    except Exception as e:
        print_error(e, f"Unable to delete file: {target_file}")
        return False
    return True

# --- Folder Location and Creation Helpers ---

def get_system_settings_folder() -> str:
    """
    Gets string path for platform default settings folder.
    """
    if platform.system() == "Windows":
        # Windows
        appdata_dir = os.environ["APPDATA"]
    elif platform.system() == "Darwin":
        # macOS
        appdata_dir = os.path.join(
            os.path.expanduser("~"),
            "Library",
            "Application Support",
            ""
        )
    else:
        # Linux
        appdata_dir = os.path.join(os.path.expanduser("~"), ".config", "")
    return appdata_dir

def get_pza_folder() -> str | None:
    """
    Getsn string path for framework settings folder.
    """
    system_folder = get_system_settings_folder()
    if not system_folder:
        return None
    pza_folder = os.path.join(system_folder, FRAMEWORK_NAME, "")
    _ = create_folder(pza_folder)
    return pza_folder

def get_pza_log_file() -> str | None:
    """
    Gets string path for framework log file.
    """
    pza_folder = get_pza_folder()
    if not pza_folder:
        return None
    log_file = os.path.join(pza_folder, f"{FRAMEWORK_NAME}.log")
    return log_file

def get_app_settings_folder(app_name: str) -> str | None:
    """
    Gets string path for app settings folder.
    Log and profile subfolders are stored in this folder.
    """
    if not app_name:
        return None
    system_folder = get_system_settings_folder()
    if not system_folder:
        return None
    app_folder = os.path.join(system_folder, app_name, "")
    _ = create_folder(app_folder)
    return app_folder

def get_profile_settings_folder(app_name: str, profile) -> str | None:
    """
    Gets string path for profile settings folder.
    """
    if not app_name or not profile:
        return None
    app_settings_folder = get_app_settings_folder(app_name)
    if not app_settings_folder:
        return None
    profile_settings_folder = os.path.join(app_settings_folder, profile, "")
    _ = create_folder(profile_settings_folder)
    return profile_settings_folder

def get_default_app_documents_folder(app_name: str) -> str | None:
    """
    Gets string path for default app documents folder.
    """
    if not app_name:
        return None
    home_documents_folder = os.path.expanduser("~")
    app_documents_folder = os.path.join(home_documents_folder, "Documents", app_name, "")
    _ = create_folder(app_documents_folder)
    return app_documents_folder

def get_default_profile_documents_folder(app_name: str, profile: str) -> str | None:
    """
    Gets string path for profile documents folder.
    """
    if not app_name or not profile:
        return None
    app_documents_folder = get_default_app_documents_folder(app_name)
    if not app_documents_folder:
        return None
    default_profile_documents_folder = os.path.join(app_documents_folder, profile, "")
    _ = create_folder(default_profile_documents_folder)
    return default_profile_documents_folder

def initialize_folders(app_name: str, profile: str) -> bool:
    """
    Creates critical folders.
    Returns the folder paths as strings.
    """
    app_settings_folder = get_app_settings_folder(app_name)
    if not app_settings_folder:
        print(f"Unable to get app settings folder")
        return False
    profile_settings_folder = get_profile_settings_folder(app_name, profile)
    if not profile_settings_folder:
        print(f"Unable to get profile settings folder")
        return False
    default_app_documents_folder = get_default_app_documents_folder(app_name)
    if not default_app_documents_folder:
        print(f"Unable to get app documents folder")
        return False
    default_profile_documents_folder = get_default_profile_documents_folder(app_name, profile)
    if not default_profile_documents_folder:
        print(f"Unable to get profile documents folder")
        return False
    log_folder = get_log_folder(app_name)
    if not log_folder:
        print(f"Unable to get log folder")
        return False
    return \
        app_settings_folder, \
        profile_settings_folder, \
        default_app_documents_folder, \
        default_profile_documents_folder, \
        log_folder

def get_log_folder(app_name: str) -> str | None:
    """
    Get string path for log folder.
    """
    if not app_name:
        return None
    app_settings_folder = get_app_settings_folder(app_name)
    if not app_settings_folder:
        return None
    log_folder = os.path.join(app_settings_folder, "logs", "")
    _ = create_folder(log_folder)
    return log_folder

# --- File Location and Creation Helpers ---

def get_log_file(app_name: str, file_name: str) -> str | None:
    """
    Gets string path for log file.
    """
    if not app_name:
        return None
    log_folder = get_log_folder(app_name)
    if not log_folder:
        return None
    log_file = os.path.join(log_folder, file_name)
    return log_file

def get_database_file(app_name: str, file_name: str) -> str | None:
    """
    Gets string path for app database file.
    """
    app_settings_folder = get_app_settings_folder(app_name)
    if not app_settings_folder:
        return None
    database_file = os.path.join(app_settings_folder, file_name)
    return database_file

def get_profile_settings_file(
    app_name: str,
    profile: str,
    file_name: str,
    default_settings: dict | None = None
) -> str | None:
    """
    Gets string path for profile settings file.
    Creates the file with defaults if it doesn't exist.
    """
    if not app_name or not profile:
        return None
    profile_folder = get_profile_settings_folder(app_name, profile)
    if not profile_folder:
        return None
    settings_file = os.path.join(profile_folder, file_name)
    if not os.path.exists(settings_file) and isinstance(default_settings, dict):
        _ = write_json_file_from_dictionary(settings_file, default_settings)
    return settings_file

# --- I/O Helpers ---

def write_json_file_from_dictionary(json_file: str, content_dictionary: dict) -> bool:
    """
    Writes dictionary content to .json file.
    """
    try:
        with open(json_file, "w", encoding="utf-8") as json_file_io:
            json.dump(content_dictionary, json_file_io, indent=4)
    except Exception as e:
        print_error(e, f"Unable to write {json_file}")
        return False
    return True

def read_json_file_to_dictionary(json_file: str) -> dict | None:
    """
    Reads from .json file.
    Returns a dictionary with the loaded data or None if the load fails
    """
    json_dictionary = None
    try:
        with open(json_file, "r", encoding="utf-8") as json_file_io:
            json_dictionary = json.load(json_file_io)
    except FileNotFoundError as e:
        print_error(e, f"Unable to read json file")
    except json.JSONDecodeError as e:
        print_error(e, f"Unable to read json file {json_file}")
    except Exception as e:
        print_error(e, f"Unable to read json file {json_file}")
    return json_dictionary

def write_file_from_list(txt_file: str, content_list: list, mode = "w") -> bool:
    """
    Writes list content to .txt file.
    """
    try:
        with open(txt_file, mode, encoding="utf-8") as txt_file_io:
            for content in content_list:
                txt_file_io.write(content + f"\n")
    except Exception as e:
        print_error(e, f"Unable to write {txt_file}")
        return False
    return True

def read_file_to_list(txt_file: str) -> list | None:
    """
    Reads from .txt file.
    Returns a list with the loaded data or None if the load fails
    """
    content_list = None
    try:
        with open(txt_file, "r", encoding="utf-8") as txt_file_io:
            content_list = txt_file_io.readlines()
            content_list = [content.strip() for content in content_list]
    except FileNotFoundError as e:
        print_error(e, f"Unable to read txt file")
    except Exception as e:
        print_error(e, f"Unable to read txt file {txt_file}")
    return content_list

# --- Download Helpers ---

def download(url: str, destination_file: str, overwrite_existing: bool = True) -> bool:
    """
    Downloads a file from url and saves as destination_file.
    Existing file will be permanently deleted if overwrite_existing is True.

    Returns True if if the file was downloaded successfully or
    download was not needed because destination_file file exists and
    overwrite_existing is False.
    """
    # Check for existing file
    if os.path.exists(destination_file):
        if overwrite_existing:
            if not delete_file(destination_file):
                return False
        else:
            return True
    # Download the content
    try:
        ssl_context = ssl.create_default_context(cafile=certifi.where())
        response = urllib.request.urlopen(url, context=ssl_context)
        content = response.read()
    except Exception as e:
        print_error(e, f"Unable to download {url}")
        return False
    # Save the content to file
    try:
        with open(destination_file, "wb") as destination_file_io:
            destination_file_io.write(content)
    except Exception as e:
        print_error(e, f"Unable to save to {destination_file}")
        return False
    # Confirm the download succeeded
    if not os.path.exists(destination_file):
        print(f"Downloaded file does not exist:  {destination_file}")
        return False
    return True

# --- System Helpers ---

def open_file(file: str) -> bool:
    """
    Launches the default application for the file.
    """
    if not file or not os.path.exists(file):
        print(f"File does not exist: {file}")
        return False
    try:
        if platform.system() == "Darwin":       # macOS
            subprocess.call(("open", file))
        elif platform.system() == "Windows":    # Windows
            os.startfile(file)
        elif platform.system() == "Linux":      # Linux variants
            subprocess.call(("xdg-open", file))
        else:
            raise OSError("Unsupported operating system")
    except Exception as e:
        print_error(e, f"Unable to open {file}")
        return False
    return True

def open_file_with_browser(file: str) -> bool:
    """
    Launches the default web browser with the file.
    """
    if not file or not os.path.exists(file):
        print(f"File does not exist: {file}")
        return False
    try:
        absolute_file = os.path.abspath(file)
        url = f"file://{absolute_file}"
        # Try named default browsers first
        for name in ["windows-default", "safari", "firefox", "mozilla", "chrome", "google-chrome"]:
            try:
                browser = webbrowser.get(using=name)
                if not browser.open(url):
                    # Keep trying if this one failed
                    continue
                return True
            except webbrowser.Error:
                continue
        # Fallback to system default (may be a text editor for file:// urls)
        browser = webbrowser.get()
        browser.open(url)
    except Exception as e:
        print_error(e, f"Unable to open {file}")
        return False
    return True

def open_file_with_editor(file: str) -> None:
    """
    Launches a text editor with the file.
    """
    editor = os.environ.get("EDITOR") or ("notepad" if os.name == "nt" else "nano")
    subprocess_list = [editor, file]
    if not file or not os.path.exists(file):
        print(f"File does not exist: {file}")
        return
    run_subprocess(subprocess_list)
    return

def run_subprocess(subprocess_list: list) -> None:
    """
    Runs a subprocess with error checking.
    """
    if not isinstance(subprocess_list, list):
        print(f"Invalid subprocess input")
        return
    try:
        subprocess.call(subprocess_list)
    except Exception as e:
        print_error(e)

# --- Introspection Helpers ---

def get_function(function_path: str):
    """
    Discovers the function object from the given path.
    Example Path: module_name.function_name
    """
    if not isinstance(function_path, str):
        print(f"Invalid function path: {function_path}")
        return None
    module_name, function_name = function_path.rsplit(".", 1)
    if not module_name:
        print(f"Invalid module name (use module_name.function_name)")
        return None
    current_function = None
    try:
        current_function = getattr(importlib.import_module(module_name), function_name)
    except Exception as e:
        print_error(e, f"Unable to discover function {function_path}")
    return current_function

def get_resource(relative_file_or_folder: str) -> str:
    """
    Returns a path string object pointing to a resource file or folder inside the package.
    """
    package_root_folder = __package__.split(".")[0]
    return str(resources.files(package_root_folder).joinpath(relative_file_or_folder))

def list_resources(relative_folder: str = "", pattern: str = "*") -> List[str]:
    """
    Lists all resource files under a given subfolder of the package.
    Returns a list of path strings for existing files.
    """
    package_root_folder = __package__.split(".")[0]
    base_folder = resources.files(package_root_folder).joinpath(relative_folder)
    if not base_folder.exists():
        return []
    return [entry for entry in base_folder.rglob(pattern) if entry.is_file()]

# --- Main Entry Point ---

def main(PzaHub: AppHub) -> None:
    """
    Displays framework version.
    """
    print(f"{FRAMEWORK_DISPLAY_NAME} version {FRAMEWORK_VERSION}")
    print()
    return

if __name__ == "__main__":

    print_header(f"{__file__}")

    print_separator()

    main()

    print_separator()

    print_footer()
