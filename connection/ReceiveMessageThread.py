import threading

from game.GameStates import GameStates
from game.Winds import Winds


class ReceiveMessageThread(threading.Thread):
	def __init__(self, connectionHandler):
		threading.Thread.__init__(self)
		self.receivedPlayerCountEvent = threading.Event()
		self.receivedPlayerCount = int
		self.receivedKeyExchangeEvent = threading.Event()
		self.receivedKey = bytes()
		self.connectionHandler = connectionHandler
		self.socket = connectionHandler.socket

	def waitForPlayerCount(self):
		self.receivedPlayerCountEvent.wait()
		self.receivedPlayerCountEvent.clear()
		return self.receivedPlayerCount

	def waitForKeyExchange(self) -> bytes:
		self.receivedKeyExchangeEvent.wait()
		self.receivedKeyExchangeEvent.clear()
		return self.receivedKey

	def run(self):
		from connection.ConnectionHandler import ConnectionStates
		if self.connectionHandler.connectionState == ConnectionStates.CONNECTED:
			self.receivedKey = self.receiveData(450)
			self.receivedKeyExchangeEvent.set()
		while True:
			receivedData: list[bytes] = self.receiveEncryptedMessages()
			if self.connectionHandler.connectionState == ConnectionStates.KEY_EXCHANGED:
				playerCount = int.from_bytes(receivedData[0])
				self.receivedPlayerCount = playerCount
				self.receivedPlayerCountEvent.set()
			gameManager = self.connectionHandler.main.gameHandler.gameManager
			gameManager.setGameState(GameStates.STARTED)
			gameWindowController = self.connectionHandler.main.guiHandler.gameWindowHandler.gameWindowController
			if self.connectionHandler.connectionState == ConnectionStates.STARTING:
				match gameManager.getGameState():
					case GameStates.STARTED:
						selfWindOrder = int.from_bytes(receivedData[0])
						print(selfWindOrder)
						gameWindowController.triggerSetPlayerWind(selfWindOrder)
						match selfWindOrder:
							case 0:
								gameManager.setSelfWind(Winds.EAST)
							case 1:
								gameManager.setSelfWind(Winds.SOUTH)
							case 2:
								gameManager.setSelfWind(Winds.WEST)
							case 3:
								gameManager.setSelfWind(Winds.NORTH)
						gameManager.setGameState(GameStates.CHANGED_WIND)
					case GameStates.CHANGED_WIND:
						pass

	def receiveEncryptedMessages(self) -> list:
		iv = self.receiveData(256)
		message = self.receiveData(256)
		dataLength = self.connectionHandler.encryptionUtils.decryptReceivedMessage(iv, message)
		messageList = list()
		for i in range(int.from_bytes(dataLength)):
			iv = self.receiveData(256)
			message = self.receiveData(256)
			data = self.connectionHandler.encryptionUtils.decryptReceivedMessage(iv, message)
			messageList.append(data)
		print(messageList)
		return messageList

	def receiveData(self, receiveByteCount: int):
		try:
			receivedData = self.socket.recv(receiveByteCount)
			while len(receivedData) < receiveByteCount:
				if not receivedData:
					print('server disconnected')
					self.socket.close()
					return
				receivedData += self.socket.recv(receiveByteCount - len(receivedData))
			return receivedData
		except Exception as e:
			self.socket.close()
			print(e)
