from game import CardUtils
from game.CardActionType import CardActionType
from game.CardType import CardType
from game.ClientActionType import ClientActionType
from game.Wind import Wind
from utils.debugUtils import debugOutput


class GameManager:
	def __init__(self, gameHandler):
		self.cardUtils: CardUtils.CardUtils | None = None
		from game.GameHandler import GameHandler
		self.gameHandler: GameHandler = gameHandler

		self.selfWind = None
		self.gotCards: list[CardType] = []
		self.orderNumberWindMap = None
		self.startAddCardCount = 0
		self.canAction: bool | None = None
		self.cardActionCardsDict: dict[CardActionType, list] = {}
		self.actionedCards: list[CardType] = []

		from connection.SendMessageUtils import SendMessageUtils
		from gui.gameWindow.GameWindowController import GameWindowController
		self.sendMessageUtils: SendMessageUtils = gameHandler.main.connectionHandler.sendMessageUtils
		self.gameWindowController: GameWindowController | None = None

		self.selfReady = False

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
		debugOutput(self.gotCards)

	def sortAllCards(self):
		self.gotCards.sort(key=lambda v: v.value, reverse=False)
		self.gameWindowController.triggerSetAllCards(self.gotCards)

	def gotNewCard(self, cardType: CardType):
		self.gotCards.append(cardType)
		self.cardActionCardsDict = {}
		concealedKongList = self.cardUtils.getAllConcealedKong()
		if len(concealedKongList) != 0:
			self.cardActionCardsDict[CardActionType.CONCEALED_KONG] = concealedKongList
		debugOutput("concealedKongList: " + str(concealedKongList))
		if CardUtils.calCanWin(self.gotCards) is True:
			self.canAction = True
			self.cardActionCardsDict[CardActionType.WIN] = [cardType]
		self.gameWindowController.triggerGotNewCard(cardType)
		self.sendMessageUtils.sendClientActionType(ClientActionType.RECEIVED_CARDS, [])

	def waitDiscard(self):
		if self.selfReady is True:
			if CardUtils.calCanWin(self.gotCards) is True:
				self.cardActionCardsDict[CardActionType.WIN] = []
				self.gameWindowController.triggerPerformCardAction(self.cardActionCardsDict)
				self.cardActionCardsDict = {}
			return
		canReadyAfterDiscardCardList = CardUtils.calCanReadyAfterDiscard(self.gotCards)
		if len(canReadyAfterDiscardCardList) != 0:
			self.cardActionCardsDict[CardActionType.READY] = canReadyAfterDiscardCardList
		if len(self.cardActionCardsDict.keys()) != 0:
			self.gameWindowController.triggerPerformCardAction(self.cardActionCardsDict)
			self.cardActionCardsDict = {}
			self.canAction = False
		else:
			self.gameWindowController.triggerWaitDiscard()

	def discard(self, discardType: CardType):
		self.gameHandler.main.guiHandler.gameWindowHandler.selfCardUiManager.waitingForDiscard = False
		self.sendMessageUtils.sendClientActionType(ClientActionType.DISCARD, [discardType.name.encode()])

	def clientDiscarded(self, wind: Wind, cardType: CardType):
		if wind is self.selfWind:
			self.gameHandler.main.guiHandler.gameWindowHandler.selfCardUiManager.waitingForDiscard = False
			self.gotCards.remove(cardType)
			self.gameWindowController.triggerSetAllCards(self.gotCards)
			self.sortAllCards()
		self.gameWindowController.triggerPlayerDiscarded(wind, cardType)
		self.canAction = False
		self.cardActionCardsDict = {}
		if cardType != CardType.FLOWER:
			if self.gameHandler.windToSide(wind) == "right" and self.selfReady is False:
				canChowList = self.cardUtils.calCanChowCards(cardType)
				debugOutput("gotCards: " + str(self.gotCards))
				debugOutput("canChowList: " + str(canChowList))
				if canChowList is not None and len(canChowList) != 0:
					self.canAction = True
					self.cardActionCardsDict[CardActionType.CHOW] = canChowList

			if wind != self.selfWind and self.cardUtils.cardTypeCanPung(cardType) is True and self.selfReady is False:
				self.canAction = True
				self.cardActionCardsDict[CardActionType.PUNG] = [cardType]

			if wind != self.selfWind and self.cardUtils.cardTypeCanKong(cardType) is True:
				self.canAction = True
				self.cardActionCardsDict[CardActionType.KONG] = [cardType]
			testCards = self.gotCards[:]
			testCards.append(cardType)
			testCards.sort(key=lambda v: v.value)
			if wind != self.selfWind and CardUtils.calCanWin(testCards) is True:
				self.canAction = True
				self.cardActionCardsDict[CardActionType.WIN] = [cardType]

		self.sendMessageUtils.sendClientActionType(ClientActionType.RECEIVED_DISCARD_ACTION, [self.canAction.to_bytes()])

	def waitCardAction(self):
		debugOutput("self.canAction: " + str(self.canAction))
		if self.canAction is True:
			self.gameWindowController.triggerPerformCardAction(self.cardActionCardsDict)
			self.cardActionCardsDict = {}
		else:
			self.cancelCardAction()
		self.canAction = False

	def cancelCardAction(self):
		self.canAction = False
		self.sendMessageUtils.sendClientActionType(ClientActionType.PERFORM_CARD_ACTION, [])

	def performChowCardAction(self, cardTypes: list[CardType]):
		sendByteList = [CardActionType.CHOW.name.encode()]
		for card in cardTypes:
			sendByteList.append(card.name.encode())
		self.sendMessageUtils.sendClientActionType(ClientActionType.PERFORM_CARD_ACTION, sendByteList)
		self.canAction = False

	def performPungCardAction(self, cardType: CardType):
		sendByteList = [CardActionType.PUNG.name.encode(), cardType.name.encode()]
		self.sendMessageUtils.sendClientActionType(ClientActionType.PERFORM_CARD_ACTION, sendByteList)
		self.canAction = False

	def performKongCardAction(self, cardType: CardType):
		sendByteList = [CardActionType.KONG.name.encode(), cardType.name.encode()]
		self.sendMessageUtils.sendClientActionType(ClientActionType.PERFORM_CARD_ACTION, sendByteList)
		self.canAction = False

	def otherPlayerGotCard(self, wind: Wind):
		self.gameWindowController.triggerOtherPlayerGotCard(wind)
		self.sendMessageUtils.sendClientActionType(ClientActionType.RECEIVED_OTHER_PLAYER_GOT_CARD, [])

	def clientPerformedCardAction(self, performedWind: Wind, cardActionType: CardActionType, cardTypes: list[CardType]):
		if performedWind == self.selfWind:
			if cardActionType == CardActionType.CHOW:
				self.gotCards.remove(cardTypes[0])
				self.gotCards.remove(cardTypes[2])
				self.actionedCards.append(cardTypes[0])
				self.actionedCards.append(cardTypes[1])
				self.actionedCards.append(cardTypes[2])
			if cardActionType == CardActionType.PUNG:
				self.gotCards.remove(cardTypes[0])
				self.gotCards.remove(cardTypes[0])
				self.actionedCards.append(cardTypes[0])
				self.actionedCards.append(cardTypes[0])
				self.actionedCards.append(cardTypes[0])
			if cardActionType == CardActionType.KONG:
				self.gotCards.remove(cardTypes[0])
				self.gotCards.remove(cardTypes[0])
				self.gotCards.remove(cardTypes[0])
				self.actionedCards.append(cardTypes[0])
				self.actionedCards.append(cardTypes[0])
				self.actionedCards.append(cardTypes[0])
				self.actionedCards.append(cardTypes[0])
			self.sortAllCards()
		self.gameWindowController.triggerPerformedCardAction(performedWind, cardTypes)

	def notPerformedCardAction(self):
		self.canAction = False
		self.cardActionCardsDict = {}
		self.gameWindowController.triggerNotPerformedCardAction()

	def performConcealedKongCardAction(self, cardType: CardType):
		self.sendMessageUtils.sendClientActionType(ClientActionType.PERFORM_SELF_CARD_ACTION, [CardActionType.CONCEALED_KONG.name.encode(), cardType.name.encode()])

	def performedConcealedKong(self, wind: Wind):
		if wind == self.selfWind:
			if self.gameWindowController.gameWindowHandler.actionsMenuManager.lastSelectedConcealedKongCard is not None:
				for i in range(4):
					self.gotCards.remove(self.gameWindowController.gameWindowHandler.actionsMenuManager.lastSelectedConcealedKongCard)
				self.sortAllCards()
		self.gameWindowController.triggerPerformedConcealedKong(wind)
		self.sendMessageUtils.sendClientActionType(ClientActionType.RECEIVED_CONCEALED_KONG, [])

	def performReadyCardAction(self, discardCardType: CardType):
		self.sendMessageUtils.sendClientActionType(ClientActionType.PERFORM_SELF_CARD_ACTION, [CardActionType.READY.name.encode(), discardCardType.name.encode()])

	def playerReady(self, wind: Wind):
		if wind == self.selfWind:
			self.selfReady = True
		self.gameWindowController.triggerPlayerReady(wind)
		self.sendMessageUtils.sendClientActionType(ClientActionType.RECEIVED_PLAYER_READY, [])

	def performWinCardAction(self):
		self.sendMessageUtils.sendClientActionType(ClientActionType.WIN, [CardActionType.WIN.name.encode()])