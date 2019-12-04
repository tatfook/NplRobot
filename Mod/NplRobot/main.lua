--[[
Title: 
Author(s): leio
Date: 2019/11/29
Desc: 
use the lib:
------------------------------------------------------------
NPL.load("(gl)Mod/NplRobot/main.lua");
------------------------------------------------------------
]]
local CmdParser = commonlib.gettable("MyCompany.Aries.Game.CmdParser");	

local NplRobot = commonlib.inherit(commonlib.gettable("Mod.ModBase"),commonlib.gettable("Mod.NplRobot"));

function NplRobot:ctor()
end

-- virtual function get mod name
function NplRobot:GetName()
	return "NplRobot"
end

-- virtual function get mod description 
function NplRobot:GetDesc()
	return "NplRobot is a plugin in paracraft"
end

function NplRobot:init()
	LOG.std(nil, "info", "NplRobot", "plugin initialized");

	-- register a new block item, id < 10512 is internal items, which is not recommended to modify. 
	GameLogic.GetFilters():add_filter("block_types", function(xmlRoot) 
		local blocks = commonlib.XPath.selectNode(xmlRoot, "/blocks/");
		if(blocks) then
			NPL.load("(gl)Mod/NplRobot/ItemNplRobotBlock.lua");
			blocks[#blocks+1] = {name="block", attr={ name="NplRobotBlock",
				id = 10517, item_class="ItemNplRobotBlock", text=L"npl robot 代码模型",
				icon = "Mod/NplRobot/textures/icon.png",
			}}
			LOG.std(nil, "info", "NplRobot", "npl robot  is registered");

		end
		return xmlRoot;
	end)

	-- add block to category list to be displayed in builder window (E key)
	GameLogic.GetFilters():add_filter("block_list", function(xmlRoot) 
		for node in commonlib.XPath.eachNode(xmlRoot, "/blocklist/category") do
			if(node.attr.name == "tool" or node.attr.name == "character") then
				node[#node+1] = {name="block", attr={name="NplRobotBlock"} };
			end
		end
		return xmlRoot;
	end)
end

function NplRobot:OnLogin()
end
-- called when a new world is loaded. 

function NplRobot:OnWorldLoad()
end
-- called when a world is unloaded. 

function NplRobot:OnLeaveWorld()
end

function NplRobot:OnDestroy()
end


