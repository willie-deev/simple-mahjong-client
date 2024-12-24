from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QLabel, QSpacerItem, QSizePolicy

from game.CardType import CardType
from game.Wind import Wind


class DiscardUiManager:
	def __init__(self, gameWindowHandler):
		from gui.gameWindow.GameWindowHandler import GameWindowHandler
		self.gameWindowHandler: GameWindowHandler = gameWindowHandler
		self.widgetUtils = self.gameWindowHandler.widgetUtils

		self.selfDiscardedLabels: dict[QLabel, CardType] = {}
		self.leftDiscardedLabels: dict[QLabel, CardType] = {}
		self.oppositeDiscardedLabels: dict[QLabel, CardType] = {}
		self.rightDiscardedLabels: dict[QLabel, CardType] = {}

		self.lastDiscardedLabel: QLabel | None = None

	def setupDiscardArea(self):
		horizontalRows = 2
		horizontalCols = 14

		verticalRows = 7
		verticalCols = 4

		self.gameWindowHandler.ui.selfDiscardedLayout.addItem(QSpacerItem(0, 0, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding), horizontalRows, 0, 1, horizontalCols)
		self.gameWindowHandler.ui.selfDiscardedLayout.addItem(QSpacerItem(0, 0, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum), 0, horizontalCols, horizontalRows, 1)

		self.gameWindowHandler.ui.leftDiscardedLayout.addItem(QSpacerItem(0, 0, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding), verticalRows, 0, 1, verticalCols)
		self.gameWindowHandler.ui.leftDiscardedLayout.addItem(QSpacerItem(0, 0, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum), 0, 0, verticalRows, 1)

		self.gameWindowHandler.ui.oppositeDiscardedLayout.addItem(QSpacerItem(0, 0, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding), 0, horizontalRows, 1, horizontalCols)
		self.gameWindowHandler.ui.oppositeDiscardedLayout.addItem(QSpacerItem(0, 0, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum), horizontalCols, 0, horizontalRows, 1)

		self.gameWindowHandler.ui.rightDiscardedLayout.addItem(QSpacerItem(0, 0, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding), 0, 0, 1, verticalCols)
		self.gameWindowHandler.ui.rightDiscardedLayout.addItem(QSpacerItem(0, 0, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum), 0, verticalCols, verticalRows, 1)

	def removeLastDiscardedLabel(self):
		self.leftDiscardedLabels.pop(self.lastDiscardedLabel, None)
		self.rightDiscardedLabels.pop(self.lastDiscardedLabel, None)
		self.oppositeDiscardedLabels.pop(self.lastDiscardedLabel, None)
		self.selfDiscardedLabels.pop(self.lastDiscardedLabel, None)
		self.lastDiscardedLabel.deleteLater()
		self.resizeDiscardedLabels()

	def playerDiscarded(self, wind: Wind, cardType: CardType):
		self.addDiscardedCard(wind, cardType)
		self.gameWindowHandler.hideOtherPlayerGotCardLabel(wind)
		self.resizeDiscardedLabels()

	def waitDiscard(self):
		self.gameWindowHandler.selfCardUiManager.waitingForDiscard = True
		self.gameWindowHandler.selfCardUiManager.updateCardButtons()

	def addDiscardedCard(self, wind: Wind, cardType: CardType):
		pixmap = QPixmap(self.widgetUtils.getPathByCardType(cardType))
		if self.gameWindowHandler.guiHandler.main.gameHandler.windToSide(wind) == "self":
			layout = self.gameWindowHandler.ui.selfDiscardedLayout
			discardedLabelList = self.selfDiscardedLabels
			cols = 14
			row = len(discardedLabelList) // cols
			col = len(discardedLabelList) % cols
		elif self.gameWindowHandler.guiHandler.main.gameHandler.windToSide(wind) == "left":
			layout = self.gameWindowHandler.ui.leftDiscardedLayout
			discardedLabelList = self.leftDiscardedLabels
			rows = 7
			cols = 4
			pixmap = self.widgetUtils.rotatePixmap(pixmap, 90)
			row = len(discardedLabelList) % rows
			col = cols - len(discardedLabelList) // rows
		elif self.gameWindowHandler.guiHandler.main.gameHandler.windToSide(wind) == "opposite":
			layout = self.gameWindowHandler.ui.oppositeDiscardedLayout
			discardedLabelList = self.oppositeDiscardedLabels
			rows = 2
			cols = 14
			pixmap = self.widgetUtils.rotatePixmap(pixmap, 180)
			row = rows - len(discardedLabelList) // cols
			col = cols - len(discardedLabelList) % cols
		else:
			layout = self.gameWindowHandler.ui.rightDiscardedLayout
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

	def resizeDiscardedLabels(self):
		widgetWidth = self.gameWindowHandler.rect().width() * 25 // 42
		widgetHeight = self.gameWindowHandler.rect().height() * 40 // 147
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

		for selfActionedLabel, cardType in self.gameWindowHandler.selfActionedCardLabels.items():
			selfActionedLabel.setFixedSize(labelWidth, labelHeight)
			pixmap = QPixmap(self.widgetUtils.getPathByCardType(cardType))
			pixmap = self.widgetUtils.rotatePixmap(pixmap, 0)
			pixmap = pixmap.scaled(labelWidth*6/7, labelHeight*6/7)
			selfActionedLabel.setPixmap(pixmap)
		for oppositeActionedLabel, cardType in self.gameWindowHandler.oppositeActionedCardLabels.items():
			oppositeActionedLabel.setFixedSize(labelWidth, labelHeight)
			pixmap = QPixmap(self.widgetUtils.getPathByCardType(cardType))
			pixmap = self.widgetUtils.rotatePixmap(pixmap, 180)
			pixmap = pixmap.scaled(labelWidth * 6 / 7, labelHeight * 6 / 7)
			oppositeActionedLabel.setPixmap(pixmap)

		widgetWidth = self.gameWindowHandler.rect().width() * 5 // 21
		widgetHeight = self.gameWindowHandler.rect().height() * 25 // 48
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

		for leftActionedLabel, cardType in self.gameWindowHandler.leftActionedCardLabels.items():
			leftActionedLabel.setFixedSize(labelWidth, labelHeight)
			pixmap = QPixmap(self.widgetUtils.getPathByCardType(cardType))
			pixmap = self.widgetUtils.rotatePixmap(pixmap, 90)
			pixmap = pixmap.scaled(labelWidth*6/7, labelHeight*6/7)
			leftActionedLabel.setPixmap(pixmap)
		for rightActionedLabel, cardType in self.gameWindowHandler.rightActionedCardLabels.items():
			rightActionedLabel.setFixedSize(labelWidth, labelHeight)
			pixmap = QPixmap(self.widgetUtils.getPathByCardType(cardType))
			pixmap = self.widgetUtils.rotatePixmap(pixmap, 270)
			pixmap = pixmap.scaled(labelWidth*6/7, labelHeight*6/7)
			rightActionedLabel.setPixmap(pixmap)