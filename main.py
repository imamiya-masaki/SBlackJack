
# -*- coding: utf-8 -*-
import random
import numpy as np
import typing as tp
import json
from typing import Tuple, Dict
from matplotlib import pyplot, rcParams
from matplotlib.ticker import (MultipleLocator, AutoMinorLocator)
rcParams['font.family'] = 'sans-serif'
rcParams['font.sans-serif'] = ['Hiragino Maru Gothic Pro', 'Yu Gothic', 'Meirio', 'Takao', 'IPAexGothic', 'IPAPGothic', 'VL PGothic', 'Noto Sans CJK JP']
import datetime

hardHandDict = {
  #エースはindex9として扱い、以降,2,3,4,.. -> 0,1,2,...として扱う
  #HIT -> 1, DOUBLE -> 2, STAY -> 0
  '2': [1,1,1,1,1,1,1,1,1,1],
  '3': [1,1,1,1,1,1,1,1,1,1],
  '4': [1,1,1,1,1,1,1,1,1,1],
  '5': [1,1,1,1,1,1,1,1,1,1],
  '6': [1,1,1,1,1,1,1,1,1,1],
  '7': [1,1,1,1,1,1,1,1,1,1],
  '8': [1,1,1,1,1,1,1,1,1,1],
  '8': [1,1,1,1,1,1,1,1,1,1],
  '9': [1,2,2,2,2,1,1,1,1,1],
  '10': [2,2,2,2,2,2,2,2,1,1],
  '11': [2,2,2,2,2,2,2,2,2,1],
  '12': [1,1,0,0,0,1,1,1,1,1],
  '13': [0,0,0,0,0,1,1,1,1,1],
  '14': [0,0,0,0,0,1,1,1,1,1],
  '15': [0,0,0,0,0,1,1,1,1,1],
  '16': [0,0,0,0,0,1,1,1,1,1],
  '17': [0,0,0,0,0,0,0,0,0,0],
  '18': [0,0,0,0,0,0,0,0,0,0],
  '19': [0,0,0,0,0,0,0,0,0,0],
  '20': [0,0,0,0,0,0,0,0,0,0],
  '21': [0,0,0,0,0,0,0,0,0,0],
}

softHandDict = {
  #エースはindex9として扱い、以降,2,3,4,.. -> 0,1,2,...として扱う
  #HIT -> 1, DOUBLE -> 2, STAY -> 0
  '12': [1,1,1,2,2,1,1,1,1,1],
  '13': [1,1,1,2,2,1,1,1,1,1],
  '14': [1,1,1,2,2,1,1,1,1,1],
  '15': [1,1,2,2,2,1,1,1,1,1],
  '16': [1,1,2,2,2,1,1,1,1,1],
  '17': [1,2,2,2,2,1,1,1,1,1],
  '18': [0,2,2,2,2,0,0,1,1,1],
  '19': [0,0,0,0,0,0,0,0,0,0],
  '20': [0,0,0,0,0,0,0,0,0,0],
  '21': [0,0,0,0,0,0,0,0,0,0],
}
CHANGE_COST = 0.5
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
  def play(self, playerSumCards:str, delerCards:str, player1D:bool, changeSumCost=0, initialPlay=None, fieldInfo=None) -> Dict[str, str]:
    soft = False
    if len(playerSumCards.split('/')) >= 2:
      soft = True
    state = str(playerSumCards)+'-'+str(delerCards)+'-'+str(player1D)
    playerNum = self.max(playerSumCards) # maxで考える
    action = 'STAY'
    if playerNum == 21:
      return {'action': action, 'state': state}
    if soft:
      #ソフトハンド
      PreplayerSelect: int[...] = softHandDict[str(playerNum)]
      playerSelect: int = PreplayerSelect[self.max(delerCards)-2]
      if playerSelect == 1:
        #STAY
        action = 'HIT'
      elif playerSelect == 2:
        action = 'DOUBLE'
      else:
        action = 'STAY'
    else:
      #ハードハンド
      PreplayerSelect: int[...] = hardHandDict[str(playerNum)]
      playerSelect: int = PreplayerSelect[self.max(delerCards)-2]
      if playerSelect == 1:
        #STAY
        action = 'HIT'
      elif playerSelect == 2:
        action = 'DOUBLE'
      else:
        action = 'STAY'
    return {'action': action, 'state': state}
    

def simpleInitialPlay (playerSumCards:str, delerCards:str, player1D:bool, key: str) -> int:
  val = 0
  if not (key  ==  'DOUBLE' and player1D == True):
    val = 99999
  else:
    val = 0
  return val

