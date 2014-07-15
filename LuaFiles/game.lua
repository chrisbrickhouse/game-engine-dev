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
local Level = require 'level'
local Game = class("Game"):include(Stateful)

function Game:initialize()
	self.loveLogo =  love.graphics.newImage("love-game-logo-256x256.png") --this image distributed under the zlib license
	self.loveWord =  love.graphics.newImage("love-logo-256x128.png")      --this image distributed under the zlib license
	self.ourLogo  =  love.graphics.newImage("fox-pawp-games5-256x478.png")
	self:gotoState("Splash") -- start on the Menu state
end

local Splash = Game:addState("Splash") --adds splash screen state

function Splash:enteredState() -- create buttons, options, etc and store them into self
	print("entering the state splash")
	level = Level:new()
	self.time = 0 --keeps track of time elapsed so logos can be switched
	self.alpha = 0 --holds progressive alphas
end

function Splash:draw() -- draw the menu
	--[[each logo is on screen for ~5 seconds but that's up for change depending on how fast or slow we want it in the final game.
	they fade up for 1 second, fade down for one second, and are at full opacity for 3 seconds in the middle]]
	love.graphics.setColor(255,255,255,self.alpha)
	if self.time <= 4.95 then
		love.graphics.draw(self.loveLogo,windowWidth/2 - 128, windowHeight/2 - 192)
		love.graphics.draw(self.loveWord,windowWidth/2 - 128, windowHeight/2 + 64)
	elseif self.time > 4.95  or self.time > 10 then
		if self.time < 5 then
			love.graphics.setColor(0,0,0,255)
			love.graphics.rectangle("fill", 0 , 0, windowWidth, windowHeight )
		else
			love.graphics.draw(self.ourLogo,windowWidth/2 - 128, windowHeight/2 - 241)
		end
	end
end

function Splash:update(dt) -- update anything that needs updates
	self._alphachange = 255 / ( 1 / dt ) --awesome math right here.
	--print(self.time)--DEBUGGING
	if self.time > 10.05 then
		self:gotoState("Menu") --goes to menu after end of logos
	elseif self.time ~= 10.05 then
		self.time = self.time + dt
	end
	if self.time <= 1 or (self.time > 5 and self.time <= 6) then
		self.alpha = self.alpha + self._alphachange
	elseif (self.time >= 4 and self.time <= 5) or (self.time > 9 and self.time <=10) then
		self.alpha = self.alpha - self._alphachange
	end
end

function Splash:exitedState() -- destroy buttons, options etc here
	print("exiting the splash state")
end

function Splash:keyreleased(key)
end

------------------------------------

local Menu = Game:addState("Menu")

function Menu:enteredState()
	love.graphics.setNewFont(26)
	self.time = 0
	self.currentItem = 'continue' --the item the arrow is currently on
	self.vertices = {windowWidth-200-2, windowHeight/2+15, windowWidth-200-2-26, windowHeight/2, windowWidth-200-2-26, windowHeight/2+30} --an array of the vertices for the arrow. More awesome math to get these numbers
	self.menuItems = {continue = windowHeight/2, newgame = windowHeight/2 + 35, options = windowHeight/2 + 35*2, exit = windowHeight/2 + 35*3} --indexes are the name of the items, values are the y-coords of their respective rectangles
end

function Menu:update(dt)
end

function Menu:draw()
	love.graphics.setColor(255,255,255,255)
	--rectangle backgrounds for the text
	love.graphics.rectangle("fill", windowWidth-200, windowHeight/2, 150,30 )
	love.graphics.rectangle("fill", windowWidth-200, windowHeight/2 + 35, 150,30 )
	love.graphics.rectangle("fill", windowWidth-200, windowHeight/2 + 35*2, 150,30 )
	love.graphics.rectangle("fill", windowWidth-200, windowHeight/2 + 35*3, 150,30 )
	--arrow
	love.graphics.polygon('fill', self.vertices)
	love.graphics.setColor(0,0,0,255)
	--text
	love.graphics.printf("Continue",windowWidth-200, windowHeight/2+2,150,"center")
	love.graphics.printf("New Game",windowWidth-200, windowHeight/2+35+2,150,"center")
	love.graphics.printf("Options",windowWidth-200, windowHeight/2+35*2+2,150,"center")
	love.graphics.printf("Exit",windowWidth-200, windowHeight/2+35*3+2,150,"center")
end

function Menu:exitedState()
end

