from Crypto.Cipher import PKCS1_OAEP, AES
from Crypto.PublicKey import RSA
from Crypto.Random import get_random_bytes

from utils.debugUtils import debugOutput


class EncryptionUtils:
	def __init__(self, connectionHandler):
		from connection.ConnectionHandler import ConnectionHandler
		self.connectionHandler: ConnectionHandler = connectionHandler

		self.keyPair = RSA.generate(2048)
		self.serverPublicKey = None
		self.receivedMessageRsaDecrypter = PKCS1_OAEP.new(self.keyPair)
		self.sendMessageRsaEncrypter = None
		self.aesKey = get_random_bytes(32)

	def setupServerKey(self, serverPublicKey: bytes):
		try:
			self.serverPublicKey = RSA.importKey(serverPublicKey)
			self.sendMessageRsaEncrypter = PKCS1_OAEP.new(self.serverPublicKey)
		except Exception as e:
			debugOutput(e)

	def encryptAesKey(self):
		return self.sendMessageRsaEncrypter.encrypt(self.aesKey)

	def encryptMessage(self, message: bytes) -> tuple[bytes, bytes]:
		iv = get_random_bytes(16)
		aesCipher = AES.new(self.aesKey, AES.MODE_CFB, iv=iv)
		encryptedIv = self.sendMessageRsaEncrypter.encrypt(iv)
		encryptedMessage = self.sendMessageRsaEncrypter.encrypt(aesCipher.encrypt(message))
		return encryptedIv, encryptedMessage

	def decryptReceivedMessage(self, iv: bytes, mes: bytes) -> bytes:
		decryptedIV = self.receivedMessageRsaDecrypter.decrypt(iv)
		aesCipher = AES.new(self.aesKey, AES.MODE_CFB, iv=decryptedIV)
		rsaDecrypted = self.receivedMessageRsaDecrypter.decrypt(mes)
		return aesCipher.decrypt(rsaDecrypted)
