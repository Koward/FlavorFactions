import csv
import warnings

import pandas as pd

DEFAULT_LANGUAGE = "enUS"
ADDITIONAL_LANGUAGES = [
    "deDE", "esES", "esMX", "frFR", "koKR", "ptBR", "ruRU", "zhCN", "zhTW"
]


def write_default_language_section(lua_file, factions_df):
    def lua_assignation(row):
        locale_column = "Name_" + DEFAULT_LANGUAGE
        localized_name = getattr(row, locale_column)
        assert (localized_name is not None)
        return f'   F[{row.ID}] = {{name="{localized_name}", isGameplayOnly={"true" if row.GameplayOnly == "1" else "false"}, isBaseFaction={row.BaseFaction}}} '

    lua_lines_df = factions_df.apply(lua_assignation, axis=1)
    lua_lines_df.to_string(buf=lua_file, index=False)


def write_additional_language_section(lua_file, factions_df, language):
    def lua_assignation(row):
        locale_column = "Name_" + language
        if hasattr(row, locale_column):
            localized_name = getattr(row, locale_column)
            if localized_name is not None:
                return f'   F[{row.ID}].name = "{localized_name}"'
        return None

    lua_lines_df = factions_df.apply(lua_assignation, axis=1)
    lua_lines_df.dropna(inplace=True)

    if not lua_lines_df.empty:
        lua_file.write(f'if GetLocale() == "{language}" then\n')
        lua_lines_df.to_string(buf=lua_file, index=False)
        lua_file.write("\nend\n")
    else:
        warnings.warn(f'Language {language} has no localization entries.')


def generate_factions_lua(lua_file_path, factions_df):
    pd.set_option("display.max_colwidth", 10000)  # disable truncation

    with open(lua_file_path, 'w', encoding='UTF-8') as lua_file:
        lua_header = """-- *** DO NOT EDIT. THIS IS A GENERATED FILE. ***
Factions = {}
local F = Factions\n"""
        lua_file.write(lua_header)

        lua_file.write(f'\n\n-- Default language ({DEFAULT_LANGUAGE})\n')
        write_default_language_section(lua_file, factions_df)

        lua_file.write(f'\n\n-- Other supported languages ({ADDITIONAL_LANGUAGES})\n')
        for language in ADDITIONAL_LANGUAGES:
            write_additional_language_section(lua_file, factions_df, language)


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
