from gui.gameWindow.gameWindow import *


class GameWindowHandler(QMainWindow):
	def __init__(self, GuiHandler):
		super().__init__()
		self.GuiHandler = GuiHandler