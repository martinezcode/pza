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

import os

# --- Pride entry point ---
# --- Runs when app is launched with command 'pride' ---

def pride(
    PzaHub: AppHub,
    out_folder: str | None = None
):
    """
    Generates modular project app template from 'pride' example app.
    """
    print(f"Pride Command")
    print()
    print(PzaHub)

    if not out_folder:
        out_folder = os.curdir

    pride_folder = pza.pie.get_resource("templates/pride/")
    exclude_names = ["__pycache__", ".DS_Store"]
    _ = pza.pie.copy_folder_contents(pride_folder, out_folder, False, exclude_names)
    print()

    return

# --- Solo entry point ---
# --- Runs when app is launched with command 'solo' ---

def solo(
    PzaHub: AppHub,
    out_file: str | None = None
):
    """
    Generates single file app template from 'solo' example app.
    """
    print(f"Solo Command")
    print()
    print(PzaHub)

    solo_file = pza.pie.get_resource("templates/solo/solo/solo.py")

    if not out_file:
        out_folder = os.curdir
        out_file = os.path.join(out_folder, os.path.basename(solo_file))

    _ = pza.pie.copy_file(solo_file, out_file)
    print()

    return

# --- Recipe entry point ---
# --- Runs when app is launched with command 'recipe' ---

def recipe(
    PzaHub: AppHub,
    py: str | None = None,
    folder: str | None = None,
    db: str | None = None
):
    """
    Generates a recipe from an existing app or database.
    """
    print(f"TODO: Recipe Command")
    print()
    print(PzaHub)
    print()
    print_with_label("py", py)
    print_with_label("folder", folder)
    print_with_label("db", db)
    print()
    return

# --- SQL entry point ---
# --- Runs when app is launched with command 'sql' ---

def sql(
    PzaHub: AppHub,
    recipe: str | None = None,
    json: str | None = None,
    json_file: str | None = None,
    out_file: str | None = None,
    run: str | None = None
):
    """
    Generates an SQL query from a recipe.
    """
    print(f"TODO: SQL Command")
    print()
    print(PzaHub)
    print()
    print_with_label("recipe", recipe)
    print_with_label("json", json)
    print_with_label("json_file", json_file)
    print_with_label("out_file", out_file)
    print_with_label("run", run)
    print()
    return

if __name__ == "__main__":

    print_header(f"{__file__}")

    print_separator()

    print()

    print_separator()

    print_footer()
