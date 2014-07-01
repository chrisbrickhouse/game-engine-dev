local class = require 'middleclass'
local Stateful = require 'stateful'
local Game = require 'game'
local Overlay = require 'overlay'

local sti = require "sti"                                      --requires the sti module so that Tiled files can be used and parsed.
collisions = require "Collisions"                        --requires the custom Collisions module
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
	game = Game:new()
	overlay = Overlay:new()
end

function love.update(dt)
	if overlay.isActive then
		overlay:update()
	end
	if love.keyboard.isDown("a") then
	  	game:gotoState("Play")
	elseif love.keyboard.isDown(" ") then
		overlay:gotoState("Dialogue")
	end
	game:update(dt)
end

function love.draw()
	game:draw()
	if overlay.isActive then
		overlay:draw()
	end
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
