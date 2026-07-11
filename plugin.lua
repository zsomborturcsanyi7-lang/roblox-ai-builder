local ChangeHistoryService = game:GetService("ChangeHistoryService")
local HttpService = game:GetService("HttpService")

local BASE_URL = "http://localhost:6000"
local GENERATE_URL = BASE_URL .. "/generate"
local POLL_URL = BASE_URL .. "/poll/"
local CLEAR_URL = BASE_URL .. "/clear"
local SWITCH_URL = BASE_URL .. "/switch"
local STATUS_URL = BASE_URL .. "/status"

-- GUI --
local toolbar = plugin:CreateToolbar("AI ARCHITECT ULTIMATE")
local toggleBtn = toolbar:CreateButton("Open AI", "Assistant", "rbxassetid://4458901886")
local widgetInfo = DockWidgetPluginGuiInfo.new(Enum.InitialDockState.Float, true, false, 350, 500, 300, 400)
local widget = plugin:CreateDockWidgetPluginGui("AI_Architect_V13", widgetInfo, "AI Developer Console")
widget.Title = "ROBLOX AI (POLLING MODE)"

local mainFrame = Instance.new("Frame", widget); mainFrame.Size = UDim2.new(1,0,1,0); mainFrame.BackgroundColor3 = Color3.fromRGB(30, 30, 30)
local scroll = Instance.new("ScrollingFrame", mainFrame); scroll.Size = UDim2.new(1,-10,0.72,-45); scroll.Position = UDim2.new(0,5,0,5); scroll.BackgroundTransparency = 1; scroll.AutomaticCanvasSize = Enum.AutomaticSize.Y; scroll.ScrollBarThickness = 6
local layout = Instance.new("UIListLayout", scroll); layout.Padding = UDim.new(0,8); layout.SortOrder = Enum.SortOrder.LayoutOrder
local input = Instance.new("TextBox", mainFrame); input.Size = UDim2.new(0.65,-10,0.12,0); input.Position = UDim2.new(0,5,0.85,0); input.BackgroundColor3 = Color3.fromRGB(50,50,50); input.TextColor3 = Color3.new(1,1,1); input.TextWrapped = true; input.ClearTextOnFocus = false; input.PlaceholderText = "Describe your game..."
local send = Instance.new("TextButton", mainFrame); send.Size = UDim2.new(0.2,-5,0.12,0); send.Position = UDim2.new(0.65,0,0.85,0); send.Text = "SEND"; send.BackgroundColor3 = Color3.fromRGB(0, 130, 200); send.TextColor3 = Color3.new(1,1,1)
local providerBtn = Instance.new("TextButton", mainFrame); providerBtn.Size = UDim2.new(0.8, -5, 0.08, 0); providerBtn.Position = UDim2.new(0, 5, 0.75, 0); providerBtn.BackgroundColor3 = Color3.fromRGB(60, 60, 60); providerBtn.TextColor3 = Color3.new(1, 1, 1); providerBtn.Text = "LOADING..."
local clearBtn = Instance.new("TextButton", mainFrame); clearBtn.Size = UDim2.new(0.2, -5, 0.08, 0); clearBtn.Position = UDim2.new(0.8, 0, 0.75, 0); clearBtn.BackgroundColor3 = Color3.fromRGB(200, 50, 50); clearBtn.TextColor3 = Color3.new(1,1,1); clearBtn.Text = "CLR"

local currentProvider = "deepseek"
local msgCount = 0

local function AddLog(txt, color, isUser)
    msgCount = msgCount + 1
    local container = Instance.new("Frame", scroll); container.BackgroundTransparency = 1; container.Size = UDim2.new(1, 0, 0, 0); container.AutomaticSize = Enum.AutomaticSize.Y; container.LayoutOrder = -msgCount
    local tag = Instance.new("TextLabel", container); tag.Size = UDim2.new(0, 50, 0, 20); tag.BackgroundTransparency = 1; tag.Text = isUser and "YOU:" or "AI:"; tag.TextColor3 = color; tag.Font = Enum.Font.SourceSansBold
    local content = Instance.new("TextBox", container); content.Position = UDim2.new(0, 45, 0, 0); content.Size = UDim2.new(1, -50, 0, 0); content.AutomaticSize = Enum.AutomaticSize.Y; content.BackgroundTransparency = 1; content.Text = txt; content.TextColor3 = Color3.new(0.9, 0.9, 0.9); content.TextWrapped = true; content.TextEditable = false; content.ClearTextOnFocus = false
    scroll.CanvasPosition = Vector2.new(0, 0)
    return content
