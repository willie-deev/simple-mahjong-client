from game.GameManager import GameManager


class GameHandler:
	def __init__(self, main):
		self.main = main
		self.gameManager = GameManager(self)
