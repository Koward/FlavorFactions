import csv

from FlavorFactions.common import unlock_file, lock_file

# Unfortunately, GetFactionInfoByGroupID does not return data for opposite faction reputations so we store them here.

LUA_FILE_PATH = 'Factions.lua'
unlock_file(LUA_FILE_PATH)

with open(LUA_FILE_PATH, 'w', encoding='UTF-8') as lua_file:
    luaHeader = """-- *** DO NOT EDIT. THIS IS A GENERATED FILE. ***
Factions = {}
local F = Factions\n"""
    lua_file.write(luaHeader)
    with open('Factions.csv', 'r', encoding='UTF-8-sig', newline='') as csv_file:
        reader = csv.DictReader(csv_file, dialect="excel-backslash")
        for row in reader:
            try:
                faction_id = int(row['ID'])
                faction_name = row['Name_lang']
                faction_description = row['Description_lang']
                faction_gameplay_only = True if int(row["GameplayOnly"]) == 1 else False
                faction_base_faction = int(row["BaseFaction"])
                lua_file.write(f'F[{faction_id}] = {{name="{faction_name}", description="{faction_description}", '
                               f'isGameplayOnly={"true" if faction_gameplay_only else "false"}, isBaseFaction='
                               f'{faction_base_faction}}}\n')
            except ValueError:
                print(f"Invalid row: {row}")

lock_file(LUA_FILE_PATH)
