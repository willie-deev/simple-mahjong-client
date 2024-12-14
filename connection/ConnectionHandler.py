import socket
import threading
from enum import Enum

from connection.ReceiveMessageThread import ReceiveMessageThread
from connection.SendMessageUtils import ConnectionUtils


class ConnectionHandler:
	def __init__(self, main):
		self.connectionState = ConnectionStates.NOT_CONNECTED
		self.receiveMessageThread = None
		self.main = main
		self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.connectionUtils = ConnectionUtils(self)
		self.connectedPlayerCount = 0

	def connectToServer(self, ip: str, port: int):
		self.socket.connect((ip, port))
		self.connectionState = ConnectionStates.CONNECTED
		self.receiveMessageThread = ReceiveMessageThread(self)
		self.receiveMessageThread.start()

	def runWaitForPlayersThread(self):
		thread = threading.Thread(target=self.waitForPlayersThread)
		thread.start()

	def waitForPlayersThread(self):
		self.connectedPlayerCount = self.receiveMessageThread.waitForPlayerCount()
		while self.connectedPlayerCount != 4:
			self.main.guiHandler.connectWindowHandler.connectWindowController.triggerUpdatePlayerCount(
				"Connected\nWaiting for other players...\nConnected player count: " + str(
					self.connectedPlayerCount) + " / 4")
			self.connectedPlayerCount = self.receiveMessageThread.waitForPlayerCount()
		self.main.guiHandler.connectWindowHandler.connectWindowController.triggerUpdatePlayerCount(
			"Connected\nWaiting for other players...\nConnected player count: 4 / 4")
		self.main.guiHandler.app.exit()


class ConnectionStates(Enum):
	NOT_CONNECTED = '0'
	CONNECTED = '1'
	STARTING = '2'
	STARTED = '3'
