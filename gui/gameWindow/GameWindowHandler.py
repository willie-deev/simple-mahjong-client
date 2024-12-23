from PySide6.QtCore import QTimer
from PySide6.QtGui import Qt
from PySide6.QtWidgets import QPushButton

from game.CardType import CardType
from game.Wind import Wind
from gui.gameWindow.ActionsMenuManager import ActionsMenuManager
from gui.gameWindow.GameWindowController import GameWindowController
from gui.gameWindow.WidgetUtils import WidgetManager
from gui.gameWindow.gameWindow import *
from utils.debugUtils import debugOutput


class GameWindowHandler(QMainWindow):
	def __init__(self, guiHandler):
		super().__init__()
		self.ui = Ui_MainWindow()
		self.guiHandler = guiHandler
		self.gameWindowController = GameWindowController(self)
		self.widgetUtils = WidgetManager(self)
		self.addedCards: dict[QPushButton, CardType] = {}
		self.waitingForDiscard = False
		self.selfDiscardedLabels: dict[QLabel, CardType] = {}
		self.leftDiscardedLabels: dict[QLabel, CardType] = {}
		self.oppositeDiscardedLabels: dict[QLabel, CardType] = {}
		self.rightDiscardedLabels: dict[QLabel, CardType] = {}

		self.lastDiscardedLabel: QLabel | None = None

		self.selfActionedCardLabels: dict[QLabel, CardType] = {}
		self.leftActionedCardLabels: dict[QLabel, CardType] = {}
		self.oppositeActionedCardLabels: dict[QLabel, CardType] = {}
		self.rightActionedCardLabels: dict[QLabel, CardType] = {}

		self.leftAddedCardLabels: list[QLabel] = []
		self.oppositeAddedCardLabels: list[QLabel] = []
		self.rightAddedCardLabels: list[QLabel] = []

		self.leftGotCardLabel = None
		self.oppositeGotCardLabel = None
		self.rightGotCardLabel = None

		self.actionsMenuManager = ActionsMenuManager(self)

	def resizeEvent(self, event):
		super().resizeEvent(event)
		self.actionsMenuManager.resizeOverlay()
		self.updateCardButtons()
		self.resizeDiscardedLabels()
		self.resizeOtherPlayerCards()

	def showEvent(self, event):
		super().showEvent(event)
		self.resizeDiscardedLabels()

	def changeEvent(self, event):
		super().changeEvent(event)
		self.actionsMenuManager.resizeOverlay()
		self.updateCardButtons()
		self.resizeDiscardedLabels()
		QTimer.singleShot(1, self.updateCardButtons)

	def setupUi(self):
		self.ui.setupUi(self)
		icon = QIcon("/home/willie/PycharmProjects/simple-mahjong-client/assets/character/1.png")
		debugOutput(icon.isNull())

		self.ui.selfCards.update()
		self.gameWindowController.setPlayerWind.connect(self.setPlayerWind)
		self.gameWindowController.startAddCards.connect(self.startAddCards)
		self.gameWindowController.setAllCards.connect(self.setAllCards)
		# self.gameWindowController.setFlowerCount.connect(self.setFlowerCount)
		self.gameWindowController.gotNewCard.connect(self.gotNewCard)
		self.gameWindowController.waitDiscard.connect(self.waitDiscard)
		self.gameWindowController.playerDiscarded.connect(self.playerDiscarded)
		self.gameWindowController.otherPlayerGotCard.connect(self.otherPlayerGotCard)
		self.gameWindowController.canDoActions.connect(self.actionsMenuManager.showActionsMenu)
		self.gameWindowController.performedCardAction.connect(self.performedCardAction)

		self.actionsMenuManager.setupActionsMenu()
		self.actionsMenuManager.hideActionsMenu()

		self.setupDiscardArea()
		self.setupOtherPlayerLabel()

		# self.guiHandler.mainWindow.show()
		debugOutput("inited")

	def setupOtherPlayerLabel(self):
		for i in range(16):
			label = self.widgetUtils.getHideCardLabel()
			self.ui.leftCardsLayout.addWidget(label)
			self.ui.leftCardsLayout.setAlignment(Qt.AlignmentFlag.AlignCenter)
			self.leftAddedCardLabels.append(label)

			label = self.widgetUtils.getHideCardLabel()
			self.ui.oppositeCardsLayout.addWidget(label)
			self.ui.oppositeCardsLayout.setAlignment(Qt.AlignmentFlag.AlignCenter)
			self.oppositeAddedCardLabels.append(label)

			label = self.widgetUtils.getHideCardLabel()
			self.ui.rightCardsLayout.addWidget(label)
			self.ui.rightCardsLayout.setAlignment(Qt.AlignmentFlag.AlignCenter)
			self.rightAddedCardLabels.append(label)

		layout = self.ui.leftNewCardsLayout
		self.leftGotCardLabel = self.widgetUtils.getHideCardLabel()
		layout.addWidget(self.leftGotCardLabel)
		layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
		self.leftGotCardLabel.hide()

		layout = self.ui.oppositeNewCardsLayout
		self.oppositeGotCardLabel = self.widgetUtils.getHideCardLabel()
		layout.addWidget(self.oppositeGotCardLabel)
		layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
		self.oppositeGotCardLabel.hide()

		layout = self.ui.rightNewCardsLayout
		self.rightGotCardLabel = self.widgetUtils.getHideCardLabel()
		layout.addWidget(self.rightGotCardLabel)
		layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
		self.rightGotCardLabel.hide()

	def performedCardAction(self, wind: Wind, cardTypes: list[CardType]):
		debugOutput("wind: " + str(wind) + " cardTypes: " + str(cardTypes))
		for cardType in cardTypes:
			self.addActionedCard(wind, cardType)
			if self.guiHandler.main.gameHandler.windToSide(wind) == "left":
				self.leftAddedCardLabels.pop().deleteLater()
			elif self.guiHandler.main.gameHandler.windToSide(wind) == "opposite":
				self.oppositeAddedCardLabels.pop().deleteLater()
			elif self.guiHandler.main.gameHandler.windToSide(wind) == "right":
				self.rightAddedCardLabels.pop().deleteLater()

		self.leftDiscardedLabels.pop(self.lastDiscardedLabel, None)
		self.rightDiscardedLabels.pop(self.lastDiscardedLabel, None)
		self.oppositeDiscardedLabels.pop(self.lastDiscardedLabel, None)
		self.selfDiscardedLabels.pop(self.lastDiscardedLabel, None)
		self.lastDiscardedLabel.deleteLater()
		self.resizeDiscardedLabels()

	def otherPlayerGotCard(self, wind: Wind):
		if self.guiHandler.main.gameHandler.windToSide(wind) == "left":
			self.leftGotCardLabel.show()
		elif self.guiHandler.main.gameHandler.windToSide(wind) == "opposite":
			self.oppositeGotCardLabel.show()
		else:
			self.rightGotCardLabel.show()
		self.resizeOtherPlayerCards()

	def otherPlayerDiscarded(self, wind: Wind):
		if self.guiHandler.main.gameHandler.windToSide(wind) == "left":
			self.leftGotCardLabel.hide()
		elif self.guiHandler.main.gameHandler.windToSide(wind) == "opposite":
			self.oppositeGotCardLabel.hide()
		elif self.guiHandler.main.gameHandler.windToSide(wind) == "right":
			self.rightGotCardLabel.hide()
		else:
			return
		self.resizeOtherPlayerCards()

	def addActionedCard(self, wind: Wind, cardType: CardType):
		pixmap = QPixmap(self.widgetUtils.getPathByCardType(cardType))
		actionedCardLabel = QLabel()
		actionedCardLabel.setPixmap(pixmap)
		actionedCardLabel.setStyleSheet("background-color: white; border-radius: 5px;")
		actionedCardLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
		reverseOrder = False
		if self.guiHandler.main.gameHandler.windToSide(wind) == "self":
			layout = self.ui.selfActionedCardsLayout
			labelDist = self.selfActionedCardLabels
		elif self.guiHandler.main.gameHandler.windToSide(wind) == "left":
			layout = self.ui.leftActionedCardsLayout
			labelDist = self.leftActionedCardLabels
		elif self.guiHandler.main.gameHandler.windToSide(wind) == "opposite":
			layout = self.ui.oppositeActionedCardsLayout
			labelDist = self.oppositeActionedCardLabels
			reverseOrder = True
		else:
			layout = self.ui.rightActionedCardsLayout
			labelDist = self.rightActionedCardLabels
			reverseOrder = True
		if reverseOrder:
			layout.insertWidget(0, actionedCardLabel)
		else:
			layout.addWidget(actionedCardLabel)
		labelDist[actionedCardLabel] = cardType

	def setupDiscardArea(self):
		horizontalRows = 2
		horizontalCols = 14

		verticalRows = 7
		verticalCols = 4

		self.ui.selfDiscardedLayout.addItem(QSpacerItem(0, 0, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding), horizontalRows, 0, 1, horizontalCols)
		self.ui.selfDiscardedLayout.addItem(QSpacerItem(0, 0, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum), 0, horizontalCols, horizontalRows, 1)

		self.ui.leftDiscardedLayout.addItem(QSpacerItem(0, 0, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding), verticalRows, 0, 1, verticalCols)
		self.ui.leftDiscardedLayout.addItem(QSpacerItem(0, 0, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum), 0, 0, verticalRows, 1)

		self.ui.oppositeDiscardedLayout.addItem(QSpacerItem(0, 0, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding), 0, horizontalRows, 1, horizontalCols)
		self.ui.oppositeDiscardedLayout.addItem(QSpacerItem(0, 0, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum), horizontalCols, 0, horizontalRows, 1)

		self.ui.rightDiscardedLayout.addItem(QSpacerItem(0, 0, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding), 0, 0, 1, verticalCols)
		self.ui.rightDiscardedLayout.addItem(QSpacerItem(0, 0, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum), 0, verticalCols, verticalRows, 1)

	def addDiscardedCard(self, wind: Wind, cardType: CardType):
		pixmap = QPixmap(self.widgetUtils.getPathByCardType(cardType))
		if self.guiHandler.main.gameHandler.windToSide(wind) == "self":
			layout = self.ui.selfDiscardedLayout
			discardedLabelList = self.selfDiscardedLabels
			cols = 14
			row = len(discardedLabelList) // cols
			col = len(discardedLabelList) % cols
		elif self.guiHandler.main.gameHandler.windToSide(wind) == "left":
			layout = self.ui.leftDiscardedLayout
			discardedLabelList = self.leftDiscardedLabels
			rows = 7
			cols = 4
			pixmap = self.widgetUtils.rotatePixmap(pixmap, 90)
			row = len(discardedLabelList) % rows
			col = cols - len(discardedLabelList) // rows
		elif self.guiHandler.main.gameHandler.windToSide(wind) == "opposite":
			layout = self.ui.oppositeDiscardedLayout
			discardedLabelList = self.oppositeDiscardedLabels
			rows = 2
			cols = 14
			pixmap = self.widgetUtils.rotatePixmap(pixmap, 180)
			row = rows - len(discardedLabelList) // cols
			col = cols - len(discardedLabelList) % cols
		else:
			layout = self.ui.rightDiscardedLayout
			discardedLabelList = self.rightDiscardedLabels
			rows = 7
			cols = 4
			pixmap = self.widgetUtils.rotatePixmap(pixmap, 270)
			row = rows - len(discardedLabelList) % rows
			col = len(discardedLabelList) // rows
		label = QLabel()
		label.setPixmap(pixmap)
		label.setStyleSheet("background-color: white; border-radius: 5px;")
		label.setAlignment(Qt.AlignmentFlag.AlignCenter)
		layout.addWidget(label, row, col)
		discardedLabelList[label] = cardType
		self.lastDiscardedLabel = label

	def resizeOtherPlayerCards(self):
		widgetWidth = self.rect().width() * 1 // 12
		widgetHeight = self.rect().height() * 7 // 8
		widgetWidth -= 2
		widgetHeight -= 17
		labelWidth = min(widgetWidth, widgetHeight // 16 * 3 // 2)
		labelHeight = min(widgetWidth // 3 * 2, widgetHeight // 16)
		labelWidth = labelWidth * 4 // 5
		labelHeight = labelHeight * 4 // 5
		for leftAddedCardLabel in self.leftAddedCardLabels:
			leftAddedCardLabel.setFixedSize(labelWidth, labelHeight)
		self.leftGotCardLabel.setFixedSize(labelWidth, labelHeight)

		labelWidth = min(widgetWidth, widgetHeight // 16 * 3 // 2)
		labelHeight = min(widgetWidth // 3 * 2, widgetHeight // 16)
		labelWidth = labelWidth * 4 // 5
		labelHeight = labelHeight * 4 // 5
		for rightAddedCardLabel in self.rightAddedCardLabels:
			rightAddedCardLabel.setFixedSize(labelWidth, labelHeight)
		self.rightGotCardLabel.setFixedSize(labelWidth, labelHeight)

		widgetWidth = self.rect().width() * 10 // 12
		widgetHeight = self.rect().height() * 7 // 48
		widgetWidth -= 17
		widgetHeight -= 2
		labelWidth = min(widgetWidth // 16, widgetHeight // 3 * 2)
		labelWidth = labelWidth * 4 // 5
		labelHeight = min(widgetWidth // 16 // 2 * 3, widgetHeight)
		labelHeight = labelHeight * 4 // 5
		for oppositeAddedCardLabel in self.oppositeAddedCardLabels:
			oppositeAddedCardLabel.setFixedSize(labelWidth, labelHeight)
		self.oppositeGotCardLabel.setFixedSize(labelWidth, labelHeight)

	def resizeDiscardedLabels(self):
		widgetWidth = self.rect().width() * 25 // 42
		widgetHeight = self.rect().height() * 40 // 147
		labelWidth = min((widgetWidth - 78) // 14 , (widgetHeight - 18) // 2 // 3 * 2)
		labelWidth = labelWidth - labelWidth // 5
		labelHeight = min((widgetWidth - 78) // 14 // 2 * 3, (widgetHeight - 18) // 2)
		labelHeight = labelHeight - labelHeight // 5
		if labelWidth < 0 or labelHeight < 0:
			return
		for selfDiscardedLabel, cardType in self.selfDiscardedLabels.items():
			selfDiscardedLabel.setFixedSize(labelWidth, labelHeight)
			pixmap = QPixmap(self.widgetUtils.getPathByCardType(cardType))
			pixmap = self.widgetUtils.rotatePixmap(pixmap, 0)
			pixmap = pixmap.scaled(labelWidth*6/7, labelHeight*6/7)
			selfDiscardedLabel.setPixmap(pixmap)
		for oppositeDiscardedLabel, cardType in self.oppositeDiscardedLabels.items():
			oppositeDiscardedLabel.setFixedSize(labelWidth, labelHeight)
			pixmap = QPixmap(self.widgetUtils.getPathByCardType(cardType))
			pixmap = self.widgetUtils.rotatePixmap(pixmap, 180)
			pixmap = pixmap.scaled(labelWidth*6/7, labelHeight*6/7)
			oppositeDiscardedLabel.setPixmap(pixmap)

		for selfActionedLabel, cardType in self.selfActionedCardLabels.items():
			selfActionedLabel.setFixedSize(labelWidth, labelHeight)
			pixmap = QPixmap(self.widgetUtils.getPathByCardType(cardType))
			pixmap = self.widgetUtils.rotatePixmap(pixmap, 0)
			pixmap = pixmap.scaled(labelWidth*6/7, labelHeight*6/7)
			selfActionedLabel.setPixmap(pixmap)
		for oppositeActionedLabel, cardType in self.oppositeActionedCardLabels.items():
			oppositeActionedLabel.setFixedSize(labelWidth, labelHeight)
			pixmap = QPixmap(self.widgetUtils.getPathByCardType(cardType))
			pixmap = self.widgetUtils.rotatePixmap(pixmap, 180)
			pixmap = pixmap.scaled(labelWidth * 6 / 7, labelHeight * 6 / 7)
			oppositeActionedLabel.setPixmap(pixmap)

		widgetWidth = self.rect().width() * 5 // 21
		widgetHeight = self.rect().height() * 25 // 48
		labelWidth = min((widgetWidth - 30) // 4, (widgetHeight - 48) // 7 * 3 // 2)
		labelWidth = labelWidth - labelWidth // 5
		labelHeight = min((widgetWidth - 30) // 4 // 3 * 2, (widgetHeight - 48) // 7)
		labelHeight = labelHeight - labelHeight // 5
		if labelWidth < 0 or labelHeight < 0:
			return
		for leftDiscardedLabel, cardType in self.leftDiscardedLabels.items():
			leftDiscardedLabel.setFixedSize(labelWidth, labelHeight)
			pixmap = QPixmap(self.widgetUtils.getPathByCardType(cardType))
			pixmap = self.widgetUtils.rotatePixmap(pixmap, 90)
			pixmap = pixmap.scaled(labelWidth*6/7, labelHeight*6/7)
			leftDiscardedLabel.setPixmap(pixmap)
		for rightDiscardedLabel, cardType in self.rightDiscardedLabels.items():
			rightDiscardedLabel.setFixedSize(labelWidth, labelHeight)
			pixmap = QPixmap(self.widgetUtils.getPathByCardType(cardType))
			pixmap = self.widgetUtils.rotatePixmap(pixmap, 270)
			pixmap = pixmap.scaled(labelWidth*6/7, labelHeight*6/7)
			rightDiscardedLabel.setPixmap(pixmap)

		for leftActionedLabel, cardType in self.leftActionedCardLabels.items():
			leftActionedLabel.setFixedSize(labelWidth, labelHeight)
			pixmap = QPixmap(self.widgetUtils.getPathByCardType(cardType))
			pixmap = self.widgetUtils.rotatePixmap(pixmap, 90)
			pixmap = pixmap.scaled(labelWidth*6/7, labelHeight*6/7)
			leftActionedLabel.setPixmap(pixmap)
		for rightActionedLabel, cardType in self.rightActionedCardLabels.items():
			rightActionedLabel.setFixedSize(labelWidth, labelHeight)
			pixmap = QPixmap(self.widgetUtils.getPathByCardType(cardType))
			pixmap = self.widgetUtils.rotatePixmap(pixmap, 270)
			pixmap = pixmap.scaled(labelWidth*6/7, labelHeight*6/7)
			rightActionedLabel.setPixmap(pixmap)

	def playerDiscarded(self, wind: Wind, cardType: CardType):
		self.addDiscardedCard(wind, cardType)
		self.otherPlayerDiscarded(wind)
		self.resizeDiscardedLabels()

	def waitDiscard(self):
		self.waitingForDiscard = True
		self.updateCardButtons()

	def clickedOnCardButton(self, cardType: CardType, clickedButton: QPushButton):
		if self.actionsMenuManager.selectingChowCard is True:
			self.actionsMenuManager.selectedChowCard(cardType, clickedButton)
		if not self.waitingForDiscard:
			return
		self.guiHandler.main.gameHandler.gameManager.setDiscardType(cardType)
		self.updateCardButtons()

	def updateCardButtons(self):
		if not self.actionsMenuManager.selectingChowCard:
			for card in self.addedCards.keys():
				styleSheet, height, width = self.getCardButtonVariables()
				card.setIconSize(QSize(width, height))
				if self.waitingForDiscard:
					styleSheet += "QPushButton:hover { background-color: lightgray; }"
				card.setStyleSheet(styleSheet)

	def getCardButtonVariables(self):
		height = self.ui.selfCards.height() // 4 * 3
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
			# self.ui.selfCards.layout().removeWidget(addedCard)
			addedCard.deleteLater()
		self.addedCards.clear()
		self.startAddCards(cardTypes)

	def gotNewCard(self, cardType: CardType):
		newPushButton = self.widgetUtils.getCardButton(cardType)
		# self.ui.selfCards.layout().addWidget(newPushButton)
		# debugOutput(str(len(self.addedCards)))
		self.ui.newCards.layout().addWidget(newPushButton)
		self.addedCards[newPushButton] = cardType
		self.updateCardButtons()

	def startAddCards(self, cardTypes: list[CardType]):
		for cardType in cardTypes:
			newPushButton = self.widgetUtils.getCardButton(cardType)
			self.ui.handCards.layout().addWidget(newPushButton)
			self.addedCards[newPushButton] = cardType
		self.updateCardButtons()

	def setPlayerWind(self, wind: Wind):
		playerWindPixmaps = self.widgetUtils.getPlayerWindPixmaps(wind)
		self.ui.selfWind.setPixmap(playerWindPixmaps[0])
		self.ui.leftWind.setPixmap(playerWindPixmaps[1])
		self.ui.oppositeWind.setPixmap(playerWindPixmaps[2])
		self.ui.rightWind.setPixmap(playerWindPixmaps[3])