function Menu:keyreleased(key)
	local missCounter = 0
	if key=='down' or key == 'up' then
		if key == 'down' then
			for i,v in ipairs(self.vertices) do
				if (i%2) == 0 then
					self.vertices[i] = v + 35
				end
			end
		elseif key == 'up' then
			for i,v in ipairs(self.vertices) do
				if (i%2) == 0 then
					self.vertices[i] = v - 35
				end
			end
		end
		for i,v in pairs(self.menuItems) do
			if v ~= self.vertices[4] then
				--this should always equal 3, if it doesn't, we know something is wrong so we don't move the arrow
				missCounter = missCounter + 1
			elseif v == self.vertices[4] then
				self.currentItem = i
			end
		end
		if missCounter > 3 then
			--this is us not moving the arrow/moving it back after having already moved it
			if key == 'down' then
				for i,v in ipairs(self.vertices) do
					if (i%2) == 0 then
						self.vertices[i] = v - 35
					end
				end
			elseif key == 'up' then
				for i,v in ipairs(self.vertices) do
					if (i%2) == 0 then
						self.vertices[i] = v + 35
					end
				end
			end
		end
	elseif key == 'return' then
		--this allows the menu to actually function, except for the fact that they all do the same thing except for exit so eventually it will work but right now it's more POC than anything
		print(self.currentItem)
		if self.currentItem  == 'exit' then
			love.event.quit()
		elseif self.currentItem == 'continue' then
			print("continuing")
			self:gotoState("Play")
		elseif self.currentItem == 'options' then
			print("options")
			self:gotoState("Play")
		elseif self.currentItem == 'newgame' then
			print("making new game")
			level:gotoState("levelOne")
			self:gotoState("Play")
		end
	end
end

----------------------------------

local Play = Game:addState("Play")

function Play:enteredState()
	print("ready to play!")
end

function Play:update(dt)
	--print(hero.x)
--	level:update(dt)
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
	if pass == 1 then
		if mod > 0 then
			if axis == "x" then 
				hero.stop.x = hero.x + (tileWidth - (hero.x%40))
				hero.x = hero.stop.x
			elseif axis == "y" then 
				hero.stop.y = hero.y + (tileWidth - (hero.y%40))
				hero.y = hero.stop.y
				end
		elseif mod < 0 then
			if axis == "x" then 
				hero.stop.x = hero.x - (hero.x%tileWidth)
				hero.x = hero.stop.x
			elseif axis == "y" then	
				hero.stop.y = hero.y - (hero.y%tileWidth)
				hero.y = hero.stop.y
				end
		end
	end
	if axis == "x" then
		if math.ceil(hero.x) ~= hero.stop.x and math.floor(hero.x) ~= hero.stop.x then
			moving = true
			--print(math.floor(hero.x),math.ceil(hero.x),hero.x,hero.stop.x)
			hero.x = hero.x + tileWidth * hero.speed * dt * mod
		elseif (math.ceil(hero.x) == hero.stop.x or math.floor(hero.x) == hero.stop.x) and moving == true then
			print(hero.stop.x,hero.x,hero.stop.y, hero.y,"released 2")
			hero.x = hero.stop.x
			print(hero.stop.x,hero.x,hero.stop.y, hero.y,"released 3")
			--print(math.floor(hero.x),math.ceil(hero.x),hero.x,hero.stop.x)
			moving = false
			iterator = 1
			mod = 0
		end
	elseif axis == "y" then
		if math.ceil(hero.y) ~= hero.stop.y and math.floor(hero.y) ~= hero.stop.y then
			moving = true
			--print(math.floor(hero.y),math.ceil(hero.y),hero.y,hero.stop.y)
			hero.y = hero.y + tileWidth * hero.speed * dt * mod
		elseif (math.ceil(hero.y) == hero.stop.y or math.floor(hero.y) == hero.stop.y) and moving == true then
			print(hero.stop.x,hero.x,hero.stop.y, hero.y,"released 4")
			hero.y = hero.stop.y
			print(hero.stop.x,hero.x,hero.stop.y, hero.y,"released 5")
			--print(math.floor(hero.y),math.ceil(hero.y),hero.y,hero.stop.y)
			moving = false
			iterator = 1
			mod = 0
		end
	end
	if love.keyboard.isDown("left","right","up","down") or pass == 1 then
	--[[ This sections runs if a directional key is pressed OR if the hero has collided with something.
	The way it works is such: if the hero collided, it modifies the mod so that it bounces back at a rate
	5x further than normal. Regardless of collision, it then checks to see if movement is in the x or y axis
	then moves the hero the correct amount in those directions. Finally, if the hero had collided, it stops
	him/her from moving, resets the mod to the value it had before, then resets the pass value.]]
		--print(mod,direction) --DEBUGGING
		moving = true
		mod,axis = movementModifier()
		--print(hero.stop.x,hero.stop.y,hero.y,mod,"ln 236",pass)
		if pass == 1 then
			if mod > 0 then
				if axis == "x" then hero.stop.x = hero.x + (tileWidth - (hero.x%40))
				elseif axis == "y" then hero.stop.y = hero.y + (tileWidth - (hero.y%40)) end
			elseif mod < 0 then
				if axis == "x" then hero.stop.x = hero.x - (hero.x%tileWidth)
				elseif axis == "y" then hero.stop.y = hero.y - (hero.y%tileWidth) end
			end
		end
		--print(hero.stop.x,hero.stop.y,hero.y,mod,"ln 241",pass)
		if axis == "x" then
			if math.floor(hero.x) == hero.stop.x or math.ceil(hero.x) == hero.stop.x then
				if mod > 0 then hero.stop.x = hero.x + (tileWidth - (hero.x%40)) + tileWidth
				elseif mod < 0 then hero.stop.x = hero.x - (hero.x%tileWidth) - tileWidth end
				--hero.stop.x = hero.stop.x + tileWidth * mod
			end
		elseif axis == "y" then
			if math.floor(hero.y) == hero.stop.y then
				if mod > 0 then hero.stop.y = hero.y + (tileWidth - (hero.y%40)) + tileWidth
				elseif mod < 0 then hero.stop.y = hero.y - (hero.y%tileWidth) - tileWidth end
				--hero.stop.y = hero.stop.y + tileWidth * mod
			end
		end
		if pass == 0.5 then
			moving = false
			mod = 0
			pass = 0
		end
	end
