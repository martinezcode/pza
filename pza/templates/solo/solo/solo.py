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
from pza.interface import run
import pza.database

# --- App Constants ---

APP_NAME = "solo"
APP_DISPLAY_NAME = "solo"
APP_VERSION = "0.4.2"

# --- App Recipe ---

def get_app_recipe() -> dict:
    """
    Defines app specifications.
    """
    recipe = {
        "name": APP_NAME,
        "display_name": APP_DISPLAY_NAME,
        "version": APP_VERSION,
        "entry_point": "solo.reason",
        "test_entry_point": "solo.test",
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
        # Override framwork default to disable onboarding setup wizard
        "onboarding_required": False,
    }
    return recipe

def get_onboarding_recipe() -> dict:
    """
    Defines app setup wizard specifications.
    """
    recipe = None
    return recipe

def get_database_recipe() -> dict:
    """
    Defines app database schema.
    """
    recipe = {
        "schema_version": "0.4.2", # Change 'schema_version' to trigger auto-update
        "Reasons": {
            "reason_id": "INTEGER PRIMARY KEY AUTOINCREMENT",
            "reason": "TEXT",
        },
        "Burns": {
            "burn_id": "INTEGER PRIMARY KEY AUTOINCREMENT",
            "burn": "TEXT",
        }
    }
    return recipe

def get_command_recipe() -> dict:
    """
    Defines command line interface commands and arguments.
    """
    recipe = {
        "burn": {
            "callback": "solo.burn",
            "help": "Generate a burn on Han Solo.",
        },
    }
    return recipe

# --- App Initialization Function ---

def initialize_app(profile: str = "default", setting_overrides: dict | None = None) -> bool:
    """
    Loads the framework environment.
    This step enables settings, database, and logging.

    Apps launched with 'pza.interface.run()' do not need to call this
    because 'run()' performs the initialization automatically.

    Call this function to initialize an environment for testing the app or running
    standalone components that do not use the command line interface.
    """
    SoloHub = AppHub(
        get_app_recipe(),
        profile,
        setting_overrides
    )
    return SoloHub

def list_properties() -> None:
    """
    Prints a list of app properties.
    """
    print_with_label("App Name", APP_NAME)
    print_with_label("App Display Name", APP_DISPLAY_NAME)
    print_with_label("App Version", APP_VERSION)
    return

# --- Interface Command Handler Callback Functions ---

def reason(SoloHub) -> None:
    """
    The main interface entry point.
    This is the default mode if no command is given.
    """
    print()
    print_line()
    print(f"Welcome to {APP_DISPLAY_NAME} version {APP_VERSION}")
    print_line()
    print()
    database_populated = populate_database(SoloHub)
    if database_populated:
        current_reason = get_random_reason(SoloHub)
        print(f"{current_reason}")
        print()
    else:
        print(f"So sorry for the error")
        print()
        # Close the app
    print_line()
    print(f"Thank you for using {APP_DISPLAY_NAME} version {APP_VERSION}")
    print_line()
    print()
    return

def burn(SoloHub) -> None:
    """
    The burn command interface entry point.
    """
    print_line()
    print(f"Welcome to {APP_DISPLAY_NAME} version {APP_VERSION}")
    print_line()
    print()
    print_line()
    print(f"BURN MODE ACTIVATED")
    print_line()
    print()
    database_populated = populate_database(SoloHub)
    if database_populated:
        current_burn = get_random_burn(SoloHub)
        print(f"{current_burn}")
        print()
    else:
        print(f"So sorry for the error")
        print()
    print_line()
    print(f"Thank you for using {APP_DISPLAY_NAME} version {APP_VERSION}")
    print_line()
    print()
    return

