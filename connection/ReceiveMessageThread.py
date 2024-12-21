import threading

from game.CardType import CardType
from game.ServerActionType import ServerActionType
from utils.debugUtils import debugOutput


class ReceiveMessageThread(threading.Thread):
	def __init__(self, connectionHandler):
		from connection.ConnectionHandler import ConnectionHandler
		self.connectionHandler: ConnectionHandler = connectionHandler

		threading.Thread.__init__(self)
		self.receivedPlayerCountEvent = threading.Event()
		self.receivedPlayerCount = int
		self.receivedKeyExchangeEvent = threading.Event()
		self.receivedKey = bytes()
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
		if self.connectionHandler.getConnectionState() == ConnectionStates.CONNECTED:
			self.receivedKey = self.receiveData(450)
			self.receivedKeyExchangeEvent.set()
		while True:
			receivedData: list[bytes] = self.receiveEncryptedMessages()

			if self.connectionHandler.getConnectionState() == ConnectionStates.KEY_EXCHANGED:
				playerCount = int.from_bytes(receivedData[0])
				self.receivedPlayerCount = playerCount
				self.receivedPlayerCountEvent.set()
			if self.connectionHandler.connectionState == ConnectionStates.STARTING:
				self.handleStartingGame(receivedData)

	def handleStartingGame(self, receivedData: list[bytes]):
		serverActionType = None
		for actionType in ServerActionType:
			if receivedData[0].decode() == actionType.name:
				serverActionType = actionType
		receivedData = receivedData[1:]
		gameManager = self.connectionHandler.main.gameHandler.gameManager
		gameWindowController = self.connectionHandler.main.guiHandler.gameWindowHandler.gameWindowController
		match serverActionType:
			case ServerActionType.CHANGE_WIND:
				selfWind = gameManager.gameHandler.getWindByName(receivedData[0].decode())
				gameWindowController.triggerSetPlayerWind(selfWind)
				gameManager.setupVariables()
				gameManager.setSelfWind(selfWind)
			case ServerActionType.START_SEND_CARDS:
				cardsStrs = receivedData
				cards = list[CardType]()
				for cardStr in cardsStrs:
					cards.append(gameManager.gameHandler.getCardTypeByName(cardStr.decode()))
				gameManager.startAddCards(cards)
			case ServerActionType.START_FLOWER_REPLACEMENT:
				cardsStrs = receivedData
				cards = list[CardType]()
				for cardStr in cardsStrs:
					cards.append(gameManager.gameHandler.getCardTypeByName(cardStr.decode()))
				gameManager.removeFlowers()
				gameManager.startAddCards(cards)
			case ServerActionType.START_FLOWER_COUNT:
				gameManager.sortAllCards()
				wind = gameManager.gameHandler.getWindByName(receivedData[0].decode())
				flowerCount = int.from_bytes(receivedData[1])
				gameManager.setFlowerCount(wind, flowerCount)
			case ServerActionType.SEND_CARD:
				gameManager.sortAllCards()
				card = gameManager.gameHandler.getCardTypeByName(receivedData[0].decode())
				gameManager.gotNewCard(card)
			case ServerActionType.FLOWER_REPLACEMENT:
				card = gameManager.gameHandler.getCardTypeByName(receivedData[0].decode())
				gameManager.removeFlowers()
				gameManager.gotNewCard(card)
			case ServerActionType.FLOWER_COUNT:
				wind = gameManager.gameHandler.getWindByName(receivedData[0].decode())
				flowerCount = int.from_bytes(receivedData[1])
				gameManager.setFlowerCount(wind, flowerCount)
			case ServerActionType.WAIT_DISCARD:
				gameManager.waitDiscard()

	def receiveEncryptedMessages(self) -> list[bytes]:
		iv = self.receiveData(256)
		message = self.receiveData(256)
		dataLength = self.connectionHandler.encryptionUtils.decryptReceivedMessage(iv, message)
		messageList = list()
		for i in range(int.from_bytes(dataLength)):
			iv = self.receiveData(256)
			message = self.receiveData(256)
			data = self.connectionHandler.encryptionUtils.decryptReceivedMessage(iv, message)
			messageList.append(data)
		debugOutput(messageList)
		return messageList

	def receiveData(self, receiveByteCount: int):
		try:
			receivedData = self.socket.recv(receiveByteCount)
			while len(receivedData) < receiveByteCount:
				if not receivedData:
					debugOutput('server disconnected')
					self.socket.close()
					return
				receivedData += self.socket.recv(receiveByteCount - len(receivedData))
			return receivedData
		except Exception as e:
			self.socket.close()
			debugOutput(e)
