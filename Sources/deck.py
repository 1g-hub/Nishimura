import card
import cardeffect
import random


# player2のデッキ
def generateDeck(player):

    # デッキ用配列
    deck = []
    # デッキ作成

    deck.append(card.Unit("Unit0", player, 1, 1, 0, 0))
    deck.append(card.Unit("Unit0", player, 1, 1, 0, 0))
    deck.append(card.Unit("Unit1", player, 2, 1, 1, 0))
    deck.append(card.Unit("Unit1", player, 2, 1, 1, 0))
    deck.append(card.Unit("Unit2", player, 3, 2, 2, 0))
    deck.append(card.Unit("Unit2", player, 3, 2, 2, 0))
    deck.append(card.Unit("Unit3", player, 4, 3, 3, 0))
    deck.append(card.Unit("Unit3", player, 4, 3, 3, 0))
    deck.append(card.Unit("Unit4", player, 5, 4, 4, 0))
    deck.append(card.Unit("Unit4", player, 5, 4, 4, 0))
    deck.append(card.Unit("spawner1", player, 2, 2, 2, 1))
    deck.append(card.Unit("spawner1", player, 2, 2, 2, 1))
    deck.append(card.Unit("spawner2", player, 2, 3, 3, 1))
    deck.append(card.Unit("spawner2", player, 2, 3, 3, 1))
    deck.append(card.Unit("drawer1", player, 1, 1, 1, 2))
    deck.append(card.Unit("drawer1", player, 1, 1, 1, 2))
    deck.append(card.Unit("drawer2", player, 1, 3, 2, 2))
    deck.append(card.Unit("drawer2", player, 1, 3, 2, 2))
    deck.append(card.Unit("attacker1", player, 2, 1, 2, 3))
    deck.append(card.Unit("attacker1", player, 2, 1, 2, 3))
    deck.append(card.Unit("attacker2", player, 3, 1, 3, 3))
    deck.append(card.Unit("attacker2", player, 3, 1, 3, 3))
    deck.append(card.Unit("damage1", player, 1, 2, 2, 4))
    deck.append(card.Unit("damage1", player, 1, 2, 2, 4))
    deck.append(card.Unit("damage2", player, 2, 3, 3, 4))
    deck.append(card.Unit("damage2", player, 2, 3, 3, 4))
    deck.append(card.Unit("healer1", player, 1, 1, 1, 5))
    deck.append(card.Unit("healer1", player, 1, 1, 1, 5))
    deck.append(card.Unit("healer2", player, 2, 1, 3, 5))
    deck.append(card.Unit("healer2", player, 2, 1, 3, 5))

    return deck
# player1のデッキ


def generateDeckEnemy(player):
    # デッキ用配列
    deck = []
    # デッキ作成 
    deck.append(card.Unit("Unit0", player, 1, 1, 0, 0))
    deck.append(card.Unit("Unit0", player, 1, 1, 0, 0))
    deck.append(card.Unit("Unit1", player, 2, 1, 1, 0))
    deck.append(card.Unit("Unit1", player, 2, 1, 1, 0))
    deck.append(card.Unit("Unit2", player, 3, 2, 2, 0))
    deck.append(card.Unit("Unit2", player, 3, 2, 2, 0))
    deck.append(card.Unit("Unit3", player, 4, 3, 3, 0))
    deck.append(card.Unit("Unit3", player, 4, 3, 3, 0))
    deck.append(card.Unit("Unit4", player, 5, 4, 4, 0))
    deck.append(card.Unit("Unit4", player, 5, 4, 4, 0))
    deck.append(card.Unit("spawner1", player, 2, 2, 2, 1))
    deck.append(card.Unit("spawner1", player, 2, 2, 2, 1))
    deck.append(card.Unit("spawner2", player, 2, 3, 3, 1))
    deck.append(card.Unit("spawner2", player, 2, 3, 3, 1))
    deck.append(card.Unit("drawer1", player, 1, 1, 1, 2))
    deck.append(card.Unit("drawer1", player, 1, 1, 1, 2))
    deck.append(card.Unit("drawer2", player, 1, 3, 2, 2))
    deck.append(card.Unit("drawer2", player, 1, 3, 2, 2))
    deck.append(card.Unit("attacker1", player, 2, 1, 2, 3))
    deck.append(card.Unit("attacker1", player, 2, 1, 2, 3))
    deck.append(card.Unit("attacker2", player, 3, 1, 3, 3))
    deck.append(card.Unit("attacker2", player, 3, 1, 3, 3))
    deck.append(card.Unit("damage1", player, 1, 2, 2, 4))
    deck.append(card.Unit("damage1", player, 1, 2, 2, 4))
    deck.append(card.Unit("damage2", player, 2, 3, 3, 4))
    deck.append(card.Unit("damage2", player, 2, 3, 3, 4))
    deck.append(card.Unit("healer1", player, 1, 1, 1, 5))
    deck.append(card.Unit("healer1", player, 1, 1, 1, 5))
    deck.append(card.Unit("healer2", player, 2, 1, 3, 5))
    deck.append(card.Unit("healer2", player, 2, 1, 3, 5))


    return deck