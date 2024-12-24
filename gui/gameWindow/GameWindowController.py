from PySide6.QtCore import QObject, Signal

from game.CardType import CardType
from game.Wind import Wind


class GameWindowController(QObject):
	setPlayerWind = Signal(Wind)
	startAddCards = Signal(list)
	setAllCards = Signal(list)
	gotNewCard = Signal(CardType)
	waitDiscard = Signal()
	playerDiscarded = Signal(Wind, CardType)
	otherPlayerGotCard = Signal(Wind)
	canDoActions = Signal(object)
	performedCardAction = Signal(Wind, list)
	notPerformedCardAction = Signal()

	def __init__(self, gameWindowHandler):
		super().__init__()
		self.gameWindowHandler = gameWindowHandler

	def triggerSetAllCards(self, cardTypes: list[CardType]):
		self.setAllCards.emit(cardTypes)

	def triggerSetPlayerWind(self, wind: Wind):
		self.setPlayerWind.emit(wind)

	def triggerStartAddCards(self, cardTypes: list[CardType]):
		self.startAddCards.emit(cardTypes)

	def triggerGotNewCard(self, cardType: CardType):
		self.gotNewCard.emit(cardType)

	def triggerWaitDiscard(self):
		self.waitDiscard.emit()

	def triggerPlayerDiscarded(self, wind: Wind, cardType: CardType):
		self.playerDiscarded.emit(wind, cardType)

	def triggerOtherPlayerGotCard(self, wind: Wind):
		self.otherPlayerGotCard.emit(wind)

	def triggerCanDoActions(self, canDoActions: dict):
		self.canDoActions.emit(canDoActions)

	def triggerPerformedCardAction(self, wind: Wind, performedCardAction: list[CardType]):
		self.performedCardAction.emit(wind, performedCardAction)

	def triggerNotPerformedCardAction(self):
		self.notPerformedCardAction.emit()
