from connection.ConnectionHandler import ConnectionHandler
from game.GameHandler import GameHandler
from gui.GuiHandler import GuiHandler


class Main:
	def __init__(self):
		self.connectionHandler = ConnectionHandler(self)
		self.guiHandler = GuiHandler(self)
		self.gameHandler = GameHandler(self)

	def main(self):
		self.guiHandler.showConnectWindow()


if __name__ == '__main__':
	main = Main()
	main.main()
