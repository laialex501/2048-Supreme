# <------------------ Imports ------------------> #

import numpy as np
from random import *
import tkinter as tk
import tkinter.messagebox
import time
from Game_World import Game_2048
from Graphics import StartGame

# <------------------ Main ------------------> #

def main():
	MainGame = StartGame()
	if MainGame.GAME.is_game_over():
		print('Game Over!')

if __name__ == "__main__":
	main()



