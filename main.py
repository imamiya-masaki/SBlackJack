
# -*- coding: utf-8 -*-
import random
import numpy as np
class Game:
  def __init__(self, decks, player1=None):
    self.decks = decks
    if player1 != None:
      self.player1 = {}
      self.player1.sum = 0
  def createDeck(self, decks):
    cards = [i for i in [1,2,3,4,5,6,7,8,9,10,11,12,13]]*decks
    return cards
  def test(self):
    print('game')
    return
  def pickCard(self, deck, list, count):
    for num in count:
      list.append(num)
    return list, deck[count:]
  def calculate(self, cards: str, card: int) -> str:
    #初期の計算はsumの責務
    #つまり三枚目以降を考えればよい
    spl = cards.split('/')
    targetCard = 10 if card >= 10 else card
    map = {}
    for val in spl:
      result = int(val) + targetCard
      map[result] = True
      if targetCard == 1:
        map[result + 10] = True
    keys: int[...] = map.keys()
    filter(lambda x: x <= 21, keys)
    lists: int[...] = keys.sort()
    str_lists: str[...] = [str(val) for val in lists]
    return str_lists.join('/')

    return ""
  def playGame(self, player1, player2):
    # 1play
    deck = random.shuffle(self.createDeck(self.decks))
    player1Cards = []
    player1D = False #ダブルダウンしたかどうか
    delerCards = []
    player1Cards,deck = self.pickCard(deck, player1Cards, 2)
    delerCards,deck = self.pickCard(deck, delerCards, 1)
    playerSum = self.ini_sum(player1Cards)
    delerSum = self.ini_sum(delerCards)
    #playerturn
    plyer1_select = []
    while True:
      get = player1.play(playerSum, delerSum, player1D)
  def ini_sum(self,cards: int[...]) -> str:
    result = "0"
    for card in cards:
      result = self.calculate(result, card)
    return result
class montekarlo:
  def __init__(self):
    self.tree = {}
  def play(self, playerSumCards: str, delerCards: str, player1D: bool):
    if self.tree[str(playerSumCards)+'-'+str(delerCards)+'-'+str(player1D)] == None:
      #初期化
      initial = {}
      initial['N'] = 0
      initial['hit'] = {}
      initial['hit']['n'] = 0
      initial['hit']['val'] = 0
      initial['stay'] = {}
      initial['stay']['n'] = 0
      initial['stay']['val'] = 0
      initial['double'] = {}
      initial['double']['n'] = 0
      initial['double']['val'] = 0
      self.tree[str(playerSumCards)+'-'+str(delerCards)+'-'+str(player1D)] = initial
    targetVal = 0
    targetKey = 'hit'
    N = self.tree[str(playerSumCards)+'-'+str(delerCards)+'-'+str(player1D)]['N']
    for key in ['hit', 'stay', 'double']:
      target = self.tree[str(playerSumCards)+'-'+str(delerCards)+'-'+str(player1D)][key]
      if target['n'] == 0:
        if not key  ==  'double' or player1D == True:
          val = 99999
        else:
          val = 0
      else:
        ucb_cost = np.sqrt(2 * np.log(N))/ target['n']
        val = target['val'] + ucb_cost
      if targetVal < val:
        targetVal = val
        targetKey = key
    return {'action': targetKey, 'state': str(playerSumCards)+'-'+str(delerCards)+'-'+str(player1D)}


if __name__ == '__main__':
    game = Game(1)
    game.test()