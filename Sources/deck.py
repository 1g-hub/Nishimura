import card
import random

#player2のデッキ
def generateDeck(player):
    #デッキ用配列
    deck = []
    #デッキ作成
    deck.append(card.Unit("Unit1",player,3,3))
    deck.append(card.Unit("Unit2",player,2,3))
    deck.append(card.Unit("Unit3",player,2,4))

    return deck
#player1のデッキ
def generateDeckEnemy(player):
    #デッキ用配列
    deck = []
    #デッキ作成
    deck.append(card.Unit("Unit1",player,3,3))
    deck.append(card.Unit("Unit2",player,1,5))
    deck.append(card.Unit("Unit3",player,4,2))




    return deck

