import csv

from FlavorFactions.common import unlock_file, lock_file

# Base neutral factions (e.g Booty Bay) are always displayed for characters already.
# So no need to handle them ourselves => we can decrease AddOn size!
base_neutral_factions = set()
with open('Factions.csv', 'r', encoding='UTF-8-sig', newline='') as csv_file:
    reader = csv.DictReader(csv_file, dialect="excel-backslash")
    for row in reader:
        try:
            faction_id = int(row['ID'])
            if int(row['BaseFaction']) == 1:
                base_neutral_factions.add(faction_id)
        except ValueError:
            print(f"Invalid row: {row}")

LUA_FILE_PATH = 'CreatureFactionInfo.lua'

unlock_file(LUA_FILE_PATH)

with open(LUA_FILE_PATH, 'w', encoding='UTF-8') as lua_file:
    luaHeader = """-- *** DO NOT EDIT. THIS IS A GENERATED FILE. ***
--- Format: F[ID] = <factionID>
CreatureFactionInfo = {}
local F = CreatureFactionInfo\n"""
    lua_file.write(luaHeader)
    with open('CreatureFactionInfo.csv', 'r', encoding='UTF-8-sig', newline='') as csv_file:
        reader = csv.DictReader(csv_file, dialect="excel-backslash")
        for row in reader:
            try:
                unit_id = int(row['ID'])
                faction_id = int(row['FactionID'])
                if faction_id not in base_neutral_factions:
                    lua_file.write(f'F[{unit_id}] = {faction_id}\n')
            except ValueError:
                print(f"Invalid row: {row}")

lock_file(LUA_FILE_PATH)
