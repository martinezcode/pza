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
import pza.database

import os
import textwrap

def get_sample_data_folder(PrideHub: AppHub) -> str | None:
    """
    Returns the path string for the folder where sample data is saved.
    """
    sample_data_folder = os.path.join(PrideHub.settings_folder, f"flags")
    folder_created = pza.pie.create_folder(sample_data_folder)
    if not folder_created:
        return None
    return sample_data_folder

def download_sample_data(output_folder: str, overwrite_existing: bool = False) -> bool:
    """
    Downloads sample pride flag data from the GPL-3 licensed Pride Flag Search project.

    Source:
    https://github.com/emily-noble/prideflagsearch
    License: GNU General Public License v3.0
    """
    repo_data_url = (
        "https://raw.githubusercontent.com/emily-noble/"
        "prideflagsearch/master/"
        "search/static/search/data/"
    )
    repo_image_url = f"{repo_data_url}img/"
    recipe_filename = "prideflags.json"
    repo_recipe_url = f"{repo_data_url}{recipe_filename}"
    output_recipe_file = os.path.join(output_folder, recipe_filename)
    folder_created = pza.pie.create_folder(output_folder)
    if not folder_created:
        print(f"Unable to download sample data")
        print()
        return False
    if not os.path.exists(output_recipe_file):
        print("Downloading sample data...")
        print()
    file_downloaded = pza.pie.download(repo_recipe_url, output_recipe_file, overwrite_existing)
    if not file_downloaded:
        print(f"Unable to download sample data")
        print()
        return False
    recipe = pza.pie.read_json_file_to_dictionary(output_recipe_file)
    if not recipe:
        print(f"Unable to download sample data")
        print()
        return False
    flag_list = recipe.get("flags", [])
    for flag in flag_list:
        if not isinstance(flag, dict):
            continue
        else:
            image_filename = flag.get("src", "").replace("/static/search/data/img/", "")
            image_url = f"{repo_image_url}{image_filename}"
            image_file = os.path.join(output_folder, image_filename)
            file_downloaded = pza.pie.download(image_url, image_file, overwrite_existing)
            if not file_downloaded:
                print(f"Unable to download {image_filename}")
                print()
    return True

