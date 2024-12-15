from game.GameStates import GameStates
from game.Winds import Winds


class GameManager:
	def __init__(self, gameHandler):
		self.gameState = None
		self.gameHandler = gameHandler
		self.selfWind = None

	def setSelfWind(self, selfWind: Winds):
		self.selfWind = selfWind
		print(selfWind)

	def getSelfWind(self):
		return self.selfWind

	def setGameState(self, gameState: GameStates):
		self.gameState = gameState

	def getGameState(self):
		return self.gameState
