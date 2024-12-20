from PySide6.QtWidgets import QApplication, QMainWindow

from connection.ConnectionHandler import ConnectionStates
from gui.connectWindow.ConnectWindowHandler import ConnectWindowHandler
from gui.gameWindow.GameWindowHandler import GameWindowHandler


class GuiHandler:
	def __init__(self, main):
		from Main import Main
		self.main: Main = main
		self.app = QApplication([])
		self.connectWindowHandler = ConnectWindowHandler(self)
		self.gameWindowHandler = None

	def showConnectWindow(self):
		self.connectWindowHandler.setupUi()
		self.connectWindowHandler.show()
		self.app.exec()
		self.connectWindowHandler.deleteLater()
		if self.main.connectionHandler.getConnectionState() == ConnectionStates.STARTING:
			self.showGameWindow()

	def showGameWindow(self):
		self.gameWindowHandler = GameWindowHandler(self)
		self.gameWindowHandler.setupUi()
		self.gameWindowHandler.show()
		self.app.exec()
