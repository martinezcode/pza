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
import pza.pie
import pza.settings
import pza.database

from pride import library

import os

# --- Primary app entry point ---
# --- Runs when app is launched by name ---

def entry_point(PrideHub: AppHub) -> None:
    """
    Displays a random pride flag.
    """
    # Validate the hub
    if not PrideHub:
        print()
        print(f"Unable to launch app")
        print()
        return

    # Introduce the app
    print()
    print_line()
    print(f"Welcome to {PrideHub.display_name} version {PrideHub.version}")
    print_line()
    print()

    # Perform onboarding if onboarding_required flag is True in settings
    if not PrideHub.setup():
        # Required onboarding failed or user quit
        print(f"{PrideHub.display_name} is unable to continue without required onboarding")
        print()
    else:
        # Make sure database is available
        if not PrideHub.database.database_created:
            print(f"The database is unavailable.")
            print()
        else:
            # Import the sample data
            data_imported = library.import_sample_data(PrideHub)
            if data_imported:
                sample_data_folder = library.get_sample_data_folder(PrideHub)
                if not sample_data_folder:
                    print(f"Unable to access sample data folder")
                    print()
                    return False
                # Get a random flag from the database
                flag_row = library.get_random_flag(PrideHub)
                flag_name = flag_row["flag_name"]
                flag_filename = flag_row["filename"]
                flag_file = os.path.join(sample_data_folder, flag_filename)
                citation_text = library.wrap(flag_row["citation_text"])
                citation_sources = library.wrap(flag_row["citation_sources"])
                citation_author = library.wrap(flag_row["citation_author"])
                colors = flag_row["colors"].replace(",", ", ")
                # Display flag information
                print(flag_name)
                print()
                print(citation_text)
                print()
                print(citation_sources)
                print()
                if citation_author != "0":
                    print(citation_author)
                    print()
                print(f"Colors: {colors}")
                print()
                # Prompt to display the flag image
                _ = input("Press 'Enter' to view the flag image:")
                print()
                _ = pza.pie.open_file_with_browser(flag_file)

    # Close the app
    print_line()
    print(f"Thank you for using {PrideHub.display_name} version {PrideHub.version}")
    print_line()
    print()

    return

# --- Test entry point ---
# --- Runs when app is launched with command 'test' ---

def test_entry_point(PrideHub: AppHub) -> None:
    """
    Runs basic framework feature tests.
    """
    # Validate the hub
    if not PrideHub:
        print()
        print(f"Unable to launch app")
        print()
        return

    # Introduce the app
    print()
    print_line()
    print(f"Welcome to {PrideHub.display_name} version {PrideHub.version}")
    print_line()
    print()
    print_line()
    print(f"Test Mode Activated")
    print_line()
    print()

    print(PrideHub)
    print()
    PrideHub.list()
    print()

    # Test Logging
    print_subheader(f"Testing Logging")

    PrideHub.logger.info("test")
    print()

    # Test Settings
    print_subheader(f"Testing Settings")

    settings = PrideHub.settings.get_settings()
    pza.settings.list_settings(settings)
    print()

    # Test Database
    print_subheader(f"Testing Database")

    conn = PrideHub.database.connect()
    print(f"Database connected" if conn else f"Unable to connect to database")
    print()

    # Close the app
    print_line()
    print(f"Thank you for using {PrideHub.display_name} version {PrideHub.version}")
    print_line()
    print()

    return

# --- Export entry point ---
# --- Runs when app is launched with command 'export' ---

def export(PrideHub: AppHub, out_folder: str = "") -> None:
    """
    Exports the sample data including flag images and .json file.
    """
    # Perform onboarding if onboarding_required flag is True in settings
    if not PrideHub.setup():
        # Required onboarding failed or user quit
        print(f"{PrideHub.display_name} is unable to continue without required onboarding")
        print()
        return
    else:
        sample_data_folder = library.get_sample_data_folder(PrideHub)
        folder_name = os.path.basename(sample_data_folder)
        if not out_folder:
            out_folder = PrideHub.settings.get_profile_documents_folder()
        destination_folder = os.path.join(out_folder, folder_name)
        data_imported = library.import_sample_data(PrideHub)
        print()
        if data_imported:
            _ = pza.pie.copy_folder(sample_data_folder, destination_folder)
            print()
    return

