
# -*- coding: utf-8 -*-
import random
import numpy as np
import typing as tp
from typing import Tuple, Dict
from matplotlib import pyplot

hardHandDict = {
  #エースはindex0として扱い、以降,2,3,4,.. -> 1,2,3,...として扱う
  #HIT -> 1, DOUBLE -> 2, STAY -> 0
  '2': [1,1,1,1,1,1,1,1,1,1],
  '3': [1,1,1,1,1,1,1,1,1,1],
  '4': [1,1,1,1,1,1,1,1,1,1],
  '5': [1,1,1,1,1,1,1,1,1,1],
  '6': [1,1,1,1,1,1,1,1,1,1],
  '7': [1,1,1,1,1,1,1,1,1,1],
  '8': [1,1,1,1,1,1,1,1,1,1],
  '8': [1,1,1,1,1,1,1,1,1,1],
  '9': [1,1,2,2,2,2,1,1,1,1],
  '10': [1,2,2,2,2,2,2,2,2,1],
  '11': [1,2,2,2,2,2,2,2,2,2],
  '12': [1,1,1,0,0,0,1,1,1,1],
  '13': [1,0,0,0,0,0,1,1,1,1],
  '14': [1,0,0,0,0,0,1,1,1,1],
  '15': [1,0,0,0,0,0,1,1,1,1],
  '16': [1,0,0,0,0,0,1,1,1,1],
  '17': [0,0,0,0,0,0,0,0,0,0],
  '18': [0,0,0,0,0,0,0,0,0,0],
  '19': [0,0,0,0,0,0,0,0,0,0],
  '20': [0,0,0,0,0,0,0,0,0,0],
  '21': [0,0,0,0,0,0,0,0,0,0],
}

softHandDict = {
  #エースはindex0として扱い、以降,2,3,4,.. -> 1,2,3,...として扱う
  #HIT -> 1, DOUBLE -> 2, STAY -> 0
  '13': [1,1,1,1,2,2,1,1,1,1],
  '14': [1,1,1,1,2,2,1,1,1,1],
  '15': [1,1,1,2,2,2,1,1,1,1],
  '16': [1,1,1,2,2,2,1,1,1,1],
  '17': [1,1,2,2,2,2,1,1,1,1],
  '18': [1,0,2,2,2,2,0,0,1,1],
  '19': [0,0,0,0,0,0,0,0,0,0],
  '20': [0,0,0,0,0,0,0,0,0,0],
}

class dealerClass:
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

class basicStorategy:

  def max(self,sumCard:str) -> int:
    cards = sumCard.split('/')
    return int(cards[len(cards) - 1]) #昇順なので最後に最大値がくる
  def __init__(self):
    self.tree = {}
  def play(self, playerSumCards:str, delerCards:str, player1D:bool) -> Dict[str, str]:
    soft = False
    if len(playerSumCards.split('/')) >= 2:
      soft = True
    state = str(playerSumCards)+'-'+str(delerCards)+'-'+str(player1D)
    playerNum = self.max(playerSumCards) # maxで考える
    if playerNum == 21:
      return {'action': 'STAY', 'state': state}
    if soft:
      #ソフトハンド
    else:
      #ハードハンド
    


def createInitial() -> dict:
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
  return initial

def multiAction(target, number) -> dict:
  action = {}
  action['N'] = target['N']*number
  action['HIT'] = {}
  action['HIT']['n'] = target['HIT']['n']
  action['HIT']['val'] = target['HIT']['val']*number
  action['STAY'] = {}
  action['STAY']['n'] = target['STAY']['n']
  action['STAY']['val'] = target['STAY']['val']*number
  action['DOUBLE'] = {}
  action['DOUBLE']['n'] = target['DOUBLE']['n']
  action['DOUBLE']['val'] = target['DOUBLE']['val']*number
  return action