BASIC_PARAM = 1 # 同一ではないが不可能ではない場合の数字
def basicStorategyPlay (playerSumCards:str, delerCards:str, player1D:bool, key: str) -> int:
  player = basicStorategy()
  player_play = player.play(playerSumCards,delerCards, player1D)
  if key == player_play['action']:
    # 選択されたkeyとplayer_playが同一な場合
    return 99999
  elif not key  ==  'DOUBLE' or player1D == True:
    # 同一ではないが不可能ではない場合
    return BASIC_PARAM
  else:
    # 不可能な場合
    return 0

def createInitial() -> dict:
  initial = {}
  initial['N'] = 0
  initial['HIT'] = {}
  initial['HIT']['n'] = 10
  initial['HIT']['val'] = 10
  initial['STAY'] = {}
  initial['STAY']['n'] = 10
  initial['STAY']['val'] = 10
  initial['DOUBLE'] = {}
  initial['DOUBLE']['n'] = 10
  initial['DOUBLE']['val'] = 10
  initial['EQUAL'] = {}
  initial['EQUAL']['n'] = 0
  initial['EQUAL']['val'] = 0
  initial['CHANGE'] = {}
  initial['CHANGE']['n'] = 0
  initial['CHANGE']['val'] = 0
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
  action['EQUAL'] = {}
  action['EQUAL']['n'] = target['EQUAL']['n']
  action['EQUAL']['val'] = target['EQUAL']['val']*number
  action['CHANGE'] = {}
  action['CHANGE']['n'] = target['CHANGE']['n']
  action['CHANGE']['val'] = target['CHANGE']['val']*number
  return action

def getStateValue(valInfo) -> float:
  value = float(0)
  for key in ['HIT', 'STAY', 'DOUBLE', 'EQUAL', 'CHANGE']:
    target = valInfo[key]
    ucb_cost = np.sqrt(2 * np.log(valInfo['N']))/ target['n']
    val = target['val'] + ucb_cost
    if value < val:
      value = val
  return value
class montekarlo:
  def __init__(self, actions = ['HIT', 'STAY', 'DOUBLE', 'EQUAL', 'CHANGE']):
    self.tree = {}
    self.actions = actions
  def play(self, playerSumCards:str, delerCards:str, player1D:bool, changeSumCost=0, initialPlay=simpleInitialPlay, fieldInfo=None) -> Dict[str, str]:
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
    for key in self.actions:
      target = self.tree[str(playerSumCards)+'-'+str(delerCards)+'-'+str(player1D)][key]
      if changeSumCost == 1 and key == 'CHANGE':
        continue
      if targetVal >= 99999:
        #targetValが初期値選定されたらそれを超えることはできないので、
        break
      if target['n'] == 0:
        val = initialPlay(playerSumCards, delerCards, player1D, key)
      else:
        ucb_cost = np.sqrt(2 * np.log(N))/ target['n']
        val = target['val'] + ucb_cost
      if targetVal < val:
        targetVal = val
        targetKey = key
    return {'action': targetKey, 'state': str(playerSumCards)+'-'+str(delerCards)+'-'+str(player1D)}
  def simpleLearning(self, actions: list, reward: float):
    actions.reverse()
    changeMode = False
    changeCnt = 0
    for info in actions:
      if info['action'] == 'CHANGE':
        changeCnt += 1
    reward += changeCnt*CHANGE_COST
    for index, info in enumerate(actions):
      action = info['action']
      state = info['state']
      if action == 'CHANGE':
        #CHANGEなら別処理
          changeMode = True
          state = actions[index]['state']
          nextState = actions[index-1]['state']
          action = actions[index]['action']
          nextAction = actions[index-1]['action']
          self.tree[state]['N'] += 1
          self.tree[state][action]['n'] += 1
          self.tree[state][action]['val'] += (self.tree[nextState][nextAction]['val']/self.tree[nextState][nextAction]['n']) - CHANGE_COST
      if changeMode:
        continue
      if state not in self.tree:
        self.tree[state] = createInitial()
      self.tree[state][action]['val'] += reward
      self.tree[state][action]['n'] += 1
      self.tree[state]['N'] += 1
    return
  def learning(self, actions: list, reward: int):
    self.simpleLearning(actions, reward) #まずシンプルラーニングはする
    if actions == []:
      # ディーラーblackjackの時は計算しない
      return
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
    output = []
    keys = list(self.tree.keys())
    for key in keys:
      output.append(key +':'+json.dumps(self.tree[key]))
    return '\n'.join(output)
