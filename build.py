from os import path, mkdir
from shutil import copy2, rmtree

from FlavorFactions.common import merge_update_csv_files, unlock_file
from FlavorFactions.generate_CreatureFactionInfo import generate_creature_faction_info_lua
from FlavorFactions.generate_Factions import generate_factions_lua, generate_faction_info_lua, get_base_neutral_factions

BUILD_DIR = "build"
SOURCE_DIR = "src"


def copy_to_build(file_path):
    copy2(path.join(SOURCE_DIR, file_path), path.join(BUILD_DIR, file_path))


if path.exists(BUILD_DIR):
    rmtree(BUILD_DIR)
mkdir(BUILD_DIR)
mkdir(path.join(BUILD_DIR, "enUS"))

copy_to_build("Core.lua")
copy_to_build("FlavorFactions.toc")
copy_to_build(path.join("enUS", "FixesFactionInfo.lua"))

# Base neutral factions (e.g Booty Bay) are always displayed for characters already.
# So no need to handle them ourselves => we can decrease AddOn size!
base_neutral_factions = get_base_neutral_factions(path.join(SOURCE_DIR, 'Factions.csv'))

# Unfortunately, GetFactionInfoByGroupID does not return data for opposite faction reputations so we store them here.
factions_csv_files = [
    path.join(SOURCE_DIR, 'Factions.csv')
]
factions_df = merge_update_csv_files(factions_csv_files, 'ID')
factions_df.ID = factions_df.ID.astype(int)
factions_df = factions_df[~factions_df.ID.isin(base_neutral_factions)]
generate_factions_lua(path.join(BUILD_DIR, 'Factions.lua'), factions_df)
generate_faction_info_lua(path.join(BUILD_DIR, 'enUS/FactionInfo.lua'), factions_df)

creature_csv_files = [
    path.join(SOURCE_DIR, 'CreatureFactionInfo.csv'),
    path.join(SOURCE_DIR, 'FixesCreatureFactionInfo.csv')
]
creature_faction_info_df = merge_update_csv_files(creature_csv_files, 'ID')
creature_faction_info_df.FactionID = creature_faction_info_df.FactionID.astype(int)
creature_faction_info_df = creature_faction_info_df[~creature_faction_info_df.FactionID.isin(base_neutral_factions)]
generate_creature_faction_info_lua(path.join(BUILD_DIR, 'CreatureFactionInfo.lua'), creature_faction_info_df)