def test(SoloHub):
    """
    The test command interface entry point.
    """
    print_header(f"{__file__}")

    print_separator()

    # Test
    print()
    SoloHub.logger.debug(f"App Started")
    print()

    print_separator()

    # Test
    print_subheader(f"App Properties")

    list_properties()
    print()

    print_separator()

    # Test
    print_subheader(f"Initializing App")
    SoloHub.logger.debug(f"App Initialized")
    print()
    print(f"Welcome to {APP_DISPLAY_NAME} version {APP_VERSION}")
    print()

    print_separator()

    # Test
    print_subheader(f"Framework Environment Properties")
    print(SoloHub)
    print()
    SoloHub.list()
    print()

    print_separator()

    # Test
    print_subheader(f"Settings for Profile '{SoloHub.profile}'")
    current_settings = SoloHub.settings.get_settings()
    pza.settings.list_settings(current_settings)
    print()

    print_separator()

    # Test
    print_subheader(f"Populating Database")

    database_populated = populate_database(SoloHub)
    message = f"Database Populated" if {database_populated} else f"Unable to populate database"
    print(f"{message}")
    print()
    SoloHub.logger.debug(f"{message}")
    print()

    print_separator()

    # Test
    print_subheader(f"Testing 'run' command")

    reason(SoloHub)

    print_separator()

    # Test
    print_subheader(f"Testing 'burn' command")

    burn(SoloHub)

    print_separator()

    print_footer()

    return

# --- Database Features ---

def populate_database(SoloHub) -> bool:
    """
    Imports data into the database.
    """
    # Connect to the database
    conn = SoloHub.database.connect()
    if not conn:
        print("Unable to connect to database")
        return False

    # Clear the database and start fresh
    # Normally we would check for updates but that can be added later
    sql = f"DELETE FROM Reasons"
    parameters = None
    executed = pza.database.sql_execute(sql, parameters, conn)
    if not executed:
        print(f"Unable to replace existing data")
        conn.close()
        return False
    sql = f"DELETE FROM Burns"
    parameters = None
    executed = pza.database.sql_execute(sql, parameters, conn)
    if not executed:
        print(f"Unable to replace existing data")
        conn.close()
        return False

    # Get the lists
    reasons = get_reason_list()
    burns = get_burn_list()

    # Import the lists
    for reason in reasons:
        sql = f"INSERT INTO Reasons (reason) VALUES (?)"
        parameters = (reason,) # Tuple required
        executed = pza.database.sql_execute(sql, parameters, conn)
        if not executed:
            print(f"Unable to add reason")
            conn.close()
            return False

    for burn in burns:
        sql = f"INSERT INTO Burns (burn) VALUES (?)"
        parameters = (burn,) # Tuple required
        executed = pza.database.sql_execute(sql, parameters, conn)
        if not executed:
            print(f"Unable to add burn")
            conn.close()
            return False

    # Close the database
    conn.close()

    return True

def get_reason_list() -> list[str]:
    """
    Generates the reason data.
    Normally we would import but that can be added later.

    Created by ChatGPT with prompt:
    'Generate a list of 20 single sentences that each give a reason why Han Solo is awesome.
    Output the list as a python list variable definition reasons = []'
    ChatGPT will also generate lists in SQL format if you ask :)
    """
    reasons = [
        "Han Solo shot first.",
        "Han Solo can fly the Millennium Falcon through an asteroid field without breaking a sweat.",
        "Han Solo has the best co-pilot in the galaxy in Chewbacca.",
        "Han Solo turned from a selfish smuggler into a hero of the Rebellion.",
        "Han Solo is legendary across the stars for his sarcastic one-liners.",
        "Han Solo can outtalk bounty hunters and Imperial officers alike.",
        "Han Solo made the Kessel Run in less than twelve parsecs.",
        "Han Solo is loyal to his friends even when he pretends not to care.",
        "Han Solo pilots the fastest hunk of junk in the galaxy.",
        "Han Solo rescued Luke and Leia more times than he admits.",
        "Han Solo is fearless in the face of impossible odds.",
        "Han Solo has the charm to win over royalty and rogues alike.",
        "Han Solo can fix, fly, and fight with equal skill.",
        "Han Solo has the confidence of someone who knows the odds and ignores them.",
        "Han Solo stands up to Darth Vader without flinching.",
        "Han Solo balances arrogance and heart in perfect measure.",
        "Han Solo is proof that even scoundrels can become legends.",
        "Han Solo has the best costume-to-attitude ratio in the galaxy.",
        "Han Solo made the phrase 'I know' one of the coolest responses in film history.",
        "Han Solo is a rogue with a conscience, and that makes him unforgettable."
    ]
    return reasons

