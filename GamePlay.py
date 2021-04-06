from Window import Display
from Enemy import Enemy
from Player import Player

class GamePlay():
	def __init__(self) :
		#create window
		self.DisplayWindow = Display()
		
		#create game player and enemy(computer)
		self.GamePlayer = Player(self.DisplayWindow)
		self.GameEnemy = Enemy(self.DisplayWindow, self.GamePlayer)

		for x in range(10) :
			for y in range(10) :
				self.GameEnemy.ButtonList[x][y].config(command = lambda x=x, y=y : self.GameEnemy.Hit_Miss(x, y))

		#finally, begin the game
		self.DisplayWindow.Root.mainloop()


if __name__ == '__main__' :
	Battleship = GamePlay()