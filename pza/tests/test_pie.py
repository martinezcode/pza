"""
Tests

Note: This test demonstrates the minimum requirements to launch an app.
(App Name + Entry Point Function)
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
from pza.tests.test_helpers import *
from pza import pie
from pza.database import *

import time

if __name__ == "__main__":

    # Set delay time between commands for viewing the output
    sleep_time = 2

    print_header(f"{__file__}")

    print_separator()

    # Test
    print_subheader(f"Testing App Hub Creation")

    test_recipe = get_test_app_recipe()
    verbose = True
    if not isinstance(test_recipe, dict):
        print(f"Invalid test recipe")

    CurrentAppHub = pie.AppHub(test_recipe)

    print(CurrentAppHub)
    print()
    CurrentAppHub.list()
    print()

    print_separator()
    time.sleep(sleep_time)

    # Test
    print_subheader(f"Testing Logging")

    CurrentAppHub.logger.info("foo")
    print()

    print_separator()
    time.sleep(sleep_time)

    # Test Settings
    print_subheader(f"Testing Edit and Read Settings")

    app_documents_folder = CurrentAppHub.settings.get_app_documents_folder()
    profile_documents_folder = CurrentAppHub.settings.get_profile_documents_folder()
    print_with_label(f"App Documents Folder", app_documents_folder)
    print_with_label(f"Profile Documents Folder", profile_documents_folder)
    print()

    setting_name = f"log_level"
    original_setting = CurrentAppHub.settings.get(setting_name)
    print_with_label(f"Original {setting_name}", original_setting)
    changed_setting = CurrentAppHub.settings.set(setting_name, f"info")
    print_with_label(f"Changed {setting_name}", changed_setting)
    saved_setting = CurrentAppHub.settings.get(setting_name)
    print_with_label(f"Saved {setting_name}", saved_setting)
    restored_setting = CurrentAppHub.settings.set(setting_name, original_setting)
    print_with_label(f"Restored {setting_name}", restored_setting)
    saved_setting = CurrentAppHub.settings.get(setting_name)
    print_with_label(f"Saved {setting_name}", saved_setting)
    print()

    print_separator()
    time.sleep(sleep_time)

    # Test
    print_subheader(f"Testing Onboarding")

    force_setup = True
    onboarding_completed = CurrentAppHub.setup(force_setup)
    print_with_label("Onboarding completed", onboarding_completed)
    print()

    print_separator()
    time.sleep(sleep_time)

    # Test
    print_subheader(f"Testing Database")

    conn = CurrentAppHub.database.connect()
    print(f"{conn}" if conn else f"Unable to connect")
    print()

    if conn:
        sql = "INSERT INTO Teams (team_name, is_ranked) VALUES (?, ?)"
        parameters = ("Sharks", False)
        db_file = None
        executed = sql_execute(sql, parameters, conn, db_file)
        conn.commit()
        print(sql)
        print(f"Parameters {parameters}")
        print()
        print(f"Executed: {executed}")
        print()

        print_separator()
        time.sleep(sleep_time)

        sql = "INSERT INTO Teams (team_name, is_ranked) VALUES (?, ?)"
        parameters = ("Tigers", False)
        db_file = None
        executed = sql_execute(sql, parameters, conn, db_file)
        conn.commit()
        print(sql)
        print(f"Parameters {parameters}")
        print()
        print(f"Executed: {executed}")
        print()

        print_separator()
        time.sleep(sleep_time)

        sql = "SELECT * FROM Teams"
        parameters = None
        db_file = None
        rows = sql_select(sql, parameters, conn, db_file)
        print(sql)
        print(f"Parameters {parameters}")
        print()
        print(f"Selected all:\n{rows}")
        print()
        for current_row in rows:
            print(f"{current_row['team_name']}")
        print()
        row = sql_select_one(sql, parameters, conn, db_file)
        print(f"Selected one:\n{row}")
        print()
        print(f"{row['team_name']}")
        print()

        print_separator()
        time.sleep(sleep_time)

        sql = f"DELETE FROM Teams WHERE team_name = ? or team_name = ?"
        parameters = ("Sharks", "Tigers")
        db_file = None
        executed = sql_execute(sql, parameters, conn, db_file)
        conn.commit()
        print(sql)
        print(f"Parameters {parameters}")
        print()
        print(f"Executed: {executed}")
        print()

        print_separator()
        time.sleep(sleep_time)

        sql = "SELECT * FROM Teams"
        parameters = None
        db_file = None
        rows = sql_select(sql, parameters, conn, db_file)
        print(sql)
        print(f"Parameters {parameters}")
        print()
        print(f"Selected all:\n{rows}")
        print()
        row = sql_select_one(sql, parameters, conn, db_file)
        print(f"Selected one:\n{row}")
        print()

        conn.close()

    print_separator()
    time.sleep(sleep_time)

    print_footer()
