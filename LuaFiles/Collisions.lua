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
local Collisions = {}

function Collisions.detection(collisionMap)
	--[[ RETURNS: passArg - passArg: boolean value as to whether the hero collided or not.
	This function detects whether the hero has collided with an object on the map or not. 
	It will eventually be modified so that any moving character can be passed to
	it and have a collision detected, but for now, it's just the hero.
	]]
	local passArg = 0
	--[[if counter == nil then
		--DEBUGGING
		counter = 0
	end]]
	local Left = math.floor(hero.x / 40) + 1
	local Top = math.floor(hero.y / 40) + 1                --These create the four edges of the hero
	local Right = math.floor((hero.x + 40) / 40) + 1
	local Bottom = math.floor((hero.y + 40) / 40) + 1
	local combos = {{Top,Bottom},{Left,Right}}             --This table holds the top/bottom and left/right edge values
	--print(heroLine,heroColumn) --DEBUGGING
	for TB = 1,2 do                                        --runs through for the top, then the bottom
		for LR = 1,2 do                                --runs through for the left, then the right
			if collisionMap["data"][combos[1][TB]][combos[2][LR]] == 1 then
			--[[this runs through all the combinations of topleft,topright,bottomleft,bottomright and makes sure
			that no part of the hero is colliding.]]
			--[[	print("collide!",counter) --DEBUGGING
				counter = counter + 1]]
				passArg = 1
			end
		end
	end
	return passArg
end

return Collisions
