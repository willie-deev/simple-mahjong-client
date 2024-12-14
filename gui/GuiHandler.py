from PySide6.QtWidgets import QApplication, QMainWindow

from connection.ConnectionHandler import ConnectionStates
from gui.connectWindow.ConnectWindowHandler import ConnectWindowHandler
from gui.gameWindow.GameWindowHandler import GameWindowHandler


class GuiHandler:
	def __init__(self, main):
		self.main = main
		self.app = QApplication([])
		self.mainWindow = QMainWindow()
		self.connectWindowHandler = ConnectWindowHandler(self)
		self.gameWindowHandler = GameWindowHandler(self)

	def showConnectWindow(self):
		self.connectWindowHandler.setupUi()
		self.mainWindow.show()
		self.app.exec()
		if self.main.connectionHandler.connectionState == ConnectionStates.STARTING:
			self.showGameWindow()

	def showGameWindow(self):
		self.gameWindowHandler.setupUi()
		self.mainWindow.show()
		self.app.exec()
