
from pza.prints import (
    print_error,
    print_footer,
    print_header,
    print_separator,
    print_subheader,
    print_with_label,
)

import sqlite3
import os
from typing import Any
from datetime import datetime

def get_sample_database_recipe() -> dict:
    """
    Defines a sample database schema recipe.
    """
    recipe = {
        "schema_version": "0.1.1",
        "Teams": {
            "team_id": "INTEGER PRIMARY KEY AUTOINCREMENT",
            "team_name": "TEXT",
            "is_ranked": "BOOLEAN DEFAULT 0",
        },
        "Players": {
            "player_id": "INTEGER PRIMARY KEY AUTOINCREMENT",
            "player_name": "TEXT",
            "jersey_number": "INTEGER",
        }
    }
    return recipe

def connect(db_file: str) -> sqlite3.Connection:
    """
    Connects to sqlite database file.
    Creates the file if it doesn't exist.
    """
    conn = None
    try:
        # Connect to the file
        conn = sqlite3.connect(db_file)
        # Enable named column access
        conn.row_factory = sqlite3.Row
        return conn
    except Exception as e:
        print_error(e, f"Unable to connect to database '{db_file}'")
        return None

def sql_execute(sql: str, parameters: tuple[Any] = None, conn: sqlite3.Connection = None, db_file: str = None) -> bool:
    """
    Executes an sql statement with error checking.
    """
    if not sql:
        print(f"Invalid sql")
        return False

    # Check for existing connection
    close_connection = False
    if not conn:
        if not db_file or not os.path.exists(db_file) or os.path.isdir(db_file):
            print(f"Invalid database file")
            return False
        close_connection = True
        conn = connect(db_file)
    # Check for valid connection
    if not conn:
        print(f"Unable to connect to database file")
        return False

    # Execute the sql
    executed = False
    try:
        db_cursor = conn.cursor()
        if parameters:
            db_cursor.execute(sql, parameters)
        else:
            db_cursor.execute(sql)
        conn.commit()
        executed = True
    except Exception as e:
        print_error(e)

    if close_connection:
        conn.close()

    return executed

def sql_select(sql: str, parameters: tuple[Any] = None, conn: sqlite3.Connection = None, db_file: str = None) -> list[sqlite3.Row]:
    """
    Executes an sql select statement with error checking.
    Returns database rows.
    """
    if not sql:
        print(f"Invalid sql")
        return None

    # Check for existing connection
    close_connection = False
    if not conn:
        if not db_file or not os.path.exists(db_file) or os.path.isdir(db_file):
            print(f"Invalid database file")
            return None
        close_connection = True
        conn = connect(db_file)
    # Check for valid connection
    if not conn:
        print(f"Unable to connect to database file")
        return None

    # Execute the sql
    rows = None
    try:
        db_cursor = conn.cursor()
        if parameters:
            db_cursor.execute(sql, parameters)
        else:
            db_cursor.execute(sql)
        rows = db_cursor.fetchall()
    except Exception as e:
        print_error(e)

    if close_connection:
        conn.close()

    return rows

def sql_select_one(sql: str, parameters: tuple[Any] = None, conn: sqlite3.Connection = None, db_file: str = None) -> sqlite3.Row:
    """
    Executes an sql select statement with error checking.
    Returns one database row.
    """
    if not sql:
        print(f"Invalid sql")
        return None

    # Check for existing connection
    close_connection = False
    if not conn:
        if not db_file or not os.path.exists(db_file) or os.path.isdir(db_file):
            print(f"Invalid database file")
            return None
        close_connection = True
        conn = connect(db_file)
    # Check for valid connection
    if not conn:
        print(f"Unable to connect to database file")
        return None

    # Execute the sql
    row = None
    try:
        db_cursor = conn.cursor()
        if parameters:
            db_cursor.execute(sql, parameters)
        else:
            db_cursor.execute(sql)
        row = db_cursor.fetchone()
    except Exception as e:
        print_error(e)

    if close_connection:
        conn.close()

    return row

def create_database_from_recipe(db_file: str, database_recipe: dict) -> bool:
    """
    Creates a database file from the given recipe.
    """
    if not db_file:
        print(f"Invalid db file")
        return False
    if not database_recipe:
        print(f"Invalid schema map")
        return False
    # Connect to database
    try:
        conn = connect(db_file)
    except Exception as e:
        print_error(e)
        return False
    cursor = conn.cursor()
    # Create tables
    for map_key, map_value in database_recipe.items():
        if map_key == "schema_version":
            # Skip schema version
            continue
        table_name = map_key
        column_info = map_value
        sql_columns = ", ".join([f"{column_name} {column_options}" for column_name, column_options in column_info.items()])
        sql = f"CREATE TABLE IF NOT EXISTS {table_name} ({sql_columns});"
        try:
            cursor.execute(sql)
        except Exception as e:
            conn.close()
            return False
    # Commit the changes
    try:
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        conn.close()
        print_error(e)
        return False

def get_sql_datetime(raw_date: datetime) -> str:
    """
    Converts a datetime to sql datetime format.
    """
    formatted_date = raw_date.strftime('%Y-%m-%d %H:%M:%S')
    return formatted_date

def get_sql_date(raw_date: datetime) -> str:
    """
    Converts a datetime to sql date format without time.
    """
    formatted_date = raw_date.strftime('%Y-%m-%d')
    return formatted_date

if __name__ == "__main__":

    print_header(f"{__file__}")

    print_separator()

    print_subheader(f"Testing")

    print_separator()

    print_footer()
