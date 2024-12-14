class ConnectionUtils:
	def __init__(self, connectionHandler):
		self.connectionHandler = connectionHandler
		self.socket = connectionHandler.socket
