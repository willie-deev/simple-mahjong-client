from game.CardType import CardType
from game.ClientActionType import ClientActionType
from game.Winds import Winds
from utils.debugUtils import debugOutput


class GameManager:
	def __init__(self, gameHandler):
		self.gameHandler = gameHandler
		self.selfWind = None
		self.gotCards = list[CardType]()
		self.sendMessageUtils = gameHandler.main.connectionHandler.sendMessageUtils
		self.orderNumberWindMap = None

	def setSelfWind(self, selfWind: Winds):
		self.selfWind = selfWind
		self.sendMessageUtils.sendClientActionType(ClientActionType.RECEIVED_CARDS, [])
		debugOutput(selfWind)

	def setFlowerCount(self, wind: Winds, flowerCount: int):
		self.gameHandler.main.guiHandler.gameWindowHandler.gameWindowController.triggerSetFlowerCount(wind, flowerCount)

	def windToOrderNumber(self, wind: Winds):
		if wind == Winds.EAST:
			return 0
		elif wind == Winds.SOUTH:
			return 1
		elif wind == Winds.WEST:
			return 2
		elif wind == Winds.NORTH:
			return 3

	def orderNumberToWind(self, orderNumber: int):
		if orderNumber == 0:
			return Winds.EAST
		elif orderNumber == 1:
			return Winds.SOUTH
		elif orderNumber == 2:
			return Winds.WEST
		elif orderNumber == 3:
			return Winds.NORTH

	def getSelfWind(self):
		return self.selfWind

	def addCards(self, cards: list[CardType]):
		for card in cards:
			self.gotCards.append(card)
		self.sendMessageUtils.sendClientActionType(ClientActionType.RECEIVED_CARDS, [])
		self.gameHandler.main.guiHandler.gameWindowHandler.gameWindowController.triggerAddCards(cards)
		if len(self.gotCards) >= 16:
			self.sortAllCards()
			# self.gameHandler.main.connectionHandler.sendMessageUtils.sendEncryptBytes()

	def removeFlowers(self):
		for card in self.gotCards:
			if card == CardType.FLOWER:
				self.gotCards.remove(card)
		self.gameHandler.main.guiHandler.gameWindowHandler.gameWindowController.triggerSetAllCards(self.gotCards)

	def sortAllCards(self):
		self.gotCards.sort(key=lambda v: v.value, reverse=True)
		self.gameHandler.main.guiHandler.gameWindowHandler.gameWindowController.triggerSetAllCards(self.gotCards)
