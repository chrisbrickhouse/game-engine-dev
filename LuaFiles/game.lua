local class = require 'middleclass'
local Stateful = require 'stateful'
local Game = class("Game"):include(Stateful)

function Game:initialize()
	self.image =  love.graphics.newImage("houseobsticle.png")
	self:gotoState("Menu") -- start on the Menu state
end

local Menu = Game:addState("Menu")

function Menu:enteredState() -- create buttons, options, etc and store them into self
	print("entering the state menu")
end

function Menu:draw() -- draw the menu
	love.graphics.draw(self.image,0,0)
end

function Menu:update(dt) -- update anything that needs updates
end

function Menu:exitedState() -- destroy buttons, options etc here
	print("exiting the menu state")
end

local Play = Game:addState("Play")

function Play:enteredState()
	print("ready to play!")
end

function Play:update(dt)
	--print(hero.x)
	deltaT = dt
	pass = collisions.detection(collisionMap)              --calls the collision detection function to see if the hero collided
	map:update(dt)                                         --updates the map
	if moving then
	--this if statement, also from the geocine example, delays the changing of the sprite frame by .2 seconds
		timer = timer + dt
		if timer > 0.2 then
			timer = 0
			iterator = iterator + 1
			if iterator > max then
				iterator = 1
			end
		end
	end
	mod,axis = movementModifier()                          --see function documentation
	mod = mapScrollingDetect(mod)
	if love.keyboard.isDown("left","right","up","down") or pass == 1 then
	--[[ This sections runs if a directional key is pressed OR if the hero has collided with something.
	The way it works is such: if the hero collided, it modifies the mod so that it bounces back at a rate
	5x further than normal. Regardless of collision, it then checks to see if movement is in the x or y axis
	then moves the hero the correct amount in those directions. Finally, if the hero had collided, it stops
	him/her from moving, resets the mod to the value it had before, then resets the pass value.]]
		--print(mod,direction) --DEBUGGING
		if pass == 1 then
			mod = mod * -5
			pass = 0.5
		end
		if axis == "x" then
			hero.x = hero.x + hero.speed * mod * dt
		elseif axis == "y" then
			hero.y = hero.y + hero.speed * mod * dt
		end
		if pass == 0.5 then
			moving = false
			mod = mod / -5
			pass = 0
		end
	end
end

function Play:draw()
	love.graphics.translate(translateX,translateY)
	map:setDrawRange(translateX,translateY,windowWidth,windowHeight)
	map:draw()
	love.graphics.draw(sprite, quads[direction][iterator], hero.x, hero.y)
	--print(translateX) --DEBUGGING
	--map:drawCollisionMap(collisionMap) --DEBUGGING
end

function movementModifier()
	--[[ RETURNS: mod, axis - mod: the moifier for the movement functions, axis: the axis along which to move
	This fixes the problem of animations and movement going wonky if more than one directional key is pressed
	at a time. It allows a single movement function for each axis an uses a modifier which tells it which direction
	along the access to go.
	]]
	if direction == "left" and moving == true then
		mod = -1
		axis = "x"
	elseif direction == "right" and moving == true then
		mod = 1
		axis = "x"
	elseif direction == "up" and moving == true then
		mod = -1
		axis = "y"
	elseif direction == "down" and moving == true then
		mod = 1
		axis = "y"
	end
	return mod,axis
end

function mapScrollingDetect(mod)
	if (hero.x + 40) >= (-1*translateX + windowWidth - 50) then
		translateX = translateX + -1*hero.speed*deltaT
	elseif hero.x <= -1*translateX + 50 then
		translateX = translateX + hero.speed*deltaT
	elseif (hero.y + 40) >= (-1*translateY + windowHeight - 50) then
		translateY = translateY + -1*hero.speed*deltaT
	elseif hero.y <= -1*translateY + 50 then
		translateY = translateY + hero.speed*deltaT
	end
	return mod
end

return Game