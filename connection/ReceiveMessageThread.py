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
		from game import GameHandler
		match serverActionType:
			case ServerActionType.CHANGE_WIND:
				selfWind = GameHandler.getWindByName(receivedData[0].decode())
				gameWindowController.triggerSetPlayerWind(selfWind)
				gameManager.setupVariables()
				gameManager.setSelfWind(selfWind)
			case ServerActionType.START_SEND_CARDS:
				cardsStrs = receivedData
				cards = list[CardType]()
				for cardStr in cardsStrs:
					cards.append(GameHandler.getCardTypeByName(cardStr.decode()))
				gameManager.startAddCards(cards)
			case ServerActionType.START_FLOWER_REPLACEMENT:
				cardsStrs = receivedData
				cards = list[CardType]()
				for cardStr in cardsStrs:
					cards.append(GameHandler.getCardTypeByName(cardStr.decode()))
				gameManager.startAddCards(cards)
			case ServerActionType.SEND_CARD:
				gameManager.sortAllCards()
				card = GameHandler.getCardTypeByName(receivedData[0].decode())
				gameManager.gotNewCard(card)
			case ServerActionType.FLOWER_REPLACEMENT:
				card = GameHandler.getCardTypeByName(receivedData[0].decode())
				gameManager.gotNewCard(card)
			case ServerActionType.WAIT_DISCARD:
				gameManager.waitDiscard()
			case ServerActionType.CLIENT_DISCARDED:
				wind = GameHandler.getWindByName(receivedData[0].decode())
				card = GameHandler.getCardTypeByName(receivedData[1].decode())
				# if card != CardType.FLOWER and gameManager.waitDiscardThread is not None and gameManager.waitDiscardThread.is_alive():
				# 	gameManager.waitDiscardEvent.set()
				gameManager.notPerformedCardAction()
				gameManager.clientDiscarded(wind, card)
			case ServerActionType.OTHER_PLAYER_GOT_CARD:
				wind = GameHandler.getWindByName(receivedData[0].decode())
				gameManager.otherPlayerGotCard(wind)
			case ServerActionType.WAIT_CARD_ACTION:
				gameManager.waitCardAction()
			case ServerActionType.CLIENT_PERFORMED_CARD_ACTION:
				if len(receivedData) != 0:
					wind = GameHandler.getWindByName(receivedData[0].decode())
					cardActionType = GameHandler.getCardActionTypeByName(receivedData[1].decode())
					receivedData = receivedData[2:]
					cardTypes: list[CardType] = []
					for cardNameBytes in receivedData:
						cardTypes.append(GameHandler.getCardTypeByName(cardNameBytes.decode()))
					gameManager.clientPerformedCardAction(wind, cardActionType, cardTypes)
				else:
					gameManager.notPerformedCardAction()
			case ServerActionType.CLIENT_CONCEALED_KONG:
				wind = GameHandler.getWindByName(receivedData[0].decode())
				gameManager.performedConcealedKong(wind)
			case ServerActionType.PLAYER_READY:
				wind = GameHandler.getWindByName(receivedData[0].decode())
				gameManager.playerReady(wind)
			case ServerActionType.GAME_OVER:
				wind = GameHandler.getWindByName(receivedData[0].decode())
				receivedData = receivedData[1:]
				print(wind, "won, cards: ", receivedData)


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
