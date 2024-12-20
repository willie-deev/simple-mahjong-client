from game.CardType import CardType
from game.GameManager import GameManager
from game.Wind import Wind
from utils.debugUtils import debugOutput


class GameHandler:
	def __init__(self, main):
		from Main import Main
		self.main: Main = main

		self.gameManager = GameManager(self)
		self.cardNumberTypeList = list[CardType]()
		for cardType in CardType:
			if cardType.name != "FLOWER":
				for i in range(4):
					self.cardNumberTypeList.append(cardType)
			else:
				for i in range(8):
					self.cardNumberTypeList.append(cardType)
		for i in range(len(self.cardNumberTypeList)):
			debugOutput(str(i) + "\t" + str(self.cardNumberTypeList[i]))

	def getWindByName(self, name):
		for wind in Wind:
			if wind.name == name:
				return wind

	def getCardTypeByName(self, name):
		for card in CardType:
			if card.name == name:
				return card

	def getCardTypeByNumber(self, number: int):
		return self.cardNumberTypeList[number]