def get_burn_list() -> list[str]:
    """
    Generates the burn data.
    Normally we would import but that can be added later.

    Created by ChatGPT with prompt (after running the reasons prompt):
    'generate a similar list of 20 times he was a jerk or too cocky or made a mistake'
    ChatGPT will also generate lists in SQL format if you ask :)
    """
    burns = [
        "Han Solo did not shoot first.",
        "Han Solo bragged about the Millennium Falcon making the Kessel Run\nin less than twelve parsecs, even though parsecs measure distance, not speed.",
        "Han Solo tried to leave the Rebellion for money instead of helping his friends at first.",
        "Han Solo mocked the Force in front of Luke and Obi-Wan, calling it a simple religion.",
        "Han Solo dismissed Leia's leadership and argued with her constantly on Hoth.",
        "Han Solo laughed at Luke's crush on Leia even though he was flirting with her too.",
        "Han Solo got cocky and walked straight into Vader's trap on Cloud City.",
        "Han Solo insulted C-3PO almost every time the droid spoke.",
        "Han Solo charged a squad of stormtroopers with no plan and got chased back down the hallway.",
        "Han Solo bragged about his piloting skills every chance he got.",
        "Han Solo owed Jabba the Hutt money for years and still acted like it was no big deal.",
        "Han Solo told Leia 'You like me because I am a scoundrel' in one of his cockiest moments.",
        "Han Solo ignored Chewbacca's advice more than once when he should have listened.",
        "Han Solo froze up when Leia confessed her love right before he was frozen in carbonite.",
        "Han Solo was overconfident that his blaster could solve any problem.",
        "Han Solo told Luke 'That's great, kid, but do not get cocky,' right after being cocky himself.",
        "Han Solo almost abandoned the Battle of Yavin before coming back at the last second.",
        "Han Solo underestimated the Ewoks and got captured by them.",
        "Han Solo walked into Jabba's palace with no solid escape plan.",
        "Han Solo argued with Leia during their mission on Endor instead of focusing on the objective."
    ]
    return burns

def get_random_reason(SoloHub) -> str:
    """
    Selects a random reason from the database.
    """
    conn = SoloHub.database.connect()
    if not conn:
        return "Reason Unavailable"
    sql = """
        SELECT reason FROM Reasons
        ORDER BY RANDOM()
        LIMIT 1
    """
    parameters = None
    reason_row = pza.database.sql_select_one(sql, parameters, conn)
    if not reason_row:
        return "Reason Unavailable"
    conn.close()
    reason = reason_row[0]
    return reason

def get_random_burn(SoloHub) -> str:
    """
    Selects a random burn from the database.
    """
    conn = SoloHub.database.connect()
    if not conn:
        return "Burn Unavailable"
    sql = """
        SELECT burn FROM Burns
        ORDER BY RANDOM()
        LIMIT 1
    """
    parameters = None
    reason_row = pza.database.sql_select_one(sql, parameters, conn)
    if not reason_row:
        return "Burn Unavailable"
    conn.close()
    burn = reason_row[0]
    return burn

# --- Main Program ---

def main() -> None:
    """
    Launches the interface with 'interface.run()'.
    Commands defined for this app are: 'config', 'test', 'burn'.
    """
    run(
        get_app_recipe(),
        verbose=False
    )
    return

if __name__ == "__main__":
    """
    Runs the main function to launch the app interface.
    """
    main()