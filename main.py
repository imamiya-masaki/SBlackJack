
# -*- coding: utf-8 -*-
import random

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
  def play(self, player1, player2):
    # 1play
    deck = random.shuffle(self.createDeck(self.decks))
    player1Cards = []
    player1D = False #ダブルダウンしたかどうか
    delerCards = []
    player1Cards,deck = self.pickCard(deck, player1Cards, 2)
    delerCards,deck = self.pickCard(deck, delerCards, 2)
    playerSum = sum(player1Cards)
    delerSum = sum(delerCards)
  def sum(self,cards):
    a = cards[0]
    b = cards[1]
    if a < b:
      # aの方が大きくなる
      swap = a
      a = b
      b = swap
    if a >= 10:
      a = 10
    if b >= 10:
      b = 10
    if a == 1 and b ==1:
      return "21"
    if b == 10 and a == 1:
      return "21"
    if b == 1:
      return str(a+10+b)+"/"+str(a+b) #これでもしこえた場合右で計算するようにする
    return str(a+b)
class montekarlo:
  def __init__(self):
    self.tree = {}
  def play(self, playerCards, delerCards, player1D):
    if self.tree[str(playerCards)-str(delerCards)-str(player1D)] == None:
      #初期化
      self.tree[str(playerCards)-str(delerCards)-str(player1D)] = {}

if __name__ == '__main__':
    game = Game(1)
    game.test()