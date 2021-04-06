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
		self.CurrentDirection = "Right"
		self.LastLocationOfShip = None
		
		while self.ShipIndex < 5 :
			if self.Place_Ship(self.ShipYard.ShipList[self.ShipIndex]) == True :
				self.ShipIndex = self.ShipIndex + 1

	def Place_Ship(self, CurrentShip) :
		#get the first location for the ship
		BaseLocation = [randint(0, 9-CurrentShip.Length), randint(0, 9-CurrentShip.Length)]

		#add this location to the current ship
		CurrentShip.Location = [BaseLocation]

		#get a random number for the horizontal bool
		CurrentShip.Horizontal = getrandbits(1)

		#if the location is valid, move to the next ship, otherwise redo this ship
		if self.Valid_Ship_Location(CurrentShip, BaseLocation) :
			self.ShipIndex = self.ShipIndex + 1
			self.Change_Button_Text(CurrentShip.Location)
		
	def Valid_Ship_Location(self, CurrentShip, BaseLocation) :
		#if the first location exists in all locations, return false
		if BaseLocation in self.ShipYard.ShipLocations : return False

		#the current location is the first location
		CurrentLocation = BaseLocation

		if CurrentShip.Horizontal == True : # ship is horizontal
			for x in range(1, CurrentShip.Length) :
				CurrentLocation = [CurrentLocation[0]+1, CurrentLocation[1]]
				if CurrentLocation in self.ShipYard.ShipLocations :
					return False
				CurrentShip.Location.append(CurrentLocation)
		else : # ship is vertical
			for x in range(1, CurrentShip.Length) :
				CurrentLocation = [CurrentLocation[0], CurrentLocation[1]+1]
				if CurrentLocation in self.ShipYard.ShipLocations :
					return False
				CurrentShip.Location.append(CurrentLocation)
		self.ShipYard.ShipLocations.extend(CurrentShip.Location)
		return True

	def Change_Button_Text(self, ShipLocation) :
		for location in ShipLocation :
			self.ButtonList[location[0]][location[1]].config(text = "X")

	def Hit_Miss(self, x, y) :
		#disable the button and change color to white
		self.ButtonList[x][y].config(state = "disable", bg = "white")

		#if it is a hit
		if [x, y] in self.ShipYard.ShipLocations :
			self.GamePlayer.Hits = self.GamePlayer.Hits + 1
			self.Display.PlayerFrame.HitText.set("Hits: " + str(self.GamePlayer.Hits))
			#find the ship
			for ship in self.ShipYard.ShipList :
				#find the coordinates
				for coordinates in ship.Location :
					#if they match, change hit count
					if coordinates == [x, y] :
						#change button color to red
						self.ButtonList[x][y].config(bg = "red")

						ship.Ship_Hit()

						#check to see if the ship is sunk
						if ship.Ship_Sunk() == True :
							self.Display.PlayerFrame.SunkText.set(self.Display.PlayerFrame.SunkText.get() + "\n" + ship.Name + " Sunk")

		#take enemy turn
		self.Take_Enemy_Turn()

	def Reset_Priority_Ship(self) :
		self.Priority = False
		self.PriorityShip = None
		self.PriorityShipLocation = []
		self.PriorityShipDirection = None
		self.CurrentDirection = "Right"
		self.LastLocationOfShip = None

	def Next_Direction(self) :
		if self.CurrentDirection == "Right" :
			self.CurrentDirection = "Up"
		elif self.CurrentDirection == "Up" :
			self.CurrentDirection = "Down" 
		elif self.CurrentDirection == "Down" :
			self.CurrentDirection = "Left"
		else :
			self.CurrentDirection = "Right"

	def Take_Enemy_Turn(self) :
		if self.Priority == True :
			TryLocation = []
			if self.PriorityShipDirection is None :
				if self.CurrentDirection == "Right" :
					TryLocation = [self.LastLocationOfShip[0]+1, self.LastLocationOfShip[1]]
				elif self.CurrentDirection == "Up" :
					TryLocation = [self.LastLocationOfShip[0], self.LastLocationOfShip[1]-1]
				elif self.CurrentDirection == "Down" :
					TryLocation = [self.LastLocationOfShip[0], self.LastLocationOfShip[1]+1]
				elif self.CurrentDirection == "Left" :
					TryLocation = [self.LastLocationOfShip[0]-1, self.LastLocationOfShip[1]]
			else : #self.PriorityShipDirection is not None
				if self.PriorityShipDirection == "Right" :
					TryLocation = [self.LastLocationOfShip[0]+1, self.LastLocationOfShip[1]]
				elif self.PriorityShipDirection == "Up" :
					TryLocation = [self.LastLocationOfShip[0], self.LastLocationOfShip[1]-1]
				elif self.PriorityShipDirection == "Down" :
					TryLocation = [self.LastLocationOfShip[0], self.LastLocationOfShip[1]+1]
				elif self.PriorityShipDirection == "Left" :
					TryLocation = [self.LastLocationOfShip[0]-1, self.LastLocationOfShip[1]]
				
			#add location to list of locations already used
			self.Locations_Used.append(TryLocation)

			#if hit, turn button red, else turn button white
			if TryLocation in self.GamePlayer.ShipYard.ShipLocations :
				self.Display.PlayerFrame.ButtonList[TryLocation[0]][TryLocation[1]].config(bg = "Red")
				self.PriorityShipDirection = self.CurrentDirection
				self.PriorityShip.Ship_Hit()
				self.PriorityShipLocation.append(TryLocation)
				self.LastLocationOfShip = TryLocation

				#Check to see if the ship is sunk
				if self.PriorityShip.Ship_Sunk() == True :
					self.Display.EnemyFrame.SunkText.set(self.Display.EnemyFrame.SunkText.get() + "\n" + self.PriorityShip.Name + " Sunk")
					self.Reset_Priority_Ship
					self.Priority = False

			else : #miss
				self.Display.PlayerFrame.ButtonList[TryLocation[0]][TryLocation[1]].config(bg = "White")
				#if direction has already been determined, flip direction
				if self.PriorityShipDirection is not None :
					#change last location of ship to first location of ship
					self.LastLocationOfShip = self.PriorityShipLocation[0]
					#flip direction of ship
					if self.PriorityShipDirection == "Right" :
						self.PriorityShipDirection = "Left"
					elif self.PriorityShipDirection == "Up" :
						self.PriorityShipDirection = "Down"
				else : #self.PriorityShipDirection is None
					self.Next_Direction()

		else : #Priority is False
			#Find random location
			TryLocation = [randint(0, 9), randint(0, 9)]

			#if it has already been used, try again
			while TryLocation in self.Locations_Used :
				TryLocation = [randint(0, 9), randint(0, 9)]

			#Add this location to the locations used so far
			self.Locations_Used.append(TryLocation)

			#Change button color of player frame to see where its hitting
			self.Display.PlayerFrame.ButtonList[TryLocation[0]][TryLocation[1]].config(bg = "White")

			#if the location is not in the shipyard, don't attempt loops
			if TryLocation not in self.GamePlayer.ShipYard.ShipLocations : return

			#find the ship
			for ship in self.GamePlayer.ShipYard.ShipList :
				#find the coordinates
				for coordinates in ship.Location :
					#if they match, change hit count
					if coordinates == TryLocation :
						#Next round through will prioritize this ship
						self.Priority = True
						self.PriorityShip = ship
						self.PriorityShipLocation.append(TryLocation)
						self.LastLocationOfShip = TryLocation

						#Change button color of player frame to see where its hitting
						self.Display.PlayerFrame.ButtonList[TryLocation[0]][TryLocation[1]].config(bg = "Red")

						#Change hit count on ship
						ship.Hits = ship.Hits + 1

						#Change hit count
						self.Hits = self.Hits+1
						self.Display.EnemyFrame.HitText.set("Hits: " + str(self.Hits))