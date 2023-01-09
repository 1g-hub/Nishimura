import card
import cardeffect
import random


# player2のデッキ
def generateDeck(player):

    # デッキ用配列
    deck = []
    # デッキ作成
    deck.append(card.Unit("Unit0", 0, player, 1, 1, 0, 0))
    deck.append(card.Unit("Unit0", 0, player, 1, 1, 0, 0))
    deck.append(card.Unit("Unit1", 1, player, 2, 1, 1, 0))
    deck.append(card.Unit("Unit1", 1, player, 2, 1, 1, 0))
    deck.append(card.Unit("Unit2", 2, player, 3, 2, 2, 0))
    deck.append(card.Unit("Unit2", 2, player, 3, 2, 2, 0))
    deck.append(card.Unit("Unit3", 3, player, 4, 3, 3, 0))
    deck.append(card.Unit("Unit3", 3, player, 4, 3, 3, 0))
    deck.append(card.Unit("Unit4", 4, player, 5, 4, 4, 0))
    deck.append(card.Unit("Unit4", 4, player, 5, 4, 4, 0))
    deck.append(card.Unit("spawner1", 5, player, 2, 2, 2, 1))
    deck.append(card.Unit("spawner1", 5, player, 2, 2, 2, 1))
    deck.append(card.Unit("spawner2", 6, player, 2, 3, 3, 1))
    deck.append(card.Unit("spawner2", 6, player, 2, 3, 3, 1))
    deck.append(card.Unit("drawer1", 7, player, 1, 1, 1, 2))
    deck.append(card.Unit("drawer1", 7, player, 1, 1, 1, 2))
    deck.append(card.Unit("drawer2", 8, player, 1, 3, 2, 2))
    deck.append(card.Unit("drawer2", 8, player, 1, 3, 2, 2))
    deck.append(card.Unit("attacker1", 9, player, 2, 1, 2, 3))
    deck.append(card.Unit("attacker1", 9, player, 2, 1, 2, 3))
    deck.append(card.Unit("attacker2", 10, player, 3, 1, 3, 3))
    deck.append(card.Unit("attacker2", 10, player, 3, 1, 3, 3))
    deck.append(card.Unit("damage1", 11, player, 1, 2, 2, 4))
    deck.append(card.Unit("damage1", 11, player, 1, 2, 2, 4))
    deck.append(card.Unit("damage2", 12, player, 2, 3, 3, 4))
    deck.append(card.Unit("damage2", 12, player, 2, 3, 3, 4))
    deck.append(card.Unit("healer1", 13, player, 1, 1, 1, 5))
    deck.append(card.Unit("healer1", 13, player, 1, 1, 1, 5))
    deck.append(card.Unit("healer2", 14, player, 2, 1, 3, 5))
    deck.append(card.Unit("healer2", 14, player, 2, 1, 3, 5))

    return deck
# player1のデッキ


def generateDeckEnemy(player):
    # デッキ用配列
    deck = []
    # デッキ作成 
    deck.append(card.Unit("Unit0", 0, player, 1, 1, 0, 0))
    deck.append(card.Unit("Unit0", 0, player, 1, 1, 0, 0))
    deck.append(card.Unit("Unit1", 1, player, 2, 1, 1, 0))
    deck.append(card.Unit("Unit1", 1, player, 2, 1, 1, 0))
    deck.append(card.Unit("Unit2", 2, player, 3, 2, 2, 0))
    deck.append(card.Unit("Unit2", 2, player, 3, 2, 2, 0))
    deck.append(card.Unit("Unit3", 3, player, 4, 3, 3, 0))
    deck.append(card.Unit("Unit3", 3, player, 4, 3, 3, 0))
    deck.append(card.Unit("Unit4", 4, player, 5, 4, 4, 0))
    deck.append(card.Unit("Unit4", 4, player, 5, 4, 4, 0))
    deck.append(card.Unit("spawner1", 5, player, 2, 2, 2, 1))
    deck.append(card.Unit("spawner1", 5, player, 2, 2, 2, 1))
    deck.append(card.Unit("spawner2", 6, player, 2, 3, 3, 1))
    deck.append(card.Unit("spawner2", 6, player, 2, 3, 3, 1))
    deck.append(card.Unit("drawer1", 7, player, 1, 1, 1, 2))
    deck.append(card.Unit("drawer1", 7, player, 1, 1, 1, 2))
    deck.append(card.Unit("drawer2", 8, player, 1, 3, 2, 2))
    deck.append(card.Unit("drawer2", 8, player, 1, 3, 2, 2))
    deck.append(card.Unit("attacker1", 9, player, 2, 1, 2, 3))
    deck.append(card.Unit("attacker1", 9, player, 2, 1, 2, 3))
    deck.append(card.Unit("attacker2", 10, player, 3, 1, 3, 3))
    deck.append(card.Unit("attacker2", 10, player, 3, 1, 3, 3))
    deck.append(card.Unit("damage1", 11, player, 1, 2, 2, 4))
    deck.append(card.Unit("damage1", 11, player, 1, 2, 2, 4))
    deck.append(card.Unit("damage2", 12, player, 2, 3, 3, 4))
    deck.append(card.Unit("damage2", 12, player, 2, 3, 3, 4))
    deck.append(card.Unit("healer1", 13, player, 1, 1, 1, 5))
    deck.append(card.Unit("healer1", 13, player, 1, 1, 1, 5))
    deck.append(card.Unit("healer2", 14, player, 2, 1, 3, 5))
    deck.append(card.Unit("healer2", 14, player, 2, 1, 3, 5))



    return deck