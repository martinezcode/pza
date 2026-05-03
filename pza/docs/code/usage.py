# Code for Basic Usage in README

# Import framework
import pza.pie

# Define app spec
def get_app_recipe() -> dict:
    """
    Defines app specifications.
    """
    recipe = {
        "name": "test_app",
        "display_name": "Test App",
        "version": "0.4.6",
    }
    return recipe

# Initialize app features
CurrentAppHub = pza.pie.AppHub(get_app_recipe())

# Display app info
CurrentAppHub.list()

# Test logging
CurrentAppHub.logger.info("foo")

# Access app folders and files
print(f"App Settings Folder: {CurrentAppHub.settings_folder}")
print(f"Profile Settings Folder: {CurrentAppHub.profile_settings_folder}")
print(f"App Documents Folder: {CurrentAppHub.settings.get_app_documents_folder()}")
print(f"Profile Documents Folder: {CurrentAppHub.settings.get_profile_documents_folder()}")
print(f"App Database File: {CurrentAppHub.database_file}")
print(f"Database Created: {CurrentAppHub.database.database_created}")