end

function Play:draw()
	love.graphics.translate(translateX,translateY)
	map:setDrawRange(translateX,translateY,windowWidth,windowHeight)
	map:draw()
	--level:draw()
	love.graphics.draw(sprite, quads[direction][iterator], hero.x, hero.y)
	--print(translateX) --DEBUGGING
	--map:drawCollisionMap(collisionMap) --DEBUGGING
end

function Play:keyreleased(key)
	if quads[key] and direction == key and math.ceil(hero.x) == hero.stop.x then -- only stop moving if we're still moving in only that direction. (Geocine comment)
		--print("why is this executing?")
		moving = false
		iterator = 1--[[
	elseif axis == "x" and math.floor(hero.x) ~= hero.stop.x then
		hero.x = hero.x + (hero.x-hero.stop.x) * deltaT * mod
	elseif axis == "y" then
		hero.y = hero.y + hero.speed * mod * deltaT
	elseif quads[key] and direction == key and math.floor(hero.x) == hero.stop.x then
		mod = 0]]
	end
	if quads[key] and direction == key then
		print(hero.stop.x,hero.x,hero.stop.y, hero.y,"released 0")
		if mod > 0 then
			if axis == "x" then hero.stop.x = hero.x + (tileWidth - (hero.x%40))
			elseif axis == "y" then hero.stop.y = hero.y + (tileWidth - (hero.y%40)) end
		elseif mod < 0 then
			if axis == "x" then hero.stop.x = hero.x - (hero.x%tileWidth)
			elseif axis == "y" then hero.stop.y = hero.y - (hero.y%tileWidth) end
		end
		print(hero.stop.x,hero.x,hero.stop.y, hero.y,"released 1")
	end
	if key == "c" then
		print("ALERT")
	end
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
	--[[ RETURNS: mod - mod: the moifier for the movement functions
	I'm still not 100% on what I was thinking when I wrote this because I've forgotten for the most part how
	this works but I'm pretty sure it's just an advanced version of the standard collision logic but there's no
	bounce back and it manages to move the screen.]]
	if (hero.x + 40) >= (-1*translateX + windowWidth - 50) then
		translateX = translateX + -tileWidth*hero.speed*deltaT
	elseif hero.x <= -1*translateX + 50 then
		translateX = translateX + tileWidth*hero.speed*deltaT
	elseif (hero.y + 40) >= (-1*translateY + windowHeight - 50) then
		translateY = translateY + -tileWidth*hero.speed*deltaT
	elseif hero.y <= -1*translateY + 50 then
		translateY = translateY + tileWidth*hero.speed*deltaT
	end
	return mod
end

return Game
