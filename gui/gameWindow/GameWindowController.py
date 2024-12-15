from PySide6.QtCore import QObject, Signal


class GameWindowController(QObject):
	setPlayerWind = Signal(int)

	def __init__(self, gameWindowHandler):
		super().__init__()
		self.gameWindowHandler = gameWindowHandler

	def triggerSetPlayerWind(self, windOrder):
		self.setPlayerWind.emit(windOrder)
