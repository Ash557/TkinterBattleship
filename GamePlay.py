#!/usr/bin/env python #
"""
	GamePlay Object
	- Creates the window
	- Creates the Player
	- Creates the Enemy
	- Runs the actual game

	Main
	- Runs Game

	Organized in order to enable future additions
"""

from Window import Display
from Enemy import Enemy
from Player import Player

class GamePlay():
	def __init__(self) :
		# Create window
		self.DisplayWindow = Display()
		
		# Create game player and enemy(computer)
		self.GamePlayer = Player(self.DisplayWindow)
		self.GameEnemy = Enemy(self.DisplayWindow, self.GamePlayer)

		# Finally, begin the game
		self.DisplayWindow.Root.mainloop()


if __name__ == '__main__' :
	Battleship = GamePlay()