# --- Search entry point ---
# --- Runs when app is launched with command 'search' ---

def search(PrideHub: AppHub, term: str = "") -> None:
    """
    Searches the database for a pride flag.
    """
    if not term:
        print(f"Invalid search term")
        print()
        return
    # Perform onboarding if onboarding_required flag is True in settings
    if not PrideHub.setup():
        # Required onboarding failed or user quit
        print(f"{PrideHub.display_name} is unable to continue without required onboarding")
        print()
        return
    else:
        # Make sure database is available
        if not PrideHub.database.database_created:
            print(f"The database is unavailable.")
            print()
        else:
            # Import sample data
            data_imported = library.import_sample_data(PrideHub)
            if data_imported:
                conn = PrideHub.database.connect()
                if not conn:
                    print(f"Database unavailable")
                    print()
                    return
                # Build the search query
                sql = """
                    SELECT
                        *,
                        (
                            SELECT group_concat(color_name)
                            FROM Colors
                            WHERE color_id IN
                                (SELECT color_id FROM ColorMap WHERE flag_id = Flags.flag_id)
                        ) AS colors
                    FROM
                        Flags
                    WHERE
                        lower(flag_name) LIKE ? OR
                        lower(filename) LIKE ? OR
                        lower(citation_text) LIKE ? OR
                        lower(citation_sources) LIKE ? OR
                        lower(citation_image) LIKE ? OR
                        lower(citation_author) LIKE ? OR
                        lower(colors) LIKE ?
                    ORDER BY lower(flag_name)
                """
                term = f"%{term}%"
                parameters = (term, term, term, term, term, term, term)
                # Search the database
                flag_rows = pza.database.sql_select(sql, parameters, conn)
                if not flag_rows:
                    print(f"No flags found")
                    print()
                    conn.close()
                    return None
                # Track corresponding sample data files
                sample_data_folder = library.get_sample_data_folder(PrideHub)
                if not sample_data_folder:
                    print(f"Unable to access sample data folder")
                    print()
                flag_indexes = {}
                idx = 0
                # Display all matches
                for flag_row in flag_rows:
                    idx += 1
                    flag_name = flag_row["flag_name"]
                    flag_filename = flag_row["filename"]
                    flag_file = os.path.join(sample_data_folder, flag_filename)
                    citation_text = library.wrap(flag_row["citation_text"])
                    citation_sources = library.wrap(flag_row["citation_sources"])
                    citation_author = library.wrap(flag_row["citation_author"])
                    colors = flag_row["colors"].replace(",", ", ")
                    flag_indexes[f"{idx}"] = flag_file
                    print_separator(f"{idx}. {flag_name}")
                    print()
                    print(citation_text)
                    print()
                    print(citation_sources)
                    print()
                    if citation_author != "0":
                        print(citation_author)
                        print()
                    print(f"Colors: {colors}")
                    print()
                # Prompt to display a flag image file
                if sample_data_folder:
                    while True:
                        response = input("Enter a number to view the flag or type 'q' to quit:")
                        if response.lower().startswith('q'):
                            print("Goodbye")
                            print()
                            break
                        else:
                            flag_file = flag_indexes.get(response, None)
                            if not flag_file:
                                print(f"Invalid flag number")
                                print()
                                continue
                            else:
                                _ = pza.pie.open_file_with_browser(flag_file)
                                print()
                conn.close()
    return

if __name__ == "__main__":

    print_header(f"{__file__}")

    print_separator()

    print()

    print_separator()

    print_footer()
