local folderName, _ = ...
local addonName = folderName

function UnitFlavorFaction(unit)
    local _, _, _, _, _, npc_id, _ = string.split("-", UnitGUID(unit));
    return CreatureFactionInfo[tonumber(npc_id)]
end

local function InsertLine(tooltip, index, tooltipText, r, g, b)
    assert(index <= tooltip:NumLines(), "Cannot insert after last element. Use tooltip:AddLine instead.")
    local tooltipName = tooltip:GetName()
    tooltip:AddLine("Placeholder")
    local k = tooltip:NumLines()
    while k > index do
        _G[tooltipName .. 'TextLeft' .. k]:SetText(_G[tooltipName .. 'TextLeft' .. k - 1]:GetText())
        local prevR, prevG, prevB, _ = _G[tooltipName .. 'TextLeft' .. k - 1]:GetTextColor()
        _G[tooltipName .. 'TextLeft' .. k]:SetTextColor(prevR, prevG, prevB)
        k = k - 1
    end
    _G[tooltipName .. 'TextLeft' .. index]:SetText(tooltipText)
    _G[tooltipName .. 'TextLeft' .. index]:SetTextColor(r, g, b)
end

--- @param condition function taking a string as parameter and returning a bool
--- @return number index of line where condition is true or nil
local function FindLine(tooltip, condition)
    local found = false
    local i = 1
    local tooltipName = tooltip:GetName()
    while _G[tooltipName .. 'TextLeft' .. i] do
        local line = _G[tooltipName .. 'TextLeft' .. i]:GetText()
        if condition(line) then
            found = true
            return i
        end
        i = i + 1
    end

    if not found then
        return nil
    end
end

local playerFaction = UnitFactionGroup("player")
local function IsBaseFaction(faction)
    return faction.isBaseFaction == 1 or
            (faction.isBaseFaction == 2 and playerFaction == "Horde") or
            (faction.isBaseFaction == 3 and playerFaction == "Alliance")
end
local function ShouldFactionBeAdded(faction)
    local isGameplayOnly = faction.isGameplayOnly
    local displayGameplayOnly = false -- TODO Ingame setting
    return not IsBaseFaction(faction) and (not isGameplayOnly or displayGameplayOnly)
end

GameTooltip:HookScript("OnTooltipSetUnit", function()
    local tooltip = GameTooltip
    local name, unitType = GameTooltip:GetUnit()
    if name and unitType then
        local guid = UnitGUID(unitType)
        if type(guid) == "string" then
            local type, _, _, _, _, _, _ = string.split("-", guid)
            if type == "Creature" then
                local factionID = UnitFlavorFaction(unitType)
                if not factionID then
                    return
                end
                local faction = Factions[factionID] -- GetFactionInfoByID(factionID) does not work for enemy factions
                if faction and ShouldFactionBeAdded(faction) then
                    -- Find line that starts with "Level" and insert faction after
                    local levelIndex = FindLine(tooltip, function(line)
                        return string.sub(line, 1, #"Level") == "Level"
                    end)
                    local faction_color = TOOLTIP_DEFAULT_COLOR
                    if not levelIndex or levelIndex == tooltip:NumLines() then
                        tooltip:AddLine(faction.name, faction_color.r, faction_color.g, faction_color.b)
                    else
                        local faction_index = levelIndex + 1
                        InsertLine(tooltip, faction_index, faction.name, faction_color.r, faction_color.g, faction_color.b)
                    end
                end
            end
        end
    end
end)