def import_sample_data(PrideHub: AppHub, overwrite_existing: bool = False) -> bool:
    """
    Imports sample data into the app database.
    """
    # Get the data
    sample_data_folder = get_sample_data_folder(PrideHub)
    if not sample_data_folder:
        print(f"Unable to access sample data folder")
        print()
        return False
    data_downloaded = download_sample_data(sample_data_folder, overwrite_existing)
    if not data_downloaded:
        print("Unable to access sample data")
        print()
        return False
    flags_recipe_filename = "prideflags.json"
    flags_recipe_file = os.path.join(sample_data_folder, flags_recipe_filename)
    flags_recipe = pza.pie.read_json_file_to_dictionary(flags_recipe_file)
    flag_list = flags_recipe.get("flags", [])

    # Import the data
    conn = PrideHub.database.connect()
    if not conn:
        print("Unable to connect to database")
        print()
        return False

    # Normally we would check for data updates
    # but in this case we can wipe and reload the entire set
    sql = f"DELETE FROM Flags"
    parameters =  None
    executed = pza.database.sql_execute(sql, parameters, conn)
    if not executed:
        print(f"Unable to replace existing flag data")
        print()
        conn.close()
        return False

    sql = f"DELETE FROM Colors"
    parameters =  None
    executed = pza.database.sql_execute(sql, parameters, conn)
    if not executed:
        print(f"Unable to replace existing color data")
        print()
        conn.close()
        return False

    sql = f"DELETE FROM ColorMap"
    parameters =  None
    executed = pza.database.sql_execute(sql, parameters, conn)
    if not executed:
        print(f"Unable to replace existing color map data")
        print()
        conn.close()
        return False

    # Process each flag
    for flag_recipe in flag_list:
        if not isinstance(flag_recipe, dict):
            continue
        else:
            flag_name = flag_recipe.get("name", "")
            filename = flag_recipe.get("src", "").replace("/static/search/data/img/", "")
            stripes = flag_recipe.get("stripes", 0)
            shapes = flag_recipe.get("shapes", False)
            src = flag_recipe.get("src", "")
            citation_recipe = flag_recipe.get("citation", {})
            citation_text = citation_recipe.get("text", 0)
            citation_sources_list = citation_recipe.get("sourceList", [])
            citation_sources = f"\n".join(citation_sources_list)
            citation_image = citation_recipe.get("imageSource", "")
            citation_author = citation_recipe.get("firstAuthoring", "")
            colors = flag_recipe.get("colors", [])

            # Add the colors and get ids for relational links
            color_ids = []
            for color in colors:
                # Check for existing color
                sql = "SELECT color_id FROM Colors WHERE color_name = ?"
                parameters = (color,)
                color_id_row = pza.database.sql_select_one(sql, parameters, conn)
                if color_id_row:
                    color_id = color_id_row[0]
                else:
                    sql = f"INSERT INTO Colors (color_name) VALUES (?)"
                    parameters = (color,)
                    executed = pza.database.sql_execute(sql, parameters, conn)
                    if not executed:
                        print(f"Unable to add color: {color}")
                        print()
                        conn.close()
                        return False
                    sql = "SELECT last_insert_rowid()"
                    parameters = None
                    last_id_row = pza.database.sql_select_one(sql, parameters, conn)
                    if not last_id_row:
                        print(f"Unable to get color id")
                        conn.close()
                        return False
                    color_id = last_id_row[0]
                color_ids.append(color_id)

            # Add the flag and get id for relational links
            sql = f"""
                INSERT INTO Flags (
                    flag_name,
                    filename,
                    stripes,
                    shapes,
                    src,
                    citation_text,
                    citation_sources,
                    citation_image,
                    citation_author
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """
            parameters = (
                flag_name,
                filename,
                stripes,
                shapes,
                src,
                citation_text,
                citation_sources,
                citation_image,
                citation_author,
            )
            executed = pza.database.sql_execute(sql, parameters, conn)
            if not executed:
                print(f"Unable to add flag")
                print()
                conn.close()
                return False
            sql = "SELECT last_insert_rowid()"
            parameters = None
            last_id_row = pza.database.sql_select_one(sql, parameters, conn)
            if not last_id_row:
                print(f"Unable to get flag id")
                print()
                conn.close()
                return False
            flag_id = last_id_row[0]

            # Add to relational link map
            for color_id in color_ids:
                sql = f"INSERT INTO ColorMap (color_id, flag_id) VALUES (?, ?)"
                parameters = (color_id, flag_id)
                executed = pza.database.sql_execute(sql, parameters, conn)
                if not executed:
                    print(f"Unable to add color link for {flag_name}")
                    print()
                    conn.close()
                    return False

    # Close the database
    conn.close()

    return True

def get_random_flag(PrideHub: AppHub) -> tuple | None:
    """
    Returns the database row for a random flag.
    """
    conn = PrideHub.database.connect()
    if not conn:
        print(f"Database unavailable")
        print()
        return None
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
        ORDER BY RANDOM()
        LIMIT 1
    """
    parameters = None
    flag_row = pza.database.sql_select_one(sql, parameters, conn)
    if not flag_row or len(flag_row) < 2:
        print(f"Flag unavailable")
        print()
        conn.close()
        return None
    conn.close()
    return flag_row

def wrap(source_text: str) -> str:
    """
    Returns a string wrapped for display.
    """
    return "\n".join(
        textwrap.wrap(
            source_text,
            width=60,
            replace_whitespace=False,
            drop_whitespace=False
        )
    )

if __name__ == "__main__":

    print_header(f"{__file__}")

    print_separator()

    print()

    print_separator()

    print_footer()