from connection.ConnectionHandler import ConnectionHandler
from gui.GuiHandler import GuiHandler


class Main:
	def __init__(self):
		self.guiHandler = None
		self.connectionHandler = None

	def main(self):
		self.guiHandler = GuiHandler(self)
		self.connectionHandler = ConnectionHandler(self)
		self.guiHandler.showConnectWindow()

if __name__ == '__main__':
	main = Main()
	main.main()