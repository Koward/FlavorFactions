from FlavorFactions.common import merge_update_csv_files
from FlavorFactions.generate_CreatureFactionInfo import generate_creature_faction_info_lua
from FlavorFactions.generate_Factions import generate_factions_lua, generate_faction_info_lua, get_base_neutral_factions

# Base neutral factions (e.g Booty Bay) are always displayed for characters already.
# So no need to handle them ourselves => we can decrease AddOn size!
base_neutral_factions = get_base_neutral_factions('Factions.csv')

# Unfortunately, GetFactionInfoByGroupID does not return data for opposite faction reputations so we store them here.
factions_csv_files = [
    'Factions.csv'
]
factions_df = merge_update_csv_files(factions_csv_files, 'ID')
factions_df.ID = factions_df.ID.astype(int)
factions_df = factions_df[~factions_df.ID.isin(base_neutral_factions)]
generate_factions_lua('Factions.lua', factions_df)
generate_faction_info_lua('enUS/FactionInfo.lua', factions_df)

creature_csv_files = [
    'CreatureFactionInfo.csv',
    'FixesCreatureFactionInfo.csv'
]
creature_faction_info_df = merge_update_csv_files(creature_csv_files, 'ID')
creature_faction_info_df.FactionID = creature_faction_info_df.FactionID.astype(int)
creature_faction_info_df = creature_faction_info_df[~creature_faction_info_df.FactionID.isin(base_neutral_factions)]
generate_creature_faction_info_lua('CreatureFactionInfo.lua', creature_faction_info_df)
