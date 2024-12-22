from game.CardType import CardType


class CardUtils:
	def __init__(self, gameHandler):
		from game.GameHandler import GameHandler
		self.gameHandler: GameHandler = gameHandler
		self.gameManager = self.gameHandler.gameManager

	def calCanChowCards(self, cardType: CardType):
		number = getNumberByCardType(cardType)
		if number is None:
			return None
		sameTypeCards, sameTypeCardNumbers = self.getSameTypeCards(cardType)
		sameTypeCardNumbers += [getNumberByCardType(cardType)]
		cardTypeNameWithoutNumber = getCardTypeWithoutNumber(cardType)
		canChowList = []
		for needCards in getCardsNeededToChow(cardType):
			haveAllCards = True
			for card in needCards:
				if card not in self.gameManager.gotCards:
					haveAllCards = False
			if haveAllCards:
				canChowList.append(needCards)
		return canChowList

	def getSameTypeCards(self, cardType: CardType):
		cards: list[CardType] = []
		cardNumbers: list[int] = []
		for card in self.gameManager.gotCards:
			if getCardTypeWithoutNumber(card) == getCardTypeWithoutNumber(cardType):
				cards.append(card)
				cardNumbers.append(getNumberByCardType(card))
		return cards, cardNumbers

def getCardsNeededToChow(cardType: CardType):
	cardNumber = getNumberByCardType(cardType)
	cardTypeWithoutNumber = getCardTypeWithoutNumber(cardType)
	canChowList = [
		[getCardTypeByNameAndNumber(cardTypeWithoutNumber, cardNumber - 2),
		 getCardTypeByNameAndNumber(cardTypeWithoutNumber, cardNumber - 1)],
		[getCardTypeByNameAndNumber(cardTypeWithoutNumber, cardNumber - 1),
		 getCardTypeByNameAndNumber(cardTypeWithoutNumber, cardNumber + 1)],
		[getCardTypeByNameAndNumber(cardTypeWithoutNumber, cardNumber + 1),
		 getCardTypeByNameAndNumber(cardTypeWithoutNumber, cardNumber + 2)],
	]
	return canChowList

def getCardTypeByNameAndNumber(cardName: str, number: int) -> CardType | None:
	for cardType in CardType:
		if cardType.name == cardName + "_" + str(number):
			return cardType
	return None

def getNumberByCardType(cardType: CardType):
	if "CHARACTER" in cardType.name:
		number = int(cardType.name.strip("CHARACTER_"))
	elif "DOT" in cardType.name:
		number = int(cardType.name.strip("DOT_"))
	elif "BAMBOO" in cardType.name:
		number = int(cardType.name.strip("BAMBOO_"))
	else:
		return None
	return number

def getCardTypeWithoutNumber(cardType: CardType):
		if "CHARACTER" in cardType.name:
			return "CHARACTER"
		elif "DOT" in cardType.name:
			return "DOT"
		elif "BAMBOO" in cardType.name:
			return "BAMBOO"
		else:
			return None
