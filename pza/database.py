
from pza.prints import (
    print_error,
    print_footer,
    print_header,
    print_separator,
    print_subheader,
    print_with_label,
)

import pza.validation

import sqlite3
import os
from typing import Any
from datetime import datetime

def get_sample_database_recipe() -> dict:
    """
    Defines a sample database schema recipe.
    """
    recipe = {
        "schema_version": "0.4.6",
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

def sql_execute(sql: str, parameters: tuple[Any] | None = None, conn: sqlite3.Connection | None = None, db_file: str | None = None) -> bool:
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

def sql_select(sql: str, parameters: tuple[Any] = None, conn: sqlite3.Connection = None, db_file: str | None = None) -> list[sqlite3.Row]:
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

def sql_select_one(sql: str, parameters: tuple[Any] = None, conn: sqlite3.Connection = None, db_file: str | None = None) -> sqlite3.Row:
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

def get_sql_from_recipe(recipe: dict) -> str | None:
    """
    Creates a sql statement from the given recipe.
    """
    if not recipe or not isinstance(recipe, dict):
        print(f"Invalid sql recipe")
        return None

    statement_type = recipe.get("statement_type", "")
    statement_type = statement_type.strip().upper()

    if statement_type not in ["SELECT"]:
        print(f"Unsupported sql statement type: {statement_type}")
        return None

    sql = ""

    if statement_type == "SELECT":
        # Get the table name for the query
        table_name = recipe.get("table_name", "")
        if not isinstance(table_name, str) or table_name.strip() == "":
            print(f"Invalid table name")
            return None
        table_name = table_name.strip()

        # Get the list of result columns
        result_columns = recipe.get("result_columns", [])
        if not isinstance(result_columns, list):
            print(f"Invalid result_columns")
            return None
        result_columns_criteria = f"{', '.join(result_columns)}"

        # Get the list of columns to search in
        search_columns = recipe.get("search_columns", [])
        if not isinstance(search_columns, list):
            print(f"Invalid search_columns (defaulting to zero search columns")
            search_columns = []

        # Get the search include parameters
        search_include_terms = recipe.get("search_include_terms", [])
        search_include_terms = pza.validation.get_valid_list(search_include_terms)
        search_include_operator = recipe.get("search_include_operator", "OR")
        search_include_operator = get_valid_operator(search_include_operator)
        search_include_whole_word = recipe.get("search_include_whole_word", False)
        search_include_whole_word = pza.validation.get_valid_boolean(search_include_whole_word)
        search_include_match_case = recipe.get("search_include_match_case", False)
        search_include_match_case = pza.validation.get_valid_boolean(search_include_match_case)

        # Build a list of conditions to look for each search_include_term in each search_column
        search_include_conditions = []
        if (len(search_columns) > 0 and len(search_include_terms) > 0):
            for search_term in search_include_terms:
                current_search_term = search_term
                if not search_include_match_case:
                    # Use lower for case insensitive search
                    current_search_term = current_search_term.lower()
                if search_include_whole_word:
                    # Use equals operater for exact whole word search
                    current_comparison = f" = '{current_search_term}'"
                else:
                    # Use like operater for substring search
                    current_comparison = f" LIKE '%{current_search_term}%'"
                for search_column in search_columns:
                    current_column = search_column
                    if not search_include_match_case:
                        # Use lower for case insensitive search
                        current_column = f"LOWER({current_column})"
                    current_condition = f"{current_column}{current_comparison}"
                    search_include_conditions.append(current_condition)

        # print(f"{search_include_conditions}")

        # Get the search exclude parameters
        search_exclude_terms = recipe.get("search_exclude_terms", [])
        search_exclude_terms = pza.validation.get_valid_list(search_exclude_terms)
        search_exclude_operator = recipe.get("search_exclude_operator", "OR")
        search_exclude_operator = get_valid_operator(search_exclude_operator)
        search_exclude_whole_word = recipe.get("search_exclude_whole_word", False)
        search_exclude_whole_word = pza.validation.get_valid_boolean(search_exclude_whole_word)
        search_exclude_match_case = recipe.get("search_exclude_match_case", False)
        search_exclude_whole_word = pza.validation.get_valid_boolean(search_exclude_whole_word)

        # Build a list of conditions to exclude each search_exclude_term from each search_column
        search_exclude_conditions = []
        if (len(search_columns) > 0 and len(search_exclude_terms) > 0):
            for search_term in search_exclude_terms:
                current_search_term = search_term
                if not search_exclude_match_case:
                    # Use lower for case insensitive search
                    current_search_term = current_search_term.lower()
                if search_exclude_whole_word:
                    # Use equals operater for exact whole word search
                    current_comparison = f" != '{current_search_term}'"
                else:
                    # Use like operater for substring search
                    current_comparison = f" NOT LIKE '%{current_search_term}%'"
                for search_column in search_columns:
                    current_column = search_column
                    if not search_exclude_match_case:
                        # Use lower for case insensitive search
                        current_column = f"LOWER({current_column})"
                    current_condition = f"{current_column}{current_comparison}"
                    search_exclude_conditions.append(current_condition)

        # print(f"{search_exclude_conditions}")

        # Get the dictionary of columns to search for matching boolean
        boolean_include_columns = recipe.get("boolean_include_columns", {})
        boolean_include_columns = pza.validation.get_valid_dictionary(boolean_include_columns)
        boolean_include_operator = recipe.get("boolean_include_operator", "OR")
        boolean_include_operator = get_valid_operator(boolean_include_operator)

        # Build a list of conditions to search for matching boolean
        boolean_include_conditions = []
        for column_name, value in boolean_include_columns.items():
            current_condition = f"{column_name} = {int(value)}"
            boolean_include_conditions.append(current_condition)

        # print(f"{boolean_include_conditions}")

        # Get the dictionary of columns to search for non-matching boolean
        boolean_exclude_columns = recipe.get("boolean_exclude_columns", {})
        boolean_exclude_columns = pza.validation.get_valid_dictionary(boolean_exclude_columns)
        boolean_exclude_operator = recipe.get("boolean_exclude_operator", "OR")
        boolean_exclude_operator = get_valid_operator(boolean_exclude_operator)

        # Build a list of conditions to search for non-matching boolean
        boolean_exclude_conditions = []
        for column_name, value in boolean_exclude_columns.items():
            current_condition = f"{column_name} != {int(value)}"
            boolean_exclude_conditions.append(current_condition)

        # print(f"{boolean_exclude_conditions}")

        # Get the dictionary of columns for comparison search
        comparison_columns = recipe.get("comparison_columns", {})
        comparison_columns = pza.validation.get_valid_dictionary(comparison_columns)
        comparison_operator = recipe.get("comparison_operator", "OR")
        comparison_operator = get_valid_operator(comparison_operator)

        # Build a list of conditions for comparison search
        comparison_conditions = []
        for column_name, comparison_options in comparison_columns.items():
            if not isinstance(comparison_options, dict):
                print(f"Invalid comparison options (skipping {column_name}")
                continue
            comparison_options_operator = comparison_options.get("operator", "OR")
            if not isinstance(comparison_options_operator, str) or \
                comparison_options_operator.strip() not in [">", ">=", "<", "<=", "=", "!="]:
                print(f"Invalid comparison_options_operator  (skipping {column_name}")
                continue
            comparison_options_operator = comparison_options_operator.strip()
            comparison_options_value = comparison_options.get("value", None)
            if comparison_options_value is None:
                print(f"Invalid comparison_operator (skipping {column_name}")
                continue
            if isinstance(comparison_options_value, str):
                current_condition = f"{column_name} {comparison_options_operator} '{comparison_options_value}'"
            else:
                current_condition = f"{column_name} {comparison_options_operator} {comparison_options_value}"
            comparison_conditions.append(current_condition)

        # print(f"{comparison_conditions}")

        # Get the dictionary of columns for empty include search
        empty_include_columns = recipe.get("empty_include_columns", {})
        empty_include_columns = pza.validation.get_valid_dictionary(empty_include_columns)

        # Build a list of conditions for empty include search
        empty_include_conditions = []
        for column_name, empty_options in empty_include_columns.items():
            if not isinstance(empty_options, dict):
                print(f"Invalid empty include options (skipping {column_name}")
                continue
            empty_options_empty_value = empty_options.get("empty_value")
            if empty_options_empty_value is None:
                current_empty_value_condition = ""
            elif isinstance(empty_options_empty_value, str):
                current_empty_value_condition = f"{column_name} = '{empty_options_empty_value}'"
            else:
                current_empty_value_condition = f"{column_name} = {empty_options_empty_value}"
            empty_options_check_null = empty_options.get("check_null", False)
            empty_options_check_null = pza.validation.get_valid_boolean(empty_options_check_null)
            if not empty_options_check_null:
                current_null_condition = ""
            else:
                current_null_condition = f"{column_name} IS NULL"
            if current_empty_value_condition == "" and current_null_condition == "":
                continue
            elif current_empty_value_condition != "" and current_null_condition != "":
                current_condition = f"({current_empty_value_condition} OR {current_null_condition})"
                empty_include_conditions.append(current_condition)
            elif current_empty_value_condition == "" and current_null_condition != "":
                current_condition = current_null_condition
                empty_include_conditions.append(current_condition)
            elif current_empty_value_condition != "" and current_null_condition == "":
                current_condition = current_empty_value_condition
                empty_include_conditions.append(current_condition)

        # print(f"{empty_include_conditions}")

        # Get the dictionary of columns for empty exclude search
        empty_exclude_columns = recipe.get("empty_exclude_columns", {})
        empty_exclude_columns = pza.validation.get_valid_dictionary(empty_exclude_columns)

        # Build a list of conditions for empty exclude search
        empty_exclude_conditions = []
        for column_name, empty_options in empty_exclude_columns.items():
            if not isinstance(empty_options, dict):
                print(f"Invalid empty exclude options (skipping {column_name}")
                continue
            empty_options_empty_value = empty_options.get("empty_value")
            if empty_options_empty_value is None:
                current_empty_value_condition = ""
            elif isinstance(empty_options_empty_value, str):
                current_empty_value_condition = f"{column_name} != '{empty_options_empty_value}'"
            else:
                current_empty_value_condition = f"{column_name} != {empty_options_empty_value}"
            empty_options_check_null = empty_options.get("check_null", False)
            empty_options_check_null = pza.validation.get_valid_boolean(empty_options_check_null)
            if not empty_options_check_null:
                current_null_condition = ""
            else:
                current_null_condition = f"{column_name} IS NOT NULL"
            if current_empty_value_condition == "" and current_null_condition == "":
                continue
            elif current_empty_value_condition != "" and current_null_condition != "":
                current_condition = f"({current_empty_value_condition} OR {current_null_condition})"
                empty_exclude_conditions.append(current_condition)
            elif current_empty_value_condition == "" and current_null_condition != "":
                current_condition = current_null_condition
                empty_exclude_conditions.append(current_condition)
            elif current_empty_value_condition != "" and current_null_condition == "":
                current_condition = current_empty_value_condition
                empty_exclude_conditions.append(current_condition)

        # print(f"{empty_exclude_conditions}")

        # Get the dictionary of columns to order by
        order_columns = recipe.get("order_columns", {})
        order_columns = pza.validation.get_valid_dictionary(order_columns)
        order_keep_case = recipe.get("order_keep_case", True)
        order_keep_case = pza.validation.get_valid_boolean(order_keep_case)

        order_criteria = []
        for column_name, direction in order_columns.items():
            if not isinstance(direction, str):
                direction = str(direction)
            direction = direction.strip().upper()
            if direction not in ["", "ASC", "DESC"]:
                print(f"Invalid order by direction (defaulting to ascending for {column_name}")
                direction = "ASC"
            if order_keep_case:
                current_criteria = f"{column_name} {direction}".strip()
            else:
                current_criteria = f"LOWER({column_name}) {direction}".strip()
            order_criteria.append(current_criteria)

        # print(f"{order_criteria}")

        # Get the limit
        limit = recipe.get("limit", None)

        limit_clause = ""
        if limit is not None:
            if not isinstance(limit, int):
                print(f"Invalid limit (converting to integer)")
                limit = int(limit)
            limit_clause = f"LIMIT {limit}"

        # print(f"{limit_clause}")

        current_operator = f" {search_include_operator} "
        search_include_expression = f"({current_operator.join(search_include_conditions)})"

        # print(f"{search_include_expression}")

        current_operator = f" {search_exclude_operator} "
        search_exclude_expression = f"({current_operator.join(search_exclude_conditions)})"

        # print(f"{search_exclude_expression}")

        current_operator = f" {boolean_include_operator} "
        boolean_include_expression = f"({current_operator.join(boolean_include_conditions)})"

        # print(f"{boolean_include_expression}")

        current_operator = f" {boolean_exclude_operator} "
        boolean_exclude_expression = f"({current_operator.join(boolean_exclude_conditions)})"

        # print(f"{boolean_exclude_expression}")

        current_operator = f" {comparison_operator} "
        comparison_expression = f"({current_operator.join(comparison_conditions)})"

        # print(f"{comparison_expression}")

        current_operator = f" {comparison_operator} "
        comparison_expression = f"({current_operator.join(comparison_conditions)})"

        # print(f"{comparison_expression}")

        current_operator = f" AND "
        empty_include_expression = f"({current_operator.join(empty_include_conditions)})"

        # print(f"{empty_include_expression}")

        current_operator = f" AND "
        empty_exclude_expression = f"({current_operator.join(empty_exclude_conditions)})"

        # print(f"{empty_exclude_expression}")

        current_operator = f", "
        order_by_clause = f"""ORDER BY {current_operator.join(order_criteria)}"""

        # print(f"{order_by_clause}")

        sql = f"""\nSELECT\n{result_columns_criteria}\nFROM\n{table_name}"""

        where_expressions = []
        if search_include_expression != "" and search_include_expression != "()":
            where_expressions.append(search_include_expression)
        if search_exclude_expression != "" and search_exclude_expression != "()":
            where_expressions.append(search_exclude_expression)
        if boolean_include_expression != "" and boolean_include_expression != "()":
            where_expressions.append(boolean_include_expression)
        if boolean_exclude_expression != "" and boolean_exclude_expression != "()":
            where_expressions.append(boolean_exclude_expression)
        if comparison_expression != "" and comparison_expression != "()":
            where_expressions.append(comparison_expression)
        if empty_include_expression != "" and empty_include_expression != "()":
            where_expressions.append(empty_include_expression)
        if empty_exclude_expression != "" and empty_exclude_expression != "()":
            where_expressions.append(empty_exclude_expression)

        if len(where_expressions) > 0:
            sql_where_clause = f"\nWHERE\n"
            sql_where_clause = sql_where_clause + "\nAND\n".join(where_expressions)
            sql = f"{sql} {sql_where_clause}"

        sql = f"{sql}\n{order_by_clause}"
        sql = f"{sql.strip()}\n{limit_clause}".strip()

        # print(f"{sql}")

    return sql

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

def get_valid_operator(original_operator: Any) -> str:
    """
    Returns a valid sql operator.
    """
    valid_operator = original_operator
    if not isinstance(valid_operator, str) or \
        valid_operator.strip().upper() not in ["OR", "AND"]:
        print(f"Invalid operator (defaulting to 'OR')")
        valid_operator = "OR"
    valid_operator = valid_operator.strip().upper()
    return valid_operator

if __name__ == "__main__":

    print_header(f"{__file__}")

    print_separator()

    print_subheader(f"Testing")

    print_separator()

    print_footer()
