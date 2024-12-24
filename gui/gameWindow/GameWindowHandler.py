from PySide6.QtCore import QTimer
from PySide6.QtGui import Qt

from game.CardType import CardType
from game.Wind import Wind
from gui.gameWindow.ActionsMenuManager import ActionsMenuManager
from gui.gameWindow.DiscardUiManager import DiscardUiManager
from gui.gameWindow.GameWindowController import GameWindowController
from gui.gameWindow.SelfCardUiManager import SelfCardUiManager
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
		self.selfCardUiManager = SelfCardUiManager(self)
		self.discardUiManager = DiscardUiManager(self)

	def resizeEvent(self, event):
		super().resizeEvent(event)
		self.actionsMenuManager.resizeOverlay()
		self.selfCardUiManager.updateCardButtons()
		self.discardUiManager.resizeDiscardedLabels()
		self.resizeOtherPlayerCards()

	def showEvent(self, event):
		super().showEvent(event)
		self.discardUiManager.resizeDiscardedLabels()

	def changeEvent(self, event):
		super().changeEvent(event)
		self.actionsMenuManager.resizeOverlay()
		self.selfCardUiManager.updateCardButtons()
		self.discardUiManager.resizeDiscardedLabels()
		QTimer.singleShot(1, self.selfCardUiManager.updateCardButtons)

	def setupUi(self):
		self.ui.setupUi(self)
		icon = QIcon("/home/willie/PycharmProjects/simple-mahjong-client/assets/character/1.png")
		debugOutput(icon.isNull())

		self.ui.selfCards.update()
		self.gameWindowController.setPlayerWind.connect(self.setPlayerWind)
		self.gameWindowController.startAddCards.connect(self.selfCardUiManager.startAddCards)
		self.gameWindowController.setAllCards.connect(self.selfCardUiManager.setAllCards)
		# self.gameWindowController.setFlowerCount.connect(self.setFlowerCount)
		self.gameWindowController.gotNewCard.connect(self.selfCardUiManager.gotNewCard)
		self.gameWindowController.waitDiscard.connect(self.discardUiManager.waitDiscard)
		self.gameWindowController.playerDiscarded.connect(self.discardUiManager.playerDiscarded)
		self.gameWindowController.otherPlayerGotCard.connect(self.showOtherPlayerGotCardLabel)
		self.gameWindowController.canDoActions.connect(self.actionsMenuManager.showActionsMenu)
		self.gameWindowController.performedCardAction.connect(self.performedCardAction)
		self.gameWindowController.notPerformedCardAction.connect(self.notPerformedCardAction)

		self.actionsMenuManager.setupActionsMenu()
		self.actionsMenuManager.hideActionsMenu()

		self.discardUiManager.setupDiscardArea()
		self.setupOtherPlayerCardLabels()

		# self.guiHandler.mainWindow.show()
		debugOutput("inited")

	def setupOtherPlayerCardLabels(self):
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

	def notPerformedCardAction(self):
		self.actionsMenuManager.cancelCardAction()

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

		self.discardUiManager.removeLastDiscardedLabel()

	def showOtherPlayerGotCardLabel(self, wind: Wind):
		if self.guiHandler.main.gameHandler.windToSide(wind) == "left":
			self.leftGotCardLabel.show()
		elif self.guiHandler.main.gameHandler.windToSide(wind) == "opposite":
			self.oppositeGotCardLabel.show()
		else:
			self.rightGotCardLabel.show()
		self.resizeOtherPlayerCards()

	def hideOtherPlayerGotCardLabel(self, wind: Wind):
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

	def setPlayerWind(self, wind: Wind):
		playerWindPixmaps = self.widgetUtils.getPlayerWindPixmaps(wind)
		self.ui.selfWind.setPixmap(playerWindPixmaps[0])
		self.ui.leftWind.setPixmap(playerWindPixmaps[1])
		self.ui.oppositeWind.setPixmap(playerWindPixmaps[2])
		self.ui.rightWind.setPixmap(playerWindPixmaps[3])
