--[[
	Copyright (c) 2014 Christian Brickhouse

	This program is free software: you can redistribute it and/or modify
	it under the terms of the GNU General Public License as published by
	the Free Software Foundation, either version 2 of the License, or
	(at your option) any later version.

	This program is distributed in the hope that it will be useful,
	but WITHOUT ANY WARRANTY; without even the implied warranty of
	MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
	GNU General Public License for more details.

	You should have received a copy of the GNU General Public License
	along with this program.  If not, see <http://www.gnu.org/licenses/>.
]]
local class = require 'middleclass'
local Stateful = require 'stateful'
local Overlay = class("Overlay"):include(Stateful)

function Overlay:initialize()
	self.isActive = false
end

local Dialogue = Overlay:addState("Dialogue")

function Dialogue:enteredState() -- create buttons, options, etc and store them into self
	love.graphics.setNewFont(20)
	self.isActive = true
	print("entering the Dialogue state")
end

function Dialogue:draw() -- draw the menu
	love.graphics.printf("This is how dialogue works. It also convenitently self wraps after reaching 800 pixels which you can see from this lovely example here.", windowWidth/2 - 400, windowHeight/2, 800) --text, x, y, width, (not shown) allignment
end

function Dialogue:update(dt) -- update anything that needs updates
end

function Dialogue:exitedState() -- destroy buttons, options etc here
	print("exiting the Dialogue state")
	self.isActive = false
end

local Inventory = Overlay:addState("Inventory")

function Inventory:enteredState()
	self.isActive = true
	print("entering the Inventory state")
end

function Inventory:update(dt)
end

function Inventory:draw()

end

function Inventory:exitedState()
	print("exiting the Inventory state")
	self.isActive = false
end

return Overlay
