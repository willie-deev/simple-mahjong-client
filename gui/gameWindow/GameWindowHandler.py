from gui.gameWindow.GameWindowController import GameWindowController
from gui.gameWindow.gameWindow import *


class GameWindowHandler(QMainWindow):
	def __init__(self, guiHandler):
		super().__init__()
		self.ui = Ui_MainWindow()
		self.guiHandler = guiHandler
		self.gameWindowController = GameWindowController(self)

	def setupUi(self):
		self.ui.setupUi(self.guiHandler.mainWindow)
		icon = QIcon("/home/willie/PycharmProjects/simple-mahjong-client/assets/character/1.png")
		print(icon.isNull())
		# self.ui.pushButton.setStyleSheet("background-image : url(assets/character/1.png);")
		self.ui.pushButton.setText("")
		self.ui.pushButton.setStyleSheet("padding: 0;")
		self.ui.pushButton.setIcon(icon)
		print(str(self.ui.pushButton.size().width()) + " " + str(self.ui.pushButton.size().height()))
		self.ui.pushButton.setIconSize(QSize(100, 100))
		self.ui.pushButton.update()

		for i in range(16):
			newPushButton = QPushButton("")
			newPushButton.setObjectName(u"2")
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
			newPushButton.setStyleSheet("padding: 0;")
			newPushButton.setCheckable(False)
			newPushButton.setFlat(False)

			newPushButton.setIcon(icon)
			newPushButton.setIconSize(QSize(100, 100))
			self.ui.selfCards.layout().insertWidget(1, newPushButton)
		self.ui.selfCards.update()
		self.gameWindowController.setPlayerWind.connect(self.setPlayerWind)
		print("inited")

	# self.setPlayerWind(1)

	def setPlayerWind(self, windOrder: int):
		eastPixmap = QPixmap("assets/wind/east.png")
		southPixmap = QPixmap("assets/wind/south.png")
		westPixmap = QPixmap("assets/wind/west.png")
		northPixmap = QPixmap("assets/wind/north.png")
		match windOrder:
			case 0:
				self.ui.selfWind.setPixmap(eastPixmap)
				self.ui.leftWind.setPixmap(southPixmap)
				self.ui.opposideWind.setPixmap(westPixmap)
				self.ui.rightWind.setPixmap(northPixmap)
			case 1:
				self.ui.selfWind.setPixmap(southPixmap)
				self.ui.leftWind.setPixmap(westPixmap)
				self.ui.opposideWind.setPixmap(northPixmap)
				self.ui.rightWind.setPixmap(eastPixmap)
			case 2:
				self.ui.selfWind.setPixmap(westPixmap)
				self.ui.leftWind.setPixmap(northPixmap)
				self.ui.opposideWind.setPixmap(eastPixmap)
				self.ui.rightWind.setPixmap(southPixmap)
			case 3:
				self.ui.selfWind.setPixmap(northPixmap)
				self.ui.leftWind.setPixmap(eastPixmap)
				self.ui.opposideWind.setPixmap(southPixmap)
				self.ui.rightWind.setPixmap(westPixmap)
