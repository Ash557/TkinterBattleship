#!/usr/bin/env python #
"""
	TkWindow
	- Creates window
	- Adds title and design

	TkFrame
	- Creates and grids elements of frames

	Display
	- Creates and grids elements
	- Places frames into window
"""

import tkinter

# Creates a tk window 
class TkWindow(tkinter.Tk):
	def __init__(self) :
		super().__init__()
		self.title("Battleship")
		self.config(background = "black")

# Create a tk frame and grid's it to the window according to the location array
# Contains - parent window
#			location array [x, y]
#			bool - determines if to create the button array or not
class TkFrame(tkinter.Frame) :
	def __init__(self, parent, location, title) :
		super().__init__(parent)
		self.grid(row = location[0], column = location[1], sticky = "NSEW")

		# Set weights on grid to enable expansion
		self.grid_columnconfigure(0, weight = 1)
		for x in range(5) :
			self.grid_rowconfigure(x, weight = 1)

		# Grid the label
		self.TitleLabel = tkinter.Label(self, text = title)
		self.TitleLabel.grid(row = 0, column = 0, sticky = "NSEW")

		# Create and grid hit text at bottom of board
		self.HitText = tkinter.StringVar()
		self.NumOfHits = tkinter.StringVar()
		self.NumOfHits.set(0)
		self.HitText.set("Hits: " + self.NumOfHits.get())
		self.HitLabel = tkinter.Label(self, textvariable = self.HitText)
		self.HitLabel.grid(row = 2, column = 0, sticky = "NSEW")

		# Create and grid sunk text at bottom of board
		self.SunkText = tkinter.StringVar()
		self.SunkText.set("Sunk: ")
		self.SunkLabel = tkinter.Label(self, textvariable = self.SunkText)
		self.SunkLabel.grid(row = 3, column = 0, sticky = "NSEW")
		
		# Create and grid board itself with buttons and create button list
		self.ButtonBoard = tkinter.Frame(self, bg = "white", bd = 5)
		self.ButtonBoard.grid(row = 1, column = 0,  sticky = "NSEW")
		self.ButtonList = self.Button_Grid()

	# Create buttons and grid into the ButtonBoard
	# Return list of buttons
	def Button_Grid(self) :
		buttonlist = []
		for x in range(10) :
			self.ButtonBoard.grid_rowconfigure(x, weight = 1)
			self.ButtonBoard.grid_columnconfigure(x, weight = 1)
			button_col_list = []
			for y in range(10) :
				button = tkinter.Button(self.ButtonBoard, bg = "grey", bd = 0.5, text = "O", state = "disable")
				button_col_list.append(button)
				button.grid(row = x, column = y, sticky = "NSEW")
			buttonlist.append(button_col_list)
		return buttonlist

	# Change all buttons states
	def Change_Buttons_States(self, state) :
		for x in range(10) :
			for y in range(10) :
				self.ButtonList[x][y].config(state = state)

# sets up window
class Display() :
	def __init__(self) :
		self.Root = TkWindow()
		
		self.PlayerFrame = TkFrame(self.Root, [0, 1], "Player")
		self.EnemyFrame = TkFrame(self.Root, [0, 0], "Enemy")

		# Grid and configure frames
		self.Root.grid_columnconfigure(2, weight = 1)
		for x, board in enumerate([self.EnemyFrame, self.PlayerFrame]):
			board.grid(row = 0, column = x, sticky = "NSEW")
			self.Root.grid_columnconfigure(x, weight = 1)
			self.Root.grid_rowconfigure(x, weight = 1)

		# Create message frame
		self.MessageFrame = tkinter.Frame(self.Root)
		self.MessageFrame.grid(row = 0, column = 2, sticky = "NSEW")

		# Create message board clear button
		self.ClearButton = tkinter.Button(self.MessageFrame, bg = "grey", bd = 0.5, text = "Clear Message", command = lambda : self.Clear_Message())
		self.ClearButton.grid(row = 0, column = 0, sticky = "NSEW")

		# Create message board on right of window inside message frame
		self.MessageText = tkinter.StringVar()
		self.MessageText.set("Place All Ships to Begin")
		self.MessageLabel = tkinter.Label(self.MessageFrame, textvariable = self.MessageText)
		self.MessageLabel.grid(row = 1, column = 0, sticky = "NSEW")

	def Clear_Message(self) :
		self.MessageText.set("")