class montekarlo:
  def __init__(self):
    self.tree = {}
  def play(self, playerSumCards:str, delerCards:str, player1D:bool) -> Dict[str, str]:
    if str(playerSumCards)+'-'+str(delerCards)+'-'+str(player1D) not in self.tree:
      if str(playerSumCards)+'-'+str(delerCards)+'-'+str(not player1D) in self.tree:
        #ダブルダウンの可否で片方が存在していれば
        self.tree[str(playerSumCards)+'-'+str(delerCards)+'-'+str(player1D)] = multiAction(self.tree[str(playerSumCards)+'-'+str(delerCards)+'-'+str(not player1D)], (1))
      else:
      #初期化
        self.tree[str(playerSumCards)+'-'+str(delerCards)+'-'+str(player1D)] = createInitial()
    targetVal: int = 0
    targetKey: str = 'HIT'
    N = self.tree[str(playerSumCards)+'-'+str(delerCards)+'-'+str(player1D)]['N']
    for key in ['HIT', 'STAY', 'DOUBLE']:
      target = self.tree[str(playerSumCards)+'-'+str(delerCards)+'-'+str(player1D)][key]
      if targetVal >= 99999:
        #targetValが初期値選定されたらそれを超えることはできないので、
        break
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
  def simpleLearning(self, actions: list, reward: int):
    for info in actions:
      action = info['action']
      state = info['state']
      if state not in self.tree:
        self.tree[state] = createInitial()
      self.tree[state][action]['val'] += reward
      self.tree[state][action]['n'] += 1
      self.tree[state]['N'] += 1
    return
  def learning(self, actions: list, reward: int):
    self.simpleLearning(actions, reward) #まずシンプルラーニングはする
    if actions[0]['state'] not in self.tree:
      self.tree[actions[0]['state']] = createInitial()
    for index in range(len(actions)-1):
      preInfo = actions[index]
      nextInfo = actions[index+1]
      preAction = preInfo['action']
      nextAction = nextInfo['action']
      preState = preInfo['state']
      nextState = nextInfo['state']
      if nextState not in self.tree:
        self.tree[nextState] = createInitial()
      self.tree[preState][preAction]['val'] += (self.tree[nextState][nextAction]['val']/self.tree[nextState][nextAction]['n'])
    return

  def output_learnData(self):
    return self.tree
class Game:
  def __init__(self, decks, player1=None):
    self.decks = decks
    if player1 != None:
      self.player1 = {}
      self.player1.sum = 0
  def createDeck(self, decks):
    cards = [i for i in [1,2,3,4,5,6,7,8,9,10,11,12,13]]*int(float(4*decks))
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

  def max(self, sumCard:str) -> int:
    cards = sumCard.split('/')
    return int(cards[len(cards) - 1]) #昇順なので最後に最大値がくる

  def judge(self, playerSum, delerSum) -> str:
    result = "DRAW"
    playerMax = self.max(playerSum)
    delerMax = self.max(delerSum)
    if playerMax > delerMax:
      result = "WIN"
    elif playerMax < delerMax:
      result = "LOSE"
    else:
      result = "DRAW"
    return result
  
  def playGame(self, player1:player or montekarlo) -> Tuple[list, int]:
    # 1play
    deck = self.createDeck(self.decks)
    random.shuffle(deck)
    result: str = "" #引き分け,勝ち,負け,etc... 
    player1Cards = []
    dealer = dealerClass()
    player1D = False #ダブルダウンしたかどうか
    playerBJ = False #playerブラックジャック
    delerCards = []
    player1Cards,deck = self.pickAndInsertCards(deck, player1Cards, 2)
    delerCards,deck = self.pickAndInsertCards(deck, delerCards, 1)
    playerSum = self.ini_sum(player1Cards)
    delerSum = self.ini_sum(delerCards)
    plyer1_select = [] #本質的にはdictの配列なんだけど、なぜか型宣言できない...
    if self.max(delerSum) == 21:
      # ディーラーが初期手札で21ならディーラーの勝ち
      return plyer1_select, -1
      #報酬を-1としているが、player1_selectがからなので影響しない~...と考えれるし、
      #インスランスをつけたくなってもいい感じにできそう
    #playerの行動
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
    if result is not "LOSE" and self.max(playerSum) == 21:
      #ディーラーが21ではなくて、playerが21なら
      value = 1.5 #playerがBJの時の返りはボーナス付き
      if player1D:
        value *= 2
      return plyer1_select, value
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
      result = self.judge(playerSum, delerSum)
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
    nextLogs = [] #learning強化
    pres = []
    logs.append(player1Sum)
    nextLogs.append(player1Sum)
    pres.append(player1Sum)
    player1 = montekarlo()
    player2 = montekarlo()
    deckCount = 1
    game = Game(deckCount)
    for i in range(1000):
      player_select, result = game.playGame(player1)
      pres.append(result+pres[len(pres)-1])
    for i in range(50000):
      # 50000回繰り返す
      player_select1, result1 = game.playGame(player1)
      player1.simpleLearning(player_select1, result1*100)
      player_select2, result2 = game.playGame(player2)
      player2.learning(player_select2, result2*100)
    for i in range(1000):
      # 100回繰り返す
      player_select1, result1 = game.playGame(player1)
      player_select2, result2 = game.playGame(player2)
      logs.append(result1+logs[len(logs)-1])
      nextLogs.append(result2+nextLogs[len(nextLogs)-1])
    x_1 = np.array([ i for i in range(len(pres)) ])
    x_2 = np.array([ i for i in range(len(logs)) ])
    x_3 = np.array([ i for i in range(len(nextLogs)) ])
    pyplot.plot(x_1, np.array(pres), color='yellow')
    pyplot.plot(x_2, np.array(logs), color='red')
    pyplot.plot(x_3, np.array(nextLogs), color='blue')
    pyplot.show()
