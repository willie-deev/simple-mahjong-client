from PySide6.QtCore import Qt, QSize
from PySide6.QtWidgets import QWidget, QSizePolicy, QHBoxLayout, QPushButton

from game.CardActionType import CardActionType
from game.CardType import CardType
from utils.debugUtils import debugOutput


class ActionsMenuManager:
	def __init__(self, gameWindowHandler):
		from gui.gameWindow import WidgetUtils
		from gui.gameWindow.GameWindowHandler import GameWindowHandler
		self.overlay = None
		self.gameWindowHandler: GameWindowHandler = gameWindowHandler
		self.ui = self.gameWindowHandler.ui
		self.widgetUtils: WidgetUtils = self.gameWindowHandler.widgetUtils

		self.winButton: QPushButton | None = None
		self.readyButton: QPushButton | None = None
		self.kongButton: QPushButton | None = None
		self.pungButton: QPushButton | None = None
		self.chowButton: QPushButton | None = None
		self.cancelButton: QPushButton | None = None

		self.cardActionCardsDict: dict[CardActionType, list] = {}
		self.selectingChowCard = False
		self.canChowCardTypes: list[CardType] | None = None
		self.selectedChowCardTypes: list[CardType] = []

	def resizeOverlay(self):
		if self.overlay is not None and not self.overlay.isHidden():
			maxWidth = self.overlay.maximumWidth()
			maxHeight = self.overlay.maximumHeight()
			width = self.gameWindowHandler.rect().width()//2
			height = self.gameWindowHandler.rect().height()//6
			exceedWidth = 0
			exceedHeight = 0
			if width > maxWidth:
				exceedWidth = width - maxWidth
				width =  maxWidth
			if height > maxHeight:
				exceedHeight = height - maxHeight
				height = maxHeight
			posX = int(self.gameWindowHandler.rect().width()//4 + exceedWidth//2)
			posY = int(self.gameWindowHandler.rect().height() - self.ui.selfCards.height() - height + exceedHeight//2)
			self.overlay.setGeometry(posX, posY, width, height)

	def showActionsMenu(self, cardActionCardsDict: dict[CardActionType, list]):
		self.cardActionCardsDict = cardActionCardsDict
		self.overlay.show()
		self.hideButtons()
		if CardActionType.CHOW in cardActionCardsDict.keys():
			self.chowButton.show()
		if CardActionType.PUNG in cardActionCardsDict.keys():
			self.pungButton.show()
		if CardActionType.KONG in cardActionCardsDict.keys():
			self.kongButton.show()
		if CardActionType.READY in cardActionCardsDict.keys():
			self.readyButton.show()
		if CardActionType.WIN in cardActionCardsDict.keys():
			self.winButton.show()
		self.resizeOverlay()

	def clickedChowButton(self):
		if self.selectingChowCard is False:
			self.selectingChowCard = True
			self.chowButton.setStyleSheet("""
						QPushButton {
			        		background-color: rgba(50, 50, 50, 200);
			        		border-radius: 10px;
			    		}
			""")
			self.canChowCardTypes = []
			for cardTypes in self.cardActionCardsDict[CardActionType.CHOW]:
				self.canChowCardTypes += cardTypes
			styleSheet = self.gameWindowHandler.selfCardUiManager.getCardButtonVariables()[0]
			for selfCardButton, cardType in self.gameWindowHandler.selfCardUiManager.addedCards.items():
				if cardType in self.canChowCardTypes:
					selfCardButton.setStyleSheet(styleSheet + "QPushButton:hover { background-color: lightgray; }")
				else:
					selfCardButton.setStyleSheet(styleSheet.replace("background-color: white;", "background-color: rgb(35, 35, 35);"))
		else:
			self.cancelSelectingChowCard()
	def clickedCancelCardActionButton(self):
		self.cancelCardAction()
		gameManager = self.gameWindowHandler.guiHandler.main.gameHandler.gameManager
		gameManager.cancelCardAction()

	def cancelCardAction(self):
		self.canChowCardTypes = []
		self.cancelSelectingChowCard()
		self.hideActionsMenu()

	def selectedChowCard(self, cardType: CardType, clickedButton: QPushButton):
		if cardType in self.canChowCardTypes:
			self.selectedChowCardTypes.append(cardType)
			if len(self.selectedChowCardTypes) <= 1:
				styleSheet = self.gameWindowHandler.selfCardUiManager.getCardButtonVariables()[0]
				clickedButton.setStyleSheet(styleSheet.replace("background-color: white;", "background-color: lightgray;"))
			elif len(self.selectedChowCardTypes) == 2:
				self.selectedChowCardTypes.sort(key=lambda v: v.value)
				if self.selectedChowCardTypes in self.cardActionCardsDict[CardActionType.CHOW]:
					debugOutput("self.selectedChowCardTypes: " + str(self.selectedChowCardTypes))
					gameManager = self.gameWindowHandler.guiHandler.main.gameHandler.gameManager
					gameManager.performChowCardAction(self.selectedChowCardTypes)
					self.cancelCardAction()
				else:
					self.cancelSelectingChowCard()

	def cancelSelectingChowCard(self):
		self.selectedChowCardTypes = []
		self.chowButton.setStyleSheet("""
								QPushButton {
				        			background-color: rgba(0, 0, 0, 100);
				        			border-radius: 10px;
				    			}
				    			QPushButton:hover {
				       				background-color: rgba(0, 0, 0, 200);
				    			}
				    		""")
		self.selectingChowCard = False
		self.gameWindowHandler.selfCardUiManager.updateCardButtons()

	def mouseLeaveButton(self):
		self.gameWindowHandler.selfCardUiManager.updateCardButtons()

	def hideActionsMenu(self):
		self.overlay.hide()

	def hideButtons(self):
		self.winButton.hide()
		self.readyButton.hide()
		self.kongButton.hide()
		self.pungButton.hide()
		self.chowButton.hide()

	def setupActionsMenu(self):
		self.overlay = QWidget(self.gameWindowHandler)
		# self.overlay.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents)
		self.overlay.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
		self.overlay.setSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Maximum)
		self.overlay.setMaximumSize(QSize(600, 100))
		self.overlay.setStyleSheet("background: rgba(0, 0, 0, 50);")

		self.resizeOverlay()

		self.chowButton = self.widgetUtils.getActionButton("chow", "Chow")
		self.pungButton = self.widgetUtils.getActionButton("pung", "Pung")
		self.kongButton = self.widgetUtils.getActionButton("kong", "Kong")
		self.readyButton = self.widgetUtils.getActionButton("ready", "Ready")
		self.winButton = self.widgetUtils.getActionButton("win", "Win")
		self.cancelButton = self.widgetUtils.getActionButton("cancel", "Cancel")

		expandingLabel = QWidget(self.overlay)
		expandingLabel.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

		layout = QHBoxLayout(self.overlay)
		layout.setContentsMargins(0, 0, 0, 0)
		layout.addWidget(expandingLabel)

		layout2 = QHBoxLayout(expandingLabel)
		layout2.setContentsMargins(20, 20, 20, 20)
		layout2.setSpacing(20)
		layout2.addWidget(self.chowButton)
		layout2.addWidget(self.pungButton)
		layout2.addWidget(self.kongButton)
		layout2.addWidget(self.readyButton)
		layout2.addWidget(self.winButton)
		layout2.addWidget(self.cancelButton)

		self.chowButton.clicked.connect(self.clickedChowButton)
		self.cancelButton.clicked.connect(self.cancelCardAction)