class montekarlo_withFieldInfo:
  def __init__(self):
    self.tree = {}
  def euclidean_distance(self, x, y)-> float:   
    return np.sqrt(np.sum((x - y) ** 2))
  def list_key(self, a: list) -> str:
    get = [str(i) for i in a]
    return '-'.join(get)
  def seisoku(self, val: float, min: float, max: float)->float:
    if max - min == 0:
      return val
    return (val - min)/(max-min)
  def getFieldInfoValue(self, key: str, fieldInfo: list, action: str) -> Tuple[int, bool]:
    if key not in self.tree:
      # keyはself.treeの中にある前提
      print('error getFieldInfoValue')
      return 0, False
    if action not in self.tree[key]:
      self.tree[key][action] = {}
    if 'fieldInfo' not in self.tree[key][action]:
      #fieldInfoにベクトルを格納していく
      self.tree[key][action]['fieldInfo'] = {}
    flag = False
    donpisita = False
    val = float(0)
    values = []
    gets = []
    for val_key in self.tree[key][action]['fieldInfo']:
      #1 ~ 13 -> 0 ~ 12として扱う
      flag = True
      spl = [int(a) for a in val_key.split('-')]
      get = float(self.tree[key][action]['fieldInfo'][val_key])
      yuku = self.euclidean_distance(np.array(spl), np.array(fieldInfo))
      values.append(yuku)
      gets.append(get)
    if len(values) == 0:
      return 0,False
    max_val = 0
    min_val = 0
    if min(values) != 0:
      max_val = 1/min(values)
    if max(values) != 0:
      min_val = 1/max(values)
    if min(values) == 0 or max_val > 100:
      max_val = 100
    if max(values) == 0 or min_val > 10:
      min_val = 10
    for index, v in enumerate(values):
      val += gets[index]*self.seisoku(v,min_val, max_val)
    return val/len(values),flag
  def play(self, playerSumCards:str, delerCards:str, player1D:bool, changeSumCost=0, initialPlay=simpleInitialPlay, fieldInfo=[0,0,0,0,0,0,0,0,0,0,0,0,0]) -> Dict[str, str]:
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
    for key in ['HIT', 'STAY', 'DOUBLE', 'EQUAL']:
      target = self.tree[str(playerSumCards)+'-'+str(delerCards)+'-'+str(player1D)][key]
      if target['n'] == 0:
        val = initialPlay(playerSumCards, delerCards, player1D, key)
      else:
        ucb_cost = np.sqrt(2 * np.log(N))/ target['n']
        val_g,flag = self.getFieldInfoValue(str(playerSumCards)+'-'+str(delerCards)+'-'+str(player1D), fieldInfo, key)
        if flag == False:
          val_g = target['val']
        val = val_g + ucb_cost
      if targetVal < val:
        targetVal = val
        targetKey = key
    return {'action': targetKey, 'state': str(playerSumCards)+'-'+str(delerCards)+'-'+str(player1D), 'fieldInfo': fieldInfo}
  def simpleLearning(self, actions: list, reward: int):
    for info in actions:
      action = info['action']
      state = info['state']
      fieldInfo = info['fieldInfo']
      if state not in self.tree:
        self.tree[state] = createInitial()
      self.tree[state][action]['val'] += reward
      self.tree[state][action]['n'] += 1
      self.tree[state]['N'] += 1
      if 'fieldInfo' in self.tree[state][action]:
        if self.list_key(fieldInfo) not in self.tree[state][action]['fieldInfo']:
          self.tree[state][action]['fieldInfo'][self.list_key(fieldInfo)] = 0
        self.tree[state][action]['fieldInfo'][self.list_key(fieldInfo)] += reward
    return
  def learning(self, actions: list, reward: int):
    self.simpleLearning(actions, reward) #まずシンプルラーニングはする
    if actions == []:
      # ディーラーblackjackの時は計算しない
      return
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
  def createDeck(self):
    cards = [i for i in [1,2,3,4,5,6,7,8,9,10,11,12,13]]*int(float(4*self.decks))
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
      map[int(val) + targetCard] = True
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
  
  def playGame(self, player1:player or montekarlo, initialPlay=simpleInitialPlay, displayCardCnt=0, initialDeck=[]) -> Tuple[list, int]:
    # 1play
    deck = []
    if len(initialDeck) == 0:
      deck = self.createDeck()
      random.shuffle(deck)
    else:
      deck = [a for a in initialDeck]
    result: str = "" #引き分け,勝ち,負け,etc... 
    player1Cards = []
    dealer = dealerClass()
    player1D = False #ダブルダウンしたかどうか
    playerBJ = False #playerブラックジャック
    delerCards = []
    displayCards = []
    player1Cards,deck = self.pickAndInsertCards(deck, player1Cards, 2)
    delerCards,deck = self.pickAndInsertCards(deck, delerCards, 2)
    displayCards, deck = self.pickAndInsertCards(deck, displayCards, displayCardCnt)
    displayMemo = [0,0,0,0,0,0,0,0,0,0,0,0,0]
    for dCard in displayCards:
      displayMemo[dCard-1] += 1
    openDelerCard = [delerCards[0]]
    playerSum = self.ini_sum(player1Cards)
    delerSum = self.ini_sum(delerCards)
    openDelerSum = self.ini_sum(openDelerCard) # プレイヤーが見えているディーラーのカード
    plyer1_select = [] #本質的にはdictの配列なんだけど、なぜか型宣言できない...
    if self.max(delerSum) == 21:
      # ディーラーが初期手札で21ならディーラーの勝ち
      return plyer1_select, -1
      #報酬を-1としているが、player1_selectがからなので影響しない~...と考えれるし、
      #インスランスをつけたくなってもいい感じにできそう
    if result is not "LOSE" and self.max(playerSum) == 21:
      #ディーラーが21ではなくて、playerが21なら
      value = 1.5 #playerがBJの時の返りはボーナス付き
      return plyer1_select, value
    #playerの行動
    equal = False
    changeSumCost = 0
    while True:
      get: Dict[str, str, str] = player1.play(playerSum, openDelerSum, player1D, changeSumCost=changeSumCost, initialPlay=initialPlay, fieldInfo=displayMemo)
      plyer1_select.append(get)
      if get['action'] == 'HIT' or get['action'] == 'DOUBLE':
        card, deck = self.pickCard(deck)
        playerSum, isSafe = self.calculate(playerSum, card)
        if isSafe == False:
          result = "LOSE"
        if get['action'] == 'DOUBLE':
          player1D = True
      if get['action'] == 'EQUAL':
        equal = True
        break
      if get['action'] == 'CHANGE':
        changeSumCost += CHANGE_COST
        pCards = []
        pCards, deck = self.pickAndInsertCards(deck, pCards, 2)
        playerSum = self.ini_sum(pCards)
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
          if isSafe == False:
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
    if equal == True and reward == 0:
      #equalルール
      reward = 8
    elif equal == True and reward != 0:
      reward = -1
    if player1D == True:
      reward *= 2
    if changeSumCost > 0:
      reward -= changeSumCost
    return plyer1_select, reward

  def ini_sum(self,cards: list) -> str:
    result = "0"
    for card in cards:
      result, flag = self.calculate(result, card)
    return result
