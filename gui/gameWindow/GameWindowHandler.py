from pickletools import long1
from shutil import chown
from time import sleep
from typing import Optional

from PySide6.QtCore import QMargins
from PySide6.QtGui import Qt

from game.CardType import CardType
from game.Wind import Wind
from gui.gameWindow.GameWindowController import GameWindowController
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
		self.addedCards = list[QPushButton]()

	def resizeEvent(self, event):
		super().resizeEvent(event)
		self.resizeOverlay()


	def setupUi(self):
		self.ui.setupUi(self)
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
		self.setupActionsMenu()
		self.hideActionsMenu()

		# self.guiHandler.mainWindow.show()
		debugOutput("inited")

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
		self.setupActionsMenu()

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

		chowButton = QPushButton()
		chowButton.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
		chowButton.setText("Chow")
		chowButton.setFont(QFont("Noto Sans", 24))
		sizePolicy = QSizePolicy(chowButton.sizePolicy().horizontalPolicy(), QSizePolicy.Policy.Expanding)
		chowButton.setSizePolicy(sizePolicy)
		chowButton.setStyleSheet("""
			QPushButton {
        		background-color: rgba(0, 0, 0, 100);
        		border-radius: 10px;
    		}
    		QPushButton:hover {
       			background-color: rgba(0, 0, 0, 200);
    		}
    	""")

		pungButton = QPushButton()
		pungButton.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
		pungButton.setText("Pung")
		pungButton.setFont(QFont("Noto Sans", 24))
		sizePolicy = QSizePolicy(pungButton.sizePolicy().horizontalPolicy(), QSizePolicy.Policy.Expanding)
		pungButton.setSizePolicy(sizePolicy)
		pungButton.setStyleSheet("""
			QPushButton {
        		background-color: rgba(0, 0, 0, 100);
        		border-radius: 10px;
    		}
    		QPushButton:hover {
       			background-color: rgba(0, 0, 0, 200);
    		}
    	""")

		kongButton = QPushButton()
		kongButton.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
		kongButton.setText("Kong")
		kongButton.setFont(QFont("Noto Sans", 24))
		sizePolicy = QSizePolicy(kongButton.sizePolicy().horizontalPolicy(), QSizePolicy.Policy.Expanding)
		kongButton.setSizePolicy(sizePolicy)
		kongButton.setStyleSheet("""
			QPushButton {
        		background-color: rgba(0, 0, 0, 100);
        		border-radius: 10px;
    		}
    		QPushButton:hover {
       			background-color: rgba(0, 0, 0, 200);
    		}
    	""")

		tenpaiButton = QPushButton()
		tenpaiButton.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
		tenpaiButton.setText("Ready")
		tenpaiButton.setFont(QFont("Noto Sans", 24))
		sizePolicy = QSizePolicy(tenpaiButton.sizePolicy().horizontalPolicy(), QSizePolicy.Policy.Expanding)
		tenpaiButton.setSizePolicy(sizePolicy)
		tenpaiButton.setStyleSheet("""
			QPushButton {
        		background-color: rgba(0, 0, 0, 100);
        		border-radius: 10px;
    		}
    		QPushButton:hover {
       			background-color: rgba(0, 0, 0, 200);
    		}
    	""")

		winButton = QPushButton()
		winButton.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
		winButton.setText("Win")
		winButton.setFont(QFont("Noto Sans", 24))
		sizePolicy = QSizePolicy(winButton.sizePolicy().horizontalPolicy(), QSizePolicy.Policy.Expanding)
		winButton.setSizePolicy(sizePolicy)
		winButton.setStyleSheet("""
			QPushButton {
        		background-color: rgba(0, 0, 0, 100);
        		border-radius: 10px;
    		}
    		QPushButton:hover {
       			background-color: rgba(0, 0, 0, 200);
    		}
    	""")

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
		layout2.addWidget(tenpaiButton)
		layout2.addWidget(winButton)

	def setFlowerCount(self, wind: Wind, flowerCount: int):
		if wind == self.wind:
			self.setRotatedText(self.ui.selfFlowerCount, str(flowerCount), 0)
		elif self.windToSide(wind) == "left":
			self.setRotatedText(self.ui.leftFlowerCount, str(flowerCount), 90)
		elif self.windToSide(wind) == "opposite":
			self.setRotatedText(self.ui.oppositeFlowerCount, str(flowerCount), 180)
		elif self.windToSide(wind) == "right":
			self.setRotatedText(self.ui.rightFlowerCount, str(flowerCount), 270)

	def sideToWind(self, side: str) -> Wind:
		if self.wind == Wind.EAST:
			if side == "left":
				return Wind.SOUTH
			elif side == "opposite":
				return Wind.WEST
			elif side == "right":
				return Wind.NORTH
		elif self.wind == Wind.SOUTH:
			if side == "left":
				return Wind.WEST
			elif side == "opposite":
				return Wind.NORTH
			elif side == "right":
				return Wind.EAST
		elif self.wind == Wind.WEST:
			if side == "left":
				return Wind.NORTH
			elif side == "opposite":
				return Wind.EAST
			elif side == "right":
				return Wind.SOUTH
		elif self.wind == Wind.NORTH:
			if side == "left":
				return Wind.EAST
			elif side == "opposite":
				return Wind.SOUTH
			elif side == "right":
				return Wind.WEST

	def windToSide(self, target_wind: Wind) -> str:
		if self.wind == Wind.EAST:
			if target_wind == Wind.SOUTH:
				return "left"
			elif target_wind == Wind.WEST:
				return "opposite"
			elif target_wind == Wind.NORTH:
				return "right"
		elif self.wind == Wind.SOUTH:
			if target_wind == Wind.WEST:
				return "left"
			elif target_wind == Wind.NORTH:
				return "opposite"
			elif target_wind == Wind.EAST:
				return "right"
		elif self.wind == Wind.WEST:
			if target_wind == Wind.NORTH:
				return "left"
			elif target_wind == Wind.EAST:
				return "opposite"
			elif target_wind == Wind.SOUTH:
				return "right"
		elif self.wind == Wind.NORTH:
			if target_wind == Wind.EAST:
				return "left"
			elif target_wind == Wind.SOUTH:
				return "opposite"
			elif target_wind == Wind.WEST:
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

	def setPlayerWind(self, wind: Wind):
		self.wind = wind
		eastPixmap = QPixmap("assets/wind/east.png")
		southPixmap = QPixmap("assets/wind/south.png")
		westPixmap = QPixmap("assets/wind/west.png")
		northPixmap = QPixmap("assets/wind/north.png")
		match wind:
			case Wind.EAST:
				self.ui.selfWind.setPixmap(eastPixmap)
				self.ui.leftWind.setPixmap(self.rotatePixmap(southPixmap, 90))
				self.ui.opposideWind.setPixmap(self.rotatePixmap(westPixmap, 180))
				self.ui.rightWind.setPixmap(self.rotatePixmap(northPixmap, 270))
			case Wind.SOUTH:
				self.ui.selfWind.setPixmap(southPixmap)
				self.ui.leftWind.setPixmap(self.rotatePixmap(westPixmap, 90))
				self.ui.opposideWind.setPixmap(self.rotatePixmap(northPixmap, 180))
				self.ui.rightWind.setPixmap(self.rotatePixmap(eastPixmap, 270))
			case Wind.WEST:
				self.ui.selfWind.setPixmap(westPixmap)
				self.ui.leftWind.setPixmap(self.rotatePixmap(northPixmap, 90))
				self.ui.opposideWind.setPixmap(self.rotatePixmap(eastPixmap, 180))
				self.ui.rightWind.setPixmap(self.rotatePixmap(southPixmap, 270))
			case Wind.NORTH:
				self.ui.selfWind.setPixmap(northPixmap)
				self.ui.leftWind.setPixmap(self.rotatePixmap(eastPixmap, 90))
				self.ui.opposideWind.setPixmap(self.rotatePixmap(southPixmap, 180))
				self.ui.rightWind.setPixmap(self.rotatePixmap(westPixmap, 270))

	def rotatePixmap(self, pixmap: QPixmap, degree: int):
		transform = QTransform().rotate(degree)
		return pixmap.transformed(transform)
