from typing import Optional

from PySide6.QtCore import QTimer
from PySide6.QtGui import Qt
from PySide6.QtWidgets import QPushButton

from game.CardType import CardType
from game.Wind import Wind
from gui.gameWindow.GameWindowController import GameWindowController
from gui.gameWindow.WidgetUtils import WidgetManager
from gui.gameWindow.gameWindow import *
from utils.debugUtils import debugOutput


class GameWindowHandler(QMainWindow):
	def __init__(self, guiHandler):
		super().__init__()
		self.overlay: Optional[QWidget] = None
		self.wind = None
		self.ui = Ui_MainWindow()
		self.guiHandler = guiHandler
		self.gameWindowController = GameWindowController(self)
		self.widgetUtils = WidgetManager(self)
		self.addedCards = list[QPushButton]()
		self.waitingForDiscard = False
		self.selfDiscardedLabels: list[QLabel] = []
		self.leftDiscardedLabels: list[QLabel] = []
		self.oppositeDiscardedLabels: list[QLabel] = []
		self.rightDiscardedLabels: list[QLabel] = []

	def resizeEvent(self, event):
		super().resizeEvent(event)
		self.resizeOverlay()
		self.updateCardButtons()
		self.resizeDiscardedLabels()

	def showEvent(self, event):
		super().showEvent(event)
		self.resizeDiscardedLabels()

	def changeEvent(self, event):
		super().changeEvent(event)
		self.resizeOverlay()
		self.updateCardButtons()
		self.resizeDiscardedLabels()

	def setupUi(self):
		self.ui.setupUi(self)
		icon = QIcon("/home/willie/PycharmProjects/simple-mahjong-client/assets/character/1.png")
		debugOutput(icon.isNull())

		self.ui.selfCards.update()
		self.gameWindowController.setPlayerWind.connect(self.setPlayerWind)
		self.gameWindowController.startAddCards.connect(self.startAddCards)
		self.gameWindowController.setAllCards.connect(self.setAllCards)
		self.gameWindowController.setFlowerCount.connect(self.setFlowerCount)
		self.gameWindowController.gotNewCard.connect(self.gotNewCard)
		self.gameWindowController.waitDiscard.connect(self.waitDiscard)
		self.gameWindowController.playerDiscarded.connect(self.playerDiscarded)

		self.widgetUtils.setupFlowerIcons()
		self.setupActionsMenu()
		self.hideActionsMenu()

		self.setupDiscardArea()

		# self.guiHandler.mainWindow.show()
		debugOutput("inited")

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
		if wind == self.wind:
			layout = self.ui.selfDiscardedLayout
			discardedLabelList = self.selfDiscardedLabels
			cols = 14
			row = len(discardedLabelList) // cols
			col = len(discardedLabelList) % cols
		elif self.widgetUtils.windToSide(wind) == "left":
			layout = self.ui.leftDiscardedLayout
			discardedLabelList = self.leftDiscardedLabels
			rows = 7
			cols = 4
			pixmap = self.widgetUtils.rotatePixmap(pixmap, 90)
			row = len(discardedLabelList) % rows
			col = cols - len(discardedLabelList) // rows
		elif self.widgetUtils.windToSide(wind) == "opposite":
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
		label.setStyleSheet("background-color: white; border-radius: 10px;")
		label.setAlignment(Qt.AlignmentFlag.AlignCenter)
		layout.addWidget(label, row, col)
		discardedLabelList.append(label)

	def resizeDiscardedLabels(self):
		widgetWidth = self.rect().width() * 25 // 42
		widgetHeight = self.rect().height() * 40 // 147
		labelWidth = min((widgetWidth - 78) // 14 , (widgetHeight - 18) // 2 // 3 * 2)
		labelWidth = labelWidth - labelWidth // 5
		labelHeight = min((widgetWidth - 78) // 14 // 2 * 3, (widgetHeight - 18) // 2)
		labelHeight = labelHeight - labelHeight // 5
		if labelWidth < 0 or labelHeight < 0:
			return
		for selfDiscardedLabel in self.selfDiscardedLabels:
			selfDiscardedLabel.setFixedSize(labelWidth, labelHeight)
		for oppositeDiscardedLabel in self.oppositeDiscardedLabels:
			oppositeDiscardedLabel.setFixedSize(labelWidth, labelHeight)

		widgetWidth = self.rect().width() * 5 // 21
		widgetHeight = self.rect().height() * 25 // 48
		labelWidth = min((widgetWidth - 30) // 4, (widgetHeight - 48) // 7 * 3 // 2)
		labelWidth = labelWidth - labelWidth // 5
		labelHeight = min((widgetWidth - 30) // 4 // 3 * 2, (widgetHeight - 48) // 7)
		labelHeight = labelHeight - labelHeight // 5
		if labelWidth < 0 or labelHeight < 0:
			return
		for leftDiscardedLabel in self.leftDiscardedLabels:
			leftDiscardedLabel.setFixedSize(labelWidth, labelHeight)
		for rightDiscardedLabel in self.rightDiscardedLabels:
			rightDiscardedLabel.setFixedSize(labelWidth, labelHeight)


	def playerDiscarded(self, wind: Wind, cardType: CardType):
		for i in range(10):
			self.addDiscardedCard(Wind.EAST, CardType.FLOWER)
			self.addDiscardedCard(Wind.SOUTH, CardType.FLOWER)
			self.addDiscardedCard(Wind.WEST, CardType.FLOWER)
			self.addDiscardedCard(Wind.NORTH, CardType.FLOWER)

	def waitDiscard(self):
		self.waitingForDiscard = True
		self.updateCardButtons()

	def discard(self, cardType: CardType):
		if not self.waitingForDiscard:
			return
		self.guiHandler.main.gameHandler.gameManager.setDiscardType(cardType)
		self.updateCardButtons()

	def updateCardButtons(self):
		for card in self.addedCards:
			height = self.ui.selfCards.height() // 4 * 3
			width = height // 3 * 2
			padding = width // 7
			borderRadius = padding
			card.setIconSize(QSize(width, height))
			styleSheet = "QPushButton{"
			styleSheet += "padding-left: " + str(padding) + "px;"
			styleSheet += "padding-right: " + str(padding) + "px;"
			styleSheet += "background-color: white; border-radius: "+ str(borderRadius)+ "px;"
			styleSheet += "}"
			if self.waitingForDiscard:
				# card.setEnabled(False)
				styleSheet += "QPushButton:hover { background-color: lightgray; }"
			card.setStyleSheet(styleSheet)

	def resizeOverlay(self):
		if self.overlay is not None and not self.overlay.isHidden():
			maxWidth = self.overlay.maximumWidth()
			maxHeight = self.overlay.maximumHeight()
			width = self.rect().width()//2
			height = self.rect().height()//6
			exceedWidth = 0
			exceedHeight = 0
			if width > maxWidth:
				exceedWidth = width - maxWidth
				width =  maxWidth
			if height > maxHeight:
				exceedHeight = height - maxHeight
				height = maxHeight
			posX = int(self.rect().width()//4 + exceedWidth//2)
			posY = int(self.rect().height() - self.ui.selfCards.height() - height + exceedHeight//2)
			self.overlay.setGeometry(posX, posY, width, height)

	def showActionsMenu(self):
		self.overlay.show()

	def hideActionsMenu(self):
		self.overlay.hide()

	def setupActionsMenu(self):
		self.overlay = QWidget(self)
		# self.overlay.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents)
		self.overlay.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
		self.overlay.setSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Maximum)
		self.overlay.setMaximumSize(QSize(600, 100))
		self.overlay.setStyleSheet("background: rgba(0, 0, 0, 50);")

		self.resizeOverlay()

		chowButton = self.widgetUtils.getActionButton("chow", "Chow")
		pungButton = self.widgetUtils.getActionButton("pung", "Pung")
		kongButton = self.widgetUtils.getActionButton("kong", "Kong")
		readyButton = self.widgetUtils.getActionButton("ready", "Ready")
		winButton = self.widgetUtils.getActionButton("win", "Win")

		expandingLabel = QWidget(self.overlay)
		expandingLabel.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

		layout = QHBoxLayout(self.overlay)
		layout.setContentsMargins(0, 0, 0, 0)
		layout.addWidget(expandingLabel)

		layout2 = QHBoxLayout(expandingLabel)
		layout2.setContentsMargins(20, 20, 20, 20)
		layout2.setSpacing(20)
		layout2.addWidget(chowButton)
		layout2.addWidget(pungButton)
		layout2.addWidget(kongButton)
		layout2.addWidget(readyButton)
		layout2.addWidget(winButton)

	def setFlowerCount(self, wind: Wind, flowerCount: int):
		if wind == self.wind:
			self.widgetUtils.setRotatedText(self.ui.selfFlowerCount, str(flowerCount), 0)
		elif self.widgetUtils.windToSide(wind) == "left":
			self.widgetUtils.setRotatedText(self.ui.leftFlowerCount, str(flowerCount), 90)
		elif self.widgetUtils.windToSide(wind) == "opposite":
			self.widgetUtils.setRotatedText(self.ui.oppositeFlowerCount, str(flowerCount), 180)
		elif self.widgetUtils.windToSide(wind) == "right":
			self.widgetUtils.setRotatedText(self.ui.rightFlowerCount, str(flowerCount), 270)

	def setAllCards(self, cardTypes: list[CardType]):
		for addedCard in self.addedCards:
			# self.ui.selfCards.layout().removeWidget(addedCard)
			addedCard.deleteLater()
		self.addedCards.clear()
		self.startAddCards(cardTypes)

	def gotNewCard(self, cardType: CardType):
		newPushButton = self.widgetUtils.getCardButton(cardType)
		# self.ui.selfCards.layout().addWidget(newPushButton)
		# debugOutput(str(len(self.addedCards)))
		self.ui.newCards.layout().addWidget(newPushButton)
		self.addedCards.append(newPushButton)
		self.updateCardButtons()

	def startAddCards(self, cardTypes: list[CardType]):
		for cardType in cardTypes:
			newPushButton = self.widgetUtils.getCardButton(cardType)
			self.ui.handCards.layout().addWidget(newPushButton)
			self.addedCards.append(newPushButton)
		self.updateCardButtons()

	def setPlayerWind(self, wind: Wind):
		self.wind = wind
		playerWindPixmaps = self.widgetUtils.getPlayerWindPixmaps(wind)
		self.ui.selfWind.setPixmap(playerWindPixmaps[0])
		self.ui.leftWind.setPixmap(playerWindPixmaps[1])
		self.ui.oppositeWind.setPixmap(playerWindPixmaps[2])
		self.ui.rightWind.setPixmap(playerWindPixmaps[3])
