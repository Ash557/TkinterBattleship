#!/usr/bin/env python #
"""
	Player
	- Place Player Ships
	- Configure Player buttons
	- Set up for Gameplay
"""

from Ship import ShipYard
from Window import Display
import tkinter

class Player() :
	def __init__(self, Display) :
		self.ShipYard = ShipYard("Player")
		self.ShipIndex = 0
		self.Hits = 0
		self.ButtonList = Display.PlayerFrame.ButtonList
		self.Display = Display
		self.CurrentShip = self.ShipYard.ShipList[self.ShipIndex]

		Display.PlayerFrame.Change_Buttons_States("normal")

		# Configure all player buttons to place ship function and to be hover buttons
		for x in range(10) :
			for y in range(10) :
				self.ButtonList[x][y].config(command = lambda x=x, y=y : self.Place_Ship(x, y))
				self.ButtonList[x][y].bind("<Enter>", lambda event, x=x, y=y : self.On_Enter(x, y))   
				self.ButtonList[x][y].bind("<Leave>", lambda event, x=x, y=y : self.On_Leave(x, y))


		# Create change orientation button for bottom of player frame
		self.ChangeOrientationButton = tkinter.Button(	Display.PlayerFrame, 
											bg = "grey", 
											text = "Change Orientation", 
											bd = 0.5, 
											command = lambda : self.CurrentShip.Change_Orientation()
										)
		self.ChangeOrientationButton.grid(row = 4, column = 0, sticky = "NSEW")

	# Change button color to purple during hover
	def On_Enter(self, x, y) :
		if self.CurrentShip.Horizontal == False and (x+self.CurrentShip.Length-1) < 10 : 
			for p in range(self.CurrentShip.Length) :
				self.ButtonList[x+p][y].config(bg = "purple")
		elif self.CurrentShip.Horizontal == True and (y+self.CurrentShip.Length-1) < 10 : 
			for p in range(self.CurrentShip.Length) :
				self.ButtonList[x][y+p].config(bg = "purple")

	# Change button color back to grey after leaving button hover area
	def On_Leave(self, x, y) :
		if self.CurrentShip.Horizontal == False and (x+self.CurrentShip.Length-1) < 10 : 
			for p in range(self.CurrentShip.Length) :
				self.ButtonList[x+p][y].config(bg = "grey")
		elif self.CurrentShip.Horizontal == True and (y+self.CurrentShip.Length-1) < 10 : 
			for p in range(self.CurrentShip.Length) :
				self.ButtonList[x][y+p].config(bg = "grey")

	# Place ship on board
	def Place_Ship(self, x, y) :
		success = True
		if self.CurrentShip.Horizontal == False and (x+self.CurrentShip.Length-1) < 10 :
			for p in range(self.CurrentShip.Length) :
				if [x+p, y] not in self.ShipYard.ShipLocations :
					self.ButtonList[x+p][y].config(text = "X", state = "disable")
					self.CurrentShip.Location.append([x+p, y])
				else :
					self.Display.MessageText.set(self.Display.MessageText.get() + "\n" + "Cannot place this ship here")
					for k in range(p-1, -1, -1) :
						self.ButtonList[x+k][y].config(text = "O", state = "normal")	
					self.CurrentShip.Location = []
					success = False
					break
		elif self.CurrentShip.Horizontal == True and (y+self.CurrentShip.Length-1) < 10 : 
			for p in range(self.CurrentShip.Length) :
				if [x, y+p] not in self.ShipYard.ShipLocations :
					self.ButtonList[x][y+p].config(text = "X", state = "disable")
					self.CurrentShip.Location.append([x, y+p])
				else :
					self.Display.MessageText.set(self.Display.MessageText.get() + "\n" + "Cannot place this ship here")
					for k in range(p-1, -1, -1) :
						self.ButtonList[x][y+k].config(text = "O", state = "normal")
					self.CurrentShip.Location = []
					success = False
					break
		else :
			success = False
		if success == True:
			if self.ShipIndex < 4 :
				self.ShipYard.ShipLocations.extend(self.CurrentShip.Location)
				self.Display.MessageText.set(self.Display.MessageText.get() + "\n" + "Placed Ship " + self.CurrentShip.Name)
				self.Next_Ship()
			else :
				self.Display.MessageText.set(self.Display.MessageText.get() + "\n" + "All Ships Placed. You may begin the game.")
				self.Display.PlayerFrame.Change_Buttons_States("disable")
				self.Display.EnemyFrame.Change_Buttons_States("normal")
				self.ChangeOrientationButton.destroy()
				for p in range(10) :
					for k in range(10) :
						self.ButtonList[p][k].unbind("<Enter>")   
						self.ButtonList[p][k].unbind("<Leave>")
						self.ButtonList[p][k].config(bg = "grey")

	def Next_Ship(self) :
		self.ShipIndex = self.ShipIndex + 1
		self.CurrentShip = self.ShipYard.ShipList[self.ShipIndex]