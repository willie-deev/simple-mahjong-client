import socket
import threading
from enum import Enum

from connection.EncryptionUtils import EncryptionUtils
from connection.ReceiveMessageThread import ReceiveMessageThread
from connection.SendMessageUtils import SendMessageUtils
from utils.debugUtils import debugOutput


class ConnectionHandler:
	def __init__(self, main):
		from Main import Main
		self.main: Main = main

		self.connectionState = None
		self.setConnectionState(ConnectionStates.NOT_CONNECTED)
		self.encryptionUtils = EncryptionUtils(self)
		self.receiveMessageThread = None
		self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.sendMessageUtils = SendMessageUtils(self)
		self.connectedPlayerCount = 0

	def setConnectionState(self, connectionState):
		self.connectionState = connectionState
		debugOutput(connectionState.name)

	def getConnectionState(self):
		return self.connectionState

	def connectToServer(self, ip: str, port: int):
		self.socket.connect((ip, port))
		self.receiveMessageThread = ReceiveMessageThread(self)
		self.setConnectionState(ConnectionStates.CONNECTED)
		self.receiveMessageThread.start()
		self.keyExchanges()
		self.sendMessageUtils.sendAesKey()
		debugOutput("key exchanged")
		self.setConnectionState(ConnectionStates.KEY_EXCHANGED)

	def keyExchanges(self):
		self.encryptionUtils.setupServerKey(self.receiveMessageThread.waitForKeyExchange())
		self.sendMessageUtils.sendBytes(self.encryptionUtils.keyPair.publickey().export_key())

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
		self.setConnectionState(ConnectionStates.STARTING)
		self.main.guiHandler.app.exit()


class ConnectionStates(Enum):
	NOT_CONNECTED = 0
	CONNECTED = 1
	KEY_EXCHANGED = 2
	STARTING = 3
	STARTED = 4
