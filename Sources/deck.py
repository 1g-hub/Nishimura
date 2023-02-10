import card
import cardeffect
import random


# player2のデッキ
def generateDeck(player, card_values):

    # デッキ用配列
    deck = []

    #可読性のためにDictoryでcard_values受け取る
    deck_dict = {}
    for i in range(45):
        if i % 3 == 0:
            deck_dict['Card' + str(i // 3) + 'Attack'] = card_values[i]
        elif i % 3 == 1:
            deck_dict['Card' + str(i // 3) + 'HP'] = card_values[i]
        else:
            deck_dict['Card' + str(i // 3) + 'Cost'] = card_values[i]

    # デッキ作成
    deck.append(card.Unit("Unit0", 0, player, deck_dict["Card0Attack"], deck_dict["Card0HP"], deck_dict["Card0Cost"], 0))
    deck.append(card.Unit("Unit0", 0, player, deck_dict["Card0Attack"], deck_dict["Card0HP"], deck_dict["Card0Cost"], 0))
    deck.append(card.Unit("Unit1", 1, player, deck_dict["Card1Attack"], deck_dict["Card1HP"], deck_dict["Card1Cost"], 0))
    deck.append(card.Unit("Unit1", 1, player, deck_dict["Card1Attack"], deck_dict["Card1HP"], deck_dict["Card1Cost"], 0))
    deck.append(card.Unit("Unit2", 2, player, deck_dict["Card2Attack"], deck_dict["Card2HP"], deck_dict["Card2Cost"], 0))
    deck.append(card.Unit("Unit2", 2, player, deck_dict["Card2Attack"], deck_dict["Card2HP"], deck_dict["Card2Cost"], 0))
    deck.append(card.Unit("Unit3", 3, player, deck_dict["Card3Attack"], deck_dict["Card3HP"], deck_dict["Card3Cost"], 0))
    deck.append(card.Unit("Unit3", 3, player, deck_dict["Card3Attack"], deck_dict["Card3HP"], deck_dict["Card3Cost"], 0))
    deck.append(card.Unit("Unit4", 4, player, deck_dict["Card4Attack"], deck_dict["Card4HP"], deck_dict["Card4Cost"], 0))
    deck.append(card.Unit("Unit4", 4, player, deck_dict["Card4Attack"], deck_dict["Card4HP"], deck_dict["Card4Cost"], 0))
    deck.append(card.Unit("spawner1", 5, player, deck_dict["Card5Attack"], deck_dict["Card5HP"], deck_dict["Card5Cost"], 1))
    deck.append(card.Unit("spawner1", 5, player, deck_dict["Card5Attack"], deck_dict["Card5HP"], deck_dict["Card5Cost"], 1))
    deck.append(card.Unit("spawner2", 6, player, deck_dict["Card6Attack"], deck_dict["Card6HP"], deck_dict["Card6Cost"], 1))
    deck.append(card.Unit("spawner2", 6, player, deck_dict["Card6Attack"], deck_dict["Card6HP"], deck_dict["Card6Cost"], 1))
    deck.append(card.Unit("drawer1", 7, player, deck_dict["Card7Attack"], deck_dict["Card7HP"], deck_dict["Card7Cost"], 2))
    deck.append(card.Unit("drawer1", 7, player, deck_dict["Card7Attack"], deck_dict["Card7HP"], deck_dict["Card7Cost"], 2))
    deck.append(card.Unit("drawer2", 8, player, deck_dict["Card8Attack"], deck_dict["Card8HP"], deck_dict["Card8Cost"], 2))
    deck.append(card.Unit("drawer2", 8, player, deck_dict["Card8Attack"], deck_dict["Card8HP"], deck_dict["Card8Cost"], 2))
    deck.append(card.Unit("attacker1", 9, player, deck_dict["Card9Attack"], deck_dict["Card9HP"], deck_dict["Card9Cost"], 3))
    deck.append(card.Unit("attacker1", 9, player, deck_dict["Card9Attack"], deck_dict["Card9HP"], deck_dict["Card9Cost"], 3))
    deck.append(card.Unit("attacker2", 10, player, deck_dict["Card10Attack"], deck_dict["Card10HP"], deck_dict["Card10Cost"], 3))
    deck.append(card.Unit("attacker2", 10, player, deck_dict["Card10Attack"], deck_dict["Card10HP"], deck_dict["Card10Cost"], 3))
    deck.append(card.Unit("damage1", 11, player, deck_dict["Card11Attack"], deck_dict["Card11HP"], deck_dict["Card11Cost"], 4))
    deck.append(card.Unit("damage1", 11, player, deck_dict["Card11Attack"], deck_dict["Card11HP"], deck_dict["Card11Cost"], 4))
    deck.append(card.Unit("damage2", 12, player, deck_dict["Card12Attack"], deck_dict["Card12HP"], deck_dict["Card12Cost"], 4))
    deck.append(card.Unit("damage2", 12, player, deck_dict["Card12Attack"], deck_dict["Card12HP"], deck_dict["Card12Cost"], 4))
    deck.append(card.Unit("healer1", 13, player, deck_dict["Card13Attack"], deck_dict["Card13HP"], deck_dict["Card13Cost"], 5))
    deck.append(card.Unit("healer1", 13, player, deck_dict["Card13Attack"], deck_dict["Card13HP"], deck_dict["Card13Cost"], 5))
    deck.append(card.Unit("healer2", 14, player, deck_dict["Card14Attack"], deck_dict["Card14HP"], deck_dict["Card14Cost"], 5))
    deck.append(card.Unit("healer2", 14, player, deck_dict["Card14Attack"], deck_dict["Card14HP"], deck_dict["Card14Cost"], 5))



    return deck

# player1のデッキ


def generateDeckEnemy(player,card_values):
    # デッキ用配列
    deck = []
    #可読性のためにDictoryでcard_values受け取る
    deck_dict = {}
    for i in range(45):
        if i % 3 == 0:
            deck_dict['Card' + str(i // 3) + 'Attack'] = card_values[i]
        elif i % 3 == 1:
            deck_dict['Card' + str(i // 3) + 'HP'] = card_values[i]
        else:
            deck_dict['Card' + str(i // 3) + 'Cost'] = card_values[i]

    # デッキ作成
    deck.append(card.Unit("Unit0", 0, player, deck_dict["Card0Attack"], deck_dict["Card0HP"], deck_dict["Card0Cost"], 0))
    deck.append(card.Unit("Unit0", 0, player, deck_dict["Card0Attack"], deck_dict["Card0HP"], deck_dict["Card0Cost"], 0))
    deck.append(card.Unit("Unit1", 1, player, deck_dict["Card1Attack"], deck_dict["Card1HP"], deck_dict["Card1Cost"], 0))
    deck.append(card.Unit("Unit1", 1, player, deck_dict["Card1Attack"], deck_dict["Card1HP"], deck_dict["Card1Cost"], 0))
    deck.append(card.Unit("Unit2", 2, player, deck_dict["Card2Attack"], deck_dict["Card2HP"], deck_dict["Card2Cost"], 0))
    deck.append(card.Unit("Unit2", 2, player, deck_dict["Card2Attack"], deck_dict["Card2HP"], deck_dict["Card2Cost"], 0))
    deck.append(card.Unit("Unit3", 3, player, deck_dict["Card3Attack"], deck_dict["Card3HP"], deck_dict["Card3Cost"], 0))
    deck.append(card.Unit("Unit3", 3, player, deck_dict["Card3Attack"], deck_dict["Card3HP"], deck_dict["Card3Cost"], 0))
    deck.append(card.Unit("Unit4", 4, player, deck_dict["Card4Attack"], deck_dict["Card4HP"], deck_dict["Card4Cost"], 0))
    deck.append(card.Unit("Unit4", 4, player, deck_dict["Card4Attack"], deck_dict["Card4HP"], deck_dict["Card4Cost"], 0))
    deck.append(card.Unit("spawner1", 5, player, deck_dict["Card5Attack"], deck_dict["Card5HP"], deck_dict["Card5Cost"], 1))
    deck.append(card.Unit("spawner1", 5, player, deck_dict["Card5Attack"], deck_dict["Card5HP"], deck_dict["Card5Cost"], 1))
    deck.append(card.Unit("spawner2", 6, player, deck_dict["Card6Attack"], deck_dict["Card6HP"], deck_dict["Card6Cost"], 1))
    deck.append(card.Unit("spawner2", 6, player, deck_dict["Card6Attack"], deck_dict["Card6HP"], deck_dict["Card6Cost"], 1))
    deck.append(card.Unit("drawer1", 7, player, deck_dict["Card7Attack"], deck_dict["Card7HP"], deck_dict["Card7Cost"], 2))
    deck.append(card.Unit("drawer1", 7, player, deck_dict["Card7Attack"], deck_dict["Card7HP"], deck_dict["Card7Cost"], 2))
    deck.append(card.Unit("drawer2", 8, player, deck_dict["Card8Attack"], deck_dict["Card8HP"], deck_dict["Card8Cost"], 2))
    deck.append(card.Unit("drawer2", 8, player, deck_dict["Card8Attack"], deck_dict["Card8HP"], deck_dict["Card8Cost"], 2))
    deck.append(card.Unit("attacker1", 9, player, deck_dict["Card9Attack"], deck_dict["Card9HP"], deck_dict["Card9Cost"], 3))
    deck.append(card.Unit("attacker1", 9, player, deck_dict["Card9Attack"], deck_dict["Card9HP"], deck_dict["Card9Cost"], 3))
    deck.append(card.Unit("attacker2", 10, player, deck_dict["Card10Attack"], deck_dict["Card10HP"], deck_dict["Card10Cost"], 3))
    deck.append(card.Unit("attacker2", 10, player, deck_dict["Card10Attack"], deck_dict["Card10HP"], deck_dict["Card10Cost"], 3))
    deck.append(card.Unit("damage1", 11, player, deck_dict["Card11Attack"], deck_dict["Card11HP"], deck_dict["Card11Cost"], 4))
    deck.append(card.Unit("damage1", 11, player, deck_dict["Card11Attack"], deck_dict["Card11HP"], deck_dict["Card11Cost"], 4))
    deck.append(card.Unit("damage2", 12, player, deck_dict["Card12Attack"], deck_dict["Card12HP"], deck_dict["Card12Cost"], 4))
    deck.append(card.Unit("damage2", 12, player, deck_dict["Card12Attack"], deck_dict["Card12HP"], deck_dict["Card12Cost"], 4))
    deck.append(card.Unit("healer1", 13, player, deck_dict["Card13Attack"], deck_dict["Card13HP"], deck_dict["Card13Cost"], 5))
    deck.append(card.Unit("healer1", 13, player, deck_dict["Card13Attack"], deck_dict["Card13HP"], deck_dict["Card13Cost"], 5))
    deck.append(card.Unit("healer2", 14, player, deck_dict["Card14Attack"], deck_dict["Card14HP"], deck_dict["Card14Cost"], 5))
    deck.append(card.Unit("healer2", 14, player, deck_dict["Card14Attack"], deck_dict["Card14HP"], deck_dict["Card14Cost"], 5))



    return deck

def generatePartialDeck(player, p_card_values):
    # デッキ用配列
    deck = []
    '''
    [
            4,4,1,#0
            2,2,2,#1
            3,3,3,#2
            4,3,4,#3
            5,4,5,#4
            2,2,2,#5
            2,3,3,#6
            1,1,1,#7
            1,3,2,#8
            2,1,2,#9
            3,1,3,#10
            1,2,2,#11
            2,3,3,#12
            1,1,1,#13
            1,1,5 #14
        ]
    '''
    # # デッキ作成
    for i in range(2):
        deck.append(card.Unit("Unit0", 0, player, p_card_values[0], p_card_values[1], p_card_values[2], 0))
        deck.append(card.Unit("Unit1", 1, player, 2,2,2, 0))
        deck.append(card.Unit("Unit2", 2, player, 3,3,3, 0))
        deck.append(card.Unit("Unit3", 3, player, 4,3,4, 0))
        deck.append(card.Unit("Unit4", 4, player, 5,4,5, 0))
        deck.append(card.Unit("spawner1", 5, player, 2,2,2, 1))
        deck.append(card.Unit("spawner2", 6, player, 2,3,3, 1))
        deck.append(card.Unit("drawer1", 7, player, 1,1,1, 2))
        deck.append(card.Unit("drawer2", 8, player, 1,3,2, 2))
        deck.append(card.Unit("attacker1", 9, player, 2,1,2, 3))
        deck.append(card.Unit("attacker2", 10, player, 3,1,3, 3))
        deck.append(card.Unit("damage1", 11, player, 1,2,2, 4))
        deck.append(card.Unit("damage2", 12, player, 2,3,3, 4))
        deck.append(card.Unit("healer1", 13, player, 1,1,1, 5))
        deck.append(card.Unit("healer2", 14, player, p_card_values[3],p_card_values[4],p_card_values[5], 5))

    return deck

