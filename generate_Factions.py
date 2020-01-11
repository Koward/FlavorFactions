import csv

import pandas as pd

from FlavorFactions.common import unlock_file, lock_file


def generate_factions_lua(lua_file_path, factions_df):
    def lua_assignation(row):
        return f'F[{row.ID}] = {{name="{row.Name_lang}", isGameplayOnly={"true" if row.GameplayOnly == "1" else "false"}, isBaseFaction={row.BaseFaction}}}'

    factions_df = factions_df.apply(lua_assignation, axis=1)

    unlock_file(lua_file_path)

    with open(lua_file_path, 'w', encoding='UTF-8') as lua_file:
        lua_header = """-- *** DO NOT EDIT. THIS IS A GENERATED FILE. ***
    Factions = {}
    local F = Factions\n"""
        lua_file.write(lua_header)
        pd.set_option("display.max_colwidth", 10000)  # disable truncation
        factions_df.to_string(buf=lua_file, index=False)

    lock_file(lua_file_path)


def generate_faction_info_lua(lua_file_path, factions_df):
    names_df = factions_df[factions_df.Name_lang != ""].apply(
        lambda row: f'L["{row.Name_lang}_Name"] = "{row.Name_lang}"', axis=1
    )

    unlock_file(lua_file_path)

    with open(lua_file_path, 'w', encoding='UTF-8') as lua_file:
        lua_header = """-- *** DO NOT EDIT. THIS IS A GENERATED FILE. ***
    local _, L = ...\n"""
        lua_file.write(lua_header)
        pd.set_option("display.max_colwidth", 10000)  # disable truncation
        names_df.to_string(buf=lua_file, index=False)

    lock_file(lua_file_path)


def get_base_neutral_factions(factions_csv_path):
    """
    :param factions_csv_path: Path to CSV file with factions
    :return: A set of integer faction IDs of neutral factions present in base World of Warcraft.
    """
    factions = set()
    with open(factions_csv_path, 'r', encoding='UTF-8-sig', newline='') as csv_file:
        reader = csv.DictReader(csv_file, dialect="excel-backslash")
        for row in reader:
            try:
                faction_id = int(row['ID'])
                if int(row['BaseFaction']) == 1:
                    factions.add(faction_id)
            except ValueError:
                print(f"Invalid row: {row}")
    return factions
