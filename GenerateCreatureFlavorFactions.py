import csv

# Create a set of faction (by ids) that we display in this addon
displayed_factions = set()
with open('DisplayedFactions.csv', 'r', encoding='UTF-8-sig', newline='') as csv_file:
    reader = csv.DictReader(csv_file)
    for row in reader:
        faction_id = row['ID']
        flavor_faction = row['FlavorFaction']
        if flavor_faction == '1':
            displayed_factions.add(faction_id)

with open('CreatureFlavorFactions.lua', 'w', encoding='UTF-8') as lua_file:
    luaHeader = """-- *** DO NOT EDIT. THIS IS A GENERATED FILE. ***
--- Format: F[ID] = <factionID>
CreatureFlavorFactions = {}
local F = CreatureFlavorFactions\n"""
    lua_file.write(luaHeader)
    with open('CreatureFactions.csv', 'r', encoding='UTF-8-sig', newline='') as csv_file:
        reader = csv.DictReader(csv_file)
        for row in reader:
            unit_id = row['ID']
            faction_id = row['FactionID']
            if faction_id in displayed_factions:
                lua_file.write('F[' + unit_id + '] = ' + faction_id + '\n')
