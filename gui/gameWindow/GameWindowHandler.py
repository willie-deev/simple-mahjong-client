from PySide6.QtWidgets import QPushButton

from game.CardType import CardType
from game.Winds import Winds
from gui.gameWindow.GameWindowController import GameWindowController
from gui.gameWindow.gameWindow import *
from utils.debugUtils import debugOutput


class GameWindowHandler(QMainWindow):
	def __init__(self, guiHandler):
		super().__init__()
		self.wind = None
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
		self.gameWindowController.setFlowerCount.connect(self.setFlowerCount)

		flowerPixmap = QPixmap("assets/flower/flower.png").scaledToHeight(48)
		self.ui.selfFlowerIcon.setPixmap(flowerPixmap)
		self.ui.leftFlowerIcon.setPixmap(self.rotatePixmap(flowerPixmap, 90))
		self.ui.oppositeFlowerIcon.setPixmap(self.rotatePixmap(flowerPixmap, 180))
		self.ui.rightFlowerIcon.setPixmap(self.rotatePixmap(flowerPixmap, 270))

		self.setRotatedText(self.ui.selfFlowerCount, "0", 0)
		self.setRotatedText(self.ui.leftFlowerCount, "0", 90)
		self.setRotatedText(self.ui.oppositeFlowerCount, "0", 180)
		self.setRotatedText(self.ui.rightFlowerCount, "0", 270)
		debugOutput("inited")

	def setFlowerCount(self, wind: Winds, flowerCount: int):
		if wind == self.wind:
			self.setRotatedText(self.ui.selfFlowerCount, str(flowerCount), 0)
		elif self.windToSide(wind) == "left":
			self.setRotatedText(self.ui.leftFlowerCount, str(flowerCount), 90)
		elif self.windToSide(wind) == "opposite":
			self.setRotatedText(self.ui.oppositeFlowerCount, str(flowerCount), 180)
		elif self.windToSide(wind) == "right":
			self.setRotatedText(self.ui.rightFlowerCount, str(flowerCount), 270)

	def sideToWind(self, side: str) -> Winds:
		if self.wind == Winds.EAST:
			if side == "left":
				return Winds.SOUTH
			elif side == "opposite":
				return Winds.WEST
			elif side == "right":
				return Winds.NORTH
		elif self.wind == Winds.SOUTH:
			if side == "left":
				return Winds.WEST
			elif side == "opposite":
				return Winds.NORTH
			elif side == "right":
				return Winds.EAST
		elif self.wind == Winds.WEST:
			if side == "left":
				return Winds.NORTH
			elif side == "opposite":
				return Winds.EAST
			elif side == "right":
				return Winds.SOUTH
		elif self.wind == Winds.NORTH:
			if side == "left":
				return Winds.EAST
			elif side == "opposite":
				return Winds.SOUTH
			elif side == "right":
				return Winds.WEST

	def windToSide(self, target_wind: Winds) -> str:
		if self.wind == Winds.EAST:
			if target_wind == Winds.SOUTH:
				return "left"
			elif target_wind == Winds.WEST:
				return "opposite"
			elif target_wind == Winds.NORTH:
				return "right"
		elif self.wind == Winds.SOUTH:
			if target_wind == Winds.WEST:
				return "left"
			elif target_wind == Winds.NORTH:
				return "opposite"
			elif target_wind == Winds.EAST:
				return "right"
		elif self.wind == Winds.WEST:
			if target_wind == Winds.NORTH:
				return "left"
			elif target_wind == Winds.EAST:
				return "opposite"
			elif target_wind == Winds.SOUTH:
				return "right"
		elif self.wind == Winds.NORTH:
			if target_wind == Winds.EAST:
				return "left"
			elif target_wind == Winds.SOUTH:
				return "opposite"
			elif target_wind == Winds.WEST:
				return "right"

	def setRotatedText(self, widget: QLabel, text: str, degree: int):
		if degree == 90 or degree == 270:
			width = widget.size().height()
			height = widget.size().width()
			height = height // 2
		else:
			width = widget.size().width()
			height = widget.size().height()
			width = width // 2
		pixmap = QPixmap(width, height)
		pixmap.fill(Qt.GlobalColor.transparent)
		painter = QPainter(pixmap)
		painter.translate(pixmap.rect().center())
		painter.rotate(degree)
		font = QFont()
		font.setPointSize(24)  # Set desired font size
		painter.setFont(font)
		painter.drawText(-width // 2, -height // 2, width, height, Qt.AlignmentFlag.AlignCenter, text)
		painter.end()
		widget.setPixmap(pixmap)
		widget.update()

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
			sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)
			sizePolicy1.setHorizontalStretch(0)
			sizePolicy1.setVerticalStretch(0)
			sizePolicy1.setHeightForWidth(newPushButton.sizePolicy().hasHeightForWidth())
			newPushButton.setSizePolicy(sizePolicy1)
			newPushButton.setMinimumSize(QSize(1, 1))
			newPushButton.setMaximumSize(QSize(16777215, 100))
			# newPushButton.setMaximumSize(QSize(70, 100))
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
		self.wind = wind
		eastPixmap = QPixmap("assets/wind/east.png")
		southPixmap = QPixmap("assets/wind/south.png")
		westPixmap = QPixmap("assets/wind/west.png")
		northPixmap = QPixmap("assets/wind/north.png")
		match wind:
			case Winds.EAST:
				self.ui.selfWind.setPixmap(eastPixmap)
				self.ui.leftWind.setPixmap(self.rotatePixmap(southPixmap, 90))
				self.ui.opposideWind.setPixmap(self.rotatePixmap(westPixmap, 180))
				self.ui.rightWind.setPixmap(self.rotatePixmap(northPixmap, 270))
			case Winds.SOUTH:
				self.ui.selfWind.setPixmap(southPixmap)
				self.ui.leftWind.setPixmap(self.rotatePixmap(westPixmap, 90))
				self.ui.opposideWind.setPixmap(self.rotatePixmap(northPixmap, 180))
				self.ui.rightWind.setPixmap(self.rotatePixmap(eastPixmap, 270))
			case Winds.WEST:
				self.ui.selfWind.setPixmap(westPixmap)
				self.ui.leftWind.setPixmap(self.rotatePixmap(northPixmap, 90))
				self.ui.opposideWind.setPixmap(self.rotatePixmap(eastPixmap, 180))
				self.ui.rightWind.setPixmap(self.rotatePixmap(southPixmap, 270))
			case Winds.NORTH:
				self.ui.selfWind.setPixmap(northPixmap)
				self.ui.leftWind.setPixmap(self.rotatePixmap(eastPixmap, 90))
				self.ui.opposideWind.setPixmap(self.rotatePixmap(southPixmap, 180))
				self.ui.rightWind.setPixmap(self.rotatePixmap(westPixmap, 270))

	def rotatePixmap(self, pixmap: QPixmap, degree: int):
		transform = QTransform().rotate(degree)
		return pixmap.transformed(transform)
