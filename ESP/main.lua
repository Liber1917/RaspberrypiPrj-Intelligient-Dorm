
-- LuaTools需要PROJECT和VERSION这两个信息
PROJECT = "bledemo"
VERSION = "1.0.0"

--[[
BLE peripheral的demo, 等待被连接的设备
支持的模块:
1. Air101/Air103, 开发板的BLE天线未引出, 需要靠近使用, 且功耗高
2. ESP32系列, 包括ESP32C3/ESP32S3

-- 配合微信小程序 "LuatOS蓝牙调试"
-- 1. 若开发板无天线, 将手机尽量靠近芯片也能搜到
-- 2. 该小程序是开源的, 每次write会自动分包
-- https://gitee.com/openLuat/luatos-miniapps
]]

log.info("main", PROJECT, VERSION)

-- 一定要添加sys.lua !!!!
sys = require("sys")

--添加硬狗防止程序卡死
if wdt then
    wdt.init(9000)--初始化watchdog设置为9s
    sys.timerLoopStart(wdt.feed, 3000)--3s喂一次狗
end

-- 监听GATT服务器的WRITE_CHR, 也就是收取数据的回调
sys.subscribe("BLE_GATT_WRITE_CHR", function(info, data)
    -- info 是个table, 但当前没有数据
    log.info("ble", "data got!!", data:toHex())
end)

local rtos_bsp = rtos.bsp()
function pinx() -- 根据不同开发板，给LED赋值不同的gpio引脚编号
    if rtos_bsp == "AIR101" then -- Air101开发板LED引脚编号
        return pin.PB08, pin.PB09, pin.PB10
    elseif rtos_bsp == "AIR103" then -- Air103开发板LED引脚编号
        return pin.PB26, pin.PB25, pin.PB24
    elseif rtos_bsp == "AIR601" then -- Air103开发板LED引脚编号
        return pin.PA7, 255, 255
    elseif rtos_bsp == "AIR105" then -- Air105开发板LED引脚编号
        return pin.PD14, pin.PD15, pin.PC3
    elseif rtos_bsp == "ESP32C3" then -- ESP32C3开发板的引脚
        return 12, 13, 255 -- 开发板上就2个灯
    elseif rtos_bsp == "ESP32S3" then -- ESP32C3开发板的引脚
        return 10, 11, 255 -- 开发板上就2个灯
    elseif rtos_bsp == "EC618" then -- Air780E开发板引脚
        return 27, 255, 255 -- AIR780E开发板上就一个灯
    elseif rtos_bsp == "UIS8850BM" then -- Air780UM开发板引脚
        return 36, 255, 255 -- Air780UM开发板上就一个灯
    else
        log.info("main", "define led pin in main.lua")
        return 0, 0, 0
    end
end


--LED引脚判断赋值结束

local P1,P2,P3=pinx()--赋值开发板LED引脚编号
local LEDA= gpio.setup(P1, 0, gpio.PULLUP)
local LEDB= gpio.setup(P2, 0, gpio.PULLUP)
local LEDC= gpio.setup(P3, 0, gpio.PULLUP)


sys.taskInit(function()
    sys.wait(2000)

    -- BLE模式, 默认是SERVER/Peripheral,即外设模式, 等待被连接的设
    -- nimble.mode(nimble.MODE_BLE_SERVER) -- 默认就是它, 不用调用

    -- 设置SERVER/Peripheral模式下的UUID, 支持设置3个
    -- 地址支持 2/4/16字节, 需要二进制数据, 例如 string.fromHex("AABB") 返回的是2个字节数据,0xAABB
    if nimble.setUUID then -- 2023-02-25之后编译的固件支持本API
        nimble.setUUID("srv", string.fromHex("380D"))      -- 服务主UUID         ,  默认值 180D
        nimble.setUUID("write", string.fromHex("FF31"))    -- 往本设备写数据的UUID,  默认值 FFF1
        nimble.setUUID("indicate", string.fromHex("FF32")) -- 订阅本设备的数据的UUID,默认值 FFF2
    end

    -- 可以自定义名称
    -- nimble.init("LuatOS-Wendal") -- 蓝牙名称可修改,也有默认值LOS-$mac地址
    nimble.init(LED) -- 蓝牙名称可修改,也有默认值LOS-$mac地址

    sys.wait(500)
    -- 打印MAC地址
    local mac = nimble.mac()
    log.info("ble", "mac", mac and mac:toHex() or "Unknwn")

    -- 发送数据
    while 1 do
        sys.wait(3000)
        nimble.send_msg(1, 0, string.char(0x5A, 0xA5, 0x12, 0x34, 0x56))
    end
end)

-- 用户代码已结束---------------------------------------------
-- 结尾总是这一句
sys.run()
-- sys.run()之后后面不要加任何语句!!!!!
