from PySide6.QtCore import QSize
from PySide6.QtWidgets import QPushButton

from game.CardType import CardType


class SelfCardUiManager:
	def __init__(self, gameWindowHandler):
		from gui.gameWindow.GameWindowHandler import GameWindowHandler
		self.gameWindowHandler: GameWindowHandler = gameWindowHandler
		self.widgetUtils = self.gameWindowHandler.widgetUtils

		self.waitingForDiscard = False
		self.addedCards: dict[QPushButton, CardType] = {}

	def clickedOnCardButton(self, cardType: CardType, clickedButton: QPushButton):
		if self.gameWindowHandler.actionsMenuManager.selectingChowCard is True:
			self.gameWindowHandler.actionsMenuManager.selectedChowCard(cardType, clickedButton)
		if not self.waitingForDiscard:
			return
		self.gameWindowHandler.guiHandler.main.gameHandler.gameManager.setDiscardType(cardType)
		self.updateCardButtons()

	def startAddCards(self, cardTypes: list[CardType]):
		for cardType in cardTypes:
			newPushButton = self.widgetUtils.getCardButton(cardType)
			self.gameWindowHandler.ui.handCards.layout().addWidget(newPushButton)
			self.addedCards[newPushButton] = cardType
		self.updateCardButtons()

	def gotNewCard(self, cardType: CardType):
		newPushButton = self.widgetUtils.getCardButton(cardType)
		# self.gameWindowHandler.ui.selfCards.layout().addWidget(newPushButton)
		# debugOutput(str(len(self.addedCards)))
		self.gameWindowHandler.ui.newCards.layout().addWidget(newPushButton)
		self.addedCards[newPushButton] = cardType
		self.updateCardButtons()

	def updateCardButtons(self):
		if not self.gameWindowHandler.actionsMenuManager.selectingChowCard:
			for card in self.addedCards.keys():
				styleSheet, height, width = self.getCardButtonVariables()
				card.setIconSize(QSize(width, height))
				if self.waitingForDiscard is True:
					styleSheet += "QPushButton:hover { background-color: lightgray; }"
				card.setStyleSheet(styleSheet)

	def getCardButtonVariables(self):
		height = self.gameWindowHandler.ui.selfCards.height() // 4 * 3
		width = height // 3 * 2
		padding = width // 7
		borderRadius = padding
		styleSheet = "QPushButton{"
		styleSheet += "padding-left: " + str(padding) + "px;"
		styleSheet += "padding-right: " + str(padding) + "px;"
		styleSheet += "background-color: white;"
		styleSheet += "border-radius: " + str(borderRadius) + "px;"
		styleSheet += "}"
		return styleSheet, height, width

	def setAllCards(self, cardTypes: list[CardType]):
		for addedCard in self.addedCards.keys():
			# self.gameWindowHandler.ui.selfCards.layout().removeWidget(addedCard)
			addedCard.deleteLater()
		self.addedCards.clear()
		self.startAddCards(cardTypes)