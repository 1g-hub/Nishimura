import player2
import randomplayer2
import deck
import card
import sys

#デッキの初期化
def initdecks(player,card_arr):
    #デッキ生成
    player.deck = deck.generateDeck(player, card_arr)
    #デッキのシャッフル
    player.shuffle()
    #対戦相手にも同じこと
    player.enemy.deck = deck.generateDeckEnemy(player.enemy, card_arr)
    player.enemy.shuffle()

#ゲーム開始時のドロー
def inithands(player):
    #敵味方5枚ずつドロー
    player.draw()
    player.draw()
    player.draw()
    player.draw()
    player.draw()
    player.enemy.draw()
    player.enemy.draw()
    player.enemy.draw()
    player.enemy.draw()
    player.enemy.draw()

#カードのis_used状態をリセット（ターン処理で呼ばれる)
def resetuse(player):
    for played_card in player.is_played:
        if played_card.attack == 0 and played_card.is_used == card.Card.use:
            played_card.is_used = True
        else:
            played_card.is_used = False

#プレイヤーのコストUpdate処理 (ターン処理で呼ばれる)
def updatecost(player):
    if player.turnmaxcost < player.maxcost:
        player.turnmaxcost += 1
    player.cost = player.turnmaxcost
    print("updated cost")
    print(player.name + ":" + str(player.cost))

def doTurn(player,isFirst,turnnum):
    print ("")
    print ("-----------------------------------------------------------------------------------------------")

    #敵のカードドロー
    if isFirst == True or turnnum != 0:
         player.enemy.draw()
    #敵がデッキ切れ起こしたらreturn
    if player.enemy.is_deckend:
        return
    #敵のカードプレイ
    log = player.enemy.playcard()
    log += player.enemy.usecard()
    #敵のresetuse
    resetuse(player.enemy)
    #敵のupdatecost
    updatecost(player.enemy)
    
    #敵の番でHP切れたらretrun
    if player.is_dead:
        return

    print ("")
    print ("-----------------------------------------------------------------------------------------------")
    #自分も同じことする
    player.draw()
    #自分がデッキ切れ起こしたらreturn 
    if player.is_deckend:
        return
    log = player.playcard()
    log += player.usecard()
    resetuse(player)
    updatecost(player)

def play(isFirst):
    player = player2.Player2()

    card_values = [
        1,1,0,#0
        2,1,1,#1
        3,2,2,#2
        4,3,3,#3
        5,4,4,#4
        2,2,2,#5
        2,3,3,#6
        1,1,1,#7
        1,3,2,#8
        2,1,2,#9
        3,1,3,#10
        1,2,2,#11
        2,3,3,#12
        1,1,1,#13
        2,1,3 #14
    ]

    initdecks(player,card_arr=card_values)

    inithands(player)

    resetuse(player)
    resetuse(player.enemy)

    turnnum = 0

    while True:
        player.enemy.printhand()
        player.printhand()
        #player1の場を表示
        player.enemy.printisplayed()

        #player2の場を表示
        player.printisplayed()
        if isFirst == True and turnnum == 0:
            log = player.playcard()
            log += player.usecard()
            resetuse(player)
            updatecost(player)

        doTurn(player,isFirst,turnnum)  
        turnnum += 1

        #勝利条件
        #敵の勝利条件
        if player.is_dead == True or player.is_deckend == True:
            print(player.enemy.name + "Win!!")
            #sys.exit(player.enemy.name + "Win!!")
            return -1
        #自分の勝利条件
        elif player.enemy.is_dead == True or player.enemy.is_deckend == True:
            print(player.name + "Win!!")
            #sys.exit(player.name + "Win!!")
            return 1

if __name__ == '__main__':
    print ("")
    print ("-----------------------")
    sum = 0
    win_sum = 0
    lose_sum = 0
    for i in range(10000):
        if play(isFirst = True) == 1:
            win_sum += 1
        else:
            lose_sum += 1
    print("win_sum " + str(win_sum))
    print("lose_sum " + str(lose_sum))
    print("win_rate " + str(win_sum / 10000))
    
    print(sum)


    

