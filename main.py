
# -*- coding: utf-8 -*-
import random
import numpy as np
import typing as tp
from typing import Tuple, Dict

class dealer:
  #　一応ディーラーもクラスで分けておく。
  def __init__(self):
    self = self
  def max(self,sumCard:str) -> int:
    cards = sumCard.split('/')
    return int(cards[len(cards) - 1]) #昇順なので最後に最大値がくる
  def play(self, delerCards:str) -> Dict[str, str]:
    if len(delerCards.split('/')) > 1:
      # エースカード入ってるなら
      if self.max(delerCards) <= 17: #ソフト17stay
        return {'action': 'HIT', 'state': 'dealer'}
      else:
        return {'action': 'STAY', 'state': 'dealer'}
    else:
      if self.max(delerCards) <= 16: #all17stay
        return {'action': 'HIT', 'state': 'dealer'}
      else:
        return {'action': 'STAY', 'state': 'dealer'}


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
  def play(self, playerSumCards:str, delerCards:str, player1D:bool) -> Dict[str, str]:
    if str(playerSumCards)+'-'+str(delerCards)+'-'+str(player1D) not in self.tree:
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
    cards = [i for i in [1,2,3,4,5,6,7,8,9,10,11,12,13]]*4*decks
    return cards
  def test(self):
    print('game')
    return
  def pickCard(self, deck:list) -> Tuple[int, list]:
    if len(deck) == 0:
      return 0, []
    return deck[0], deck[1:]
  def pickAndInsertCards(self, deck: list, list: list, count: int) -> Tuple[list, list]:
    for num in range(count):
      list.append(deck[num])
    if deck is None:
      return list, None
    return list, deck[count:]
  def calculate(self, cards:str, card:int) -> Tuple[str, bool]:
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
    keys: int[...] = list(map.keys())
    keys = list(filter(lambda x: x <= 21, keys))
    if len(keys) == 0:
      return '', False
    lists: int[...] = keys
    lists.sort()
    str_lists: str[...] = [str(val) for val in lists]
    return '/'.join(str_lists), True

    return ""
  def max(self, sumCard:str) -> int:
    cards = sumCard.split('/')
    return int(cards[len(cards) - 1]) #昇順なので最後に最大値がくる
  
  def playGame(self, player1:player or montekarlo) -> Tuple[list, int]:
    # 1play
    deck = self.createDeck(self.decks)
    random.shuffle(deck)
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
    if self.max(delerSum) == 21:
      # ディーラーが初期手札で21ならディーラーの勝ち
      return plyer1_select, -1
      #報酬を-1としているが、player1_selectがからなので影響しない~...と考えれるし、
      #インスランスをつけたくなってもいい感じにできそう
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
        #playerがstayを選択か、(バースト等して)負けかダブルダウンを選択したら、プレイヤーの行動は終了
        break
    #ディーラーの行動
    if result is not "LOSE":
      while True:
        get: Dict[str, str] = dealer.play(delerSum)
        if get['action'] == 'HIT':
          card, deck = self.pickCard(deck)
          delerSum, isSafe = self.calculate(delerSum, card)
          if isSafe is False:
            # プレイヤーが負けていない状態で、ディーラーがバーストしたら、勝ち
            result = "WIN"
        if get['action'] == 'STAY' or result == 'WIN':
          break
    #比較
    if result == '':
      #結果がまだ決まってないなら
      playerMax = self.max(playerSum)
      delerMax = self.max(delerSum)
      if playerMax > delerMax:
        result = "WIN"
      elif playerMax < delerMax:
        result = "LOSE"
      else:
        result = "DRAW"
    reward = 0
    if result == "WIN":
      reward = 1
    elif result == "LOSE":
      reward = -1
    if player1D is True:
      reward *= 2
    return plyer1_select, reward

  def ini_sum(self,cards: list) -> str:
    result = "0"
    for card in cards:
      result, flag = self.calculate(result, card)
    return result


if __name__ == '__main__':
    player1Sum = 0 # player0の勝ち星　グラフよう
    logs = [] # playerのログをとる
    logs.append(player1Sum)
    player1 = montekarlo()
    for i in range(10):
      # 100回繰り返す
      game = Game(1)
      player_select, result = game.playGame(player1)
      print(player_select, result)
