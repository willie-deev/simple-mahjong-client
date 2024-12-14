from gui.connectWindow.connectWindow import *


class ConnectWindowHandler(QMainWindow):
	def __init__(self, guiHandler):
		super().__init__()
		self.ui = Ui_MainWindow()
		self.guiHandler = guiHandler

	def setupUi(self, mainWindow):
		self.ui.setupUi(mainWindow)
