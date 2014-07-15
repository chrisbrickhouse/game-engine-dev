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
local class = require 'middleclass'                            --middleclass module implements classes
local Stateful = require 'stateful'                            --introduces game states
local Game = require 'game'                                    --custom module with gameplay states and classes
local Overlay = require 'overlay'                              --custom module with overlays like dialogue and inventory

local sti = require "sti"                                      --requires the sti module so that Tiled files can be used and parsed.
collisions = require "Collisions"                              --requires the custom Collisions module
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
	local success = {} --this table will contain all success values. eventually it will be used to detect if things actually failed but for now it's just a place to stow those pesky success returns
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
	hero.speed = 2
	tileWidth = 40
	hero.stop = {}
	hero.stop.x = 400
	hero.stop.y = 400
	iterator = 1
	max = 4 --maximum number of frames
	timer = 0
	moving = false
	direction = "down"
	windowWidth, windowHeight = love.graphics.getDimensions()
	translateX,translateY = 0,0
	map:resize(windowWidth, windowHeight)
	game = Game:new()
	overlay = Overlay:new()
end

function love.update(dt)
	if overlay.isActive then --only updates the overlay section if one of the overlays is on
		overlay:update()
	end
	if love.keyboard.isDown("a") then --lets me skip the splash screen and menu
	  	game:gotoState("Play")
	elseif love.keyboard.isDown(" ") then --dialogue testing
		overlay:gotoState("Dialogue")
	end
	game:update(dt) --updates game
end

function love.draw()
	game:draw() --always draws the game layer first
	if overlay.isActive then --only draws the overlay if it's active
		overlay:draw()
	end
end

function love.quit()
	print("Exiting Gracefully...") 
end

function love.keypressed(key)
	if quads[key] and moving == false then 
		moving = true                 
		direction = key
	end
	if key == "escape" then
		love.event.quit()
	end
end
function love.keyreleased(key)
	game:keyreleased(key) --depending on the state, different keys do different things when keys are released. this helps with that
end
