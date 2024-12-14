from gui.connectWindow.ConnectWindowController import ConnectWindowController
from gui.connectWindow.connectWindow import *


class ConnectWindowHandler(QMainWindow):
	def __init__(self, guiHandler):
		super().__init__()
		self.ui = Ui_MainWindow()
		self.guiHandler = guiHandler
		self.connectWindowController = ConnectWindowController(self)

	def setupUi(self):
		self.ui.setupUi(self.guiHandler.mainWindow)
		self.ui.connectToServer.clicked.connect(self.clicked)
		self.connectWindowController.updatePlayerCount.connect(self.ui.debugOutput.setText)

	def clicked(self):
		try:
			self.guiHandler.main.connectionHandler.connectToServer(self.ui.ip.text(), int(self.ui.port.text()))
		except Exception as e:
			self.ui.debugOutput.setText("Debug Output:\n" + str(e))
			print(e)
		else:
			self.ui.ip.deleteLater()
			self.ui.port.deleteLater()
			self.ui.label.deleteLater()
			self.ui.connectToServer.deleteLater()
			self.ui.debugOutput.clear()
			self.guiHandler.main.connectionHandler.runWaitForPlayersThread()
