import threading


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
		while True:
			if self.connectionHandler.connectionState == ConnectionStates.CONNECTED:
				self.receivedKey = self.receiveData(450)
				self.receivedKeyExchangeEvent.set()
				self.connectionHandler.connectionState = ConnectionStates.KEY_EXCHANGED
			while self.connectionHandler.connectionState == ConnectionStates.KEY_EXCHANGED:
				playerCount = int.from_bytes(self.receiveEncryptedMessages()[0])
				self.receivedPlayerCount = playerCount
				self.receivedPlayerCountEvent.set()
			while self.connectionHandler.connectionState == ConnectionStates.STARTING:
				receivedData = self.receiveEncryptedMessages()

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
