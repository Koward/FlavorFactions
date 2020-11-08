from os import path, mkdir
from shutil import copy2, rmtree

from FlavorFactions.common import merge_update_df, read_from_csv, join_df
from FlavorFactions.generate_CreatureFactionInfo import generate_creature_faction_info_lua
from FlavorFactions.generate_Factions import generate_factions_lua, get_base_neutral_factions

BUILD_DIR = "build"
SOURCE_DIR = "src"


def copy_to_build(file_path):
    copy2(path.join(SOURCE_DIR, file_path), path.join(BUILD_DIR, file_path))


if path.exists(BUILD_DIR):
    rmtree(BUILD_DIR)
mkdir(BUILD_DIR)

copy_to_build("Core.lua")
copy_to_build("FlavorFactions.toc")

# Base neutral factions (e.g Booty Bay) are always displayed for characters already.
# So no need to handle them ourselves => we can decrease AddOn size!
base_neutral_factions = get_base_neutral_factions(path.join(SOURCE_DIR, 'Factions.csv'))

print("Processing faction names..")
# GetFactionInfoByGroupID does not return data for opposite faction reputations so we store them in csv files.
factions_csv_files = [
    path.join(SOURCE_DIR, 'Factions.csv'),
    path.join(SOURCE_DIR, 'FactionsLocalization.csv'),  # Add Blizzard localization for faction names
]
factions_df = join_df(read_from_csv(factions_csv_files), 'ID')

# Custom improved localization
list_factions_fix = [factions_df]
list_factions_fix.extend(read_from_csv([path.join(SOURCE_DIR, "FixesFactions.csv")]))
factions_df = merge_update_df(list_factions_fix, "Name_lang")

factions_df.ID = factions_df.ID.astype(int)
factions_df = factions_df[~factions_df.ID.isin(base_neutral_factions)]
factions_df.sort_values('ID', inplace=True)
generate_factions_lua(path.join(BUILD_DIR, 'Factions.lua'), factions_df)

print("Processing faction information for all creatures..")
creature_csv_files = [
    path.join(SOURCE_DIR, 'CreatureFactionInfo.csv'),
    path.join(SOURCE_DIR, 'FixesCreatureFactionInfo.csv')
]
creature_faction_info_df = merge_update_df(read_from_csv(creature_csv_files), 'ID')
creature_faction_info_df.FactionID = creature_faction_info_df.FactionID.astype(int)
creature_faction_info_df = creature_faction_info_df[~creature_faction_info_df.FactionID.isin(base_neutral_factions)]
generate_creature_faction_info_lua(path.join(BUILD_DIR, 'CreatureFactionInfo.lua'), creature_faction_info_df)
