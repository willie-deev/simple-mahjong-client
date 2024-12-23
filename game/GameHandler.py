from game.CardActionType import CardActionType
from game.CardType import CardType
from game.CardUtils import CardUtils
from game.GameManager import GameManager
from game.Wind import Wind
from utils.debugUtils import debugOutput


class GameHandler:
	def __init__(self, main):
		from Main import Main
		self.main: Main = main

		self.gameManager = GameManager(self)
		self.cardUtils = CardUtils(self)
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

	def getCardTypeByNumber(self, number: int):
		return self.cardNumberTypeList[number]

	def windToSide(self, target_wind: Wind) -> str:
		if self.gameManager.selfWind == target_wind:
			return "self"
		if self.gameManager.selfWind == Wind.EAST:
			if target_wind == Wind.SOUTH:
				return "left"
			elif target_wind == Wind.WEST:
				return "opposite"
			elif target_wind == Wind.NORTH:
				return "right"
		elif self.gameManager.selfWind == Wind.SOUTH:
			if target_wind == Wind.WEST:
				return "left"
			elif target_wind == Wind.NORTH:
				return "opposite"
			elif target_wind == Wind.EAST:
				return "right"
		elif self.gameManager.selfWind == Wind.WEST:
			if target_wind == Wind.NORTH:
				return "left"
			elif target_wind == Wind.EAST:
				return "opposite"
			elif target_wind == Wind.SOUTH:
				return "right"
		elif self.gameManager.selfWind == Wind.NORTH:
			if target_wind == Wind.EAST:
				return "left"
			elif target_wind == Wind.SOUTH:
				return "opposite"
			elif target_wind == Wind.WEST:
				return "right"

def getWindByName(name):
	for wind in Wind:
		if wind.name == name:
			return wind

def getCardTypeByName(name):
	for card in CardType:
		if card.name == name:
			return card

def getCardActionTypeByName(name):
	for cardActionType in CardActionType:
		if cardActionType.name == name:
			return cardActionType