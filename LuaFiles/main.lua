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
local sti = require "sti"                                      --requires the sti module so that Tiled files can be used and parsed.
local collisions = require "Collisions"                        --requires the custom Collisions module
local Quad = love.graphics.newQuad                             --quad module for using sprite sheets
function love.load()
	pass = 0                                               --this variable tells whether the hero has collided (1) or not (0)
	map = sti.new("level1")                                --loads the first level map
	collisionMap = map:getCollisionMap("Tile Layer 3")     --loads the layer to use for collision (must be tile layer, not object)
	modes = love.window.getFullscreenModes()
	table.sort(modes, function(a, b) return a.width*a.height > b.width*b.height end)   -- sort from largest to smallest
	--[[for i,v in ipairs(modes) do
		print(modes[i]["width"])
	end]]
	local success = {}
	table.insert(success, love.window.setMode( modes[1]["width"] , modes[1]["height"]))
	table.insert(success, love.window.setFullscreen( true , "desktop"))
	--[[for k,v in pairs(collisionMap["data"]) do
		--DEBUGGING FUNCTION
		print(k,",",v)
	end]]
	sprite = love.graphics.newImage("SpriteDev/spritesheet.png") --Loads Spritesheet
	quads = {
		--[[
		This lovely table, and the method of implementing spritesheet animation handling is
		adapted from the example SpriteAnimation by geocine. It can be found here: 
		https://github.com/geocine/lua2d-examples/blob/master/SpriteAnimation/main.lua
		]]
		left = {
			Quad( 0,   0, 40, 40, 160, 160);
			Quad(40,   0, 40, 40, 160, 160);
			Quad(80,   0, 40, 40, 160, 160);
			Quad(120,  0, 40, 40, 160, 160);
		};
		up = {
			Quad( 0,   40, 40, 40, 160, 160);
			Quad(40,   40, 40, 40, 160, 160);
			Quad(80,   40, 40, 40, 160, 160);
			Quad(120,  40, 40, 40, 160, 160);
		};
		right = {
			Quad( 0,   80, 40, 40, 160, 160);
			Quad(40,   80, 40, 40, 160, 160);
			Quad(80,   80, 40, 40, 160, 160);
			Quad(120,  80, 40, 40, 160, 160);
		};
		down = {
			Quad( 0,   120, 40, 40, 160, 160);
			Quad(40,   120, 40, 40, 160, 160);
			Quad(80,   120, 40, 40, 160, 160);
			Quad(120,  120, 40, 40, 160, 160);
		};
	}
	hero = {}					       --this table holds data on the user controled character
	hero.x = 400
	hero.y = 400
	hero.speed = 100
	iterator = 1
	max = 4 --maximum number of frames
	timer = 0
	moving = false
	direction = "down"
	windowWidth, windowHeight = love.graphics.getDimensions()
	translateX,translateY = 0,0
	map:resize(windowWidth, windowHeight)
end

function love.update(dt)
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

function love.draw()
	love.graphics.translate(translateX,translateY)
	map:setDrawRange(translateX,translateY,windowWidth,windowHeight)
	map:draw()
	love.graphics.draw(sprite, quads[direction][iterator], hero.x, hero.y)
	--print(translateX) --DEBUGGING
	--map:drawCollisionMap(collisionMap) --DEBUGGING
end

function love.quit()
	print("Exiting Gracefully...")
end

function love.keypressed(key)
	if quads[key] and moving == false then -- this is really ugly. Don't do it like this in your final game (Geocine comment)
		moving = true                  -- DON'T TELL ME HOW TO LIVE MY LIFE (my comment)
		direction = key
	end
	if key == "escape" then
		love.event.quit()
	end
end
function love.keyreleased(key)
	if quads[key] and direction == key then -- only stop moving if we're still moving in only that direction. (Geocine comment)
		moving = false
		iterator = 1
	end
	if key == "left" or key == "up" and mod == 0 then
		mod = 1
	elseif key == "down" or key == "right" and mod == 0 then
		mod = -1
	end
	if axis == "x" then
		hero.x = hero.x + hero.speed * mod * deltaT
	elseif axis == "y" then
		hero.y = hero.y + hero.speed * mod * deltaT
	end
	mod = 0
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
