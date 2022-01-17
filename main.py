
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
rcParams["figure.figsize"] = (12, 6)
import datetime

hardHandDict = {
  #エースはindex9として扱い、以降,2,3,4,.. -> 0,1,2,...として扱う
  #STAY -> 0, HIT -> 1, DOUBLE -> 2, CHANGE -> 3, EQUAL -> 4
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
  #STAY -> 0, HIT -> 1, DOUBLE -> 2, CHANGE -> 3, EQUAL -> 4
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
  def __init__(self, soft=softHandDict, hard=hardHandDict):
    self.tree = {}
    self.soft = soft
    self.hard = hard
  def simpleLearning (self) -> None:
     #他のモデルと合わせるため
    return None
  def playerSelectNumberMap (self, playerNum: str, delerCards: str, selectDict: dict, changeSumCost: int, soft=True) -> str:
    PreplayerSelect: int[...] = selectDict[playerNum]
    playerSelect: int = PreplayerSelect[self.max(delerCards)-2]
    defaultDict = softHandDict
    if soft == False:
      defaultDict = hardHandDict
    action = ''
    if playerSelect == 1:
      action = 'HIT'
    elif playerSelect == 2:
      action = 'DOUBLE'
    elif playerSelect == 3:
      if changeSumCost < 1:
        action = 'CHANGE'
      else:
        action = self.playerSelectNumberMap(playerNum, delerCards, defaultDict, changeSumCost, soft)
    elif playerSelect == 4:
      action = 'EQUAL'
    else:
      #STAY -> 0
      action = 'STAY'
    return action
  def play(self, playerSumCards:str, delerCards:str, player1D:bool, changeSumCost=0, initialPlay=None, fieldInfo=None) -> Dict[str, str]:
    soft = False
    if len(playerSumCards.split('/')) >= 2:
      soft = True
    state = str(playerSumCards)+'-'+str(delerCards)
    playerNum = self.max(playerSumCards) # maxで考える
    action = 'STAY'
    if playerNum == 21:
      return {'action': action, 'state': state}
    if soft:
      #ソフトハンド
      action = self.playerSelectNumberMap(str(playerNum), delerCards, self.soft, changeSumCost, soft=True)
    else:
      #ハードハンド
      action = self.playerSelectNumberMap(str(playerNum), delerCards, self.hard, changeSumCost, soft=False)
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
    if str(playerSumCards)+'-'+str(delerCards) not in self.tree:
        #初期化
        self.tree[str(playerSumCards)+'-'+str(delerCards)] = createInitial()
    targetVal: int = 0
    targetKey: str = 'HIT'
    first = False
    N = self.tree[str(playerSumCards)+'-'+str(delerCards)]['N']
    for key in self.actions:
      target = self.tree[str(playerSumCards)+'-'+str(delerCards)][key]
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
      if targetVal < val or first == False:
        first = True
        targetVal = val
        targetKey = key
    return {'action': targetKey, 'state': str(playerSumCards)+'-'+str(delerCards)}
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
        #後ろから考えると、チェンジを結構するたびにCHANGE_COST分マイナス
          reward -= CHANGE_COST
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
    keys: list[str] = list(self.tree.keys())
    for key in keys:
      spl = key.split('-')
      output.append(key +':'+json.dumps(self.tree[key]) + ', play: ' + self.play(spl[0], spl[1], False)['action'])
    return '\n'.join(output)
class montekarlo_withFieldInfo:
  def __init__(self, actions = ['HIT', 'STAY', 'DOUBLE', 'EQUAL', 'CHANGE']):
    self.tree = {}
    self.actions = actions
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
    if str(playerSumCards)+'-'+str(delerCards) not in self.tree:
      if str(playerSumCards)+'-'+str(delerCards)+'-'+str(not player1D) in self.tree:
        #ダブルダウンの可否で片方が存在していれば
        self.tree[str(playerSumCards)+'-'+str(delerCards)] = multiAction(self.tree[str(playerSumCards)+'-'+str(delerCards)+'-'+str(not player1D)], (1))
      else:
        #初期化
        self.tree[str(playerSumCards)+'-'+str(delerCards)] = createInitial()
    targetVal: int = 0
    targetKey: str = 'HIT'
    first = False
    N = self.tree[str(playerSumCards)+'-'+str(delerCards)]['N']
    for key in self.actions:
      if changeSumCost == 1 and key == 'CHANGE':
        continue
      target = self.tree[str(playerSumCards)+'-'+str(delerCards)][key]
      if target['n'] == 0:
        val = initialPlay(playerSumCards, delerCards, player1D, key)
      else:
        ucb_cost = np.sqrt(2 * np.log(N))/ target['n']
        val_g,flag = self.getFieldInfoValue(str(playerSumCards)+'-'+str(delerCards), fieldInfo, key)
        if flag == False:
          val_g = target['val']
        val = val_g + ucb_cost
      if targetVal < val or first == False:
        first = True
        targetVal = val
        targetKey = key
    return {'action': targetKey, 'state': str(playerSumCards)+'-'+str(delerCards), 'fieldInfo': fieldInfo}
  def simpleLearning(self, actions: list, reward: int):
    actions.reverse()
    changeCnt = 0
    for info in actions:
      if info['action'] == 'CHANGE':
        changeCnt += 1
    reward += changeCnt*CHANGE_COST
    for info in actions:
      action = info['action']
      state = info['state']
      fieldInfo = info['fieldInfo']
      if state not in self.tree:
        self.tree[state] = createInitial()
      if action == 'CHANGE':
        #後ろから考えると、チェンジを結構するたびにCHANGE_COST分マイナス
          reward -= CHANGE_COST
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
  
  def playGame(self, player1:player or montekarlo, initialPlay=simpleInitialPlay, displayCardCnt=10, initialDeck=[]) -> Tuple[list, int]:
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
    self.cnt = {}
  def getName (self) -> str:
    return self.name
  def createX(self, list) -> np.ndarray:
    return np.array([ i for i in range(len(list)) ])
  def push(self, a, actions=[]) -> None:
    self.results.append(a)
    for action in actions:
      state = action['state']
      if state not in self.states:
        self.states[state] = 0
        self.cnt[state] = 0
      self.states[state] += a
      self.cnt[state] += 1
  def createGraph(self) -> Tuple[np.ndarray, np.ndarray]:
    result = 0
    logs = []
    logs.append(result)
    for a in self.results:
      logs.append(a+logs[len(logs)-1])
    return self.createX(logs), np.array(logs)
  def summaryGraphPlot(self, ax: pyplot.Axes, color) -> None:
    x,y = self.createGraph()
    ax.plot(x, y, label=self.name, color=color)
  def increaseGraph(self, ax: pyplot.Axes, color) -> None:
    targetList = list(self.states.keys())
    ax.bar(np.array(targetList), np.array(list(self.states.values())), label=self.name, width=1.5)
  def increasePickUp(self, b: dict) -> dict:
    # bよりも高い場合pickupする
    output = {}
    for key, value in self.states.items():
      if key in b['state']:
        if float(value/self.cnt[key]) - float(b['state'][key]/b['cnt'][key]) > 0 and float(self.cnt[key]) > 0:
          output[key] = (value/self.cnt[key]) - (b['state'][key]/b['cnt'][key])
    return output
  def logDiffPlot(self, ax: pyplot.Axes, b: any, name='') -> None:
    a1,b1 = self.createGraph()
    a2,b2 = b.createGraph()
    output = []
    for index in a1:
      output.append(b1[index] - b2[index])
    ax.plot(a1, np.array(output), label=self.name + 'と' + b.name + 'のdiff')
  def max(self,sumCard:str) -> int:
    cards = sumCard.split('/')
    return int(cards[len(cards) - 1]) #昇順なので最後に最大値がくる
  def pickUpOutput(self, compareDiffDict, name, player) -> tuple:
    compareDiffDictTuples: list[Tuple[str, str]] = sorted(compareDiffDict.items(), key=lambda x:x[1])
    compareDiffDictTuples.reverse()
    diff_x = []
    diff_y = []
    fileOutputDiff = {}
    soft = {}
    hard = {}
    for key,value in softHandDict.items():
      soft[key] = [ a for a in value]
    for key,value in hardHandDict.items():
      hard[key] = [ a for a in value]
    for x, y in compareDiffDictTuples:
      diff_x.append(x)
      diff_y.append(y)
      spl = x.split('-')
      fileOutputDiff[x] = {'value': y, 'action': player.play(spl[0], spl[1], False)}
      meCard = str(self.max(spl[0]))
      enemyCard = self.max(spl[1]) - 2
      if len(spl[0].split('/')) == 1:
        # hard
        if fileOutputDiff[x]['action']['action'] == 'STAY':
          hard[meCard][enemyCard] = 0
        if fileOutputDiff[x]['action']['action'] == 'HIT':
          hard[meCard][enemyCard] = 1
        elif fileOutputDiff[x]['action']['action'] == 'DOUBLE':
          hard[meCard][enemyCard] = 2
        if fileOutputDiff[x]['action']['action'] == 'CHANGE':
          hard[meCard][enemyCard] = 3
        elif fileOutputDiff[x]['action']['action'] == 'EQUAL':
          hard[meCard][enemyCard] = 4
      else:
        # soft
        if fileOutputDiff[x]['action']['action'] == 'STAY':
          soft[meCard][enemyCard] = 0
        if fileOutputDiff[x]['action']['action'] == 'HIT':
          soft[meCard][enemyCard] = 1
        elif fileOutputDiff[x]['action']['action'] == 'DOUBLE':
          soft[meCard][enemyCard] = 2
        if fileOutputDiff[x]['action']['action'] == 'CHANGE':
          soft[meCard][enemyCard] = 3
        elif fileOutputDiff[x]['action']['action'] == 'EQUAL':
          soft[meCard][enemyCard] = 4
    f = open(name, 'w')
    f.write(json.dumps(fileOutputDiff, indent=2))
    f = open('basic-impro-' + name + '.json', 'w')
    f.write(json.dumps({'hard': hard, 'soft': soft}, indent=2))
    return diff_x, diff_y
  def getStates(self) -> dict:
    return {'state': self.states, 'cnt': self.cnt}
  def targetState(self, index):
    #increaseGraphでindex -> stateのメモカをしているので
    return self.states.keys()[index]

if __name__ == '__main__':
    player1Sum = 0 # player0の勝ち星　グラフよう
    logs = BJLog('通常のモンテカルロ木') # playerのログをとる
    nextLogs = BJLog('ベーシックストラテジーを学習に取り入れたモンテカルロ木') #learning強化
    basicLogs = BJLog('ベーシックストラテジー') #basicStorategy
    basicLogs_imp = BJLog('ルールに対応したベーシックストラテジー') #basicStorategy
    pres = BJLog('学習していないモンテカルロ木')
    newnewLogs = BJLog('特徴ベクトルモンテカルロ木')
    newnewLogs2 = BJLog('特徴ベクトルモンテカルロ木: CHANGEとEQUALがない')
    noChangeAndEqualLog = BJLog('CHANGEとEQUALがない【ベーシックストラテジーを学習に取り入れたモンテカルロ木】')
    noChangeAndEqualLogWeak = BJLog('CHANGEとEQUALがない【通常のモンテカルロ木】')
    noChangeAndEqualLogWeakWithCHANGE = BJLog('EQUALがない【通常のモンテカルロ木】')
    noChangeAndEqualLogWeakWithEQUAL = BJLog('CHANGEがない【通常のモンテカルロ木】')
    player1 = montekarlo()
    player2 = montekarlo()
    player3 = montekarlo()
    player7 = montekarlo_withFieldInfo()
    player8 = montekarlo_withFieldInfo(actions=['HIT', 'STAY', 'DOUBLE'])
    basicPlayer = basicStorategy()
    json_basic_imp = json.load(open('basic-impro-2ParamDiffData.json', 'r'))
    basicPlayer_imp = basicStorategy(soft=json_basic_imp['soft'], hard=json_basic_imp['hard'])
    noChangeAndEqual = montekarlo(actions=['HIT', 'STAY', 'DOUBLE'])
    noChangeAndEqual_weak = montekarlo(actions=['HIT', 'STAY', 'DOUBLE'])
    noChangeAndEqual_weak_with_CHANGE = montekarlo(actions=['HIT', 'STAY', 'DOUBLE', 'CHANGE'])
    noChangeAndEqual_weak_with_EQUAL = montekarlo(actions=['HIT', 'STAY', 'DOUBLE', 'EQUAL'])
    modelAndLogs = []
    deckCount = 1
    game = Game(deckCount)
    doribun = 500000
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
    for i in range(doribun):
      decks = game.createDeck()
      random.shuffle(decks)
      player_select1, result1 = game.playGame(player1,initialPlay,0,decks)
      player1.simpleLearning(player_select1, result1)

      player_select2, result2 = game.playGame(basicPlayer, initialPlay,0,decks)
      player2.simpleLearning(player_select2, result2)

      player_select7, result7 = game.playGame(player7, initialPlay,0,decks)
      player7.simpleLearning(player_select7, result7)

      player_select8, result8 = game.playGame(player8, initialPlay,0,decks)
      player8.simpleLearning(player_select8, result8)

      player_selectChange, result3 = game.playGame(basicPlayer, initialPlay,0,decks)
      noChangeAndEqual.simpleLearning(player_selectChange, result3)

      player_selectChange_week, result4 = game.playGame(noChangeAndEqual_weak, initialPlay,0,decks)
      noChangeAndEqual_weak.simpleLearning(player_selectChange_week, result4)

      player_selectChange_week_CHANGE, result5 = game.playGame(noChangeAndEqual_weak_with_CHANGE, initialPlay,0,decks)
      noChangeAndEqual_weak_with_CHANGE.simpleLearning(player_selectChange_week_CHANGE, result5)

      player_selectChange_week_EQUAL, result6 = game.playGame(noChangeAndEqual_weak_with_EQUAL, initialPlay,0,decks)
      noChangeAndEqual_weak_with_EQUAL.simpleLearning(player_selectChange_week_EQUAL, result6)
      # player_select3, result3 = game.playGame(basicPlayer, initialPlay)
      # player3.learning(player_select3, result3*1)
    for i in range(doribun):
      decks = game.createDeck()
      random.shuffle(decks)
      player_select1, result1 = game.playGame(player1,initialPlay,0,decks)
      player1.simpleLearning(player_select1, result1*1)

      player_select2, result2 = game.playGame(player2, initialPlay,0,decks)
      player2.simpleLearning(player_select2, result2*1)

      player_select7, result7 = game.playGame(player7, initialPlay,0,decks)
      player7.simpleLearning(player_select7, result7)

      player_select8, result8 = game.playGame(player8, initialPlay,0,decks)
      player8.simpleLearning(player_select8, result8)

      player_selectChange, nochange_result = game.playGame(noChangeAndEqual, initialPlay,0,decks)
      noChangeAndEqual.simpleLearning(player_selectChange, nochange_result)

      player_selectChange_week, result4 = game.playGame(noChangeAndEqual_weak, initialPlay,0,decks)
      noChangeAndEqual_weak.simpleLearning(player_selectChange_week, result4)

      player_selectChange_week_CHANGE, result5 = game.playGame(noChangeAndEqual_weak_with_CHANGE, initialPlay,0,decks)
      noChangeAndEqual_weak_with_CHANGE.simpleLearning(player_selectChange_week_CHANGE, result5)

      player_selectChange_week_EQUAL, result6 = game.playGame(noChangeAndEqual_weak_with_EQUAL, initialPlay,0,decks)
      noChangeAndEqual_weak_with_EQUAL.simpleLearning(player_selectChange_week_EQUAL, result6)
      # player_select3, result3 = game.playGame(basicPlayer, initialPlay)
      # player3.learning(player_select3, result3*1)
    print('done:learning')
    for i in range(10000):
      # 10000回繰り返す
      decks = game.createDeck()
      random.shuffle(decks)

      player_select1, result1 = game.playGame(player1,initialPlay,0,decks)
      player1.simpleLearning(player_select1, result1)

      player_select2, result2 = game.playGame(player2, initialPlay,0,decks)
      player2.simpleLearning(player_select2, result2)

      player_select7, result7 = game.playGame(player7, initialPlay,0,decks)
      player7.simpleLearning(player_select7, result7)

      player_select8, result8 = game.playGame(player8, initialPlay,0,decks)
      player8.simpleLearning(player_select8, result8)

      player_selectChange, nochange_result = game.playGame(noChangeAndEqual, initialPlay,0,decks)
      noChangeAndEqual.simpleLearning(player_selectChange, nochange_result)

      player_selectChange_week, nochange_result_weak = game.playGame(noChangeAndEqual_weak, initialPlay,0,decks)
      noChangeAndEqual_weak.simpleLearning(player_selectChange_week, nochange_result_weak)

      player_basic, result3 = game.playGame(basicPlayer)

      player_basic_imp, result3_imp = game.playGame(basicPlayer_imp)

      player_selectChange_week_CHANGE, result5 = game.playGame(noChangeAndEqual_weak_with_CHANGE, initialPlay,0,decks)
      noChangeAndEqual_weak_with_CHANGE.simpleLearning(player_selectChange_week_CHANGE, result5)

      player_selectChange_week_EQUAL, result6 = game.playGame(noChangeAndEqual_weak_with_EQUAL, initialPlay,0,decks)
      noChangeAndEqual_weak_with_EQUAL.simpleLearning(player_selectChange_week_EQUAL, result6)
      logs.push(result1, player_select1)
      nextLogs.push(result2, player_select2)
      basicLogs.push(result3, player_basic)
      basicLogs_imp.push(result3_imp, player_basic_imp)
      noChangeAndEqualLog.push(nochange_result, player_selectChange)
      noChangeAndEqualLogWeak.push(nochange_result_weak, player_selectChange_week)
      noChangeAndEqualLogWeakWithCHANGE.push(result5, player_selectChange_week_CHANGE)
      noChangeAndEqualLogWeakWithEQUAL.push(result6, player_selectChange_week_EQUAL)
      newnewLogs.push(result7, player_select7)
      newnewLogs2.push(result8, player_select8)
    print('done:write:')
    fig, ax = pyplot.subplots()
    fig.suptitle(str(doribun*2)+'回学習させたモデルの結果')
    logs.summaryGraphPlot(ax,color='red')
    nextLogs.summaryGraphPlot(ax,color='blue')
    basicLogs.summaryGraphPlot(ax,color='orange')
    noChangeAndEqualLog.summaryGraphPlot(ax,color='pink')
    noChangeAndEqualLogWeak.summaryGraphPlot(ax,color='green')
    basicLogs_imp.summaryGraphPlot(ax, color='gray')
    # newnewLogs.summaryGraphPlot(ax,color='black')
    # newnewLogs2.summaryGraphPlot(ax, color='gray')
    f = open('player2Data', 'w')
    f.write(player2.output_learnData())
    f = open('player1Data', 'w')
    f.write(player1.output_learnData())
    f = open('noChangeAndEqualData', 'w')
    f.write(noChangeAndEqual.output_learnData())
    f = open('noChangeAndEqual_weak_with_CHANGEData', 'w')
    f.write(noChangeAndEqual_weak_with_CHANGE.output_learnData())
    f = open('noChangeAndEqual_weak_with_EQUALData', 'w')
    f.write(noChangeAndEqual_weak_with_EQUAL.output_learnData())
    dt_now = datetime.datetime.now()
    fig.legend(bbox_to_anchor=(1, 0.25))
    fig.savefig('outputsummaryGraph/' + dt_now.strftime('%Y-%m-%d %H:%M:%S') +'.png')
    fig2, ax2 = pyplot.subplots()
    pyplot.xticks(rotation=90)
    logs.increaseGraph(ax2, color='red')
    noChangeAndEqualLogWeak.increaseGraph(ax2, color='blue')
    compareDiffDictWeak = logs.increasePickUp(noChangeAndEqualLogWeak.getStates())
    compareDiffDictWeakWithEqual = logs.increasePickUp(noChangeAndEqualLogWeakWithEQUAL.getStates())
    compareDiffDictWeakWithCHANGE = logs.increasePickUp(noChangeAndEqualLogWeakWithCHANGE.getStates())
    fig2.legend()
    fig2.savefig('outputIncreaseGraph/' + dt_now.strftime('%Y-%m-%d %H:%M:%S') +'.png')
    fig3, ax3 = pyplot.subplots(nrows=1, ncols=3)
    pyplot.xticks(rotation=90)
    diff_x_weak, diff_y_weak = logs.pickUpOutput(compareDiffDictWeak, '2ParamDiffData', player1)
    diff_x_weak_equal, diff_y_weak_equal = logs.pickUpOutput(compareDiffDictWeak, '1ParamDiffDataWithEqual', noChangeAndEqual_weak_with_EQUAL)
    diff_x_weak_change, diff_y_weak_change = logs.pickUpOutput(compareDiffDictWeak, '1ParamDiffDataWithCHANGE', noChangeAndEqual_weak_with_CHANGE)
    ax3[0].bar(np.array(list(diff_x_weak)), np.array(list(diff_y_weak)), width=1.0, tick_label=np.array(list(diff_x_weak)))
    ax3[0].set_title(noChangeAndEqualLogWeak.getName())
    ax3[1].bar(np.array(list(diff_x_weak_equal)), np.array(list(diff_y_weak_equal)), width=1.0, tick_label=np.array(list(diff_x_weak_equal)))
    ax3[1].set_title(noChangeAndEqualLogWeakWithEQUAL.getName())
    ax3[2].bar(np.array(list(diff_x_weak_change)), np.array(list(diff_y_weak_change)), width=1.0, tick_label=np.array(list(diff_x_weak_change)))
    ax3[2].set_title(noChangeAndEqualLogWeakWithCHANGE.getName())
    fig3.suptitle('通常のモンテカルロ木 > n のdiff')
    fig3.legend()
    fig3.savefig('outputDiffGraph/' + dt_now.strftime('%Y-%m-%d %H:%M:%S') +'.png')

    # 改良ベーシックストラテジー
    fig4, ax4 = pyplot.subplots()
    fig4.suptitle('ベーシックストラテジーの改良前,後')
    basicLogs_imp.summaryGraphPlot(ax4, color='blue')
    basicLogs.summaryGraphPlot(ax4,color='red')
    fig4.legend()
    fig4.savefig('outputsummaryGraph_unique/' + dt_now.strftime('%Y-%m-%d %H:%M:%S') +'.png')

    fig5, ax5 = pyplot.subplots()
    fig5.suptitle('ベーシックストラテジーの改良前/後のdiffと、モンテカルロ木のルール追加前/後')
    logs.logDiffPlot(ax5,noChangeAndEqualLogWeak)
    basicLogs_imp.logDiffPlot(ax5,basicLogs)
    fig5.legend()
    fig5.savefig('outputDiffs/' + dt_now.strftime('%Y-%m-%d %H:%M:%S') +'.png')
    pyplot.show()