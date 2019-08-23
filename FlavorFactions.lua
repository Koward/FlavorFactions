function UnitFlavorFaction(unit)
    local _, _, _, _, _, npc_id, _ = string.split("-", UnitGUID(unit));
    return CreatureFlavorFactions[tonumber(npc_id)]
end

local function InsertLine(tooltip, index, tooltipText, r, g, b)
    assert(index <= tooltip:NumLines(), "Cannot insert after last element. Use tooltip:AddLine instead.")
    local tooltipName = tooltip:GetName()
    tooltip:AddLine("Placeholder")
    local k = tooltip:NumLines()
    while k > index do
        _G[tooltipName .. 'TextLeft' .. k]:SetText(_G[tooltipName .. 'TextLeft' .. k-1]:GetText())
        local prevR, prevG, prevB, _ = _G[tooltipName .. 'TextLeft' .. k-1]:GetTextColor()
        _G[tooltipName .. 'TextLeft' .. k]:SetTextColor( prevR, prevG, prevB)
        k = k - 1
    end
    _G[tooltipName .. 'TextLeft' .. index]:SetText(tooltipText)
    _G[tooltipName .. 'TextLeft' .. index]:SetTextColor(r, g, b)
end

--- @param condition function taking a string as parameter and returning a bool
--- @return index number of line where condition is true or nil
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

    if not found then return nil end
end

local function GetFactionDisplayName(factionID)
    if FactionInfoOverrides[factionID] then
        return FactionInfoOverrides[factionID][1]
    else
        return GetFactionInfoByID(factionID)
    end
end

GameTooltip:HookScript("OnTooltipSetUnit", function()
    local tooltip = GameTooltip
    local _, unitType = GameTooltip:GetUnit()
    local type, _, _, _, _, _, _ = string.split("-", UnitGUID(unitType));
    if type == "Creature" then
        local factionID = UnitFlavorFaction(unitType)
        if factionID then
            -- Find line that starts with "Level"
            local levelIndex = FindLine(tooltip, function(line) return string.sub(line, 1, #"Level") == "Level" end)
            local faction_name = GetFactionDisplayName(factionID)
            local faction_color = TOOLTIP_DEFAULT_COLOR
            if not levelIndex or levelIndex == tooltip:NumLines() then
                tooltip:AddLine(faction_name, faction_color.r, faction_color.g, faction_color.b)
            else
                local faction_index = levelIndex + 1
                InsertLine(tooltip, faction_index, faction_name, faction_color.r, faction_color.g, faction_color.b)
            end
        end
    end
end)


