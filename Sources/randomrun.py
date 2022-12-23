import randomplayer2
import deck
import card
import sys

#デッキの初期化
def initdecks(player):
    #デッキ生成
    player.deck = deck.generateDeck(player)
    #デッキのシャッフル
    player.shuffle()
    #対戦相手にも同じこと
    player.enemy.deck = deck.generateDeckEnemy(player.enemy)
    player.enemy.shuffle()

#ゲーム開始時のドロー
def inithands(player):
    #敵味方3枚ずつドロー
    player.draw()
    player.draw()
    player.draw()
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


def doTurn(player,isFirst,turnnum):
    print ("'RandomPlayer 1 '")
    print ("-----------------------------------------------------------------------------------------------")

    #敵のカードドロー
    if isFirst == True or turnnum != 0:
         player.enemy.draw()
    #敵がデッキ切れ起こしたらreturn
    if player.enemy.is_deckend:
        return
    
    while 1:
        if player.is_dead:
            break
        if player.enemy.take_action() == 39:
            resetuse(player.enemy)
            break
    
    #敵の番でHP切れたらretrun
    if player.is_dead:
        return

    print ("'Random Player 2'")
    print ("-----------------------------------------------------------------------------------------------")
    #自分も同じことする
    player.draw()
    #自分がデッキ切れ起こしたらreturn 
    if player.is_deckend:
        return
    
    while 1:
        if player.enemy.is_dead:
            break
        if player.take_action() == 39:
            resetuse(player)
            break
    
    if player.enemy.is_dead:
        return

def play(isFirst):
    player = randomplayer2.RandomPlayer2()

    initdecks(player)

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
            while 1:
                if player.take_action() == 39:
                    resetuse(player)
                    break

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
    for i in range(1):
        if play(isFirst = True) == 1:
            win_sum += 1
        else:
            lose_sum += 1
    print("win_sum " + str(win_sum))
    print("lose_sum " + str(lose_sum))
    print("win_rate " + str(win_sum / 10000))
    
    print(sum)
