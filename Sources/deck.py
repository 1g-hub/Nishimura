import card
import random

def generateDeck(player):
    #デッキ用配列
    deck = []
    #デッキ作成
    deck.append(card.Unit("Unit1",player,3,2))
    deck.append(card.Unit("Unit2",player,2,4))
    deck.append(card.Unit("Unit3",player,4,1))
    deck.append(card.Unit("Unit1",player,3,2))
    deck.append(card.Unit("Unit2",player,2,4))
    deck.append(card.Unit("Unit3",player,4,1))
    deck.append(card.Unit("Unit1",player,3,2))
    deck.append(card.Unit("Unit2",player,2,4))
    deck.append(card.Unit("Unit3",player,4,1))

    return deck