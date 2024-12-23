import threading
from threading import Thread

from game.CardActionType import CardActionType
from game.CardType import CardType
from game.ClientActionType import ClientActionType
from game.Wind import Wind
from utils.debugUtils import debugOutput


class GameManager:
	def __init__(self, gameHandler):
		from game.GameHandler import GameHandler
		self.gameHandler: GameHandler = gameHandler

		self.selfWind = None
		self.gotCards = list[CardType]()
		self.orderNumberWindMap = None
		self.waitDiscardEvent = threading.Event()
		self.waitDiscardThread: Thread | None = None
		self.waitCardActionThread: Thread | None = None
		self.discardedCardType = None
		self.startAddCardCount = 0
		self.canAction: bool | None = None
		self.cardActionCardsDict: dict[CardActionType, list] = {}

		from connection.SendMessageUtils import SendMessageUtils
		from gui.gameWindow.GameWindowController import GameWindowController
		self.sendMessageUtils: SendMessageUtils = gameHandler.main.connectionHandler.sendMessageUtils
		self.gameWindowController: GameWindowController | None = None

	def setupVariables(self):
		self.gameWindowController = self.gameHandler.main.guiHandler.gameWindowHandler.gameWindowController
		self.cardUtils = self.gameHandler.cardUtils

	def setSelfWind(self, selfWind: Wind):
		self.selfWind = selfWind
		self.sendMessageUtils.sendClientActionType(ClientActionType.RECEIVED_CARDS, [])
		debugOutput(selfWind)

	def windToOrderNumber(self, wind: Wind):
		if wind == Wind.EAST:
			return 0
		elif wind == Wind.SOUTH:
			return 1
		elif wind == Wind.WEST:
			return 2
		elif wind == Wind.NORTH:
			return 3

	def orderNumberToWind(self, orderNumber: int):
		if orderNumber == 0:
			return Wind.EAST
		elif orderNumber == 1:
			return Wind.SOUTH
		elif orderNumber == 2:
			return Wind.WEST
		elif orderNumber == 3:
			return Wind.NORTH

	def getSelfWind(self):
		return self.selfWind

	def startAddCards(self, cards: list[CardType]):
		for card in cards:
			self.gotCards.append(card)
		self.sendMessageUtils.sendClientActionType(ClientActionType.RECEIVED_CARDS, [])
		self.gameWindowController.triggerStartAddCards(cards)
		self.startAddCardCount += 1
		if self.startAddCardCount == 4:
			self.sortAllCards()
		print(self.gotCards)

	def sortAllCards(self):
		self.gotCards.sort(key=lambda v: v.value, reverse=False)
		self.gameWindowController.triggerSetAllCards(self.gotCards)

	def gotNewCard(self, cardType: CardType):
		self.gotCards.append(cardType)
		self.gameWindowController.triggerGotNewCard(cardType)
		self.sendMessageUtils.sendClientActionType(ClientActionType.RECEIVED_CARDS, [])

	def waitDiscard(self):
		self.gameWindowController.triggerWaitDiscard()
		self.waitDiscardThread = threading.Thread(target=self.waitDiscardThreadFunction)
		self.waitDiscardThread.start()

	def setDiscardType(self, discardType):
		self.discardedCardType = discardType
		self.waitDiscardEvent.set()

	def waitDiscardThreadFunction(self):
		self.waitDiscardEvent.wait()
		self.waitDiscardEvent.clear()
		self.gameHandler.main.guiHandler.gameWindowHandler.waitingForDiscard = False
		if self.discardedCardType is not None:
			self.sendMessageUtils.sendClientActionType(ClientActionType.DISCARD, [self.discardedCardType.name.encode()])
			self.discardedCardType = None

	def clientDiscarded(self, wind: Wind, cardType: CardType):
		if wind is self.selfWind:
			self.gotCards.remove(cardType)
			self.gameWindowController.triggerSetAllCards(self.gotCards)
			self.sortAllCards()
		self.gameWindowController.triggerPlayerDiscarded(wind, cardType)
		self.canAction = False
		self.cardActionCardsDict = {}
		if cardType != CardType.FLOWER:
			if self.gameHandler.windToSide(wind) == "right":
				canChowList = self.cardUtils.calCanChowCards(cardType)
				debugOutput("gotCards: " + str(self.gotCards))
				debugOutput("canChowList: " + str(canChowList))
				if canChowList is not None and len(canChowList) != 0:
					self.canAction = True
					self.cardActionCardsDict[CardActionType.CHOW] = canChowList
		self.sendMessageUtils.sendClientActionType(ClientActionType.RECEIVED_DISCARD_ACTION, [self.canAction.to_bytes()])

	def waitCardAction(self):
		if self.canAction:
			self.waitCardActionThread = threading.Thread(target=self.waitCardActionThreadFunction)
			self.waitCardActionThread.run()

	def waitCardActionThreadFunction(self):
		cardActionCardsDict = self.cardActionCardsDict.copy()
		self.gameWindowController.triggerCanDoActions(cardActionCardsDict)

	def otherPlayerGotCard(self, wind: Wind):
		self.gameWindowController.triggerOtherPlayerGotCard(wind)
		self.sendMessageUtils.sendClientActionType(ClientActionType.RECEIVED_OTHER_PLAYER_GOT_CARD, [])