end

local function Convert(p, v)
    if (p == "Position" or p == "Size" or p == "Orientation") then
        if type(v) == "string" and v:find(",") then
            local n = v:split(",")
            return Vector3.new(tonumber(n[1]) or 0, tonumber(n[2]) or 0, tonumber(n[3]) or 0)
        elseif type(v) == "table" then
            return Vector3.new(v[1] or v.X or 0, v[2] or v.Y or 0, v[3] or v.Z or 0)
        end
    end
    if type(v) ~= "string" then return v end
    if p == "Color" or p == "Color3" then
        if type(v) == "table" then
            -- Handle [1, 0, 0] or {r=1, g=0, b=0}
            local r = v[1] or v.r or v.R or 1
            local g = v[2] or v.g or v.G or 1
            local b = v[3] or v.b or v.B or 1
            return Color3.new(r, g, b)
        elseif type(v) == "string" then
            if v:find(",") then
                local n = v:split(",")
                return Color3.new(tonumber(n[1]) or 1, tonumber(n[2]) or 1, tonumber(n[3]) or 1)
            else
                return Color3.fromHex(v)
            end
        end
    end
    if p == "Material" then 
        local success, res = pcall(function() return Enum.Material[v] end)
        return success and res or v
    end
    if v == "true" then return true elseif v == "false" then return false end
    return v
end

local function Execute(cmds)
    ChangeHistoryService:SetWaypoint("AI_Action")
    for _, c in ipairs(cmds) do
        if c.action == "create" then
            local obj = Instance.new(c.type or "Part")
            obj.Name = c.name or obj.Name
            if c.properties then for k,v in pairs(c.properties) do pcall(function() obj[k] = Convert(k,v) end) end end
            if c.source and obj:IsA("LuaSourceContainer") then obj.Source = c.source end
            obj.Parent = (c.parent and game:FindFirstChild(c.parent, true)) or workspace
        elseif c.action == "print" then
            AddLog(c.message, Color3.new(0.4, 0.8, 1), false)
        end
    end
    ChangeHistoryService:SetWaypoint("AI_Action_End")
end

function SendRequest(txt)
    AddLog(txt, Color3.new(0.8,0.8,0.8), true)
    local statusLog = AddLog("Thinking...", Color3.new(1, 1, 0), false)

    local success, response = pcall(function() 
        return HttpService:PostAsync(GENERATE_URL, HttpService:JSONEncode({prompt=txt})) 
    end)

    if success then
        local data = HttpService:JSONDecode(response)
        local jobId = data.job_id
        
        -- Start Polling Loop
        while true do
            wait(2)
            local s, r = pcall(function() return HttpService:GetAsync(POLL_URL .. jobId) end)
            if s then
                local job = HttpService:JSONDecode(r)
                if job.status == "completed" then
                    statusLog.Text = "Done!"
                    Execute(job.result)
                    break
                elseif job.status == "error" then
                    statusLog.Text = "Error: " .. tostring(job.message)
                    break
                end
            else
                statusLog.Text = "Connection lost during polling."
                break
            end
        end
    else
        statusLog.Text = "Server Offline."
    end
end

send.MouseButton1Click:Connect(function()
    if input.Text == "" then return end
    local t = input.Text; input.Text = ""; SendRequest(t)
end)

clearBtn.MouseButton1Click:Connect(function()
    HttpService:PostAsync(CLEAR_URL, "{}")
    for _, c in pairs(scroll:GetChildren()) do if not c:IsA("UIListLayout") then c:Destroy() end end
    msgCount = 0
end)

providerBtn.MouseButton1Click:Connect(function()
    local nextP = (currentProvider == "gemini") and "deepseek" or "gemini"
    local s, r = pcall(function() return HttpService:PostAsync(SWITCH_URL, HttpService:JSONEncode({provider = nextP})) end)
    if s then currentProvider = nextP; providerBtn.Text = "MODE: " .. nextP:upper() end
end)

toggleBtn.Click:Connect(function() widget.Enabled = not widget.Enabled end)
spawn(function()
    local s, r = pcall(function() return HttpService:GetAsync(STATUS_URL) end)
    if s then 
        local d = HttpService:JSONDecode(r)
        currentProvider = d.provider
        providerBtn.Text = "MODE: " .. currentProvider:upper()
    end
end)
