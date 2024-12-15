from PySide6.QtWidgets import QPushButton

from game.CardType import CardType
from game.Winds import Winds
from gui.gameWindow.GameWindowController import GameWindowController
from gui.gameWindow.gameWindow import *
from utils.debugUtils import debugOutput


class GameWindowHandler(QMainWindow):
	def __init__(self, guiHandler):
		super().__init__()
		self.ui = Ui_MainWindow()
		self.guiHandler = guiHandler
		self.gameWindowController = GameWindowController(self)
		self.addedCards = list[QPushButton]()

	def setupUi(self):
		self.ui.setupUi(self.guiHandler.mainWindow)
		icon = QIcon("/home/willie/PycharmProjects/simple-mahjong-client/assets/character/1.png")
		debugOutput(icon.isNull())

		self.ui.selfCards.update()
		self.gameWindowController.setPlayerWind.connect(self.setPlayerWind)
		self.gameWindowController.addCards.connect(self.gotCards)
		self.gameWindowController.setAllCards.connect(self.setAllCards)
		debugOutput("inited")

	def setAllCards(self, cardTypes: list[CardType]):
		for addedCard in self.addedCards:
			# self.ui.selfCards.layout().removeWidget(addedCard)
			addedCard.deleteLater()
		self.addedCards.clear()
		self.gotCards(cardTypes)

	def gotCards(self, cardTypes: list[CardType]):
		for cardType in cardTypes:
			if "CHARACTER" in cardType.name:
				number = cardType.name.split("_")[1]
				path = f"assets/character/{number}.png"
			elif "DOT" in cardType.name:
				number = cardType.name.split("_")[1]
				path = f"assets/dot/{number}.png"
			elif "BAMBOO" in cardType.name:
				number = cardType.name.split("_")[1]
				path = f"assets/bamboo/{number}.png"
			elif "WIND" in cardType.name:
				wind = cardType.name.split("_")[0].lower()
				path = f"assets/wind/{wind}.png"
			elif "DRAGON" in cardType.name:
				dragon = cardType.name.split("_")[0].lower()
				path = f"assets/dragon/{dragon}.png"
			else:
				path = f"assets/flower/flower.png"
			pixmap = QPixmap(path)
			scaled_pixmap = pixmap.scaled(60, 80)
			icon = QIcon(scaled_pixmap)
			newPushButton = QPushButton("")
			# newPushButton.setObjectName(u"2")
			sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
			sizePolicy1.setHorizontalStretch(0)
			sizePolicy1.setVerticalStretch(0)
			sizePolicy1.setHeightForWidth(newPushButton.sizePolicy().hasHeightForWidth())
			newPushButton.setSizePolicy(sizePolicy1)
			newPushButton.setMinimumSize(QSize(1, 1))
			newPushButton.setMaximumSize(QSize(70, 100))
			newPushButton.setBaseSize(QSize(0, 0))
			font = QFont()
			font.setPointSize(12)
			font.setBold(False)
			font.setStrikeOut(False)
			font.setKerning(True)
			newPushButton.setFont(font)
			newPushButton.setStyleSheet(f"padding: 0px;")
			newPushButton.setCheckable(False)
			newPushButton.setFlat(False)

			newPushButton.setIcon(icon)
			newPushButton.setIconSize(QSize(60, 80))
			self.ui.selfCards.layout().insertWidget(1, newPushButton)
			self.addedCards.append(newPushButton)

	def setPlayerWind(self, wind: Winds):
		eastPixmap = QPixmap("assets/wind/east.png")
		southPixmap = QPixmap("assets/wind/south.png")
		westPixmap = QPixmap("assets/wind/west.png")
		northPixmap = QPixmap("assets/wind/north.png")
		match wind:
			case Winds.EAST:
				self.ui.selfWind.setPixmap(eastPixmap)
				self.ui.leftWind.setPixmap(southPixmap)
				self.ui.opposideWind.setPixmap(westPixmap)
				self.ui.rightWind.setPixmap(northPixmap)
			case Winds.SOUTH:
				self.ui.selfWind.setPixmap(southPixmap)
				self.ui.leftWind.setPixmap(westPixmap)
				self.ui.opposideWind.setPixmap(northPixmap)
				self.ui.rightWind.setPixmap(eastPixmap)
			case Winds.WEST:
				self.ui.selfWind.setPixmap(westPixmap)
				self.ui.leftWind.setPixmap(northPixmap)
				self.ui.opposideWind.setPixmap(eastPixmap)
				self.ui.rightWind.setPixmap(southPixmap)
			case Winds.NORTH:
				self.ui.selfWind.setPixmap(northPixmap)
				self.ui.leftWind.setPixmap(eastPixmap)
				self.ui.opposideWind.setPixmap(southPixmap)
				self.ui.rightWind.setPixmap(westPixmap)
