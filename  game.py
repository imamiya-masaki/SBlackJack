import random
class ClassName:
  def __init__(self, decks, player1, player2):
    self.decks = decks
    if player1 != None:
      self.player1 = {}
      self.player1.sum = 0
    if player2 != None:
      self.player2 = {}
      self.player2.sum = 0
  def createDeck(self, decks):
    cards = [i for i in [1,2,3,4,5,6,7,8,9,10,11,12,13]]*decks
    return cards
  def pickCard(self, deck, list, count):
    for num in count:
      list.append(num)
    return list, deck[count:]
  def play(self, player1, player2):
    # 1play
    deck = random.shuffle(self.createDeck(self.decks))
    player1Cards = []
    player1D = False #ダブルダウンしたかどうか
    player2Cards = []
    player2D = False #ダブルダウンしたかどうか
    player1Cards,deck = self.pickCard(deck, player1Cards, 2)
    player2Cards,deck = self.pickCard(deck, player2Cards, 2)
