--[[
Title: ItemNplRobotBlock
Author(s): leio
Date: 2019/11/29
Desc: 
use the lib:
------------------------------------------------------------
NPL.load("(gl)Mod/NplRobot/ItemNplRobotBlock.lua");
local ItemNplRobotBlock = commonlib.gettable("MyCompany.Aries.Game.Items.ItemNplRobotBlock");
-------------------------------------------------------
]]
NPL.load("(gl)script/apps/Aries/Creator/Game/Common/Files.lua");
local Files = commonlib.gettable("MyCompany.Aries.Game.Common.Files");
local EntityManager = commonlib.gettable("MyCompany.Aries.Game.EntityManager");
local BlockEngine = commonlib.gettable("MyCompany.Aries.Game.BlockEngine")
local block_types = commonlib.gettable("MyCompany.Aries.Game.block_types")
local GameLogic = commonlib.gettable("MyCompany.Aries.Game.GameLogic")
local ItemStack = commonlib.gettable("MyCompany.Aries.Game.Items.ItemStack");

local ItemNplRobotBlock = commonlib.inherit(commonlib.gettable("MyCompany.Aries.Game.Items.Item"), commonlib.gettable("MyCompany.Aries.Game.Items.ItemNplRobotBlock"));

block_types.RegisterItemClass("ItemNplRobotBlock", ItemNplRobotBlock);

function ItemNplRobotBlock:ctor()
end

function ItemNplRobotBlock:TryCreate(itemStack, entityPlayer, x,y,z, side, data, side_region)
	if (itemStack and itemStack.count == 0) then
		return;
	elseif (entityPlayer and not entityPlayer:CanPlayerEdit(x,y,z, data, itemStack)) then
		return;
	elseif (self:CanPlaceOnSide(x,y,z,side, data, side_region, entityPlayer, itemStack)) then
		NPL.load("(gl)script/apps/Aries/Creator/Game/Items/ItemClient.lua");
		local ItemClient = commonlib.gettable("MyCompany.Aries.Game.Items.ItemClient");
		local names = commonlib.gettable("MyCompany.Aries.Game.block_types.names");
		local item = ItemClient.GetItem(names.CodeBlock);
		if(item) then
			NPL.load("(gl)script/apps/Aries/Creator/Game/Items/ItemStack.lua");
			local ItemStack = commonlib.gettable("MyCompany.Aries.Game.Items.ItemStack");
			local item_stack = ItemStack:new():Init(names.CodeBlock, 1);
			item_stack:SetDataField("langConfigFile", "npl_microbit");
			item_stack:SetDataField("codeLanguageType", "python");

			-- add purple color to the code block using 8bit color data
			local color8_data = 0xe000; 
			return item:TryCreate(item_stack, entityPlayer, x,y,z, side, (data or 0)+color8_data, side_region);
		end
	end
end
