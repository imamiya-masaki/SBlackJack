
# -*- coding: utf-8 -*-
import random
import numpy as np
from typing import Tuple, Dict

class player:
  # 型を簡単に作るために模擬的なもの
  def __init__(self):
    self.tree = {}
  @staticmethod
  def play() -> Dict[str, str]:
    return {'action': 'player', 'state': 'player'}

class montekarlo:
  def __init__(self):
    self.tree = {}
  def play(self, playerSumCards: str, delerCards: str, player1D: bool) -> Dict[str, str]:
    if self.tree[str(playerSumCards)+'-'+str(delerCards)+'-'+str(player1D)] == None:
      #初期化
      initial = {}
      initial['N'] = 0
      initial['HIT'] = {}
      initial['HIT']['n'] = 0
      initial['HIT']['val'] = 0
      initial['STAY'] = {}
      initial['STAY']['n'] = 0
      initial['STAY']['val'] = 0
      initial['DOUBLE'] = {}
      initial['DOUBLE']['n'] = 0
      initial['DOUBLE']['val'] = 0
      self.tree[str(playerSumCards)+'-'+str(delerCards)+'-'+str(player1D)] = initial
    targetVal: int = 0
    targetKey: str = 'HIT'
    N = self.tree[str(playerSumCards)+'-'+str(delerCards)+'-'+str(player1D)]['N']
    for key in ['HIT', 'STAY', 'DOUBLE']:
      target = self.tree[str(playerSumCards)+'-'+str(delerCards)+'-'+str(player1D)][key]
      if target['n'] == 0:
        if not key  ==  'DOUBLE' or player1D == True:
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
  def pickCard(self, deck: int[...]) -> Tuple[int, int[...]]:
    return deck[0], deck[1:]
  def pickAndInsertCards(self, deck: int[...], list: int[...], count: int) -> Tuple[int[...], int[...]]:
    for num in count:
      list.append(num)
    return list, deck[count:]
  def calculate(self, cards: str, card: int) -> Tuple[str, bool]:
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
    if len(keys) == 0:
      return '', False
    lists: int[...] = keys.sort()
    str_lists: str[...] = [str(val) for val in lists]
    return str_lists.join('/'), True

    return ""
  def Max(sumCard: str) -> int:
    cards = sumCard.split('/')
    return int(cards[len(cards) - 1]) #昇順なので最後に最大値がくる
  
  def playGame(self, player1: player):
    # 1play
    deck = random.shuffle(self.createDeck(self.decks))
    result: str = "" #引き分け,勝ち,負け,etc... 
    player1Cards = []
    player1D = False #ダブルダウンしたかどうか
    delerCards = []
    player1Cards,deck = self.pickAndInsertCards(deck, player1Cards, 2)
    delerCards,deck = self.pickAndInsertCards(deck, delerCards, 1)
    playerSum = self.ini_sum(player1Cards)
    delerSum = self.ini_sum(delerCards)
    #playerの行動
    plyer1_select = [] #本質的にはdictの配列なんだけど、なぜか型宣言できない...
    while True:
      get: Dict[str, str] = player1.play(playerSum, delerSum, player1D)
      plyer1_select.append(get)
      if get['action'] == 'HIT' or get['action'] == 'DOUBLE':
        card, deck = self.pickCard(deck)
        playerSum, isSafe = self.calculate(playerSum, card)
        if isSafe is False:
          result = "LOSE"
        if get['action'] == 'DOUBLE':
          player1D = True
      if get['action'] == 'STAY' or result == 'LOSE' or player1D == True:
        #playerがstayを選択か、バーストして負けかダブルダウンを選択したら、プレイヤーの行動は終了
        break
    #ディーラーの行動

  def ini_sum(self,cards: int[...]) -> str:
    result = "0"
    for card in cards:
      result = self.calculate(result, card)
    return result


if __name__ == '__main__':
    game = Game(1)
    game.test()