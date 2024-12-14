class SendMessageUtils:
	def __init__(self, connectionHandler):
		self.connectionHandler = connectionHandler
		self.socket = connectionHandler.socket

	def sendBytes(self, message: bytes):
		self.socket.sendall(message)

	def sendAesKey(self):
		print(len(self.connectionHandler.encryptUtils.encryptAesKey()))
		self.socket.sendall(self.connectionHandler.encryptUtils.encryptAesKey())

	def sendEncryptBytes(self, message: bytes):
		dataLength = self.connectionHandler.encryptUtils.encryptMessage(int.to_bytes(1))
		self.socket.sendall(dataLength[0])
		self.socket.sendall(dataLength[1])

		data = self.connectionHandler.encryptUtils.encryptMessage(message)
		self.socket.sendall(data[0])
		self.socket.sendall(data[1])

	def sendEncryptByteList(self, message: list):
		dataLength = self.connectionHandler.encryptUtils.encryptMessage(int.to_bytes(len(message)))
		self.socket.sendall(dataLength[0])
		self.socket.sendall(dataLength[1])

		for data in message:
			encryptedData = self.connectionHandler.encryptUtils.encryptMessage(data)
			self.socket.sendall(encryptedData[0])
			self.socket.sendall(encryptedData[1])
