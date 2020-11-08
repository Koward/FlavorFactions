import pandas as pd


def generate_creature_faction_info_lua(lua_file_path, creature_faction_info_df):
    creature_faction_info_df = creature_faction_info_df.apply(lambda row: f"F[{row.ID}] = {row.FactionID}", axis=1)
    pd.set_option("display.max_colwidth", 10000)  # disable truncation

    with open(lua_file_path, 'w', encoding='UTF-8') as lua_file:
        lua_header = """-- *** DO NOT EDIT. THIS IS A GENERATED FILE. ***
--- Format: F[ID] = <factionID>
CreatureFactionInfo = {}
local F = CreatureFactionInfo\n"""
        lua_file.write(lua_header)
        creature_faction_info_df.to_string(buf=lua_file, index=False)
