from typing import Optional

from game.CardType import CardType
from game.ClientActionType import ClientActionType
from game.Wind import Wind
from utils.debugUtils import debugOutput


class GameManager:
	def __init__(self, gameHandler):
		from game.GameHandler import GameHandler
		self.gameHandler: GameHandler = gameHandler

		self.selfWind = None
		self.gotCards = list[CardType]()
		self.orderNumberWindMap = None

		from connection.SendMessageUtils import SendMessageUtils
		from gui.gameWindow.GameWindowController import GameWindowController
		self.sendMessageUtils: SendMessageUtils = gameHandler.main.connectionHandler.sendMessageUtils
		self.gameWindowController: Optional[GameWindowController] = None

	def setupVariables(self):
		self.gameWindowController = self.gameHandler.main.guiHandler.gameWindowHandler.gameWindowController

	def setSelfWind(self, selfWind: Wind):
		self.selfWind = selfWind
		self.sendMessageUtils.sendClientActionType(ClientActionType.RECEIVED_CARDS, [])
		debugOutput(selfWind)

	def setFlowerCount(self, wind: Wind, flowerCount: int):
		gameWindowController = self.gameWindowController
		gameWindowController.triggerSetFlowerCount(wind, flowerCount)
		self.sendMessageUtils.sendClientActionType(ClientActionType.RECEIVED_FLOWER_COUNT, [])

	def windToOrderNumber(self, wind: Wind):
		if wind == Wind.EAST:
			return 0
		elif wind == Wind.SOUTH:
			return 1
		elif wind == Wind.WEST:
			return 2
		elif wind == Wind.NORTH:
			return 3

	def orderNumberToWind(self, orderNumber: int):
		if orderNumber == 0:
			return Wind.EAST
		elif orderNumber == 1:
			return Wind.SOUTH
		elif orderNumber == 2:
			return Wind.WEST
		elif orderNumber == 3:
			return Wind.NORTH

	def getSelfWind(self):
		return self.selfWind

	def startAddCards(self, cards: list[CardType]):
		for card in cards:
			self.gotCards.append(card)
		self.sendMessageUtils.sendClientActionType(ClientActionType.RECEIVED_CARDS, [])
		self.gameWindowController.triggerStartAddCards(cards)
		print(self.gotCards)

	def removeFlowers(self):
		while CardType.FLOWER in self.gotCards:
			self.gotCards.remove(CardType.FLOWER)
		self.gameWindowController.triggerSetAllCards(self.gotCards)

	def sortAllCards(self):
		self.gotCards.sort(key=lambda v: v.value, reverse=False)
		self.gameWindowController.triggerSetAllCards(self.gotCards)

	def gotNewCard(self, cardType: CardType):
		self.gotCards.append(cardType)
		self.gameWindowController.triggerGotNewCard(cardType)
		self.sendMessageUtils.sendClientActionType(ClientActionType.RECEIVED_CARDS, [])

	def waitDiscard(self):
		self.gameWindowController.triggerWaitDiscard()