class BJLog:
  def __init__(self, name):
    self.name = name
    self.results = []
    self.actions = []
    self.states = {}
  def createX(self, list) -> np.ndarray:
    return np.array([ i for i in range(len(list)) ])
  def push(self, a, actions=[]) -> None:
    self.results.append(a)
    for action in actions:
      state = action['state']
      if state not in self.states:
        self.states[state] = 0
      self.states[state] += a
  def summaryGraph(self, ax, color) -> None:
    result = 0
    logs = []
    logs.append(result)
    for a in self.results:
      logs.append(a+logs[len(logs)-1])
    ax.plot(self.createX(logs), np.array(logs), label=self.name)
  def increaseGraph(self, ax: pyplot.Axes, color) -> None:
    targetList = list(self.states.keys())
    ax.bar(np.array(targetList), np.array(list(self.states.values())), label=self.name, width=1.5)
  def targetState(self, index):
    #increaseGraphでindex -> stateのメモカをしているので
    return self.states.keys()[index]

if __name__ == '__main__':
    player1Sum = 0 # player0の勝ち星　グラフよう
    logs = BJLog('通常のモンテカルロ木') # playerのログをとる
    nextLogs = BJLog('ベーシックストラテジーを学習に取り入れたモンテカルロ木') #learning強化
    basicLogs = BJLog('ベーシックストラテジー') #basicStorategy
    pres = BJLog('学習していないモンテカルロ木')
    newnewLogs = BJLog('newnewLogs')
    noChangeAndEqualLog = BJLog('CHANGEとEQUALがない【ベーシックストラテジーを学習に取り入れたモンテカルロ木】')
    noChangeAndEqualLogWeak = BJLog('CHANGEとEQUALがない【通常のモンテカルロ木】')
    player1 = montekarlo()
    player2 = montekarlo()
    player3 = montekarlo()
    basicPlayer = basicStorategy()
    noChangeAndEqual = montekarlo(actions=['HIT', 'STAY', 'DOUBLE'])
    noChangeAndEqual_weak = montekarlo(actions=['HIT', 'STAY', 'DOUBLE'])
    deckCount = 1
    game = Game(deckCount)
    #initialPlayの設定
    initialPlay = simpleInitialPlay
    basicInitial = basicStorategyPlay
    # gameクラステスト
    # testGame = Game(deckCount)
    # print(testGame.calculate('1/11', 1))
    for i in range(0000):
      player_select, result = game.playGame(player1,initialPlay)
      pres.push(result)
    print('done:pre')
    for i in range(500000):
      # 10000回繰り返す
      decks = game.createDeck()
      random.shuffle(decks)
      player_select1, result1 = game.playGame(player1,initialPlay,0,decks)
      player1.simpleLearning(player_select1, result1*1)
      player_select2, result2 = game.playGame(basicPlayer, initialPlay,0,decks)
      player2.simpleLearning(player_select2, result2*1)
      player_selectChange, result3 = game.playGame(basicPlayer, initialPlay,0,decks)
      noChangeAndEqual.simpleLearning(player_selectChange, result3)
      player_selectChange_week, result4 = game.playGame(noChangeAndEqual_weak, initialPlay,0,decks)
      noChangeAndEqual_weak.simpleLearning(player_selectChange_week, result4)
      # player_select3, result3 = game.playGame(basicPlayer, initialPlay)
      # player3.learning(player_select3, result3*1)
    for i in range(500000):
      # 10000回繰り返す
      decks = game.createDeck()
      random.shuffle(decks)
      player_select1, result1 = game.playGame(player1,initialPlay,0,decks)
      player1.simpleLearning(player_select1, result1*1)
      player_select2, result2 = game.playGame(player2, initialPlay,0,decks)
      player2.simpleLearning(player_select2, result2*1)
      player_selectChange, nochange_result = game.playGame(noChangeAndEqual, initialPlay,0,decks)
      noChangeAndEqual.simpleLearning(player_selectChange, nochange_result)
      player_selectChange_week, result4 = game.playGame(noChangeAndEqual_weak, initialPlay,0,decks)
      noChangeAndEqual_weak.simpleLearning(player_selectChange_week, result4)
      # player_select3, result3 = game.playGame(basicPlayer, initialPlay)
      # player3.learning(player_select3, result3*1)
    print('done:learning')
    for i in range(1000):
      # 10000回繰り返す
      decks = game.createDeck()
      random.shuffle(decks)
      player_select1, result1 = game.playGame(player1,initialPlay,0,decks)
      player_select2, result2 = game.playGame(player2, initialPlay,0,decks)
      player_selectChange, nochange_result = game.playGame(noChangeAndEqual, initialPlay,0,decks)
      player_selectChange_week, nochange_result_weak = game.playGame(noChangeAndEqual_weak, initialPlay,0,decks)
      player_basic, result3 = game.playGame(basicPlayer)
      logs.push(result1, player_select1)
      nextLogs.push(result2, player_select2)
      basicLogs.push(result3, player_basic)
      noChangeAndEqualLog.push(nochange_result, player_selectChange)
      noChangeAndEqualLogWeak.push(nochange_result_weak, player_selectChange_week)
    print('done:write')
    fig, ax = pyplot.subplots()
    pres.summaryGraph(ax,color='yellow')
    logs.summaryGraph(ax,color='red')
    nextLogs.summaryGraph(ax,color='blue')
    basicLogs.summaryGraph(ax,color='orange')
    noChangeAndEqualLog.summaryGraph(ax,color='pink')
    noChangeAndEqualLogWeak.summaryGraph(ax,color='green')
    f = open('player2Data', 'w')
    f.write(player2.output_learnData())
    f = open('player1Data', 'w')
    f.write(player1.output_learnData())
    f = open('noChangeAndEqualData', 'w')
    f.write(noChangeAndEqual.output_learnData())
    dt_now = datetime.datetime.now()
    fig.legend()
    fig.savefig('outputSummaryGraph/' + dt_now.strftime('%Y-%m-%d %H:%M:%S') +'.png')
    fig2, ax2 = pyplot.subplots()
    pyplot.xticks(rotation=90)
    logs.increaseGraph(ax2, color='red')
    noChangeAndEqualLogWeak.increaseGraph(ax2, color='blue')
    fig2.legend()
    fig2.savefig('outputIncreaseGraph/' + dt_now.strftime('%Y-%m-%d %H:%M:%S') +'.png')
    pyplot.show()