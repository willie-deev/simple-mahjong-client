from PySide6.QtCore import QObject, Signal

from game.CardType import CardType
from game.Winds import Winds


class GameWindowController(QObject):
	setPlayerWind = Signal(Winds)
	addCards = Signal(list)
	setAllCards = Signal(list)

	def __init__(self, gameWindowHandler):
		super().__init__()
		self.gameWindowHandler = gameWindowHandler

	def triggerSetAllCards(self, cardTypes: list[CardType]):
		self.setAllCards.emit(cardTypes)

	def triggerSetPlayerWind(self, wind: Winds):
		self.setPlayerWind.emit(wind)

	def triggerAddCards(self, cardTypes: list[CardType]):
		self.addCards.emit(cardTypes)
