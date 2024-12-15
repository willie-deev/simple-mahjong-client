from time import sleep

from game.CardType import CardType
from game.GameStates import GameStates
from game.Winds import Winds
from utils.debugUtils import debugOutput


class GameManager:
	def __init__(self, gameHandler):
		self.gameState = None
		self.gameHandler = gameHandler
		self.selfWind = None
		self.gotCards = list[CardType]()

	def setSelfWind(self, selfWind: Winds):
		self.selfWind = selfWind
		debugOutput(selfWind)

	def getSelfWind(self):
		return self.selfWind

	def setGameState(self, gameState: GameStates):
		self.gameState = gameState
		debugOutput("gameStateNow: " + gameState.name)

	def getGameState(self):
		return self.gameState

	def addCards(self, cards: list[CardType]):
		for card in cards:
			self.gotCards.append(card)
		self.gameHandler.main.guiHandler.gameWindowHandler.gameWindowController.triggerAddCards(cards)
		if len(self.gotCards) >= 16:
			sleep(1)
			self.sortAllCards()
			self.setGameState(GameStates.STARTED)

	def sortAllCards(self):
		self.gotCards.sort(key=lambda v: v.value, reverse=True)
		self.gameHandler.main.guiHandler.gameWindowHandler.gameWindowController.triggerSetAllCards(self.gotCards)
