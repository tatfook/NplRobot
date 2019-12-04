--[[
Title: NplRobotHelper
Author(s): leio
Date: 2019/12/4
Desc: 
use the lib:
------------------------------------------------------------
local NplRobotHelper = NPL.load("(gl)Mod/NplRobot/NplRobotHelper.lua");
NplRobotHelper.WriteFile("test/test.hex",NplRobotHelper.CombineHex(NplRobotHelper.TempCodes()));
NplRobotHelper.WriteFile("test/test.py",NplRobotHelper.CombineScripts(NplRobotHelper.TempCodes()));
-------------------------------------------------------
]]
NPL.load("(gl)script/ide/math/bit.lua");

local NplRobotHelper = NPL.export();

function NplRobotHelper.TempCodes2()
    local s = [[
angle = None


angle = 0
]]
    return s
end
function NplRobotHelper.TempCodes()
    local s = [[
angle = None
angle = 0
servo(7, angle)
microbit.display.show(GetImage("1110000100001000010000111"))
while True:
  if microbit.button_a.is_pressed():
    angle = ((angle) + (1))
    if ((angle) > (180)):
      angle = 180

    servo(7, angle)

  if ((microbit.button_a.is_pressed()) and (microbit.button_b.is_pressed())):
    angle = 0
    servo(7, angle)
    microbit.display.show(GetImage("1111100100001000010000100"))
]]
    return s
end
function NplRobotHelper.find_uicr_line(arr)
    for k,v in ipairs(arr) do
        if(string.match(v,":020000041000EA"))then
            return k;
        end
    end
end

function NplRobotHelper.CombineScripts(script)
    local header = NplRobotHelper.ReadFile("Mod/NplRobot/HexHeader.py");
    local s = string.format("%s\n%s",header,script);
    return s;
end
function NplRobotHelper.CombineHex(script)
    script = script or "";
    local firmware_arr = NplRobotHelper.SplitStr(NplRobotHelper.ReadFile("Mod/NplRobot/firmware.hex"));
    local index = NplRobotHelper.find_uicr_line(firmware_arr);

    script = NplRobotHelper.CombineScripts(script);
    local hexfile_arr = NplRobotHelper.HexlifyScript(script);
    local output = {};
    for k = 1,(index-1) do
        table.insert(output,firmware_arr[k] .. "\n");
    end
    for k,v in ipairs(hexfile_arr) do
        table.insert(output,hexfile_arr[k] .. "\n");
    end
    for k = index,#firmware_arr do
        table.insert(output,firmware_arr[k] .. "\n");
    end
    return table.concat(output);
end
function NplRobotHelper.hexlify_internal(arr)
    local result = "";
    for k,v in ipairs(arr) do
        if(arr[k] < 16)then
            result = result .. "0"
        end

        result = result .. mathlib.bit.Dec2Hex(arr[k]);
    end
    return result;
end
function NplRobotHelper.HexlifyScript(script)
    script = script or "";
    local len_script = string.len(script);
    -- add header, pad to multiple of 16 bytes
    local data = {};
    local data_len = 4 + len_script + (16 - math.mod(4 + len_script, 16));
    data = NplRobotHelper.FillTable(data,data_len,0);
    data[1] = 77; -- 'M'
    data[2] = 80; -- 'P'
    data[3] = mathlib.bit.band(len_script, 0xff)
    data[4] = mathlib.bit.band(mathlib.bit.rshift(len_script, 8),0xff);
    for i = 1, len_script do
        local char_code = string.byte(script,i);
        data[4+i] = char_code;
    end
    --TODO check data.length < 0x2000
    -- convert to .hex format
    local addr = 0x3e000; -- magic start address in flash
    local chunk_len = 5 + 16;
    local chunk = {};
    chunk = NplRobotHelper.FillTable(chunk,chunk_len,0);
    local output = {};
    table.insert(output,":020000040003F7"); -- extended linear address, 0x0003
    for i = 1, data_len, 16 do
        chunk[1] = 16; -- length of data section
        chunk[2] = mathlib.bit.band(mathlib.bit.rshift(addr, 8),0xff); -- high byte of 16-bit addr
        chunk[3] = mathlib.bit.band(addr, 0xff); -- low byte of 16-bit addr
        chunk[4] = 0; -- type (data)
        for j = 1,16 do
            chunk[4 + j] = data[i + j - 1];
        end
        local checksum = 0;
        for j = 1, (4+16) do
            checksum = checksum + chunk[j];
        end
        chunk[4 + 16 + 1] = mathlib.bit.band(-checksum, 0xff);

        local v = NplRobotHelper.hexlify_internal(chunk);
        v = string.upper(v);
        table.insert(output, ":" .. v);

        addr = addr + 16
    end
    return output;
end
function NplRobotHelper.ReadFile(filename)
	local file = ParaIO.open(filename,"r");
    if(file:IsValid()) then
        local txt = file:GetText();
        file:close();
        return txt;
    end
    
end

function NplRobotHelper.WriteFile(filename,s)
    if(not s)then
       return 
    end
    local file = ParaIO.open(filename,"w");
    if(file:IsValid()) then
        file:write(s,#s);
        file:close();
    end
end
function NplRobotHelper.FillTable(arr,len,v)
    for k =1,len do
        table.insert(arr,v);
    end
    return arr;
end
function NplRobotHelper.SplitStr(s)
    if(not s)then
        return {}
    end
    local arr = {};
    for line in string.gfind(s, "[^\r\n]+") do
        table.insert(arr,line);
    end
    return arr;
end