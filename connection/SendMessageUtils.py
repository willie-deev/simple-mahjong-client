from game.ClientActionType import ClientActionType
from utils.debugUtils import debugOutput


class SendMessageUtils:
	def __init__(self, connectionHandler):
		self.connectionHandler = connectionHandler
		self.socket = connectionHandler.socket

		self.encryptionUtils = connectionHandler.encryptionUtils

	def sendClientActionType(self, clientActionType: ClientActionType, messages: list):
		newList = [clientActionType.name.encode()] + messages
		self.sendEncryptByteList(newList)

	def sendBytes(self, message: bytes):
		self.socket.sendall(message)

	def sendAesKey(self):
		debugOutput(len(self.encryptionUtils.encryptAesKey()))
		self.socket.sendall(self.encryptionUtils.encryptAesKey())

	def sendEncryptBytes(self, message: bytes):
		dataLength = self.encryptionUtils.encryptMessage(int.to_bytes(1))
		self.socket.sendall(dataLength[0])
		self.socket.sendall(dataLength[1])

		data = self.encryptionUtils.encryptMessage(message)
		self.socket.sendall(data[0])
		self.socket.sendall(data[1])

	def sendEncryptByteList(self, message: list):
		dataLength = self.encryptionUtils.encryptMessage(int.to_bytes(len(message)))
		self.socket.sendall(dataLength[0])
		self.socket.sendall(dataLength[1])

		for data in message:
			encryptedData = self.encryptionUtils.encryptMessage(data)
			self.socket.sendall(encryptedData[0])
			self.socket.sendall(encryptedData[1])
