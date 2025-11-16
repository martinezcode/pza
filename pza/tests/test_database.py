"""
Tests
"""

from pza.prints import (
    print_error,
    print_footer,
    print_header,
    print_separator,
    print_subheader,
)
from pza.database import (
    connect,
    get_sample_database_recipe,
    create_database_from_recipe,
    sql_execute,
    sql_select,
    sql_select_one
)
from pza.tests.test_helpers import *

import time


if __name__ == "__main__":

    print_header(f"{__file__}")

    print_separator()

    # Set delay time between commands for viewing the output
    sleep_time = 1.5

    # Test
    print_subheader(f"Connecting to database")

    temp_file = get_test_database_file()
    conn = connect(temp_file)
    print(f"{conn}" if conn else f"Unable to connect")
    print()
    if conn:
        conn.close()

    print_separator()
    time.sleep(sleep_time)

    # Test
    print_subheader(f"Creating database")

    app_data_created = create_database_from_recipe(
        temp_file,
        get_sample_database_recipe()
    )
    print(f"App Data Created: {app_data_created}")
    print()

    print_separator()
    time.sleep(sleep_time)

    # Test
    print_subheader(f"Updating database")

    conn = connect(temp_file)
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

        print_separator()
        time.sleep(sleep_time)

        sql = f"DELETE FROM Teams WHERE team_name = ?"
        parameters = ("Sharks",)
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
