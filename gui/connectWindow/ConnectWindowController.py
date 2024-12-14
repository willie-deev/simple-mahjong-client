from PySide6.QtCore import QObject, Signal


class ConnectWindowController(QObject):
	updatePlayerCount = Signal(str)
	removeConnectWindow = Signal()

	def __init__(self, connectWindowHandler):
		super().__init__()
		self.connectWindowHandler = connectWindowHandler

	def triggerUpdatePlayerCount(self, new_text):
		self.updatePlayerCount.emit(new_text)
