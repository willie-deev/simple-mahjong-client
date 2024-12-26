from PySide6.QtCore import QSize, Qt
from PySide6.QtGui import QPixmap, QIcon, QFont, QTransform, QPainter
from PySide6.QtWidgets import QPushButton, QSizePolicy, QLabel, QWidget

from game.CardType import CardType
from game.Wind import Wind


class WidgetManager:
	def __init__(self, gameWindowHandler):
		self.gameWindowHandler = gameWindowHandler

	def getCardButton(self, cardType: CardType):
		pixmap = QPixmap(self.getPathByCardType(cardType))
		scaled_pixmap = pixmap.scaled(600, 800)
		icon = QIcon(scaled_pixmap)
		newPushButton = QPushButton()
		# newPushButton.setObjectName(u"2")
		sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum)
		sizePolicy1.setHorizontalStretch(0)
		sizePolicy1.setVerticalStretch(0)
		sizePolicy1.setHeightForWidth(newPushButton.sizePolicy().hasHeightForWidth())
		newPushButton.setSizePolicy(sizePolicy1)
		newPushButton.setMinimumSize(QSize(1, 1))
		newPushButton.setMaximumSize(QSize(16777215, 16777215))
		# newPushButton.setMaximumSize(QSize(70, 100))
		newPushButton.setBaseSize(QSize(0, 0))
		font = QFont()
		font.setPointSize(12)
		font.setBold(False)
		font.setStrikeOut(False)
		font.setKerning(True)
		newPushButton.setFont(font)
		# newPushButton.setStyleSheet(f"padding: 0px;")
		newPushButton.setCheckable(False)
		newPushButton.setFlat(False)

		newPushButton.setIcon(icon)
		newPushButton.setIconSize(QSize(60, 80))

		newPushButton.clicked.connect(lambda _: self.gameWindowHandler.selfCardUiManager.clickedOnCardButton(cardType, newPushButton))

		return newPushButton

	def getHideCardLabel(self):
		newLabel = QLabel()
		sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum)
		# sizePolicy1.setHorizontalStretch(0)
		# sizePolicy1.setVerticalStretch(0)
		# sizePolicy1.setHeightForWidth(newLabel.sizePolicy().hasHeightForWidth())
		# sizePolicy1.setWidthForHeight(True)
		newLabel.setSizePolicy(sizePolicy1)
		# newLabel.setMinimumSize(QSize(1, 1))
		newLabel.setMaximumSize(QSize(16777215, 16777215))
		# newLabel.setBaseSize(QSize(0, 0))

		newLabel.setStyleSheet("background-color: gray; border-radius: 5px;")

		return newLabel

	def getPathByCardType(self, cardType: CardType):
		if cardType is None:
			return None
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
		return path

	def getPlayerWindPixmaps(self, wind: Wind):
		windPixmaps = [
			QPixmap("assets/wind/east.png"),
			QPixmap("assets/wind/south.png"),
			QPixmap("assets/wind/west.png"),
			QPixmap("assets/wind/north.png")
		]
		playerWindPixmaps = []
		match wind:
			case Wind.EAST:
				for i in range(4):
					rotatedImage = self.rotatePixmap(windPixmaps[i], 90 * len(playerWindPixmaps))
					playerWindPixmaps.append(rotatedImage)
			case Wind.SOUTH:
				for i in range(1, 4):
					rotatedImage = self.rotatePixmap(windPixmaps[i], 90 * len(playerWindPixmaps))
					playerWindPixmaps.append(rotatedImage)
				for i in range(1):
					rotatedImage = self.rotatePixmap(windPixmaps[i], 90 * len(playerWindPixmaps))
					playerWindPixmaps.append(rotatedImage)
			case Wind.WEST:
				for i in range(2, 4):
					rotatedImage = self.rotatePixmap(windPixmaps[i], 90 * len(playerWindPixmaps))
					playerWindPixmaps.append(rotatedImage)
				for i in range(2):
					rotatedImage = self.rotatePixmap(windPixmaps[i], 90 * len(playerWindPixmaps))
					playerWindPixmaps.append(rotatedImage)
			case Wind.NORTH:
				for i in range(3, 4):
					rotatedImage = self.rotatePixmap(windPixmaps[i], 90 * len(playerWindPixmaps))
					playerWindPixmaps.append(rotatedImage)
				for i in range(3):
					rotatedImage = self.rotatePixmap(windPixmaps[i], 90 * len(playerWindPixmaps))
					playerWindPixmaps.append(rotatedImage)
		return playerWindPixmaps

	def rotatePixmap(self, pixmap: QPixmap, degree: int):
		transform = QTransform().rotate(degree)
		return pixmap.transformed(transform)

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

	def getActionButton(self, name: str, text: str):
		button = QPushButton(name)
		button.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
		button.setText(text)
		button.setFont(QFont("Noto Sans", 24))
		sizePolicy = QSizePolicy(button.sizePolicy().horizontalPolicy(), QSizePolicy.Policy.Expanding)
		button.setSizePolicy(sizePolicy)
		button.setStyleSheet("""
					QPushButton {
		        		background-color: rgba(0, 0, 0, 100);
		        		border-radius: 10px;
		    		}
		    		QPushButton:hover {
		       			background-color: rgba(0, 0, 0, 200);
		    		}
		    	""")
		return button

