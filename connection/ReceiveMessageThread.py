import threading


class ReceiveMessageThread(threading.Thread):
	def __init__(self, connectionHandler):
		threading.Thread.__init__(self)
		self.receivedPlayerCountEvent = threading.Event()
		self.receivedPlayerCount = int
		self.connectionHandler = connectionHandler
		self.socket = connectionHandler.socket

	def waitForPlayerCount(self):
		self.receivedPlayerCountEvent.wait()
		self.receivedPlayerCountEvent.clear()
		return self.receivedPlayerCount

	def run(self):
		from connection.ConnectionHandler import ConnectionStates
		while self.connectionHandler.connectionState is ConnectionStates.CONNECTED:
			try:
				playerCount = int.from_bytes(self.socket.recv(1))
				if not playerCount:
					print('server disconnected')
					self.socket.close()
					return
				self.receivedPlayerCount = playerCount
				self.receivedPlayerCountEvent.set()
			except Exception as e:
				print(e)
