from PySide6.QtCore import QObject, Signal

from game.CardType import CardType
from game.Wind import Wind


class GameWindowController(QObject):
	setPlayerWind = Signal(Wind)
	startAddCards = Signal(list)
	setAllCards = Signal(list)
	gotNewCard = Signal(CardType)
	setFlowerCount = Signal(Wind, int)

	def __init__(self, gameWindowHandler):
		super().__init__()
		self.gameWindowHandler = gameWindowHandler

	def triggerSetAllCards(self, cardTypes: list[CardType]):
		self.setAllCards.emit(cardTypes)

	def triggerSetPlayerWind(self, wind: Wind):
		self.setPlayerWind.emit(wind)

	def triggerStartAddCards(self, cardTypes: list[CardType]):
		self.startAddCards.emit(cardTypes)

	def triggerSetFlowerCount(self, wind: Wind, flowerCount: int):
		self.setFlowerCount.emit(wind, flowerCount)

	def triggerGotNewCard(self, cardType: CardType):
		self.gotNewCard.emit(cardType)
