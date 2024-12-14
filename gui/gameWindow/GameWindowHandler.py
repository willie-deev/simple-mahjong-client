from gui.gameWindow.gameWindow import *


class GameWindowHandler(QMainWindow):
	def __init__(self, guiHandler):
		super().__init__()
		self.ui = Ui_MainWindow()
		self.guiHandler = guiHandler

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
