#!/usr/bin/env python #
"""
	Enemy
	- Place Enemy Ships Randomly
	- Tracks Player Activity
	- Randomly chooses a spot to go, until a ship is found and prioritized to sink

	Current Bugs :
		Try location out of bounds - need to fix function Find_Priority_Location
"""

from Ship import ShipYard
from Window import Display
import tkinter
from random import randint 
from random import getrandbits

class Enemy():
	def __init__(self, Display, GamePlayer) :
		self.ShipYard = ShipYard("Enemy")
		self.ShipIndex = 0
		self.Hits = 0
		self.ButtonList = Display.EnemyFrame.ButtonList
		self.Display = Display
		self.GamePlayer = GamePlayer
		self.Locations_Used = []
		self.Priority = False
		self.PriorityShip = None
		self.PriorityShipLocation = []
		self.PriorityShipDirection = None
		self.CheckDirection = "Right"
		self.LastLocationOfShip = None
		
		while self.ShipIndex < 5 :
			if self.Place_Ship(self.ShipYard.ShipList[self.ShipIndex]) == True :
				self.ShipIndex = self.ShipIndex + 1

		# Activate button list for enemy
		for x in range(10) :
			for y in range(10) :
				self.ButtonList[x][y].config(command = lambda x=x, y=y : self.Hit_Miss(x, y))

	def Place_Ship(self, CurrentShip) :
		# Get the first location for the ship
		BaseLocation = [randint(0, 9-CurrentShip.Length), randint(0, 9-CurrentShip.Length)]

		# Add this location to the current ship
		CurrentShip.Location = [BaseLocation]

		# Get a random number for the horizontal bool
		CurrentShip.Horizontal = getrandbits(1)

		# If the location is valid, move to the next ship, otherwise redo this ship
		if self.Valid_Ship_Location(CurrentShip, BaseLocation) :
			self.ShipIndex = self.ShipIndex + 1
			self.Change_Button_Text(CurrentShip.Location) # DEBUG
		
	def Valid_Ship_Location(self, CurrentShip, BaseLocation) :
		# If the first location exists in all locations, return false
		if BaseLocation in self.ShipYard.ShipLocations : return False

		# The current location is the first location
		CurrentLocation = BaseLocation

		if CurrentShip.Horizontal == True : # Ship is horizontal
			for x in range(1, CurrentShip.Length) :
				CurrentLocation = [CurrentLocation[0]+1, CurrentLocation[1]]
				if CurrentLocation in self.ShipYard.ShipLocations :
					return False
				CurrentShip.Location.append(CurrentLocation)
		else : # Ship is vertical
			for x in range(1, CurrentShip.Length) :
				CurrentLocation = [CurrentLocation[0], CurrentLocation[1]+1]
				if CurrentLocation in self.ShipYard.ShipLocations :
					return False
				CurrentShip.Location.append(CurrentLocation)
		self.ShipYard.ShipLocations.extend(CurrentShip.Location)
		return True

	# DEBUG - Change O to X to track where the enemy put the ships
	def Change_Button_Text(self, ShipLocation) :
		for location in ShipLocation :
			self.ButtonList[location[0]][location[1]].config(text = "X")

	def Hit_Miss(self, x, y) :
		# If it is a hit
		if [x, y] in self.ShipYard.ShipLocations :
			self.GamePlayer.Hits = self.GamePlayer.Hits + 1
			self.Display.PlayerFrame.HitText.set("Hits: " + str(self.GamePlayer.Hits)) # Update displayed hit number
			
			# Necessary to find the ship that is sunk to append text and track ship
			for ship in self.ShipYard.ShipList : # Find the ship
				for coordinates in ship.Location : # Find the coordinates
					if coordinates == [x, y] : # If they match, change hit count
						# Change button color to red
						self.ButtonList[x][y].config(state = "disable", bg = "red")
						ship.Ship_Hit()

						# Check to see if the ship is sunk
						if ship.Ship_Sunk() == True : self.Display.PlayerFrame.SunkText.set(self.Display.PlayerFrame.SunkText.get() + "\n" + ship.Name + " Sunk")
						break

			# Player Won!
			if self.GamePlayer.Hits >= 17 : 
				self.Display.MessageText.set("Winner is... Player!")
				self.Display.PlayerFrame.Change_Buttons_States("disable")
				self.Display.EnemyFrame.Change_Buttons_States("disable")

		else: # It was a miss
			#disable the button and change color to white
			self.ButtonList[x][y].config(state = "disable", bg = "white")

		# Take enemy turn
		self.Take_Enemy_Turn()

	# When the enemy gets a hit, it prioritizes that ship. Once the ship is sunk, it returns to this function to reset values
	def Reset_Priority_Ship(self) :
		self.Priority = False
		self.PriorityShip = None
		self.PriorityShipLocation = []
		self.PriorityShipDirection = None
		self.CheckDirection = "Right"
		self.LastLocationOfShip = None


	# Flip directions - used after the enemy determines the direction of a priority ship and misses without sinking the ship
	def Flip_Directions(self, Direction) :
		if Direction == "Right" : Direction = "Left"
		elif Direction == "Left" : Direction = "Right"
		elif Direction == "Up" : Direction = "Down"
		else : Direction = "Up"
		return Direction
	
	# Rotate directions in a counter clockwise manner
	def Rotate_Directions(self, Direction) :
		if self.CheckDirection == "Right" :
			self.CheckDirection = "Up"
		elif self.CheckDirection == "Up" :
			self.CheckDirection = "Left" 
		elif self.CheckDirection == "Left" :
			self.CheckDirection = "Down"
		else :
			self.CheckDirection = "Right"
		return Direction

	def Find_Priority_Location(self) :
		TryThis = [] # Clear out any previous location to ensure no incorrect data slips through

		while (TryThis in self.Locations_Used or TryThis is None): 
			if self.PriorityShipDirection is None : # Haven't found the direction of the ship yet
				if self.CheckDirection == "Right" : TryThis = [self.LastLocationOfShip[0]+1, self.LastLocationOfShip[1]]
				elif self.CheckDirection == "Left" : TryThis = [self.LastLocationOfShip[0]-1, self.LastLocationOfShip[1]]
				elif self.CheckDirection == "Up" : TryThis = [self.LastLocationOfShip[0], self.LastLocationOfShip[1]-1]
				elif self.CheckDirection == "Down" : TryThis = [self.LastLocationOfShip[0], self.LastLocationOfShip[1]+1]
				
			else : # Self.PriorityShipDirection is not None - means we have found the direction of the ship already
				if self.PriorityShipDirection == "Right" : TryThis = [self.LastLocationOfShip[0]+1, self.LastLocationOfShip[1]]
				elif self.PriorityShipDirection == "Left" : TryThis = [self.LastLocationOfShip[0]-1, self.LastLocationOfShip[1]]
				elif self.PriorityShipDirection == "Up" : TryThis = [self.LastLocationOfShip[0], self.LastLocationOfShip[1]-1]
				elif self.PriorityShipDirection == "Down" : TryThis = [self.LastLocationOfShip[0], self.LastLocationOfShip[1]+1]

		return TryThis

	def Take_Enemy_Turn(self) :
		if self.Priority == True :
			TryLocation = self.Find_Priority_Location()

			# Add location to list of locations already used
			self.Locations_Used.append(TryLocation)

			# If hit, turn button red, else turn button white
			if TryLocation in self.GamePlayer.ShipYard.ShipLocations :
				self.Hits += 1
				self.Display.EnemyFrame.HitText.set("Hits: " + str(self.Hits))
				
				self.Display.PlayerFrame.ButtonList[TryLocation[0]][TryLocation[1]].config(bg = "Red")
				self.PriorityShipDirection = self.CheckDirection
				self.PriorityShip.Ship_Hit()
				self.PriorityShipLocation.append(TryLocation)
				self.LastLocationOfShip = TryLocation

				# Check to see if the ship is sunk
				if self.PriorityShip.Ship_Sunk() == True :
					self.Display.EnemyFrame.SunkText.set(self.Display.EnemyFrame.SunkText.get() + "\n" + self.PriorityShip.Name + " Sunk")
					self.Reset_Priority_Ship()
					self.Priority = False
				

			else : # Miss
				self.Display.PlayerFrame.ButtonList[TryLocation[0]][TryLocation[1]].config(bg = "White")
				# If direction has already been determined, flip direction
				if self.PriorityShipDirection is not None :
					# Change last location of ship to first location of ship
					self.LastLocationOfShip = self.PriorityShipLocation[0]
					# Flip direction of search
					self.PriorityShipDirection = self.Flip_Directions(self.PriorityShipDirection)
				else : # Self.PriorityShipDirection is None
					self.CheckDirection = self.Rotate_Directions(self.CheckDirection)

		else : # Priority is False
			# Find random location
			TryLocation = [randint(0, 9), randint(0, 9)]

			# If it has already been used, try again
			while TryLocation in self.Locations_Used :
				TryLocation = [randint(0, 9), randint(0, 9)]

			# Add this location to the locations used so far
			self.Locations_Used.append(TryLocation)

			# Change button color of player frame to see where its hitting
			self.Display.PlayerFrame.ButtonList[TryLocation[0]][TryLocation[1]].config(bg = "White")

			# Miss - if the location is not in the shipyard, don't attempt loops
			if TryLocation not in self.GamePlayer.ShipYard.ShipLocations : return
			
			# It is a hit - find the ship
			for ship in self.GamePlayer.ShipYard.ShipList :
				for coordinates in ship.Location : # Find the coordinates
					if coordinates == TryLocation : # If they match, change hit count
						# Next round through will prioritize this ship
						self.Priority = True
						self.PriorityShip = ship
						self.PriorityShipLocation.append(TryLocation)
						self.LastLocationOfShip = TryLocation

						# Change button color of player frame to see where its hitting
						self.Display.PlayerFrame.ButtonList[TryLocation[0]][TryLocation[1]].config(bg = "Red")

						# Change hit count on ship
						ship.Hits += 1

						# Change hit count for enemy
						self.Hits += 1
						self.Display.EnemyFrame.HitText.set("Hits: " + str(self.Hits))

						# The enemy has won!
						if self.Hits >= 17: 
							self.Display.MessageText.set("Winner is... Enemy!")
							self.Display.PlayerFrame.Change_Buttons_States("disable")
							self.Display.EnemyFrame.Change_Buttons_States("disable")
						
						return