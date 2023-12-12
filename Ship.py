#!/usr/bin/env python #
"""
	Ship Object
	- Stores Object data for each Ship
	- Determines if a Ship has been sunk

	ShipYard Object
	- Stores Object data for each ShipYard
	- Initializes 5 classic ships for the game Battleship
	- Has a master list of Ship locations for easy query
"""

class Ship():
	def __init__(self, name, length) :
		self.Name = name
		self.Length = length
		self.Horizontal = True
		self.Location = []
		self.Hits = 0

	def Change_Orientation(self) :
		self.Horizontal = not self.Horizontal

	def Ship_Hit(self) :
		self.Hits += 1

	def Ship_Sunk(self) :
		if self.Hits == self.Length :
			return True
		return False

class ShipYard() :
	def __init__(self, owner) :
		self.Owner = owner
		self.ShipList = [		Ship("Carrier", 5), 
								Ship("Battleship", 4), 
								Ship("Submarine", 3), 
								Ship("Cruiser", 3),
								Ship("Destroyer", 2)	]
		self.ShipLocations = []