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
