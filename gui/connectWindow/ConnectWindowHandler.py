from gui.connectWindow.ConnectWindowController import ConnectWindowController
from gui.connectWindow.connectWindow import *
from utils import debugUtils
from utils.debugUtils import debugOutput


class ConnectWindowHandler(QMainWindow):
	def __init__(self, guiHandler):
		super().__init__()
		self.ui = Ui_MainWindow()
		from gui.GuiHandler import GuiHandler
		self.guiHandler: GuiHandler = guiHandler
		self.connectWindowController = ConnectWindowController(self)

	def setupUi(self):
		self.ui.setupUi(self)
		self.ui.connectToServer.clicked.connect(self.clicked)
		self.connectWindowController.updatePlayerCount.connect(self.ui.debugOutput.setText)
		if debugUtils.debug:
			self.ui.ip.setText("127.0.0.1")
			self.ui.port.setText("12345")
			self.clicked()

	def clicked(self):
		connectionHandler = self.guiHandler.main.connectionHandler

		try:
			connectionHandler.connectToServer(self.ui.ip.text(), int(self.ui.port.text()))
		except Exception as e:
			self.ui.debugOutput.setText("Debug Output:\n" + str(e))
			debugOutput(e)
		else:
			self.ui.ip.deleteLater()
			self.ui.port.deleteLater()
			self.ui.label.deleteLater()
			self.ui.connectToServer.deleteLater()
			self.ui.debugOutput.clear()
			connectionHandler.runWaitForPlayersThread()
