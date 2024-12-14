from gui.gameWindow.gameWindow import *


class GameWindowHandler(QMainWindow):
	def __init__(self, guiHandler):
		super().__init__()
		self.ui = Ui_MainWindow()
		self.guiHandler = guiHandler

	def setupUi(self):
		self.ui.setupUi(self.guiHandler.mainWindow)
